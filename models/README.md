# 🤖 Modelos de Machine Learning

## ℹ️ Modelos incluídos no repositório

Os modelos ML já estão disponíveis na pasta `models/`:

|Arquivo                       |Descrição                |
|------------------------------|-------------------------|
|`ml_optimizer_reserva.pkl`    |Modelo para % Reserva    |
|`ml_optimizer_crescimento.pkl`|Modelo para % Crescimento|
|`ml_optimizer_risco.pkl`      |Modelo para % Risco      |
|`ml_optimizer_scaler.pkl`     |Normalizador de features |

Caso queira re-treinar com novos dados ou parâmetros diferentes, siga as instruções abaixo.

## 📋 Como Re-treinar

### Opção 1: Automático (Recomendado)

```bash
cd src
python ml_optimizer.py
```

Isso irá:

1. Gerar 10.000 amostras de treino
1. Treinar 3 modelos Random Forest
1. Salvar os modelos como `.pkl`

**Tempo estimado**: 2-5 minutos  
**Espaço em disco**: ~10-20 MB

### Opção 2: Manual

```python
import sys
sys.path.insert(0, 'src')

from ml_optimizer import MLOptimizer

optimizer = MLOptimizer()
optimizer.generate_training_data(n_samples=10000)
optimizer.train()
optimizer.save_models(prefix="models/ml_optimizer")
```

## 📊 Performance Esperada

- **R² Reserva**: ~0.92
- **R² Crescimento**: ~0.94
- **R² Risco**: ~0.89

## 🚀 Uso

```python
import sys
sys.path.insert(0, 'src')

from ml_optimizer import MLOptimizer
from cash_allocation_model import InputParameters

# Carregar modelos
optimizer = MLOptimizer()
optimizer.load_models("models/ml_optimizer")

# Fazer predição
params = InputParameters(...)
alocacao = optimizer.predict_allocation(params)  # Instantâneo!
```

## 🔧 Troubleshooting

### Treinamento muito lento

- Reduza o número de amostras: `n_samples=5000`
- Use menos árvores: `RandomForestRegressor(n_estimators=50)`

### Falta de memória

- Reduza `n_samples` para 3000 ou menos
- Feche outros aplicativos

## 📝 Notas

- Os modelos são específicos para os parâmetros de treino
- Re-treinar com dados diferentes pode melhorar performance
- Os modelos aprendem com o modelo base (CashAllocationModel)
