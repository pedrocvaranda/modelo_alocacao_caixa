"""
Exemplo de Uso do Modelo de Alocação de Caixa
"""

import sys
sys.path.insert(0, 'src')

from cash_allocation_model import (
    InputParameters, 
    AllocationStrategy, 
    CashAllocationModel
)
import numpy as np


def exemplo_basico():
    """Exemplo básico de uso do modelo"""
    print("=" * 80)
    print("EXEMPLO 1: Pequeno Operador - Cenário Conservador")
    print("=" * 80)
    
    # Definir parâmetros de entrada
    params = InputParameters(
        dinheiro_em_maos=100000.0,  # R$ 100.000
        caixa_mensal_esperado=15000.0,  # R$ 15.000/mês
        despesas_fixas=8000.0,  # R$ 8.000/mês
        despesas_variaveis=3000.0,  # R$ 3.000/mês
        volatilidade_caixa=0.15,  # 15% de volatilidade
        tolerancia_risco=0.3,  # Baixa tolerância a risco
        meses_protegidos=6  # Proteção de 6 meses
    )
    
    # Criar modelo
    modelo = CashAllocationModel(params)
    
    # Sugestão automática de alocação
    print("\n📊 SUGESTÃO AUTOMÁTICA DE ALOCAÇÃO:")
    alocacao_sugerida = modelo.suggest_allocation()
    print(f"   Reserva de Segurança: {alocacao_sugerida.reserva_seguranca_pct:.2f}%")
    print(f"   Crescimento: {alocacao_sugerida.crescimento_pct:.2f}%")
    print(f"   Risco: {alocacao_sugerida.risco_pct:.2f}%")
    
    # Avaliar alocação
    print("\n🔄 EXECUTANDO SIMULAÇÕES...")
    resultado = modelo.evaluate_allocation(alocacao_sugerida, use_monte_carlo=True)
    
    # Mostrar resultados
    print("\n" + "=" * 80)
    print("RESULTADO DA ANÁLISE")
    print("=" * 80)
    
    if resultado.alocacao_valida:
        print("✅ ALOCAÇÃO VÁLIDA - VOCÊ SOBREVIVE NO CENÁRIO RUIM!")
    else:
        print("❌ ALOCAÇÃO INVÁLIDA - RISCO ALTO DE NÃO SOBREVIVER!")
    
    print(f"\n💰 VALORES ABSOLUTOS:")
    print(f"   Reserva de Segurança: R$ {resultado.reserva_seguranca_valor:,.2f}")
    print(f"   Crescimento: R$ {resultado.crescimento_valor:,.2f}")
    print(f"   Risco: R$ {resultado.risco_valor:,.2f}")
    
    print(f"\n📊 PERCENTUAIS:")
    print(f"   Reserva de Segurança: {resultado.reserva_seguranca_pct:.2f}%")
    print(f"   Crescimento: {resultado.crescimento_pct:.2f}%")
    print(f"   Risco: {resultado.risco_pct:.2f}%")
    
    print(f"\n📈 CENÁRIO RUIM:")
    print(f"   Probabilidade de Sobrevivência: {resultado.probabilidade_sobrevivencia_ruim:.1%}")
    if resultado.tempo_ate_zero_ruim != float('inf'):
        print(f"   Tempo até Zero: {resultado.tempo_ate_zero_ruim:.1f} meses")
    else:
        print(f"   Tempo até Zero: ∞ (não quebra)")
    
    # Exportar resultados
    print("\n💾 EXPORTANDO RESULTADOS...")
    excel_file = modelo.export_to_excel(resultado, "exemplo1_resultado.xlsx")
    json_file = modelo.export_to_json(resultado, "exemplo1_resultado.json")
    print(f"   Excel: {excel_file}")
    print(f"   JSON: {json_file}")
    
    return resultado


