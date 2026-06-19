# Guia Rápido — Modelo de Alocação de Caixa

**Comece a usar o modelo em menos de 5 minutos.**

---

## Comecar em 5 Minutos

### 1. Instalar dependências

```bash
pip install numpy pandas matplotlib seaborn openpyxl
```

### 2. Executar exemplo rápido

```bash
python teste_rapido.py
```

### 3. Verificar resultados

- `teste_resultado.xlsx` — planilha com todos os dados
- `teste_resultado.json` — dados estruturados para integração
- `graficos_teste/` — visualizações gráficas

---

## Uso Básico

### Código Mínimo

```python
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

print(f"Válido? {resultado.alocacao_valida}")
print(f"Probabilidade: {resultado.probabilidade_sobrevivencia_ruim:.1%}")
```

---

## Interpretar Resultados

### Resposta Principal

- **Alocação válida** — você sobrevive no cenário ruim (probabilidade >= 70%)
- **Alocação inválida** — risco alto; ajuste a alocação

### Componentes da Alocação

**Reserva de Segurança (verde)**
Capital líquido e disponível para emergências e despesas. Risco baixíssimo.

**Crescimento (azul)**
Investimentos de médio risco com retorno moderado e estável. Ex: fundos de índice, CDI+.

**Risco (vermelho)**
Alto potencial de retorno com alta volatilidade. Ex: projetos, apostas calculadas.

---

## Cenários Simulados

### Cenário Bom

- Receitas 15% acima do esperado
- Despesas 10% abaixo
- Retornos 20% maiores

### Cenário Neutro

- Tudo conforme esperado
- Baseline para comparação

### Cenário Ruim

- Receitas 30% abaixo do esperado
- Despesas 20% acima
- Retornos 50% menores
- **É neste cenário que você deve sobreviver**

---

## Dicas Práticas

### Se a alocação está inválida

Aumentar a reserva de segurança:

```python
alocacao = AllocationStrategy(
    reserva_seguranca_pct=60.0,  # Era 40%
    crescimento_pct=30.0,
    risco_pct=10.0
)
```

Aumentar os meses protegidos:

```python
params.meses_protegidos = 12  # Era 6
```

Reduzir exposição a risco:

```python
params.tolerancia_risco = 0.2  # Era 0.5
```

### Se quer mais exposição a oportunidades

- Aumente o capital inicial
- Reduza despesas fixas
- Aumente a receita mensal
- Melhore a previsibilidade (menor volatilidade)

---

## Personalização

### Taxas de Retorno

```python
params = InputParameters(
    ...,
    retorno_seguro=0.01,        # 1% a.m. (CDI)
    retorno_medio_risco=0.015,  # 1.5% a.m. (Fundos)
    retorno_alto_risco=0.08     # 8% a.m. (Projetos)
)
```

### Testar Múltiplas Estratégias

```python
estrategias = [
    ("Conservadora", AllocationStrategy(70, 25, 5)),
    ("Balanceada",   AllocationStrategy(40, 40, 20)),
    ("Agressiva",    AllocationStrategy(20, 40, 40)),
]

for nome, alocacao in estrategias:
    resultado = modelo.evaluate_allocation(alocacao)
    print(f"{nome}: {'Válida' if resultado.alocacao_valida else 'Inválida'}")
```

---

## Arquivos do Projeto

| Arquivo | Descrição |
|---------|-----------|
| `cash_allocation_model.py` | Motor principal |
| `visualizer.py` | Gerador de gráficos |
| `teste_rapido.py` | Teste rápido |
| `exemplo_uso.py` | Exemplos completos |
| `gui_streamlit.py` | Interface web (desabilitada) |
| `ml_optimizer.py` | Otimização com ML (desabilitada) |

---

## Avisos

- **Não é consultoria financeira** — modelo educacional
- **Resultados probabilísticos** — não garantem o futuro
- **Ajuste à sua realidade** — cada negócio é único
- **Revise periodicamente** — condições mudam

---

## Resolução de Problemas

### Erro: "Module not found"

```bash
pip install -r requirements.txt
```

### Gráficos não aparecem

```python
# Salvar ao invés de mostrar
viz.plot_dashboard("meu_dashboard.png")
```

### Simulação muito lenta

```python
resultado = modelo.evaluate_allocation(alocacao, use_monte_carlo=False)
```

---

## Próximos Passos

1. Executar `teste_rapido.py`
2. Ajustar parâmetros para sua realidade
3. Analisar os gráficos gerados
4. Testar diferentes estratégias
5. Exportar e revisar a planilha Excel
