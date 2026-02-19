"""Template prompt per l'analisi DCF."""

PROMPT_DCF_ANALISI = """Esegui una valutazione DCF per {ticker} ({nome}).

## Dati Disponibili
- Ricavi: {ricavi}
- EBIT: {ebit}
- Tax Rate: {tax_rate:.1%}
- CapEx: {capex}
- Deprezzamento: {deprezzamento}
- Delta Working Capital: {delta_wc}
- WACC: {wacc:.2%}
- Debito Netto: {debito_netto}
- Azioni Outstanding: {shares_outstanding}
- Prezzo Corrente: {prezzo_corrente}

## Richiesta
1. Calcola il FCFF base
2. Proietta i cash flow con modello a 3 fasi:
   - Fase alta ({anni_alta} anni): crescita {crescita_alta:.1%}
   - Fase transizione ({anni_transizione} anni)
   - Fase stabile: crescita {crescita_stabile:.1%}
3. Calcola il Terminal Value (Gordon Growth)
4. Determina il valore per azione
5. Confronta con il prezzo di mercato
"""

PROMPT_DCF_RIEPILOGO = """Riepilogo valutazione DCF per {ticker}:

| Componente | Valore |
|-----------|--------|
| FCFF Base | {fcff_base} |
| PV Cash Flow Espliciti | {pv_cf} |
| Terminal Value | {tv} |
| PV Terminal Value | {pv_tv} |
| Valore Firm | {valore_firm} |
| - Debito Netto | {debito_netto} |
| = Valore Equity | {valore_equity} |
| Azioni Outstanding | {shares} |
| **Valore per Azione** | **{valore_per_azione}** |
| Prezzo Corrente | {prezzo_corrente} |
| **Upside/Downside** | **{upside}** |
"""

PROMPT_DCF_ASSUNZIONI = """Verifica le assunzioni DCF per {ticker}:

1. La crescita alta ({crescita_alta:.1%}) e' sostenibile per {anni_alta} anni?
2. Il Terminal Growth ({crescita_stabile:.1%}) e' inferiore alla crescita del GDP?
3. Il WACC ({wacc:.2%}) e' coerente con il profilo di rischio?
4. Il Terminal Value e' {pct_tv:.0%} del valore totale (soglia max: 80%)
5. Il reinvestment rate implicito e' coerente con la crescita?
"""
