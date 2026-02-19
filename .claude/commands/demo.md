---
name: demo
description: Esegue una demo del sistema di valutazione con dati sample
user_invocable: true
---

# Comando: /demo

Esegue una demo interattiva del sistema Valuation Analyst usando i dati sample.

## Azioni
1. Verifica che il pacchetto sia installato (`pip install -e .`)
2. Chiedi quale demo eseguire (o esegui tutte in sequenza)
3. Esegui lo script demo selezionato dalla cartella `demos/`

## Demo Disponibili
1. `demos/01_cost_of_capital.py` - Calcolo WACC per Apple
2. `demos/02_dcf_valuation.py` - DCF FCFF/FCFE per Apple
3. `demos/03_comparable_analysis.py` - Multipli e comparabili Tech
4. `demos/04_option_pricing.py` - Equity come opzione (caso distress)
5. `demos/05_private_valuation.py` - Valutazione societa' privata
6. `demos/06_ma_synergy.py` - M&A con sinergie
7. `demos/07_sensitivity_analysis.py` - Sensitivity e Monte Carlo
8. `demos/08_full_report.py` - Report completo orchestrato

## Formato
```bash
# Demo singola
python demos/01_cost_of_capital.py

# Tutte le demo
for f in demos/0*.py; do python "$f"; echo "---"; done
```
