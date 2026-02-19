"""Template prompt per la valutazione M&A."""

PROMPT_MA = """Analisi M&A: {acquirente} acquisisce {target}.

## Acquirente
- Valore Standalone: {valore_acquirente}
- Utile Netto: {utile_acquirente}
- Azioni: {azioni_acquirente}

## Target
- Valore Standalone: {valore_target}
- Utile Netto: {utile_target}
- Azioni: {azioni_target}

## Deal
- Prezzo Offerta/Azione: {prezzo_offerta}
- Struttura: {struttura}

## Richiesta
1. Stima sinergie operative e finanziarie
2. Calcola valore acquisizione
3. Analisi accretion/dilution
4. Determina prezzo massimo
"""

PROMPT_MA_RISULTATO = """Risultato analisi M&A:

| Componente | Valore |
|-----------|--------|
| Valore Standalone Target | {valore_target} |
| + Sinergie di Costo | {sinergie_costo} |
| + Sinergie di Ricavo | {sinergie_ricavo} |
| + Sinergie Finanziarie | {sinergie_fin} |
| - Costi Integrazione | {costi_integrazione} |
| = **Valore Acquisizione** | **{valore_acquisizione}** |
| Prezzo Offerto | {prezzo_offerta} |
| Surplus Acquirente | {surplus} |
| EPS Accretion/Dilution | {accretion_dilution} |
"""
