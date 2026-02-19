---
name: cost-of-capital
description: Calcola il costo del capitale (WACC, CAPM, beta) per un'azienda seguendo la metodologia Damodaran
user_invocable: true
---

# Skill: Calcolo Costo del Capitale

Calcola WACC, costo equity (CAPM) e costo debito per un'azienda specificata.

## Utilizzo
```
/cost-of-capital AAPL
/cost-of-capital "Ferrari NV"
/cost-of-capital AAPL --paese IT --settore "Automobiles"
```

## Workflow

### 1. Raccolta Dati
- Ottieni dati azienda da Massive.com (o da input utente)
- Scarica dataset Damodaran per beta di settore e ERP

### 2. Calcolo
Esegui lo script Python:
```bash
cd /Users/gianpaoloriva/Documents/Consulting/Valuation/coderepository/valuation_analyst
python -c "
from valuation_analyst.tools.capm import calcola_costo_equity
from valuation_analyst.tools.wacc import calcola_wacc
from valuation_analyst.tools.beta_estimation import stima_beta_bottom_up
from valuation_analyst.tools.risk_premium import get_equity_risk_premium
# ... esegui calcoli
"
```

### 3. Output
Presenta i risultati in formato tabellare:

| Componente | Valore |
|-----------|--------|
| Risk-Free Rate | X.XX% |
| Beta Unlevered (settore) | X.XX |
| Beta Levered | X.XX |
| ERP | X.XX% |
| Country Risk Premium | X.XX% |
| Costo Equity | X.XX% |
| Costo Debito (pre-tax) | X.XX% |
| Costo Debito (post-tax) | X.XX% |
| Peso Equity | X.XX% |
| Peso Debito | X.XX% |
| **WACC** | **X.XX%** |

### 4. Logging
Logga il risultato in prompt_log.md usando:
```python
from valuation_analyst.utils.logging_utils import log_prompt
log_prompt("cost-of-capital", "{input}", "cost-of-capital", "{summary}")
```