def exemplo_agressivo():
    """Exemplo com perfil agressivo"""
    print("\n\n" + "=" * 80)
    print("EXEMPLO 2: Pequeno Operador - Cenário Agressivo")
    print("=" * 80)
    
    params = InputParameters(
        dinheiro_em_maos=200000.0,  # R$ 200.000
        caixa_mensal_esperado=25000.0,  # R$ 25.000/mês
        despesas_fixas=12000.0,  # R$ 12.000/mês
        despesas_variaveis=5000.0,  # R$ 5.000/mês
        volatilidade_caixa=0.25,  # 25% de volatilidade (alta)
        tolerancia_risco=0.7,  # Alta tolerância a risco
        meses_protegidos=3,  # Apenas 3 meses de proteção
        retorno_alto_risco=0.08  # Projetos muito rentáveis (8% ao mês)
    )
    
    modelo = CashAllocationModel(params)
    
    # Testar alocação agressiva personalizada
    print("\n📊 TESTANDO ALOCAÇÃO AGRESSIVA:")
    alocacao_agressiva = AllocationStrategy(
        reserva_seguranca_pct=30.0,
        crescimento_pct=40.0,
        risco_pct=30.0
    )
    print(f"   Reserva de Segurança: {alocacao_agressiva.reserva_seguranca_pct:.2f}%")
    print(f"   Crescimento: {alocacao_agressiva.crescimento_pct:.2f}%")
    print(f"   Risco: {alocacao_agressiva.risco_pct:.2f}%")
    
    print("\n🔄 EXECUTANDO SIMULAÇÕES...")
    resultado = modelo.evaluate_allocation(alocacao_agressiva, use_monte_carlo=True)
    
    print("\n" + "=" * 80)
    print("RESULTADO DA ANÁLISE")
    print("=" * 80)
    
    if resultado.alocacao_valida:
        print("✅ ALOCAÇÃO VÁLIDA - VOCÊ SOBREVIVE NO CENÁRIO RUIM!")
    else:
        print("❌ ALOCAÇÃO INVÁLIDA - RISCO ALTO DE NÃO SOBREVIVER!")
    
    print(f"\n💰 VALORES ABSOLUTOS:")
    print(f"   Reserva de Segurança: R$ {resultado.reserva_seguranca_valor:,.2f}")
    print(f"   Crescimento: R$ {resultado.crescimento_valor:,.2f}")
    print(f"   Risco: R$ {resultado.risco_valor:,.2f}")
    
    print(f"\n📈 RESULTADOS POR CENÁRIO:")
    cenarios = [
        ('Bom', resultado.resultado_bom),
        ('Neutro', resultado.resultado_neutro),
        ('Ruim', resultado.resultado_ruim)
    ]
    
    for nome, cenario in cenarios:
        status = "✅ Sobrevive" if cenario.sobrevive else "❌ Quebra"
        tempo = f"{cenario.meses_ate_zero:.1f} meses" if cenario.meses_ate_zero != float('inf') else "∞"
        caixa_final = cenario.trajetoria_caixa[-1]
        print(f"   {nome:8s}: {status} | Tempo até zero: {tempo:12s} | Caixa final: R$ {caixa_final:,.2f}")
    
    # Exportar
    modelo.export_to_excel(resultado, "exemplo2_resultado.xlsx")
    modelo.export_to_json(resultado, "exemplo2_resultado.json")
    
    return resultado


def exemplo_comparacao():
    """Compara múltiplas estratégias"""
    print("\n\n" + "=" * 80)
    print("EXEMPLO 3: Comparação de Estratégias")
    print("=" * 80)
    
    params = InputParameters(
        dinheiro_em_maos=150000.0,
        caixa_mensal_esperado=20000.0,
        despesas_fixas=10000.0,
        despesas_variaveis=4000.0,
        volatilidade_caixa=0.20,
        tolerancia_risco=0.5,
        meses_protegidos=6
    )
    
    modelo = CashAllocationModel(params)
    
    # Definir estratégias para comparar
    estrategias = [
        ("Ultra Conservadora", AllocationStrategy(70, 25, 5)),
        ("Conservadora", AllocationStrategy(50, 40, 10)),
        ("Balanceada", AllocationStrategy(40, 40, 20)),
        ("Agressiva", AllocationStrategy(30, 40, 30)),
        ("Ultra Agressiva", AllocationStrategy(20, 30, 50))
    ]
    
    print("\n📊 COMPARANDO ESTRATÉGIAS:\n")
    
    resultados = []
    for nome, estrategia in estrategias:
        resultado = modelo.evaluate_allocation(estrategia, use_monte_carlo=False)
        resultados.append((nome, resultado))
        
        status = "✅" if resultado.alocacao_valida else "❌"
        print(f"{status} {nome:20s} | Prob. Sobrev: {resultado.probabilidade_sobrevivencia_ruim:.1%} | "
              f"R: {estrategia.reserva_seguranca_pct:.0f}% C: {estrategia.crescimento_pct:.0f}% A: {estrategia.risco_pct:.0f}%")
    
    # Encontrar a melhor válida
    validas = [(n, r) for n, r in resultados if r.alocacao_valida]
    if validas:
        melhor = max(validas, key=lambda x: x[1].risco_pct)  # Maior exposição a risco entre as válidas
        print(f"\n🏆 MELHOR ESTRATÉGIA VÁLIDA: {melhor[0]}")
    
    return resultados


