"""Template prompt per la valutazione relativa."""

PROMPT_COMPARABILI = """Esegui un'analisi dei comparabili per {ticker} ({nome}).

## Target
- Settore: {settore}
- Market Cap: {market_cap}
- P/E: {pe}x
- EV/EBITDA: {ev_ebitda}x

## Richiesta
1. Identifica 5-10 societa' comparabili nel settore {settore}
2. Raccogli i multipli (P/E, EV/EBITDA, P/B, EV/Sales)
3. Calcola statistiche (mediana, media, quartili)
4. Applica i multipli mediani per derivare il valore per azione
5. Confronta con il prezzo corrente
"""

PROMPT_MULTIPLI_RIEPILOGO = """Riepilogo multipli per {ticker}:

| Multiplo | Target | Mediana Comp. | Premium/Discount |
|----------|--------|--------------|-----------------|
| P/E | {pe_target}x | {pe_mediana}x | {pe_diff} |
| EV/EBITDA | {ev_ebitda_target}x | {ev_ebitda_mediana}x | {ev_ebitda_diff} |
| P/B | {pb_target}x | {pb_mediana}x | {pb_diff} |
| EV/Sales | {ev_sales_target}x | {ev_sales_mediana}x | {ev_sales_diff} |
"""

PROMPT_VALORE_IMPLICITO = """Valori impliciti per {ticker} basati sui multipli dei comparabili:

| Multiplo | Valore/Azione |
|----------|--------------|
| P/E | {valore_pe} |
| EV/EBITDA | {valore_ev_ebitda} |
| P/B | {valore_pb} |
| EV/Sales | {valore_ev_sales} |
| **Media** | **{valore_medio}** |
| **Mediana** | **{valore_mediano}** |
"""
