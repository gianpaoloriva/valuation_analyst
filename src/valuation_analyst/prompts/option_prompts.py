"""Template prompt per la valutazione con option pricing."""

PROMPT_EQUITY_OPZIONE = """Valuta l'equity di {ticker} come una call option sugli asset.

## Input Black-Scholes
- Valore Asset (V): {valore_asset}
- Debito Nominale (K): {debito_nominale}
- Scadenza Media Debito (T): {scadenza} anni
- Risk-Free Rate: {rf:.2%}
- Volatilita' Asset (sigma): {sigma:.1%}

## Richiesta
1. Calcola d1 e d2
2. Calcola il valore dell'equity (call option)
3. Calcola il valore del debito (V - E)
4. Determina la probabilita' di default N(-d2)
5. Confronta con la valutazione DCF
"""

PROMPT_OPZIONE_RISULTATO = """Risultato Option Pricing per {ticker}:

| Componente | Valore |
|-----------|--------|
| Valore Asset (V) | {V} |
| Debito Nominale (K) | {K} |
| d1 | {d1:.4f} |
| d2 | {d2:.4f} |
| N(d1) | {N_d1:.4f} |
| N(d2) | {N_d2:.4f} |
| **Valore Equity** | **{equity}** |
| Valore Debito | {debito} |
| Prob. Default | {prob_default:.2%} |
| YTM Implicito | {ytm:.2%} |
| Default Spread | {spread:.2%} |
"""
