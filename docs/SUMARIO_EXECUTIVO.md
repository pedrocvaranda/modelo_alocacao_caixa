# Sumário Executivo — Modelo de Alocação de Caixa para Pequenos Operadores

**Decisão objetiva de alocação de capital sob incerteza, baseada em simulação e ML.**

---

## Objetivo

Responder à pergunta crítica: **"Como um pequeno operador deve alocar seu caixa entre poupança, reinvestimento e risco em um cenário de incerteza?"**

---

## Proposta de Valor

- **Decisão objetiva** — retorna "válido" ou "inválido" baseado em simulações
- **3 cenários** — Bom, Neutro e Ruim (pior caso)
- **Garantia de sobrevivência** — protege N meses definidos
- **Maximiza oportunidades** — preserva exposição a crescimento e risco

---

## Inputs do Modelo (7 Variáveis)

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| **Dinheiro em mãos** | Capital disponível | R$ 100.000 |
| **Caixa mensal esperado** | Receita mensal média | R$ 15.000 |
| **Despesas fixas** | Custos fixos mensais | R$ 8.000 |
| **Despesas variáveis** | Custos variáveis mensais | R$ 3.000 |
| **Volatilidade do caixa** | Incerteza da receita | 15% |
| **Tolerância a risco** | Apetite por risco | 30% |
| **Meses protegidos** | Período de segurança | 6 meses |

### Oportunidades de Investimento

- **Seguras** — CDI, Tesouro (~0.9% a.m.)
- **Médio Risco** — Fundos de índice (~1% a.m.)
- **Alto Risco** — Projetos, apostas (~5% a.m.)

---

## Outputs do Modelo

### Resposta Principal

```text
SE alocação válida   → "VOCE SOBREVIVE NO CENARIO RUIM"
SE alocação inválida → "RISCO ALTO DE NAO SOBREVIVER"
```

### Métricas Detalhadas

1. % Reserva de Segurança (capital líquido)
2. % Crescimento (investimentos médio risco)
3. % Risco (investimentos alto risco)
4. Probabilidade de Sobrevivência (cenário ruim)
5. Tempo até Zero (cenário ruim, se aplicável)

---

## Metodologia

### Simulação de Cenários

**Cenário Bom** — receitas +15%, despesas −10%, retornos +20%

**Cenário Neutro** — condições esperadas (baseline)

**Cenário Ruim** — receitas −30%, despesas +20%, retornos −50%

### Critério de Validade

Alocação é **válida** quando:
- Probabilidade de sobrevivência >= 70% no cenário ruim
- Todos os N meses definidos estão protegidos

### Monte Carlo

500–1.000 simulações para estimar probabilidades com alta precisão.

---

## Arquitetura Técnica

### Módulos Core

```text
cash_allocation_model.py
├── InputParameters       # Dataclass com inputs
├── AllocationStrategy    # Estratégia de alocação (%, %, %)
├── SimulationResult      # Resultado por cenário
├── ModelOutput           # Output completo
└── CashAllocationModel   # Motor principal
    ├── suggest_allocation()     # Sugestão automática
    ├── simulate_scenario()      # Simula um cenário
    ├── run_monte_carlo()        # Simulação probabilística
    ├── evaluate_allocation()    # Avalia estratégia
    ├── export_to_excel()        # Exporta para XLSX
    └── export_to_json()         # Exporta para JSON
```

### Módulos Auxiliares

- `visualizer.py` — gráficos (matplotlib, seaborn)
- `exemplo_uso.py` — 4 exemplos práticos
- `teste_rapido.py` — teste automatizado

### Expansões Futuras (Templates)

- `gui_streamlit.py` — interface web interativa
- `ml_optimizer.py` — otimização com ML

---

## Formato dos Dados

### Excel (.xlsx) — 5 Abas

| Aba | Conteúdo |
|-----|----------|
| Decisão | Resposta principal (válido/inválido) |
| Valores | Alocação em R$ |
| Parâmetros | Inputs utilizados |
| Trajetórias | Evolução mês a mês |
| Detalhes Cenários | Análise comparativa |

### JSON (.json) — Estruturado

```json
{
  "decisao": {
    "alocacao_valida": true,
    "probabilidade_sobrevivencia_ruim": 0.85
  },
  "alocacao": {
    "reserva_seguranca_pct": 45.2,
    "crescimento_pct": 42.3,
    "risco_pct": 12.5
  },
  "parametros": {},
  "cenarios": {}
}
```

---

## Visualizações

1. **Pizza** — distribuição da alocação (%)
2. **Trajetórias** — evolução do caixa nos 3 cenários
3. **Barras** — probabilidade de sobrevivência
4. **Dashboard** — visão completa consolidada

---

## Roadmap

### Fase 1 — Implementado

- [x] Modelo core funcional
- [x] Simulação de 3 cenários
- [x] Exportação Excel + JSON
- [x] Visualizações completas
- [x] Documentação extensiva

### Fase 2 — Planejado

- [ ] Interface gráfica (Streamlit)
- [ ] Otimização com ML
- [ ] API REST
- [ ] Integração com bancos (OFX/CSV)
- [ ] Atualização automática de taxas

### Fase 3 — Avançado

- [ ] App mobile
- [ ] Multi-usuário / colaborativo
- [ ] Relatórios automatizados
- [ ] Alertas e notificações
- [ ] Backtesting com dados históricos

---

## Stack Tecnológico

| Camada | Tecnologia |
|--------|-----------|
| Core | Python 3.12+, NumPy, Pandas |
| Visualização | Matplotlib, Seaborn |
| Storage | OpenPyXL (Excel), JSON |
| Futuro | Scikit-learn, Streamlit, FastAPI |

---

## Casos de Uso

### Pequeno Empreendedor

Situação: R$ 100k no caixa, receita volátil. Resultado: proteção de 6 meses + exposição a crescimento.

### Freelancer

Situação: renda irregular, despesas fixas altas. Resultado: evitar quebra em meses ruins.

### Startup Early-Stage

Situação: capital limitado, runway crítico. Resultado: maximizar runway sem perder oportunidades.

### Trader / Investidor

Situação: gestão de capital de trading. Resultado: preservar capital em drawdowns.

---

## Limitações e Disclaimers

- **Não é consultoria financeira**
- **Modelo probabilístico** — não garante o futuro
- **Simplificações** — não captura todos os riscos
- **Requer validação** — ajustar à realidade específica

---

## Status do Projeto

**Versão**: 1.0.0 | **Status**: Funcional e testado | **Última atualização**: Janeiro 2026