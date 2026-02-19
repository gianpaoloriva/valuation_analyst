---
name: private-valuation
description: Valutazione di societa' private con sconti di illiquidita' e premi di controllo
user_invocable: true
---

# Skill: Valutazione Societa' Private

Applica aggiustamenti specifici per societa' non quotate alla valutazione base.

## Utilizzo
```
/private-valuation --ricavi 50000000 --ebitda 8000000 --settore "Manufacturing"
/private-valuation --valutazione-base 100000000 --tipo-partecipazione maggioranza
```

## Workflow

### 1. Valutazione Base
- Usa DCF o multipli come per una societa' quotata equivalente

### 2. Aggiustamenti
```python
from valuation_analyst.tools.illiquidity_discount import calcola_sconto_illiquidita
from valuation_analyst.tools.control_premium import calcola_premio_controllo
```

### 3. Output
Valutazione base, dettaglio sconti/premi, valore finale aggiustato.

### 4. Logging
Logga in prompt_log.md.
