# 💰 Modelo de Alocação de Caixa para Pequenos Operadores

Sistema inteligente de análise e alocação de caixa com simulação de cenários, desenvolvido para responder: **"Como um pequeno operador deve alocar seu caixa entre poupança, reinvestimento e risco em um cenário de incerteza?"**

## 🎯 Objetivo

Maximizar a probabilidade de sobreviver **N meses**, preservando exposição a oportunidades, garantindo que os N meses estejam sempre protegidos.

## 📊 Funcionamento

O modelo recebe 7 variáveis principais:
1. **Dinheiro em mãos agora** - Capital disponível
2. **Caixa mensal esperado** - Receita mensal
3. **Despesas fixas** - Custos fixos mensais
4. **Despesas variáveis** - Custos variáveis mensais
5. **Volatilidade do caixa mensal** - Incerteza da receita (0-1)
6. **Tolerância a risco** - Apetite por risco (0-1)
7. **Oportunidades de investimento**:
   - **Seguras** (ex: CDI ~0.9% a.m.)
   - **Médio risco** (ex: Index ~1% a.m.)
   - **Alto risco** (projetos, apostas ~5% a.m.)

### Processo de Análise

1. **Simula 3 cenários**: Bom, Neutro e Ruim
2. **Responde a pergunta**: "Se eu alocar meu dinheiro assim, eu sobrevivo no cenário ruim?"
3. **Output**:
   - ✅/❌ **Alocação válida ou inválida**
   - % Reserva de segurança
   - % Crescimento
   - % Risco
   - Probabilidade de sobrevivência
   - Tempo até zero no cenário ruim

## 🚀 Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Ou instalar individualmente
pip install numpy pandas matplotlib seaborn openpyxl scikit-learn
```

## 💻 Uso Básico

### Exemplo 1: Uso Simples

```python
from cash_allocation_model import InputParameters, CashAllocationModel

# Definir parâmetros
params = InputParameters(
    dinheiro_em_maos=100000.0,      # R$ 100k
    caixa_mensal_esperado=15000.0,  # R$ 15k/mês
    despesas_fixas=8000.0,          # R$ 8k/mês
    despesas_variaveis=3000.0,      # R$ 3k/mês
    volatilidade_caixa=0.15,        # 15% volatilidade
    tolerancia_risco=0.3,           # Baixa tolerância
    meses_protegidos=6              # 6 meses protegidos
)

# Criar modelo
modelo = CashAllocationModel(params)

# Sugerir alocação automática
alocacao = modelo.suggest_allocation()

# Avaliar alocação
resultado = modelo.evaluate_allocation(alocacao)

# Verificar resultado
if resultado.alocacao_valida:
    print("✅ ALOCAÇÃO VÁLIDA - Você sobrevive!")
else:
    print("❌ ALOCAÇÃO INVÁLIDA - Risco alto!")

print(f"Probabilidade sobrevivência: {resultado.probabilidade_sobrevivencia_ruim:.1%}")
```

### Exemplo 2: Alocação Personalizada

```python
from cash_allocation_model import AllocationStrategy

# Definir alocação manual
alocacao_custom = AllocationStrategy(
    reserva_seguranca_pct=40.0,
    crescimento_pct=40.0,
    risco_pct=20.0
)

# Avaliar
resultado = modelo.evaluate_allocation(alocacao_custom)
```

### Exemplo 3: Exportar Resultados

```python
# Exportar para Excel
modelo.export_to_excel(resultado, "minha_analise.xlsx")

# Exportar para JSON (útil para ML)
modelo.export_to_json(resultado, "minha_analise.json")
```

### Exemplo 4: Visualizações

```python
from visualizer import Visualizer

# Criar visualizador
viz = Visualizer(resultado, params)

# Gerar dashboard completo
viz.plot_dashboard("dashboard.png")

