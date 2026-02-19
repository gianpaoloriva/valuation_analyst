"""Template prompt per la valutazione di societa' private."""

PROMPT_PRIVATA = """Valutazione di una societa' privata.

## Dati Azienda
- Ricavi: {ricavi}
- EBITDA: {ebitda}
- Margine EBITDA: {margine_ebitda:.1%}
- Settore: {settore}
- Tipo Partecipazione: {tipo_partecipazione}

## Richiesta
1. Calcola la valutazione base (come se quotata)
2. Applica sconto illiquidita' (Damodaran)
3. Applica premio di controllo (se maggioranza)
4. Determina il valore finale aggiustato
"""

PROMPT_PRIVATA_RISULTATO = """Risultato valutazione privata:

| Passaggio | Valore | Aggiustamento |
|----------|--------|---------------|
| Valore "come se quotata" | {valore_quotata} | - |
| + Premio Controllo | {dopo_controllo} | {premio_controllo:.1%} |
| - Sconto Illiquidita' | {valore_finale} | {sconto_illiquidita:.1%} |
| **Valore Finale** | **{valore_finale}** | |
"""
