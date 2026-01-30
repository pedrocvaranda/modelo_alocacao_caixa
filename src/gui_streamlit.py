"""
Interface Gráfica com Streamlit
Para executar: python -m streamlit run src/gui_streamlit.py
"""

import sys
sys.path.insert(0, '.')

import streamlit as st
import pandas as pd
from ml_optimizer import MLOptimizer
from cash_allocation_model import InputParameters, AllocationStrategy, CashAllocationModel
from visualizer import Visualizer
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Alocação de Caixa",
    page_icon="💰",
    layout="wide"
)

# Cache para o otimizador ML (inicializa uma vez apenas)
@st.cache_resource
def load_ml_optimizer():
    """Carrega ou treina o otimizador ML"""
    optimizer = MLOptimizer()
    
    # Tentar carregar modelos já treinados da pasta models/
    try:
        if os.path.exists("models/ml_optimizer_reserva.pkl"):
            optimizer.load_models(folder="models")
            st.sidebar.success("✅ Modelos ML carregados!")
            return optimizer
    except Exception as e:
        st.sidebar.warning(f"⚠️ Não foi possível carregar modelos: {e}")
    
    # Se não conseguir carregar, treinar
    st.sidebar.info("🔄 Treinando modelos ML (primeira execução)...")
    try:
        optimizer.train()
        optimizer.save_models(folder="models")
        st.sidebar.success("✅ Modelos ML treinados e salvos!")
    except Exception as e:
        st.sidebar.error(f"❌ Erro ao treinar modelos: {e}")
    
    return optimizer

st.title("💰 Modelo de Alocação de Caixa")
st.markdown("### Análise inteligente para pequenos operadores")

# Carregar otimizador ML
ml_optimizer = load_ml_optimizer()

# Sidebar para inputs
with st.sidebar:
    st.header("📋 Parâmetros de Entrada")
    
    st.subheader("💵 Dados Financeiros")
    dinheiro = st.number_input(
        "Dinheiro em mãos (R$)", 
        min_value=1000.0, 
        value=100000.0,
        step=1000.0
    )
    
    caixa_mensal = st.number_input(
        "Caixa mensal esperado (R$)", 
        min_value=0.0, 
        value=15000.0,
        step=500.0
    )
    
    despesas_fixas = st.number_input(
        "Despesas fixas (R$)", 
        min_value=0.0, 
        value=8000.0,
        step=500.0
    )
    
    despesas_variaveis = st.number_input(
        "Despesas variáveis (R$)", 
        min_value=0.0, 
        value=3000.0,
        step=500.0
    )
    
    st.subheader("⚙️ Parâmetros de Risco")
    volatilidade = st.slider(
        "Volatilidade do caixa (%)", 
        min_value=0, 
        max_value=50, 
        value=15
    ) / 100
    
    tolerancia = st.slider(
        "Tolerância a risco (%)", 
        min_value=0, 
        max_value=100, 
        value=30
    ) / 100
    
    meses = st.number_input(
        "Meses a proteger", 
        min_value=1, 
        max_value=24, 
        value=6
    )
    
    st.subheader("📈 Oportunidades")
    retorno_seguro = st.number_input(
        "Retorno seguro (% a.m.)", 
        min_value=0.0, 
        max_value=5.0, 
        value=0.9,
        step=0.1
    ) / 100
    
    retorno_medio = st.number_input(
        "Retorno médio risco (% a.m.)", 
        min_value=0.0, 
        max_value=10.0, 
        value=1.0,
        step=0.1
    ) / 100
    
    retorno_alto = st.number_input(
        "Retorno alto risco (% a.m.)", 
        min_value=0.0, 
        max_value=20.0, 
        value=5.0,
        step=0.5
    ) / 100
    
    analisar = st.button("🚀 Analisar", type="primary", use_container_width=True)

# Opção de usar ML ou método tradicional (ANTES do check de analisar para persistir)
col_method = st.columns([1, 2])
with col_method[1]:
    usar_ml = st.radio(
        "Método de cálculo:",
        ("🤖 Machine Learning (Rápido)", "📐 Tradicional (Preciso)"),
        horizontal=True,
        key="method_selector"
    )

