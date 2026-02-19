---
name: ma-valuation
description: Valutazione M&A con stima sinergie e calcolo del valore di acquisizione
user_invocable: true
---

# Skill: Valutazione M&A e Sinergie

Calcola il valore di un'acquisizione includendo sinergie operative e finanziarie.

## Utilizzo
```
/ma-valuation --acquirente MSFT --target ATVI
/ma-valuation --acquirente MSFT --target ATVI --sinergie-costo 0.05 --sinergie-ricavo 0.03
```

## Workflow

### 1. Valutazione Standalone
- Valuta acquirente e target separatamente (DCF + multipli)

### 2. Stima Sinergie
```python
from valuation_analyst.tools.synergy_valuation import stima_sinergie
from valuation_analyst.tools.acquisition_value import calcola_valore_acquisizione
```

### 3. Output
Valutazione standalone, valore sinergie, prezzo massimo offerta, accretion/dilution.

### 4. Logging
Logga in prompt_log.md.
