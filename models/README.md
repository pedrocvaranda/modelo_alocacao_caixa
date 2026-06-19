# Modelos de Machine Learning

**Os modelos ML estão incluídos no repositório — você não precisa treiná-los localmente.**

---


## Como Treinar

### Opção 1: Automático (Recomendado)

```bash
cd src
python ml_optimizer.py
```

Isso irá:

1. Gerar 10.000 amostras de treino
2. Treinar 3 modelos Random Forest
3. Salvar os modelos como `.pkl`

### Opção 2: Manual

```python
from ml_optimizer import MLOptimizer

optimizer = MLOptimizer()
optimizer.generate_training_data(n_samples=10000)
optimizer.train()
optimizer.save_models(prefix="models/ml_optimizer")
```

---

## Arquivos Gerados

| Arquivo | Descrição | Tamanho |
|---------|-----------|---------|
| `ml_optimizer_reserva.pkl` | Modelo para % Reserva | ~2–5 MB |
| `ml_optimizer_crescimento.pkl` | Modelo para % Crescimento | ~2–5 MB |
| `ml_optimizer_risco.pkl` | Modelo para % Risco | ~2–5 MB |
| `ml_optimizer_scaler.pkl` | Normalizador de features | ~50 KB |

---

## Performance Esperada

- **R² Reserva**: ~0.92
- **R² Crescimento**: ~0.94
- **R² Risco**: ~0.89

---

## Uso após Treinamento

```python
from ml_optimizer import MLOptimizer
from cash_allocation_model import InputParameters

# Carregar modelos
optimizer = MLOptimizer()
optimizer.load_models("models/ml_optimizer")

# Fazer predição
params = InputParameters(...)
alocacao = optimizer.predict_allocation(params)  # Instantâneo
```

---

## Resolução de Problemas

### Erro: "Modelos não encontrados"

Execute o treinamento conforme as instruções acima e verifique se os arquivos `.pkl` estão na pasta `models/`.

### Treinamento muito lento

```python
# Reduza o número de amostras
optimizer.generate_training_data(n_samples=5000)
# Use menos árvores
RandomForestRegressor(n_estimators=50)
```

### Falta de memória

Reduza `n_samples` para 3.000 ou menos e feche outros aplicativos.

---

## Notas

- Os modelos são específicos para os parâmetros de treino
- Re-treinar com dados diferentes pode melhorar a performance
- Os modelos aprendem com o modelo base (`CashAllocationModel`)
