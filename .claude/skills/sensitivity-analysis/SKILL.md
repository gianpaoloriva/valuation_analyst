---
name: sensitivity-analysis
description: Analisi di sensitivita' 2D, scenari best/base/worst e simulazione Monte Carlo
user_invocable: true
---

# Skill: Analisi di Sensitivita' e Rischio

Esegue analisi di sensitivita', scenari e simulazioni Monte Carlo sulla valutazione.

## Utilizzo
```
/sensitivity-analysis AAPL --tipo sensitivity
/sensitivity-analysis AAPL --tipo scenari
/sensitivity-analysis AAPL --tipo montecarlo --iterazioni 10000
```

## Workflow

### 1. Input
- Modello di valutazione base (DCF o altro)
- Parametri da variare e range

### 2. Calcolo
```python
from valuation_analyst.tools.sensitivity_table import crea_tabella_sensitivity
from valuation_analyst.tools.scenario_analysis import analisi_scenari
from valuation_analyst.tools.monte_carlo import simulazione_monte_carlo
```

### 3. Output
Tabelle sensitivity, valore atteso scenari, distribuzione Monte Carlo.

### 4. Logging
Logga in prompt_log.md.