# Main content
if analisar:
    
    with st.spinner("Analisando..."):
        # Criar parâmetros
        params = InputParameters(
            dinheiro_em_maos=dinheiro,
            caixa_mensal_esperado=caixa_mensal,
            despesas_fixas=despesas_fixas,
            despesas_variaveis=despesas_variaveis,
            volatilidade_caixa=volatilidade,
            tolerancia_risco=tolerancia,
            meses_protegidos=int(meses),
            retorno_seguro=retorno_seguro,
            retorno_medio_risco=retorno_medio,
            retorno_alto_risco=retorno_alto
        )
        
        # Criar modelo
        modelo = CashAllocationModel(params)
        
        # Escolher alocação com base no método selecionado
        if "Machine Learning" in usar_ml and ml_optimizer.is_trained:
            try:
                alocacao = ml_optimizer.predict_allocation(params)
                st.info("💡 Alocação sugerida por Machine Learning")
            except Exception as e:
                st.warning(f"⚠️ Erro no ML, usando método tradicional: {e}")
                alocacao = modelo.suggest_allocation()
        else:
            alocacao = modelo.suggest_allocation()
            st.info("💡 Alocação sugerida por método tradicional")
        
        # Sempre executar Monte Carlo para validação
        resultado = modelo.evaluate_allocation(alocacao, use_monte_carlo=True)
        
        # Decisão principal
        if resultado.alocacao_valida:
            st.success("✅ ALOCAÇÃO VÁLIDA - Você sobrevive no cenário ruim!")
        else:
            st.error("❌ ALOCAÇÃO INVÁLIDA - Risco alto de não sobreviver!")
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Reserva Segurança", 
                f"{resultado.reserva_seguranca_pct:.1f}%",
                f"R$ {resultado.reserva_seguranca_valor:,.0f}"
            )
        
        with col2:
            st.metric(
                "Crescimento", 
                f"{resultado.crescimento_pct:.1f}%",
                f"R$ {resultado.crescimento_valor:,.0f}"
            )
        
        with col3:
            st.metric(
                "Risco", 
                f"{resultado.risco_pct:.1f}%",
                f"R$ {resultado.risco_valor:,.0f}"
            )
        
        with col4:
            st.metric(
                "Prob. Sobrevivência", 
                f"{resultado.probabilidade_sobrevivencia_ruim:.1%}",
                "Cenário Ruim"
            )
        
        # Tabs para diferentes visualizações
        tab1, tab2, tab3 = st.tabs(["📊 Alocação", "📈 Trajetórias", "📋 Detalhes"])
        
        with tab1:
            # Gráfico de pizza
            fig = go.Figure(data=[go.Pie(
                labels=['Reserva', 'Crescimento', 'Risco'],
                values=[
                    resultado.reserva_seguranca_valor,
                    resultado.crescimento_valor,
                    resultado.risco_valor
                ],
                marker_colors=['#2ecc71', '#3498db', '#e74c3c']
            )])
            fig.update_layout(title="Distribuição da Alocação")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Gráfico de trajetórias
            fig = go.Figure()
            meses_range = list(range(len(resultado.resultado_ruim.trajetoria_caixa)))
            
            fig.add_trace(go.Scatter(
                x=meses_range,
                y=resultado.resultado_bom.trajetoria_caixa,
                mode='lines',
                name='Cenário Bom',
                line=dict(color='green', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=meses_range,
                y=resultado.resultado_neutro.trajetoria_caixa,
                mode='lines',
                name='Cenário Neutro',
                line=dict(color='blue', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=meses_range,
                y=resultado.resultado_ruim.trajetoria_caixa,
                mode='lines',
                name='Cenário Ruim',
                line=dict(color='red', width=2)
            ))
            
            fig.update_layout(
                title="Evolução do Caixa por Cenário",
                xaxis_title="Meses",
                yaxis_title="Caixa (R$)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Tabela de resultados
            df_results = pd.DataFrame([
                {
                    'Cenário': 'Bom',
                    'Sobrevive': '✅' if resultado.resultado_bom.sobrevive else '❌',
                    'Caixa Final': f"R$ {resultado.resultado_bom.trajetoria_caixa[-1]:,.2f}"
                },
                {
                    'Cenário': 'Neutro',
                    'Sobrevive': '✅' if resultado.resultado_neutro.sobrevive else '❌',
                    'Caixa Final': f"R$ {resultado.resultado_neutro.trajetoria_caixa[-1]:,.2f}"
                },
                {
                    'Cenário': 'Ruim',
                    'Sobrevive': '✅' if resultado.resultado_ruim.sobrevive else '❌',
                    'Caixa Final': f"R$ {resultado.resultado_ruim.trajetoria_caixa[-1]:,.2f}"
                }
            ])
            
            st.dataframe(df_results, use_container_width=True)
        
        # Download
        st.subheader("💾 Download dos Resultados")
        col1, col2 = st.columns(2)
        
        with col1:
            excel_file = modelo.export_to_excel(resultado, "resultado_streamlit.xlsx")
            with open(excel_file, "rb") as f:
                st.download_button(
                    label="📊 Baixar Excel",
                    data=f,
                    file_name="analise_alocacao.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col2:
            json_file = modelo.export_to_json(resultado, "resultado_streamlit.json")
            with open(json_file, "r") as f:
                st.download_button(
                    label="📄 Baixar JSON",
                    data=f,
                    file_name="analise_alocacao.json",
                    mime="application/json"
                )

else:
    st.info("👈 Configure os parâmetros na barra lateral e clique em 'Analisar'")
    st.markdown("""
    ### Como usar:
    1. Insira seus dados financeiros na barra lateral
    2. Ajuste os parâmetros de risco
    3. Configure as oportunidades de investimento
    4. Escolha o método de cálculo (ML ou Tradicional)
    5. Clique em 'Analisar' para ver os resultados
    
    ### Métodos de Cálculo:
    - **🤖 Machine Learning**: Mais rápido, usa modelos treinados em 10.000 cenários
    - **📐 Tradicional**: Mais preciso, usa análise detalhada de parâmetros
    
    ⚠️ Na primeira execução, o ML treinará automaticamente (leva ~30 segundos)
    """)

