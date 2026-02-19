# Valuation Analyst - Sistema Multi-Agente per Equity Valuation

Toolkit completo di agenti e skills Claude Code per l'analisi di equity valuation,
basato sulle metodologie di **Aswath Damodaran** (NYU Stern).

## Scopo

1. **Strumento di lavoro** affidabile per analisti finanziari
2. **Demo** per mostrare ad altri analisti come usare Claude Code per la valutazione aziendale

## Metodologie Implementate

| Metodologia | Descrizione |
|-------------|-------------|
| **DCF (FCFF/FCFE)** | Discounted Cash Flow con modelli multi-stage |
| **CAPM/WACC** | Costo del capitale con beta bottom-up |
| **Relative Valuation** | Multipli (P/E, EV/EBITDA, P/B, EV/Sales) |
| **Black-Scholes** | Equity come opzione per aziende in distress |
| **Private Company** | Sconti illiquidita' e premio di controllo |
| **M&A** | Sinergie e valore di acquisizione |
| **Risk Analysis** | Sensitivity, scenari, Monte Carlo |

## Setup Rapido

```bash
# Clona il repository
git clone <repo-url>
cd valuation_analyst

# Crea virtual environment
python -m venv .venv
source .venv/bin/activate

# Installa dipendenze
pip install -e ".[dev]"

# Configura API key
cp .env.example .env
# Modifica .env con la tua MASSIVE_API_KEY

# Esegui i test
pytest tests/ --cov
```

## Agenti Specializzati

Il sistema usa 8 agenti Claude Code specializzati:

- **Orchestrator** - Coordina tutti gli agenti e sintetizza i risultati
- **DCF Analyst** - Valutazione DCF (FCFF e FCFE multi-stage)
- **Relative Analyst** - Valutazione relativa con multipli e comparabili
- **Cost of Capital** - WACC, CAPM, beta e risk premium
- **Option Pricing** - Black-Scholes e equity come opzione
- **Private Valuation** - Sconti illiquidita' e premio di controllo
- **M&A Analyst** - Sinergie e valore di acquisizione
- **Risk Analyst** - Sensitivity, scenari e simulazioni Monte Carlo

## Fonti Dati

- **Massive.com** - Dati aziendali reali (bilanci, prezzi, ratios)
- **Dataset Damodaran** - Parametri di settore (beta, ERP, WACC settoriali)

## Analisi di un Titolo

Lo script unico `scripts/run_analysis.py` genera un report di valutazione completo
per qualsiasi ticker configurato. I parametri dell'analista sono in file JSON separati.

### Uso

```bash
python scripts/run_analysis.py GOOGL   # Analisi Alphabet
python scripts/run_analysis.py MSFT    # Analisi Microsoft
python scripts/run_analysis.py AAPL    # Analisi Apple
```

Il report viene scritto in `report/{TICKER}_valuation_report_{data}.md`.

### Struttura dei file

```
scripts/
  run_analysis.py           # Script unico di analisi
  fetch_dati.py             # Fetch dati live da Massive.com
  configs/
    GOOGL.json              # Configurazione analista per Alphabet
    MSFT.json               # Configurazione analista per Microsoft
    AAPL.json               # Configurazione analista per Apple
```

### Aggiungere un nuovo ticker

1. Crea `scripts/configs/{TICKER}.json` copiando un JSON esistente
2. Modifica i parametri dell'analista (vedi sezione successiva)
3. Lancia `python scripts/run_analysis.py {TICKER}`

### Configurazione JSON

Ogni file `scripts/configs/{TICKER}.json` contiene **solo i parametri decisi
dall'analista**, non recuperabili automaticamente da API. I dati di mercato
(prezzo, market cap, shares outstanding, risk-free rate) vengono sempre
recuperati live da Massive.com.

| Sezione | Cosa contiene | Quando modificarla |
|---------|---------------|--------------------|
| `erp` | Equity Risk Premium (es. 0.055 per US) | Quando cambia la stima ERP Damodaran |
| `rating_credito` | Rating S&P dell'azienda (es. "AA+") | Quando cambia il rating |
| `crescita_alta` | Tasso di crescita fase alta del DCF | Per riflettere le tue stime |
| `crescita_stabile` | Tasso di crescita perpetua (fase terminale) | Tipicamente 2-3% |
| `anni_alta` / `anni_transizione` | Durata delle fasi di crescita | Per il profilo di crescita |
| `comparabili` | Lista di aziende peer con i loro multipli | Per aggiornare i peer o i multipli |
| `sensitivity` | Range per le tabelle di sensitivita' | Per esplorare scenari diversi |
| `scenari` | Probabilita' e descrizioni Best/Base/Worst | Per le tue ipotesi di scenario |
| `monte_carlo` | Deviazioni standard per la simulazione | Per la dispersione delle stime |
| `rischi_rialzo` / `rischi_ribasso` | Fattori di rischio qualitativi | Per ogni azienda |
| `fondamentali_fallback` | Dati di bilancio di fallback | Quando l'API non fornisce i fondamentali |

**Esempio: modificare la crescita attesa per GOOGL**

Apri `scripts/configs/GOOGL.json` e cambia:
```json
{
  "crescita_alta": 0.18,
  "crescita_stabile": 0.03,
  "anni_alta": 7
}
```

Poi rilancia `python scripts/run_analysis.py GOOGL` per rigenerare il report.

### Dati finanziari

Lo script recupera i dati in due modi:

1. **Dati di mercato** (sempre live da Massive.com): prezzo, market cap, shares, risk-free rate
2. **Fondamentali** (bilancio, conto economico, cash flow):
   - Se il piano API Massive.com include `/stocks/financials/*`: dati live
   - Altrimenti: usa i valori nella sezione `fondamentali_fallback` del JSON config

Per aggiornare i fondamentali di fallback, modifica la sezione `fondamentali_fallback`
nel JSON del ticker con i dati dal bilancio piu' recente (valori in milioni USD).

## Demos

Nella cartella `demos/` trovi 8 script numerati che dimostrano ogni funzionalita'
con dati di esempio (no API richiesta):

```bash
python demos/01_cost_of_capital.py   # WACC e CAPM
python demos/02_dcf_valuation.py     # DCF FCFF/FCFE
python demos/03_comparable_analysis.py  # Multipli
python demos/04_option_pricing.py    # Black-Scholes
python demos/05_private_valuation.py # Societa' private
python demos/06_ma_synergy.py        # M&A e sinergie
python demos/07_sensitivity_analysis.py  # Monte Carlo
python demos/08_full_report.py       # Report completo
```

## Documentazione

- [Architettura](docs/architecture.md)
- [Guida Agenti](docs/agent_guide.md)
- [Metodologia](docs/methodology.md)
- [Fonti Dati](docs/data_sources.md)
- [Walkthrough Demo](docs/demo_walkthrough.md)

## Licenza

MIT