def exemplo_interativo():
    """Interface interativa simples"""
    print("\n\n" + "=" * 80)
    print("MODO INTERATIVO - Insira seus dados")
    print("=" * 80)
    
    try:
        print("\n💵 DADOS FINANCEIROS:")
        dinheiro = float(input("   Dinheiro em mãos (R$): "))
        caixa_mensal = float(input("   Caixa mensal esperado (R$): "))
        despesas_fixas = float(input("   Despesas fixas mensais (R$): "))
        despesas_variaveis = float(input("   Despesas variáveis mensais (R$): "))
        
        print("\n⚙️ PARÂMETROS DE RISCO:")
        volatilidade = float(input("   Volatilidade do caixa (0-1, ex: 0.15 para 15%): "))
        tolerancia = float(input("   Tolerância a risco (0-1, ex: 0.5 para médio): "))
        meses = int(input("   Meses a proteger: "))
        
        params = InputParameters(
            dinheiro_em_maos=dinheiro,
            caixa_mensal_esperado=caixa_mensal,
            despesas_fixas=despesas_fixas,
            despesas_variaveis=despesas_variaveis,
            volatilidade_caixa=volatilidade,
            tolerancia_risco=tolerancia,
            meses_protegidos=meses
        )
        
        modelo = CashAllocationModel(params)
        alocacao = modelo.suggest_allocation()
        
        print(f"\n📊 ALOCAÇÃO SUGERIDA:")
        print(f"   Reserva: {alocacao.reserva_seguranca_pct:.2f}%")
        print(f"   Crescimento: {alocacao.crescimento_pct:.2f}%")
        print(f"   Risco: {alocacao.risco_pct:.2f}%")
        
        confirma = input("\nAvaliar esta alocação? (s/n): ")
        if confirma.lower() == 's':
            resultado = modelo.evaluate_allocation(alocacao)
            
            if resultado.alocacao_valida:
                print("\n✅ ALOCAÇÃO VÁLIDA!")
            else:
                print("\n❌ ALOCAÇÃO INVÁLIDA!")
            
            print(f"Probabilidade de sobrevivência (cenário ruim): {resultado.probabilidade_sobrevivencia_ruim:.1%}")
            
            modelo.export_to_excel(resultado, "resultado_interativo.xlsx")
            modelo.export_to_json(resultado, "resultado_interativo.json")
            print("\n💾 Resultados exportados!")
            
    except Exception as e:
        print(f"\n❌ Erro: {e}")


if __name__ == "__main__":
    # Executar exemplos
    print("\n🚀 MODELO DE ALOCAÇÃO DE CAIXA - EXEMPLOS DE USO\n")
    
    # Exemplo 1: Conservador
    exemplo_basico()
    
    # Exemplo 2: Agressivo
    exemplo_agressivo()
    
    # Exemplo 3: Comparação
    exemplo_comparacao()
    
    # Exemplo 4: Interativo
    resposta = input("\n\nDeseja usar o modo interativo? (s/n): ")
    if resposta.lower() == 's':
        exemplo_interativo()
    
    print("\n\n✅ Exemplos concluídos!")
    print("📁 Verifique os arquivos .xlsx e .json gerados")