# Ou gerar todos os gráficos
viz.generate_all_plots("meus_graficos/")
```

## 📁 Estrutura do Projeto

```
.
├── cash_allocation_model.py   # Modelo principal
├── visualizer.py               # Módulo de visualização
├── exemplo_uso.py              # Exemplos práticos
├── requirements.txt            # Dependências
├── README.md                   # Documentação
└── [Futuro]
    ├── gui_interface.py        # Interface gráfica
    ├── ml_optimizer.py         # Otimização com ML
    └── api_server.py           # API REST
```

## 📊 Outputs

### Excel (.xlsx)
- **Aba Decisão**: Resposta principal (válido/inválido)
- **Aba Valores**: Valores absolutos em R$
- **Aba Parâmetros**: Inputs utilizados
- **Aba Trajetórias**: Evolução do caixa mês a mês
- **Aba Detalhes Cenários**: Análise por cenário

### JSON (.json)
```json
{
  "decisao": {
    "alocacao_valida": true,
    "probabilidade_sobrevivencia_ruim": 0.85,
    "tempo_ate_zero_ruim": null
  },
  "alocacao": {
    "reserva_seguranca_pct": 45.2,
    "crescimento_pct": 42.3,
    "risco_pct": 12.5
  },
  "parametros": {...},
  "cenarios": {...}
}
```

### Gráficos (.png)
- Pizza da alocação
- Trajetória dos cenários
- Probabilidade de sobrevivência
- Dashboard completo

## 🎓 Conceitos Principais

### Cenários de Simulação

- **Cenário Bom**: Receitas maiores, despesas menores, retornos acima da média
- **Cenário Neutro**: Condições esperadas, sem desvios
- **Cenário Ruim**: Receitas menores, despesas maiores, retornos reduzidos

### Critério de Validade

Uma alocação é considerada **válida** se:
- Probabilidade de sobrevivência no cenário ruim ≥ 70%
- Consegue proteger os N meses definidos

### Simulação Monte Carlo

O modelo usa Monte Carlo (500-1000 simulações) para estimar com precisão a probabilidade de sobrevivência, considerando a volatilidade e incertezas.

## 🔮 Expansões Futuras

### 1. Interface Gráfica (Streamlit/Gradio)
```python
# gui_interface.py 
import streamlit as st

st.title("💰 Alocação de Caixa")
dinheiro = st.number_input("Dinheiro em mãos")
# ... mais inputs
```

### 2. Otimização com Machine Learning
```python
# ml_optimizer.py 
from sklearn.ensemble import RandomForestRegressor

# Treinar modelo para sugerir melhor alocação
# baseado em histórico de resultados
```

## 📝 Exemplos Práticos

### Executar Exemplos

```bash
# Executar todos os exemplos
python exemplo_uso.py

# Modo interativo
python exemplo_uso.py
# > Escolher "s" no modo interativo
```

## 🧪 Testes e Validação

```python
# Testar múltiplas estratégias
from exemplo_uso import exemplo_comparacao

resultados = exemplo_comparacao()
# Compara: Ultra Conservadora, Conservadora, Balanceada, 
#          Agressiva, Ultra Agressiva
```

## 📈 Interpretação dos Resultados

### Reserva de Segurança (Verde)
- Capital líquido para emergências
- Rende próximo ao CDI
- Baixíssimo risco

### Crescimento (Azul)
- Investimentos de médio risco
- Retorno moderado e estável
- Ex: Fundos de índice

### Risco (Vermelho)
- Alto potencial de retorno
- Alta volatilidade
- Ex: Projetos, apostas calculadas

## ⚠️ Avisos Importantes

1. **Não é consultoria financeira**: Este é um modelo educacional
2. **Resultados são probabilísticos**: Não garantem o futuro
3. **Ajuste os parâmetros**: Cada negócio é único
4. **Revise periodicamente**: Condições mudam com o tempo

## 🤝 Contribuindo

Sugestões de melhorias:
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/melhoria`)
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

MIT License - Livre para uso pessoal e comercial

---

**Desenvolvido para ajudar pequenos operadores a tomar decisões financeiras mais inteligentes e baseadas em dados** 🚀
