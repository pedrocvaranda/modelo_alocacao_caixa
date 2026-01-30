"""
Teste Rápido do Modelo
"""

import sys
sys.path.insert(0, 'src')

from cash_allocation_model import InputParameters, AllocationStrategy, CashAllocationModel
from visualizer import Visualizer

print("=" * 80)
print("🚀 TESTE DO MODELO DE ALOCAÇÃO DE CAIXA")
print("=" * 80)

# Cenário: Pequeno negócio com R$ 100k no caixa
params = InputParameters(
    dinheiro_em_maos=100000.0,
    caixa_mensal_esperado=15000.0,
    despesas_fixas=8000.0,
    despesas_variaveis=3000.0,
    volatilidade_caixa=0.15,
    tolerancia_risco=0.3,
    meses_protegidos=6
)

print("\n📋 PARÂMETROS DE ENTRADA:")
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

# Avaliar (sem Monte Carlo para rapidez)
print("\n🔄 AVALIANDO ALOCAÇÃO...")
resultado = modelo.evaluate_allocation(alocacao, use_monte_carlo=False)

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

if not resultado.resultado_ruim.sobrevive:
    print(f"   ⚠️  Tempo até quebrar (ruim): {resultado.tempo_ate_zero_ruim:.1f} meses")

# Exportar
print("\n💾 EXPORTANDO RESULTADOS...")
excel_file = modelo.export_to_excel(resultado, "outputs/teste_resultado.xlsx")
json_file = modelo.export_to_json(resultado, "outputs/teste_resultado.json")
print(f"   ✓ {excel_file}")
print(f"   ✓ {json_file}")

# Visualizações
print("\n📊 GERANDO VISUALIZAÇÕES...")
try:
    viz = Visualizer(resultado, params)
    viz.generate_all_plots("outputs/graficos_teste")
    print("   ✓ Gráficos salvos em 'outputs/graficos_teste/'")
except Exception as e:
    print(f"   ⚠️  Erro ao gerar gráficos: {e}")

print("\n" + "=" * 80)
print("✅ TESTE CONCLUÍDO COM SUCESSO!")
print("=" * 80)
print("\n📁 Arquivos gerados:")
print("   • outputs/teste_resultado.xlsx - Planilha completa")
print("   • outputs/teste_resultado.json - Dados estruturados")
print("   • outputs/graficos_teste/ - Visualizações")
