---
name: option-valuation
description: Valutazione tramite option pricing (Black-Scholes) - equity come call option sugli asset aziendali
user_invocable: true
---

# Skill: Valutazione con Option Pricing

Valuta l'equity di un'azienda come una call option sugli asset usando Black-Scholes.
Particolarmente utile per aziende in distress o con alto leverage.

## Utilizzo
```
/option-valuation TICKER
/option-valuation TICKER --volatilita 0.40 --scadenza-debito 5.0
```

## Workflow

### 1. Raccolta Input
- Valore asset (V): Market cap + debito di mercato
- Debito nominale (K): Face value obbligazioni
- Scadenza media debito (T): Maturity ponderata
- Risk-free rate e volatilita'

### 2. Calcolo
```python
from valuation_analyst.tools.equity_as_option import valuta_equity_come_opzione
risultato = valuta_equity_come_opzione(V, K, T, rf, sigma)
```

### 3. Output
Valore equity, valore debito, probabilita' default, sensitivity su sigma.

### 4. Logging
Logga in prompt_log.md.
