---
name: dcf-valuation
description: Esegue una valutazione DCF (Discounted Cash Flow) completa con modelli FCFF/FCFE multi-stage
user_invocable: true
---

# Skill: Valutazione DCF

Calcola il valore intrinseco di un'azienda tramite Discounted Cash Flow (FCFF o FCFE).

## Utilizzo
```
/dcf-valuation AAPL
/dcf-valuation AAPL --metodo FCFF --fasi 3
/dcf-valuation AAPL --wacc 0.09 --terminal-growth 0.025
```

## Workflow

### 1. Raccolta Dati
- Dati finanziari da Massive.com API
- WACC dal modulo cost-of-capital (o da parametro)
- Crescita storica per calibrazione proiezioni

### 2. Calcolo FCFF
```python
from valuation_analyst.tools.dcf_fcff import calcola_dcf_fcff
from valuation_analyst.tools.terminal_value import calcola_terminal_value
from valuation_analyst.tools.growth_models import modello_crescita_3_fasi

risultato = calcola_dcf_fcff(
    fcff_base=fcff,
    wacc=wacc,
    crescita_alta=g_alta,
    crescita_stabile=g_stabile,
    anni_alta=5,
    anni_transizione=5,
)
```

### 3. Output
Tabella proiezione cash flow + valore finale per azione.

### 4. Logging
Logga in prompt_log.md.
