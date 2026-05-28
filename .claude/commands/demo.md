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
3. Esegui lo script demo selezionato dalla cartella `examples/damodaran/`

## Demo Disponibili
1. `examples/damodaran/01_cost_of_capital.py` - Calcolo WACC per Apple
2. `examples/damodaran/02_dcf_valuation.py` - DCF FCFF/FCFE per Apple
3. `examples/damodaran/03_comparable_analysis.py` - Multipli e comparabili Tech
4. `examples/damodaran/04_option_pricing.py` - Equity come opzione (caso distress)
5. `examples/damodaran/05_private_valuation.py` - Valutazione societa' privata
6. `examples/damodaran/06_ma_synergy.py` - M&A con sinergie
7. `examples/damodaran/07_sensitivity_analysis.py` - Sensitivity e Monte Carlo
8. `examples/damodaran/08_full_report.py` - Report completo orchestrato

## Formato
```bash
# Demo singola
python examples/damodaran/01_cost_of_capital.py

# Tutte le demo
for f in examples/damodaran/0*.py; do python "$f"; echo "---"; done
```
