"""
Módulo de Visualização - Gráficos e Dashboards
"""

import matplotlib.pyplot as plt
import seaborn as sns
from cash_allocation_model import ModelOutput, InputParameters
import numpy as np
from typing import List
import os


class Visualizer:
    """Classe para visualização de resultados"""
    
    def __init__(self, output: ModelOutput, params: InputParameters):
        self.output = output
        self.params = params
        
        # Configurar estilo
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
    
    def plot_allocation_pie(self, save_path: str = None):
        """Gráfico de pizza da alocação"""
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        
        sizes = [
            self.output.reserva_seguranca_pct,
            self.output.crescimento_pct,
            self.output.risco_pct
        ]
        labels = ['Reserva de Segurança', 'Crescimento', 'Risco']
        colors = ['#2ecc71', '#3498db', '#e74c3c']
        explode = (0.05, 0, 0)  # Destacar reserva
        
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
               autopct='%1.1f%%', shadow=True, startangle=90)
        ax.set_title('Distribuição da Alocação de Caixa', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_scenarios_trajectory(self, save_path: str = None):
        """Gráfico de trajetória dos cenários"""
        fig, ax = plt.subplots(1, 1, figsize=(14, 7))
        
        meses = range(len(self.output.resultado_ruim.trajetoria_caixa))
        
        # Plotar trajetórias
        ax.plot(meses, self.output.resultado_bom.trajetoria_caixa, 
                'g-', linewidth=2, label='Cenário Bom', alpha=0.8)
        ax.plot(meses, self.output.resultado_neutro.trajetoria_caixa, 
                'b-', linewidth=2, label='Cenário Neutro', alpha=0.8)
        ax.plot(meses, self.output.resultado_ruim.trajetoria_caixa, 
                'r-', linewidth=2, label='Cenário Ruim', alpha=0.8)
        
        # Linha do período protegido
        ax.axvline(x=self.params.meses_protegidos, color='orange', 
                   linestyle='--', linewidth=2, label=f'{self.params.meses_protegidos} meses protegidos')
        
        # Linha de zero
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.3)
        
        # Área de risco
        ax.fill_between(meses, 0, 
                        max(self.output.resultado_bom.trajetoria_caixa), 
                        alpha=0.1, color='red', label='Zona de Risco')
        
        ax.set_xlabel('Meses', fontsize=12)
        ax.set_ylabel('Caixa Total (R$)', fontsize=12)
        ax.set_title('Evolução do Caixa por Cenário', fontsize=16, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Formatar eixo Y
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_survival_probability(self, save_path: str = None):
        """Gráfico de barras com probabilidade de sobrevivência"""
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        cenarios = ['Cenário Bom', 'Cenário Neutro', 'Cenário Ruim']
        probabilidades = [
            1.0 if self.output.resultado_bom.sobrevive else 0.0,
            1.0 if self.output.resultado_neutro.sobrevive else 0.0,
            self.output.probabilidade_sobrevivencia_ruim
        ]
        colors = ['#2ecc71', '#3498db', '#e74c3c']
        
        bars = ax.bar(cenarios, probabilidades, color=colors, alpha=0.7, edgecolor='black')
        
        # Adicionar valores nas barras
        for i, (bar, prob) in enumerate(zip(bars, probabilidades)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{prob:.1%}',
                   ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        # Linha de referência (70% - limiar de validade)
        ax.axhline(y=0.7, color='orange', linestyle='--', linewidth=2, 
                   label='Limiar de Validade (70%)')
        
        ax.set_ylabel('Probabilidade de Sobrevivência', fontsize=12)
        ax.set_title('Probabilidade de Sobrevivência por Cenário', 
                     fontsize=16, fontweight='bold')
        ax.set_ylim(0, 1.1)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_allocation_bars(self, save_path: str = None):
        """Gráfico de barras empilhadas da alocação"""
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        categorias = ['Alocação Atual']
        reserva = [self.output.reserva_seguranca_valor]
        crescimento = [self.output.crescimento_valor]
        risco = [self.output.risco_valor]
        
        x = np.arange(len(categorias))
        width = 0.5
        
        p1 = ax.bar(x, reserva, width, label='Reserva de Segurança', color='#2ecc71')
        p2 = ax.bar(x, crescimento, width, bottom=reserva, 
                   label='Crescimento', color='#3498db')
        p3 = ax.bar(x, risco, width, 
                   bottom=np.array(reserva) + np.array(crescimento),
                   label='Risco', color='#e74c3c')
        
        # Adicionar valores
        for i, (r, c, a) in enumerate(zip(reserva, crescimento, risco)):
            # Reserva
            ax.text(i, r/2, f'R$ {r:,.0f}\n({self.output.reserva_seguranca_pct:.1f}%)',
                   ha='center', va='center', fontweight='bold', color='white')
            # Crescimento
            ax.text(i, r + c/2, f'R$ {c:,.0f}\n({self.output.crescimento_pct:.1f}%)',
                   ha='center', va='center', fontweight='bold', color='white')
            # Risco
            ax.text(i, r + c + a/2, f'R$ {a:,.0f}\n({self.output.risco_pct:.1f}%)',
                   ha='center', va='center', fontweight='bold', color='white')
        
        ax.set_ylabel('Valor (R$)', fontsize=12)
        ax.set_title('Alocação em Valores Absolutos', fontsize=16, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(categorias)
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_dashboard(self, save_path: str = None):
        """Dashboard completo com todos os gráficos"""
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. Pizza da Alocação
        ax1 = fig.add_subplot(gs[0, 0])
        sizes = [
            self.output.reserva_seguranca_pct,
            self.output.crescimento_pct,
            self.output.risco_pct
        ]
        labels = ['Reserva', 'Crescimento', 'Risco']
        colors = ['#2ecc71', '#3498db', '#e74c3c']
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                shadow=True, startangle=90)
        ax1.set_title('Distribuição (%)', fontweight='bold')
        
        # 2. Valores Absolutos
        ax2 = fig.add_subplot(gs[0, 1])
        valores = [
            self.output.reserva_seguranca_valor,
            self.output.crescimento_valor,
            self.output.risco_valor
        ]
        bars = ax2.barh(labels, valores, color=colors, alpha=0.7)
        ax2.set_xlabel('Valor (R$)')
        ax2.set_title('Valores Absolutos', fontweight='bold')
        ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k'))
        
        # Adicionar valores nas barras
        for bar, val in zip(bars, valores):
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2,
                    f'R$ {val:,.0f}',
                    ha='left', va='center', fontsize=9, fontweight='bold')
        
        # 3. Trajetória dos Cenários
        ax3 = fig.add_subplot(gs[1, :])
        meses = range(len(self.output.resultado_ruim.trajetoria_caixa))
        ax3.plot(meses, self.output.resultado_bom.trajetoria_caixa, 
                'g-', linewidth=2, label='Bom', alpha=0.8)
        ax3.plot(meses, self.output.resultado_neutro.trajetoria_caixa, 
                'b-', linewidth=2, label='Neutro', alpha=0.8)
        ax3.plot(meses, self.output.resultado_ruim.trajetoria_caixa, 
                'r-', linewidth=2, label='Ruim', alpha=0.8)
        ax3.axvline(x=self.params.meses_protegidos, color='orange', 
                   linestyle='--', linewidth=2, label=f'{self.params.meses_protegidos}M protegidos')
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.3)
        ax3.set_xlabel('Meses')
        ax3.set_ylabel('Caixa (R$)')
        ax3.set_title('Evolução do Caixa', fontweight='bold')
        ax3.legend(loc='best', ncol=4)
        ax3.grid(True, alpha=0.3)
        ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k'))
        
        # 4. Probabilidade de Sobrevivência
        ax4 = fig.add_subplot(gs[2, 0])
        cenarios = ['Bom', 'Neutro', 'Ruim']
        probs = [
            1.0 if self.output.resultado_bom.sobrevive else 0.0,
            1.0 if self.output.resultado_neutro.sobrevive else 0.0,
            self.output.probabilidade_sobrevivencia_ruim
        ]
        bars = ax4.bar(cenarios, probs, color=colors, alpha=0.7)
        ax4.axhline(y=0.7, color='orange', linestyle='--', linewidth=2)
        ax4.set_ylabel('Probabilidade')
        ax4.set_title('Prob. Sobrevivência', fontweight='bold')
        ax4.set_ylim(0, 1.1)
        ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
        
        for bar, prob in zip(bars, probs):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{prob:.0%}',
                    ha='center', va='bottom', fontweight='bold')
        
        # 5. Informações Resumidas
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.axis('off')
        
        # Status da alocação
        status = "✅ VÁLIDA" if self.output.alocacao_valida else "❌ INVÁLIDA"
        status_color = 'green' if self.output.alocacao_valida else 'red'
        
        info_text = f"""
RESUMO DA ANÁLISE

Status: {status}
        
Capital Total: R$ {self.params.dinheiro_em_maos:,.2f}

Despesas Mensais:
  • Fixas: R$ {self.params.despesas_fixas:,.2f}
  • Variáveis: R$ {self.params.despesas_variaveis:,.2f}
  
Caixa Mensal: R$ {self.params.caixa_mensal_esperado:,.2f}

Volatilidade: {self.params.volatilidade_caixa:.1%}
Tolerância Risco: {self.params.tolerancia_risco:.1%}

Prob. Sobrev. (Ruim): {self.output.probabilidade_sobrevivencia_ruim:.1%}
"""
        
        ax5.text(0.1, 0.9, info_text, transform=ax5.transAxes,
                fontsize=10, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        # Título principal
        fig.suptitle('DASHBOARD - ANÁLISE DE ALOCAÇÃO DE CAIXA', 
                    fontsize=18, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def generate_all_plots(self, output_dir: str = "graficos"):
        """Gera todos os gráficos e salva em um diretório"""
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"📊 Gerando gráficos em '{output_dir}/'...")
        
        self.plot_allocation_pie(f"{output_dir}/alocacao_pizza.png")
        print("   ✓ alocacao_pizza.png")
        
        self.plot_scenarios_trajectory(f"{output_dir}/trajetoria_cenarios.png")
        print("   ✓ trajetoria_cenarios.png")
        
        self.plot_survival_probability(f"{output_dir}/probabilidade_sobrevivencia.png")
        print("   ✓ probabilidade_sobrevivencia.png")
        
        self.plot_allocation_bars(f"{output_dir}/alocacao_barras.png")
        print("   ✓ alocacao_barras.png")
        
        self.plot_dashboard(f"{output_dir}/dashboard_completo.png")
        print("   ✓ dashboard_completo.png")
        
        print(f"\n✅ Todos os gráficos salvos em '{output_dir}/'")
