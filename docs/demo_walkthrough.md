# Walkthrough Demo - Valuation Analyst

## Prerequisiti

```bash
# 1. Installa il pacchetto
pip install -e ".[dev]"

# 2. (Opzionale) Configura API key per dati live
cp .env.example .env
# Modifica .env con la tua MASSIVE_API_KEY
```

## Demo 01: Costo del Capitale

```bash
python demos/01_cost_of_capital.py
```

**Cosa fa**: Calcola il WACC per Apple Inc. usando:
- Risk-free rate = 4.2% (US Treasury 10Y)
- Beta bottom-up dal settore Technology
- ERP = 5.5% (Damodaran)
- Costo debito da rating AA+

**Output atteso**: WACC ~9-10%

## Demo 02: DCF Valuation

```bash
python demos/02_dcf_valuation.py
```

**Cosa fa**: Valutazione DCF FCFF di Apple con:
- FCFF base calcolato dai dati finanziari
- Modello 3 fasi (5+5+terminal)
- Terminal value con Gordon Growth

**Output atteso**: Valore per azione nell'intorno di $150-$200

## Demo 03: Comparable Analysis

```bash
python demos/03_comparable_analysis.py
```

**Cosa fa**: Valutazione relativa usando:
- 7 comparabili del settore Tech (da sample data)
- Multipli: P/E, EV/EBITDA, P/B, EV/Sales
- Statistiche e valore implicito

## Demo 04: Option Pricing

```bash
python demos/04_option_pricing.py
```

**Cosa fa**: Valutazione dell'equity come opzione per un'azienda
ipotetica in distress con alto leverage.

## Demo 05: Private Valuation

```bash
python demos/05_private_valuation.py
```

**Cosa fa**: Valutazione di un'azienda manifatturiera privata
con sconto illiquidita' e premio di controllo.

## Demo 06: M&A Synergy

```bash
python demos/06_ma_synergy.py
```

**Cosa fa**: Analisi di un'acquisizione tech-on-tech con
sinergie di costo, ricavo e finanziarie.

## Demo 07: Sensitivity Analysis

```bash
python demos/07_sensitivity_analysis.py
```

**Cosa fa**: Sensitivity WACC vs Growth + Monte Carlo per Apple DCF.

## Demo 08: Full Report

```bash
python demos/08_full_report.py
```

**Cosa fa**: Esegue WACC, DCF, multipli e sensitivity per Apple
e produce un report sintetico completo.

## Esecuzione Completa

```bash
# Tutte le demo in sequenza
for f in demos/0*.py; do
    echo "=== Esecuzione: $f ==="
    python "$f"
    echo ""
done
```

## Uso con Claude Code

Oltre ai demo scripts Python, puoi usare le skill direttamente in Claude Code:

```
/cost-of-capital AAPL
/dcf-valuation AAPL
/comparable-analysis AAPL
/valuation-report AAPL
```

Oppure usare gli agenti specializzati direttamente dalla conversazione:
"Valuta Apple Inc. usando il DCF con FCFF"
