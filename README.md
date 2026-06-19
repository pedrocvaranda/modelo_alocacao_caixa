# Cash Allocation Model

**Smart cash allocation system with scenario simulation and Machine Learning optimization**

---

## What is This?

This project answers a practical question: **"How should a small operator allocate their cash between safety, growth, and risk under uncertainty?"**

**Key Features:**

- **3-scenario simulation** — Best, Neutral, and Worst cases via Monte Carlo (500–1,000 iterations)
- **Automatic allocation suggestion** — optimized recommendation based on your input parameters
- **Strategy validation** — checks whether your allocation guarantees survival in the worst-case scenario
- **Full visualizations** — dashboard with allocation pie, cash trajectories, and survival probabilities
- **Export** — results in Excel (.xlsx) and JSON formats

---

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/pedrocvaranda/modelo_alocacao_caixa.git
cd modelo_alocacao_caixa

# Install dependencies
pip install -r requirements.txt
```

### Your First Analysis

```python
from cash_allocation_model import InputParameters, CashAllocationModel

# Define parameters
params = InputParameters(
    dinheiro_em_maos=100000.0,      # R$ 100k available
    caixa_mensal_esperado=15000.0,  # R$ 15k/month revenue
    despesas_fixas=8000.0,          # R$ 8k/month fixed costs
    despesas_variaveis=3000.0,      # R$ 3k/month variable costs
    volatilidade_caixa=0.15,        # 15% revenue uncertainty
    tolerancia_risco=0.3,           # Low risk tolerance
    meses_protegidos=6              # Protect 6 months of runway
)

# Create model and suggest allocation
modelo = CashAllocationModel(params)
alocacao = modelo.suggest_allocation()
resultado = modelo.evaluate_allocation(alocacao)

# Check result
if resultado.alocacao_valida:
    print("VALID ALLOCATION — You survive the worst-case scenario!")
else:
    print("INVALID ALLOCATION — Too much risk!")

print(f"Survival probability: {resultado.probabilidade_sobrevivencia_ruim:.1%}")
```

---

## Model

### The 7 Input Variables

| # | Variable | Description |
|---|----------|-------------|
| 1 | Cash on hand | Capital currently available |
| 2 | Expected monthly cash flow | Projected monthly revenue |
| 3 | Fixed expenses | Monthly fixed costs |
| 4 | Variable expenses | Monthly variable costs |
| 5 | Cash flow volatility | Revenue uncertainty (0–1) |
| 6 | Risk tolerance | Appetite for risk (0–1) |
| 7 | Investment opportunities | Safe, medium-risk, and high-risk options |

### Validity Criterion

An allocation is considered **valid** when the worst-case survival probability is ≥ 70% and the N protected months are fully guaranteed.

### The 3 Capital Buckets

```text
Safety Reserve (green)  →  immediate liquidity, low-risk fixed income
Growth (blue)           →  medium risk, e.g. index funds (~1%/month)
Risk (red)              →  high potential, e.g. projects (~5%/month)
```

---

## Project Structure

```text
modelo_alocacao_caixa/
├── README.md
├── src/
│   ├── cash_allocation_model.py   # Core model and simulation engine
│   ├── visualizer.py              # Dashboard and chart generation
│   ├── ml_optimizer.py            # ML-based optimization
│   └── gui_interface.py           # Graphical interface
├── examples/
│   └── exemplo_uso.py             # START HERE
├── data/                          # Input and reference data
├── models/                        # Trained models
├── outputs/                       # Generated results
├── assets/                        # Images and resources
└── docs/                          # Additional documentation
```

---

## Examples

### Example 1: Custom Allocation

```python
from cash_allocation_model import AllocationStrategy

custom_allocation = AllocationStrategy(
    reserva_seguranca_pct=40.0,
    crescimento_pct=40.0,
    risco_pct=20.0
)

resultado = modelo.evaluate_allocation(custom_allocation)
```

### Example 2: Comparing Strategies

```python
from examples.exemplo_uso import exemplo_comparacao

# Compares: Ultra Conservative, Conservative, Balanced, Aggressive, Ultra Aggressive
results = exemplo_comparacao()
```

### Example 3: Exporting Results

```python
# Export to Excel (5 sheets: Decision, Values, Parameters, Trajectories, Scenario Details)
modelo.export_to_excel(resultado, "my_analysis.xlsx")

# Export to JSON (useful for ML pipelines)
modelo.export_to_json(resultado, "my_analysis.json")
```

### Example 4: Visualizations

```python
from src.visualizer import Visualizer

viz = Visualizer(resultado, params)
viz.plot_dashboard("dashboard.png")     # Full dashboard
viz.generate_all_plots("charts/")       # All charts individually
```

---

## Important Disclaimers

- **Not financial advice** — this is an educational and decision-support tool
- **Results are probabilistic** — they do not guarantee future outcomes
- **Tune your parameters** — every business has its own dynamics
- **Review periodically** — market conditions change over time

---

## About the Author

**Pedro Coutinho Varanda**

- **#1 Brazil** — National Astronomy Olympiad (OBA 2025, Perfect Score)
- **#2 Brazil** — OBA 2023
- **#3 Brazil** — OBA 2024
- **3x Selected** — International Olympiad on Astronomy and Astrophysics (IOAA)
- **4x Gold** — Canguru Mathematics Competition (2022–2025)

ML/AI enthusiast | Rio de Janeiro, Brazil

[GitHub](https://github.com/pedrocvaranda) • [ORCID](https://orcid.org/0009-0004-5199-1745) • [Email](mailto:pedrocvaranda@gmail.com)

---

## Contributing

Contributions are welcome! Feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Related Projects

- [Varandian Optics Simulator](https://github.com/pedrocvaranda/varadian-optics-simulator) — Light propagation simulator in curved spaces
- [Chess Trainer](https://github.com/pedrocvaranda/treinador-xadrez) — AI-powered chess opening trainer

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.18529639-blue?style=flat&logo=doi)](https://doi.org/10.5281/zenodo.18529639) [![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org) [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![ML](https://img.shields.io/badge/ML-scikit--learn-orange.svg)](https://scikit-learn.org) [![Status](https://img.shields.io/badge/status-active-success.svg)]()