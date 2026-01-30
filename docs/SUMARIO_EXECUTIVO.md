# 📋 SUMÁRIO EXECUTIVO
## Modelo de Alocação de Caixa para Pequenos Operadores

---

## 🎯 Objetivo

Responder à pergunta crítica: **"Como um pequeno operador deve alocar seu caixa entre poupança, reinvestimento e risco em um cenário de incerteza?"**

---

## 🔑 Proposta de Valor

✅ **Decisão Objetiva**: Retorna "SIM" ou "NÃO" baseado em simulações  
✅ **3 Cenários**: Bom, Neutro e Ruim (pior caso)  
✅ **Garantia de Sobrevivência**: Protege N meses definidos  
✅ **Maximiza Oportunidades**: Preserva exposição a crescimento e risco  

---

## 📊 Inputs do Modelo (7 Variáveis)

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

- **Seguras**: CDI, Tesouro (~0.9% a.m.)
- **Médio Risco**: Fundos de índice (~1% a.m.)
- **Alto Risco**: Projetos, apostas (~5% a.m.)

---

## 📈 Outputs do Modelo

### Resposta Principal
```
SE alocação válida → ✅ "VOCÊ SOBREVIVE NO CENÁRIO RUIM"
SE alocação inválida → ❌ "RISCO ALTO DE NÃO SOBREVIVER"
```

### Métricas Detalhadas

1. **% Reserva de Segurança** (capital líquido)
2. **% Crescimento** (investimentos médio risco)
3. **% Risco** (investimentos alto risco)
4. **Probabilidade de Sobrevivência** (cenário ruim)
5. **Tempo até Zero** (cenário ruim, se aplicável)

---

## 🔄 Metodologia

### 1. Simulação de Cenários

**Cenário Bom:**
- Receitas +15%
- Despesas -10%
- Retornos +20%

**Cenário Neutro:**
- Condições esperadas
- Baseline

**Cenário Ruim:**
- Receitas -30%
- Despesas +20%
- Retornos -50%

### 2. Critério de Validade

Alocação é **válida** se:
- Probabilidade de sobrevivência ≥ 70% no cenário ruim
- Protege todos os N meses definidos

### 3. Monte Carlo (Opcional)

500-1000 simulações para estimar probabilidades com alta precisão

---

## 💻 Arquitetura Técnica

### Módulos Core

```
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

- **visualizer.py**: Gráficos (matplotlib, seaborn)
- **exemplo_uso.py**: 4 exemplos práticos
- **teste_rapido.py**: Teste automatizado

### Expansões Futuras (Templates)

- **gui_streamlit.py**: Interface web interativa
- **ml_optimizer.py**: Otimização com ML

---

## 📊 Formato dos Dados

### Excel (.xlsx) - 5 Abas

1. **Decisão**: Resposta principal (válido/inválido)
2. **Valores**: Alocação em R$
3. **Parâmetros**: Inputs utilizados
4. **Trajetórias**: Evolução mês a mês
5. **Detalhes Cenários**: Análise comparativa

### JSON (.json) - Estruturado

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
  "parametros": {...},
  "cenarios": {...}
}
```

---

## 🎨 Visualizações

1. **Pizza**: Distribuição da alocação (%, %)
2. **Trajetórias**: Evolução do caixa nos 3 cenários
3. **Barras**: Probabilidade de sobrevivência
4. **Dashboard**: Visão completa consolidada

---

## 🔮 Roadmap de Expansões

### Fase 1: Implementado ✅
- [x] Modelo core funcional
- [x] Simulação de 3 cenários
- [x] Exportação Excel + JSON
- [x] Visualizações completas
- [x] Documentação extensiva

### Fase 2: Planejado 🔄
- [ ] Interface gráfica (Streamlit)
- [ ] Otimização com ML
- [ ] API REST
- [ ] Integração com bancos (OFX/CSV)
- [ ] Atualização automática de taxas

### Fase 3: Avançado 🚀
- [ ] App mobile
- [ ] Multi-usuário / colaborativo
- [ ] Relatórios automatizados
- [ ] Alertas e notificações
- [ ] Backtesting com dados históricos

---

## ⚙️ Stack Tecnológico

### Core
- Python 3.12+
- NumPy (simulações numéricas)
- Pandas (manipulação de dados)

### Visualização
- Matplotlib (gráficos)
- Seaborn (estilização)

### Storage
- OpenPyXL (Excel)
- JSON (estruturado)

### Futuro
- Scikit-learn (ML)
- Streamlit/Gradio (GUI)
- FastAPI (API)

---

## 📏 Métricas de Sucesso

### Para o Usuário
- ✅ Decisão clara em <1 minuto
- ✅ Múltiplas estratégias comparáveis
- ✅ Dados exportáveis e auditáveis
- ✅ Visualizações intuitivas

### Para Desenvolvedores
- ✅ Código modular e extensível
- ✅ Documentação completa
- ✅ Fácil integração (API JSON)
- ✅ Testes automatizados

---

## 🎓 Casos de Uso

### 1. Pequeno Empreendedor
**Situação**: R$ 100k no caixa, receita volátil  
**Uso**: Decidir quanto alocar vs quanto investir  
**Resultado**: Proteção de 6 meses + exposição a crescimento

### 2. Freelancer
**Situação**: Renda irregular, despesas fixas altas  
**Uso**: Planejar reserva de emergência  
**Resultado**: Evitar quebra em meses ruins

### 3. Startup Early-Stage
**Situação**: Capital limitado, runway crítico  
**Uso**: Balancear burn rate vs investimento  
**Resultado**: Maximizar runway sem perder oportunidades

### 4. Trader/Investidor
**Situação**: Gestão de capital de trading  
**Uso**: Alocar entre risco e segurança  
**Resultado**: Preservar capital em drawdowns

---

## ⚖️ Limitações e Disclaimers

⚠️ **Não é consultoria financeira**  
⚠️ **Modelo probabilístico** (não garante o futuro)  
⚠️ **Simplificações** (não captura todos os riscos)  
⚠️ **Requer validação** (ajustar à realidade específica)

---

## 📞 Suporte e Contribuições

### Como Usar
1. Ler `GUIA_RAPIDO.md`
2. Executar `teste_rapido.py`
3. Adaptar parâmetros
4. Analisar resultados

### Como Contribuir
1. Fork do projeto
2. Implementar melhorias
3. Testar extensivamente
4. Pull request com documentação

---

## 📄 Licença

MIT License - Livre para uso pessoal e comercial

---

## ✅ Status do Projeto

**Versão**: 1.0.0  
**Status**: ✅ Funcional e Testado  
**Data**: Janeiro 2026  
**Última Atualização**: 29/01/2026  

---

**Desenvolvido para empoderar pequenos operadores com decisões financeiras inteligentes baseadas em dados.** 🚀
