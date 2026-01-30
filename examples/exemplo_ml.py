"""
Exemplo de uso do ML Optimizer
Demonstra predições instantâneas vs simulação tradicional
"""

import sys
sys.path.insert(0, 'src')

from ml_optimizer import MLOptimizer
from cash_allocation_model import InputParameters, CashAllocationModel
import time

print("=" * 80)
print("🤖 DEMONSTRAÇÃO: ML OPTIMIZER vs MODELO TRADICIONAL")
print("=" * 80)

# Carregar modelo ML treinado
print("\n📥 Carregando modelos ML treinados...")
try:
    optimizer = MLOptimizer()
    optimizer.load_models("models/ml_optimizer")
    print("✅ Modelos carregados!")
except FileNotFoundError:
    print("❌ Modelos não encontrados!")
    print("\n⚠️  Você precisa treinar os modelos primeiro:")
    print("   cd src")
    print("   python ml_optimizer.py")
    print("\n   Isso gerará os arquivos .pkl necessários.")
    print("   Depois mova-os para a pasta models/")
    exit(1)

# Cenário de teste
params = InputParameters(
    dinheiro_em_maos=150000.0,
    caixa_mensal_esperado=25000.0,
    despesas_fixas=12000.0,
    despesas_variaveis=5000.0,
    volatilidade_caixa=0.20,
    tolerancia_risco=0.5,
    meses_protegidos=6
)

print("\n" + "=" * 80)
print("COMPARAÇÃO DE PERFORMANCE")
print("=" * 80)

# Método 1: ML (rápido)
print("\n🤖 MÉTODO 1: Machine Learning")
start = time.time()
alocacao_ml = optimizer.predict_allocation(params)
tempo_ml = time.time() - start

print(f"⚡ Tempo: {tempo_ml*1000:.2f}ms")
print(f"   Reserva: {alocacao_ml.reserva_seguranca_pct:.2f}%")
print(f"   Crescimento: {alocacao_ml.crescimento_pct:.2f}%")
print(f"   Risco: {alocacao_ml.risco_pct:.2f}%")

# Método 2: Tradicional (simulação)
print("\n🔄 MÉTODO 2: Simulação Tradicional")
start = time.time()
modelo = CashAllocationModel(params)
alocacao_tradicional = modelo.suggest_allocation()
tempo_tradicional = time.time() - start

print(f"⏱️  Tempo: {tempo_tradicional*1000:.2f}ms")
print(f"   Reserva: {alocacao_tradicional.reserva_seguranca_pct:.2f}%")
print(f"   Crescimento: {alocacao_tradicional.crescimento_pct:.2f}%")
print(f"   Risco: {alocacao_tradicional.risco_pct:.2f}%")

# Comparação
print("\n📊 ANÁLISE:")
if tempo_ml > 0:
    print(f"   ML foi {tempo_tradicional/tempo_ml:.0f}x mais rápido!")
else:
    print(f"   ML foi instantâneo!")
    
diff_reserva = abs(alocacao_ml.reserva_seguranca_pct - alocacao_tradicional.reserva_seguranca_pct)
print(f"   Diferença na alocação: {diff_reserva:.2f} pontos percentuais")

# Validar predição do ML
print("\n✅ VALIDAÇÃO DA PREDIÇÃO ML:")
resultado = modelo.evaluate_allocation(alocacao_ml)
if resultado.alocacao_valida:
    print(f"   ✅ Alocação VÁLIDA (sobrevive no cenário ruim)")
    print(f"   Probabilidade: {resultado.probabilidade_sobrevivencia_ruim:.1%}")
else:
    print(f"   ⚠️  Alocação INVÁLIDA")

print("\n" + "=" * 80)
print("💡 CONCLUSÃO:")
print("   ML é ideal para: análises em tempo real, APIs, dashboards")
print("   Tradicional é ideal para: máxima precisão, exploração")
print("=" * 80)
