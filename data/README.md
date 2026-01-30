# 📊 Dados de Treinamento

## training_data.csv

Dados sintéticos gerados por simulação Monte Carlo para treinar os modelos ML.

### ⚠️ IMPORTANTE: Arquivo não incluído

O arquivo `training_data.csv` **não está no repositório** pois:
- Tamanho: ~500 KB - 1 MB
- Pode ser regenerado facilmente
- Específico para cada treinamento

## 🔄 Como Gerar

### Automático (durante treinamento ML)

```bash
cd src
python ml_optimizer.py
```

O arquivo será criado automaticamente na raiz do projeto.

### Manual

```python
from ml_optimizer import MLOptimizer

optimizer = MLOptimizer()
df = optimizer.generate_training_data(n_samples=10000)
# Salvo automaticamente como 'training_data.csv'
```

## 📋 Estrutura dos Dados

### Colunas (Features - Input)

| Coluna | Descrição |
|--------|-----------|
| `dinheiro` | Capital inicial |
| `caixa_mensal` | Receita mensal esperada |
| `despesas_fixas` | Despesas fixas mensais |
| `despesas_variaveis` | Despesas variáveis mensais |
| `volatilidade` | Volatilidade do caixa (0-1) |
| `tolerancia` | Tolerância a risco (0-1) |
| `meses_protegidos` | Período de proteção |
| `indice_folga` | Receita / Despesas (calculado) |
| `meses_reserva` | Capital / Despesas (calculado) |

### Colunas (Targets - Output)

| Coluna | Descrição |
|--------|-----------|
| `reserva_pct` | % Reserva de Segurança |
| `crescimento_pct` | % Crescimento |
| `risco_pct` | % Risco |
| `valida` | Alocação é válida? (bool) |
| `prob_sobrev` | Probabilidade de sobrevivência |

### Estatísticas

- **Linhas**: 10.000 (padrão)
- **Formato**: CSV UTF-8
- **Tamanho**: ~500 KB - 1 MB
- **Separador**: `,` (vírgula)

## 🔍 Exemplo de Dados

```csv
dinheiro,caixa_mensal,despesas_fixas,despesas_variaveis,volatilidade,tolerancia,meses_protegidos,indice_folga,meses_reserva,reserva_pct,crescimento_pct,risco_pct,valida,prob_sobrev
100000.0,15000.0,8000.0,3000.0,0.15,0.3,6,1.36,9.09,16.2,76.26,7.54,1.0,1.0
```

## 📊 Análise Exploratória

Você pode analisar os dados gerados:

```python
import pandas as pd

df = pd.read_csv('training_data.csv')
print(df.describe())
print(f"Alocações válidas: {df['valida'].mean():.1%}")
```

## 🧹 Limpeza

Para regenerar dados frescos:

```bash
rm training_data.csv
cd src && python ml_optimizer.py
```

## 📝 Notas

- Dados são sintéticos (gerados por simulação)
- Representam cenários diversos de pequenos operadores
- Usados apenas para treinar modelos ML
- Não contêm dados reais ou sensíveis
