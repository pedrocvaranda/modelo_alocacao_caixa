"""
Exemplo de Análise Personalizada
Adapte este arquivo com seus próprios dados
"""

import sys
sys.path.insert(0, 'src')

from cash_allocation_model import InputParameters, CashAllocationModel
from visualizer import Visualizer

print("=" * 80)
print("💰 MINHA ANÁLISE PERSONALIZADA")
print("=" * 80)

# ========================================
# CONFIGURE SEUS DADOS AQUI
# ========================================

params = InputParameters(
    dinheiro_em_maos=150000.0,       # SEU caixa atual
    caixa_mensal_esperado=25000.0,   # SUA receita mensal
    despesas_fixas=12000.0,          # SUAS despesas fixas
    despesas_variaveis=5000.0,       # SUAS despesas variáveis
    volatilidade_caixa=0.20,         # SUA incerteza (0.20 = 20%)
    tolerancia_risco=0.5,            # SEU apetite por risco (0.5 = médio)
    meses_protegidos=6               # Quantos meses VOCÊ quer garantir
)

# ========================================
# ANÁLISE AUTOMÁTICA
# ========================================

print("\n📋 SEUS PARÂMETROS:")
print(f"   Capital disponível: R$ {params.dinheiro_em_maos:,.2f}")
print(f"   Receita mensal: R$ {params.caixa_mensal_esperado:,.2f}")
print(f"   Despesas fixas: R$ {params.despesas_fixas:,.2f}")
print(f"   Despesas variáveis: R$ {params.despesas_variaveis:,.2f}")
print(f"   Volatilidade: {params.volatilidade_caixa:.1%}")
print(f"   Tolerância a risco: {params.tolerancia_risco:.1%}")
print(f"   Meses protegidos: {params.meses_protegidos}")

# Criar modelo
modelo = CashAllocationModel(params)

# Sugerir alocação
print("\n🤖 SUGESTÃO AUTOMÁTICA DO MODELO:")
alocacao = modelo.suggest_allocation()
print(f"   📊 Reserva de Segurança: {alocacao.reserva_seguranca_pct:.2f}%")
print(f"   📈 Crescimento: {alocacao.crescimento_pct:.2f}%")
print(f"   🎲 Risco: {alocacao.risco_pct:.2f}%")

# Avaliar
print("\n🔄 AVALIANDO ALOCAÇÃO...")
resultado = modelo.evaluate_allocation(alocacao, use_monte_carlo=True)

# Resultado
print("\n" + "=" * 80)
print("📊 RESULTADO")
print("=" * 80)

if resultado.alocacao_valida:
    print("\n✅ ALOCAÇÃO VÁLIDA - VOCÊ SOBREVIVE NO CENÁRIO RUIM!\n")
else:
    print("\n❌ ALOCAÇÃO INVÁLIDA - RISCO DE NÃO SOBREVIVER!\n")

print(f"💰 VALORES (R$):")
print(f"   Reserva: R$ {resultado.reserva_seguranca_valor:,.2f}")
print(f"   Crescimento: R$ {resultado.crescimento_valor:,.2f}")
print(f"   Risco: R$ {resultado.risco_valor:,.2f}")
print(f"   TOTAL: R$ {params.dinheiro_em_maos:,.2f}")

print(f"\n📈 ANÁLISE POR CENÁRIO:")
print(f"   Cenário BOM:    {'✅ Sobrevive' if resultado.resultado_bom.sobrevive else '❌ Quebra'}")
print(f"   Cenário NEUTRO: {'✅ Sobrevive' if resultado.resultado_neutro.sobrevive else '❌ Quebra'}")
print(f"   Cenário RUIM:   {'✅ Sobrevive' if resultado.resultado_ruim.sobrevive else '❌ Quebra'}")

print(f"\n🎯 CENÁRIO RUIM (pior caso):")
print(f"   Probabilidade de sobrevivência: {resultado.probabilidade_sobrevivencia_ruim:.1%}")
if resultado.tempo_ate_zero_ruim != float('inf'):
    print(f"   ⚠️  Tempo até quebrar: {resultado.tempo_ate_zero_ruim:.1f} meses")
else:
    print(f"   ✅ Não quebra durante o período simulado")

# Exportar
print("\n💾 EXPORTANDO RESULTADOS...")
excel_file = modelo.export_to_excel(resultado, "outputs/minha_analise.xlsx")
json_file = modelo.export_to_json(resultado, "outputs/minha_analise.json")
print(f"   ✓ {excel_file}")
print(f"   ✓ {json_file}")

# Visualizações
print("\n📊 GERANDO VISUALIZAÇÕES...")
try:
    viz = Visualizer(resultado, params)
    viz.generate_all_plots("outputs/meus_graficos")
    print("   ✓ Gráficos salvos em 'outputs/meus_graficos/'")
except Exception as e:
    print(f"   ⚠️  Erro ao gerar gráficos: {e}")
    print("   (Isso é normal se estiver sem display gráfico)")

print("\n" + "=" * 80)
print("✅ ANÁLISE CONCLUÍDA!")
print("=" * 80)
print("\n📁 Arquivos gerados:")
print("   • outputs/minha_analise.xlsx - Planilha completa")
print("   • outputs/minha_analise.json - Dados estruturados")
print("   • outputs/meus_graficos/ - Visualizações (se disponível)")
print("\n💡 Próximos passos:")
print("   1. Abra minha_analise.xlsx no Excel")
print("   2. Veja os gráficos em meus_graficos/dashboard_completo.png")
print("   3. Ajuste os parâmetros acima e rode novamente!")
