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

## Demos

Nella cartella `demos/` trovi 8 script numerati che dimostrano ogni funzionalita':

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
