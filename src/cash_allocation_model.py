"""
Modelo de Alocação de Caixa para Pequenos Operadores
Análise de sobrevivência em cenários de incerteza
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple
from datetime import datetime
import json


@dataclass
class InputParameters:
    """Parâmetros de entrada do modelo"""
    dinheiro_em_maos: float  # Capital inicial disponível
    caixa_mensal_esperado: float  # Receita mensal esperada
    despesas_fixas: float  # Despesas fixas mensais
    despesas_variaveis: float  # Despesas variáveis mensais (média)
    volatilidade_caixa: float  # Desvio padrão do caixa mensal (0-1)
    tolerancia_risco: float  # Tolerância a risco (0-1, onde 1 = máximo risco)
    meses_protegidos: int  # N meses que devem estar protegidos
    
    # Oportunidades de investimento (retorno mensal esperado)
    retorno_seguro: float = 0.009  # ~CDI mensal (exemplo: 0.9%)
    retorno_medio_risco: float = 0.01  # ~Index mensal
    retorno_alto_risco: float = 0.05  # Projetos/apostas
    
    # Volatilidades das oportunidades
    volatilidade_seguro: float = 0.001
    volatilidade_medio_risco: float = 0.05
    volatilidade_alto_risco: float = 0.15


@dataclass
class AllocationStrategy:
    """Estratégia de alocação proposta"""
    reserva_seguranca_pct: float  # % em reserva de segurança (líquida)
    crescimento_pct: float  # % em investimentos seguros/médio risco
    risco_pct: float  # % em alto risco
    
    def __post_init__(self):
        total = self.reserva_seguranca_pct + self.crescimento_pct + self.risco_pct
        if not np.isclose(total, 100.0, atol=0.01):
            raise ValueError(f"Alocação deve somar 100%. Atual: {total}%")


@dataclass
class SimulationResult:
    """Resultado da simulação de um cenário"""
    cenario: str  # 'bom', 'neutro', 'ruim'
    sobrevive: bool
    meses_ate_zero: float  # Tempo até o caixa zerar (inf se não zerar)
    probabilidade_sobrevivencia: float
    trajetoria_caixa: List[float]  # Evolução do caixa mês a mês
    
    
@dataclass
class ModelOutput:
    """Output completo do modelo"""
    alocacao_valida: bool
    reserva_seguranca_pct: float
    crescimento_pct: float
    risco_pct: float
    probabilidade_sobrevivencia_ruim: float
    tempo_ate_zero_ruim: float
    
    # Resultados detalhados por cenário
    resultado_bom: SimulationResult
    resultado_neutro: SimulationResult
    resultado_ruim: SimulationResult
    
    # Valores absolutos em R$
    reserva_seguranca_valor: float
    crescimento_valor: float
    risco_valor: float
    
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class CashAllocationModel:
    """Modelo principal de alocação de caixa"""
    
    def __init__(self, params: InputParameters):
        self.params = params
        self.simulation_months = params.meses_protegidos + 12  # Simula além do período protegido
        
    def calculate_minimum_reserve(self) -> float:
        """Calcula reserva mínima necessária para N meses de proteção"""
        despesas_mensais = self.params.despesas_fixas + self.params.despesas_variaveis
        
        # Cenário ruim: despesas maiores e caixa menor
        despesas_ruim = despesas_mensais * 1.2  # 20% a mais em despesas
        caixa_ruim = self.params.caixa_mensal_esperado * (1 - 2 * self.params.volatilidade_caixa)
        caixa_ruim = max(0, caixa_ruim)  # Não pode ser negativo
        
        deficit_mensal_ruim = max(0, despesas_ruim - caixa_ruim)
        reserva_minima = deficit_mensal_ruim * self.params.meses_protegidos
        
        return reserva_minima
    
    def suggest_allocation(self) -> AllocationStrategy:
        """Sugere uma alocação baseada nos parâmetros"""
        reserva_minima = self.calculate_minimum_reserve()
        reserva_pct = (reserva_minima / self.params.dinheiro_em_maos) * 100
        
        # Garante que a reserva não ultrapasse 100%
        reserva_pct = min(reserva_pct, 100.0)
        
        # Distribui o restante entre crescimento e risco baseado na tolerância
        restante = 100.0 - reserva_pct
        risco_pct = restante * self.params.tolerancia_risco * 0.3  # Max 30% do restante em risco
        crescimento_pct = restante - risco_pct
        
        return AllocationStrategy(
            reserva_seguranca_pct=round(reserva_pct, 2),
            crescimento_pct=round(crescimento_pct, 2),
            risco_pct=round(risco_pct, 2)
        )
    
    def simulate_scenario(
        self, 
        allocation: AllocationStrategy, 
        scenario: str
    ) -> SimulationResult:
        """
        Simula um cenário específico (bom, neutro, ruim)
        """
        # Definir multiplicadores por cenário
        scenario_params = {
            'bom': {
                'caixa_mult': 1 + self.params.volatilidade_caixa,
                'despesas_mult': 0.9,
                'retorno_mult': 1.2
            },
            'neutro': {
                'caixa_mult': 1.0,
                'despesas_mult': 1.0,
                'retorno_mult': 1.0
            },
            'ruim': {
                'caixa_mult': 1 - 2 * self.params.volatilidade_caixa,
                'despesas_mult': 1.2,
                'retorno_mult': 0.5
            }
        }
        
        params = scenario_params[scenario]
        
        # Valores iniciais de alocação
        total = self.params.dinheiro_em_maos
        reserva = total * (allocation.reserva_seguranca_pct / 100)
        crescimento = total * (allocation.crescimento_pct / 100)
        risco = total * (allocation.risco_pct / 100)
        
        caixa_total = reserva + crescimento + risco
        trajetoria = [caixa_total]
        
        # Simulação mês a mês
        for mes in range(self.simulation_months):
            # Receitas (com volatilidade)
            caixa_mensal = self.params.caixa_mensal_esperado * params['caixa_mult']
            noise = np.random.normal(0, self.params.volatilidade_caixa * caixa_mensal)
            caixa_mensal = max(0, caixa_mensal + noise)
            
            # Despesas
            despesas_fixas = self.params.despesas_fixas * params['despesas_mult']
            despesas_variaveis = self.params.despesas_variaveis * params['despesas_mult']
            despesas_variaveis += np.random.normal(0, despesas_variaveis * 0.1)
            despesas_totais = despesas_fixas + despesas_variaveis
            
            # Resultado operacional do mês
            resultado_mensal = caixa_mensal - despesas_totais
            
            # Retornos dos investimentos
            ret_crescimento = crescimento * (
                self.params.retorno_medio_risco * params['retorno_mult'] +
                np.random.normal(0, self.params.volatilidade_medio_risco)
            )
            
            ret_risco = risco * (
                self.params.retorno_alto_risco * params['retorno_mult'] +
                np.random.normal(0, self.params.volatilidade_alto_risco)
            )
            
            ret_reserva = reserva * self.params.retorno_seguro * params['retorno_mult']
            
            # Atualizar valores
            crescimento += ret_crescimento
            risco = max(0, risco + ret_risco)  # Risco pode zerar
            reserva += ret_reserva
            
            # Se resultado mensal negativo, usar reserva
            if resultado_mensal < 0:
                reserva += resultado_mensal
                if reserva < 0:
                    # Liquidar crescimento se necessário
                    crescimento += reserva
                    reserva = 0
                    if crescimento < 0:
                        # Liquidar risco em último caso
                        risco += crescimento
                        crescimento = 0
                        if risco < 0:
                            risco = 0
            else:
                # Reinvestir superávit na reserva (lugar seguro)
                # Mantém o capital seguro enquanto ganha retorno
                reserva += resultado_mensal
            
            caixa_total = reserva + crescimento + risco
            trajetoria.append(caixa_total)
            
            # Verifica se quebrou
            if caixa_total <= 0:
                meses_ate_zero = mes + 1
                sobrevive = mes >= self.params.meses_protegidos
                # Completa trajetória com zeros
                trajetoria.extend([0] * (self.simulation_months - mes))
                
                return SimulationResult(
                    cenario=scenario,
                    sobrevive=sobrevive,
                    meses_ate_zero=meses_ate_zero,
                    probabilidade_sobrevivencia=0.0 if not sobrevive else (mes / self.simulation_months),
                    trajetoria_caixa=trajetoria
                )
        
        # Sobreviveu todo o período
        return SimulationResult(
            cenario=scenario,
            sobrevive=True,
            meses_ate_zero=float('inf'),
            probabilidade_sobrevivencia=1.0,
            trajetoria_caixa=trajetoria
        )
    
    def run_monte_carlo(
        self, 
        allocation: AllocationStrategy, 
        scenario: str,
        n_simulations: int = 1000
    ) -> Tuple[float, float]:
        """
        Executa simulação Monte Carlo para estimar probabilidade de sobrevivência
        Retorna: (probabilidade_sobrevivencia, tempo_medio_ate_zero)
        """
        sobrevivencias = []
        tempos_ate_zero = []
        
        for _ in range(n_simulations):
            result = self.simulate_scenario(allocation, scenario)
            sobrevivencias.append(1.0 if result.sobrevive else 0.0)
            if result.meses_ate_zero != float('inf'):
                tempos_ate_zero.append(result.meses_ate_zero)
        
        prob_sobrevivencia = np.mean(sobrevivencias)
        tempo_medio = np.mean(tempos_ate_zero) if tempos_ate_zero else float('inf')
        
        return prob_sobrevivencia, tempo_medio
    
    def evaluate_allocation(
        self, 
        allocation: AllocationStrategy,
        use_monte_carlo: bool = True
    ) -> ModelOutput:
        """
        Avalia uma estratégia de alocação
        """
        # Simular cenários
        resultado_bom = self.simulate_scenario(allocation, 'bom')
        resultado_neutro = self.simulate_scenario(allocation, 'neutro')
        resultado_ruim = self.simulate_scenario(allocation, 'ruim')
        
        # Monte Carlo no cenário ruim para precisão
        if use_monte_carlo:
            prob_sobrev_ruim, tempo_medio_ruim = self.run_monte_carlo(
                allocation, 'ruim', n_simulations=500
            )
        else:
            prob_sobrev_ruim = 1.0 if resultado_ruim.sobrevive else 0.0
            tempo_medio_ruim = resultado_ruim.meses_ate_zero
        
        # Calcular valores absolutos
        total = self.params.dinheiro_em_maos
        reserva_valor = total * (allocation.reserva_seguranca_pct / 100)
        crescimento_valor = total * (allocation.crescimento_pct / 100)
        risco_valor = total * (allocation.risco_pct / 100)
        
        # Alocação é válida se sobrevive no cenário ruim com alta probabilidade
        alocacao_valida = prob_sobrev_ruim >= 0.7  # 70% de confiança
        
        return ModelOutput(
            alocacao_valida=alocacao_valida,
            reserva_seguranca_pct=allocation.reserva_seguranca_pct,
            crescimento_pct=allocation.crescimento_pct,
            risco_pct=allocation.risco_pct,
            probabilidade_sobrevivencia_ruim=prob_sobrev_ruim,
            tempo_ate_zero_ruim=tempo_medio_ruim,
            resultado_bom=resultado_bom,
            resultado_neutro=resultado_neutro,
            resultado_ruim=resultado_ruim,
            reserva_seguranca_valor=reserva_valor,
            crescimento_valor=crescimento_valor,
            risco_valor=risco_valor
        )
    
    def export_to_excel(self, output: ModelOutput, filename: str = "resultado_alocacao.xlsx"):
        """Exporta resultados para Excel"""
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Aba 1: Resumo da Decisão
            decisao = pd.DataFrame([{
                'Alocação Válida?': 'SIM ✓' if output.alocacao_valida else 'NÃO ✗',
                'Reserva Segurança (%)': output.reserva_seguranca_pct,
                'Crescimento (%)': output.crescimento_pct,
                'Risco (%)': output.risco_pct,
                'Probabilidade Sobrevivência (Cenário Ruim)': f"{output.probabilidade_sobrevivencia_ruim:.1%}",
                'Meses até Zero (Cenário Ruim)': output.tempo_ate_zero_ruim if output.tempo_ate_zero_ruim != float('inf') else 'N/A',
                'Timestamp': output.timestamp
            }])
            decisao.to_excel(writer, sheet_name='Decisão', index=False)
            
            # Aba 2: Valores Absolutos
            valores = pd.DataFrame([{
                'Dinheiro Total': self.params.dinheiro_em_maos,
                'Reserva Segurança (R$)': output.reserva_seguranca_valor,
                'Crescimento (R$)': output.crescimento_valor,
                'Risco (R$)': output.risco_valor,
                'Caixa Mensal Esperado': self.params.caixa_mensal_esperado,
                'Despesas Fixas': self.params.despesas_fixas,
                'Despesas Variáveis': self.params.despesas_variaveis
            }])
            valores.to_excel(writer, sheet_name='Valores', index=False)
            
            # Aba 3: Parâmetros de Entrada
            params_df = pd.DataFrame([asdict(self.params)])
            params_df.to_excel(writer, sheet_name='Parâmetros', index=False)
            
            # Aba 4: Trajetórias dos Cenários
            trajetorias = pd.DataFrame({
                'Mês': range(len(output.resultado_ruim.trajetoria_caixa)),
                'Cenário Bom': output.resultado_bom.trajetoria_caixa,
                'Cenário Neutro': output.resultado_neutro.trajetoria_caixa,
                'Cenário Ruim': output.resultado_ruim.trajetoria_caixa
            })
            trajetorias.to_excel(writer, sheet_name='Trajetórias', index=False)
            
            # Aba 5: Detalhes por Cenário
            detalhes = pd.DataFrame([
                {
                    'Cenário': 'Bom',
                    'Sobrevive?': 'Sim' if output.resultado_bom.sobrevive else 'Não',
                    'Meses até Zero': output.resultado_bom.meses_ate_zero if output.resultado_bom.meses_ate_zero != float('inf') else 'N/A',
                    'Caixa Final': output.resultado_bom.trajetoria_caixa[-1]
                },
                {
                    'Cenário': 'Neutro',
                    'Sobrevive?': 'Sim' if output.resultado_neutro.sobrevive else 'Não',
                    'Meses até Zero': output.resultado_neutro.meses_ate_zero if output.resultado_neutro.meses_ate_zero != float('inf') else 'N/A',
                    'Caixa Final': output.resultado_neutro.trajetoria_caixa[-1]
                },
                {
                    'Cenário': 'Ruim',
                    'Sobrevive?': 'Sim' if output.resultado_ruim.sobrevive else 'Não',
                    'Meses até Zero': output.resultado_ruim.meses_ate_zero if output.resultado_ruim.meses_ate_zero != float('inf') else 'N/A',
                    'Caixa Final': output.resultado_ruim.trajetoria_caixa[-1]
                }
            ])
            detalhes.to_excel(writer, sheet_name='Detalhes Cenários', index=False)
        
        return filename
    
    def export_to_json(self, output: ModelOutput, filename: str = "resultado_alocacao.json"):
        """Exporta resultados para JSON (útil para ML)"""
        
        def convert_value(val):
            """Converte valores para tipos serializáveis em JSON"""
            if isinstance(val, (np.integer, np.floating)):
                return float(val)
            elif isinstance(val, np.ndarray):
                return val.tolist()
            elif isinstance(val, (bool, np.bool_)):
                return bool(val)
            return val
        
        data = {
            'decisao': {
                'alocacao_valida': bool(output.alocacao_valida),
                'probabilidade_sobrevivencia_ruim': float(output.probabilidade_sobrevivencia_ruim),
                'tempo_ate_zero_ruim': float(output.tempo_ate_zero_ruim) if output.tempo_ate_zero_ruim != float('inf') else None
            },
            'alocacao': {
                'reserva_seguranca_pct': float(output.reserva_seguranca_pct),
                'crescimento_pct': float(output.crescimento_pct),
                'risco_pct': float(output.risco_pct),
                'reserva_seguranca_valor': float(output.reserva_seguranca_valor),
                'crescimento_valor': float(output.crescimento_valor),
                'risco_valor': float(output.risco_valor)
            },
            'parametros': {k: convert_value(v) for k, v in asdict(self.params).items()},
            'cenarios': {
                'bom': {
                    'sobrevive': bool(output.resultado_bom.sobrevive),
                    'meses_ate_zero': float(output.resultado_bom.meses_ate_zero) if output.resultado_bom.meses_ate_zero != float('inf') else None,
                    'trajetoria': [float(x) for x in output.resultado_bom.trajetoria_caixa]
                },
                'neutro': {
                    'sobrevive': bool(output.resultado_neutro.sobrevive),
                    'meses_ate_zero': float(output.resultado_neutro.meses_ate_zero) if output.resultado_neutro.meses_ate_zero != float('inf') else None,
                    'trajetoria': [float(x) for x in output.resultado_neutro.trajetoria_caixa]
                },
                'ruim': {
                    'sobrevive': bool(output.resultado_ruim.sobrevive),
                    'meses_ate_zero': float(output.resultado_ruim.meses_ate_zero) if output.resultado_ruim.meses_ate_zero != float('inf') else None,
                    'trajetoria': [float(x) for x in output.resultado_ruim.trajetoria_caixa]
                }
            },
            'timestamp': output.timestamp
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filename
