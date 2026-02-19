---
name: comparable-analysis
description: Esegue analisi dei comparabili e valutazione relativa tramite multipli di mercato
user_invocable: true
---

# Skill: Analisi Comparabili e Valutazione Relativa

Calcola il valore di un'azienda attraverso multipli di mercato e confronto con societa' comparabili.

## Utilizzo
```
/comparable-analysis AAPL
/comparable-analysis AAPL --multipli "PE,EV_EBITDA,PB"
/comparable-analysis AAPL --comparabili "MSFT,GOOGL,META,AMZN"
```

## Workflow

### 1. Identificazione Comparabili
- Stesso settore/industria
- Dimensione simile (market cap)
- Profilo di crescita comparabile
- Stessa area geografica (preferibilmente)

### 2. Calcolo Multipli
```python
from valuation_analyst.tools.multiples import calcola_multipli, statistiche_multipli
from valuation_analyst.tools.comparable_screen import seleziona_comparabili
```

### 3. Output
Tabella comparabili + valore implicito per azione per ogni multiplo.

### 4. Logging
Logga in prompt_log.md.
