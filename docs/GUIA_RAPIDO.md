# 🚀 GUIA RÁPIDO - Modelo de Alocação de Caixa

## ⚡ Começar em 5 Minutos

### 1. Instalar dependências

```bash
pip install -r src/requirements.txt
```

### 2. Executar exemplo rápido

```bash
python examples/teste_rapido.py
```

### 3. Verificar resultados

- 📊 **teste_resultado.xlsx** - Planilha com todos os dados
- 📄 **teste_resultado.json** - Dados estruturados para integração
- 📁 **graficos_teste/** - Visualizações gráficas

-----

## 🎯 Uso Básico

### Código Mínimo (3 linhas)

```python
import sys
sys.path.insert(0, 'src')

from cash_allocation_model import InputParameters, CashAllocationModel

params = InputParameters(
    dinheiro_em_maos=100000,
    caixa_mensal_esperado=15000,
    despesas_fixas=8000,
    despesas_variaveis=3000,
    volatilidade_caixa=0.15,
    tolerancia_risco=0.3,
    meses_protegidos=6
)

modelo = CashAllocationModel(params)
alocacao = modelo.suggest_allocation()
resultado = modelo.evaluate_allocation(alocacao)

print(f"Válido? {'✅ SIM' if resultado.alocacao_valida else '❌ NÃO'}")
print(f"Probabilidade: {resultado.probabilidade_sobrevivencia_ruim:.1%}")
```

-----

## 📊 Interpretar Resultados

### Resposta Principal

- **✅ ALOCAÇÃO VÁLIDA**: Você sobrevive no cenário ruim (≥70% de probabilidade)
- **❌ ALOCAÇÃO INVÁLIDA**: Risco alto - ajuste a alocação

### Componentes da Alocação

🟢 **Reserva de Segurança** (Verde)

- Capital líquido e disponível
- Para emergências e despesas
- Risco: Baixíssimo

🔵 **Crescimento** (Azul)

- Investimentos de médio risco
- Retorno moderado e estável
- Ex: Fundos de índice, CDI+

🔴 **Risco** (Vermelho)

- Alto potencial de retorno
- Alta volatilidade
- Ex: Projetos, apostas calculadas

-----

## 📈 Cenários Simulados

### Cenário Bom

- Receitas 15% acima do esperado
- Despesas 10% abaixo
- Retornos 20% maiores

### Cenário Neutro

- Tudo conforme esperado
- Baseline para comparação

### Cenário Ruim ⚠️

- Receitas 30% abaixo do esperado
- Despesas 20% acima
- Retornos 50% menores
- **É neste cenário que você DEVE sobreviver**

-----

## 💡 Dicas Práticas

### Como Ajustar a Alocação?

**Se a alocação está INVÁLIDA:**

1. ✅ Aumentar a reserva de segurança
   
   ```python
   alocacao = AllocationStrategy(
       reserva_seguranca_pct=60.0,  # Era 40%
       crescimento_pct=30.0,         # Era 40%
       risco_pct=10.0                # Era 20%
   )
   ```
1. ✅ Aumentar os meses protegidos
   
   ```python
   params.meses_protegidos = 12  # Era 6
   ```
1. ✅ Reduzir exposição a risco
   
   ```python
   params.tolerancia_risco = 0.2  # Era 0.5
   ```

**Se quer mais exposição a oportunidades:**

- Aumente o capital inicial
- Reduza despesas fixas
- Aumente a receita mensal
- Melhore a previsibilidade (menor volatilidade)

-----

## 🔧 Personalização

### Taxas de Retorno

```python
params = InputParameters(
    ...
    retorno_seguro=0.01,        # 1% a.m. (CDI)
    retorno_medio_risco=0.015,  # 1.5% a.m. (Fundos)
    retorno_alto_risco=0.08     # 8% a.m. (Projetos)
)
```

### Testar Múltiplas Estratégias

```python
estrategias = [
    ("Conservadora", AllocationStrategy(70, 25, 5)),
    ("Balanceada", AllocationStrategy(40, 40, 20)),
    ("Agressiva", AllocationStrategy(20, 40, 40))
]

for nome, alocacao in estrategias:
    resultado = modelo.evaluate_allocation(alocacao)
    print(f"{nome}: {'✅' if resultado.alocacao_valida else '❌'}")
```

-----

## 📁 Arquivos do Projeto

### Principais

- **src/cash_allocation_model.py** - Motor principal
- **src/visualizer.py** - Gerador de gráficos
- **examples/teste_rapido.py** - Teste rápido
- **examples/exemplo_uso.py** - Exemplos completos

### Expansões (disponíveis em `src/`)

- **gui_streamlit.py** - Interface web (Streamlit)
- **ml_optimizer.py** - Otimização com ML

### Outputs

- ***.xlsx** - Planilhas Excel
- ***.json** - Dados estruturados
- **graficos_teste/** - Gráficos PNG

-----

## ⚠️ Avisos

1. **Não é consultoria financeira** - Modelo educacional
1. **Resultados probabilísticos** - Não garantem o futuro
1. **Ajuste à sua realidade** - Cada negócio é único
1. **Revise periodicamente** - Condições mudam

-----

## 🆘 Resolução de Problemas

### Erro: “Module not found”

```bash
pip install -r src/requirements.txt
```

### Gráficos não aparecem

```python
# Salvar ao invés de mostrar
viz.plot_dashboard("meu_dashboard.png")
```

### Simulação muito lenta

```python
# Desabilitar Monte Carlo
resultado = modelo.evaluate_allocation(alocacao, use_monte_carlo=False)
```

-----

## 📞 Próximos Passos

1. ✅ Executar `python examples/teste_rapido.py`
1. ✅ Ajustar parâmetros para sua realidade
1. ✅ Analisar os gráficos gerados
1. ✅ Testar diferentes estratégias
1. ✅ Exportar e revisar a planilha Excel

**Boa sorte com sua alocação! 🚀**
