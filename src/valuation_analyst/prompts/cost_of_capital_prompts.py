"""Template prompt per il costo del capitale."""

PROMPT_WACC = """Calcola il WACC per {ticker} ({nome}).

## Dati Input
- Settore: {settore}
- Paese: {paese}
- Market Cap: {market_cap}
- Total Debt: {total_debt}
- Tax Rate: {tax_rate:.1%}
- Beta di mercato: {beta}

## Richiesta
1. Determina il risk-free rate appropriato
2. Stima il beta bottom-up (unlevered settore -> relevered per D/E)
3. Calcola l'ERP (+ Country Risk Premium se applicabile)
4. Calcola il costo equity (CAPM)
5. Stima il costo del debito (da rating o interest coverage)
6. Calcola il WACC
"""

PROMPT_WACC_RISULTATO = """Risultato WACC per {ticker}:

| Componente | Valore |
|-----------|--------|
| Risk-Free Rate | {rf:.2%} |
| Beta Unlevered (settore) | {beta_u:.2f} |
| Beta Levered | {beta_l:.2f} |
| ERP | {erp:.2%} |
| CRP | {crp:.2%} |
| **Costo Equity** | **{re:.2%}** |
| Costo Debito Pre-Tax | {rd_pre:.2%} |
| Costo Debito Post-Tax | {rd_post:.2%} |
| Peso Equity | {we:.1%} |
| Peso Debito | {wd:.1%} |
| **WACC** | **{wacc:.2%}** |
"""
