# Valuation Analyst - Istruzioni per Claude Code

## Panoramica Progetto

Toolkit multi-agente per equity valuation basato sulle metodologie di Aswath Damodaran (NYU Stern).
Doppio scopo: (1) strumento di lavoro per analisti finanziari, (2) demo per mostrare Claude Code.

## Convenzioni

- **Lingua**: Tutto in italiano (commenti, docstring, README, docs, skill descriptions)
- **Python**: 3.11+, type hints ovunque, dataclass per modelli dati
- **Stile**: ruff per formatting, mypy per type checking
- **Test**: pytest, 165 test (unit + integration)

## Data Provider

- **Massive.com** (https://massive.com) per dati aziendali reali
- **Damodaran datasets** (https://pages.stern.nyu.edu/~adamodar/) per parametri di settore
- API key in `.env` (mai committare)

## Struttura

```
valuation_analyst/
  src/valuation_analyst/        Package Python principale
    config/                     Impostazioni, costanti, URL Damodaran
    models/                     Dataclass (Company, CashFlow, Comparable, etc.)
    tools/                      Moduli di calcolo + fetch_dati.py
    utils/                      Math, formatting, logging, validazione
  configs/                      File JSON di configurazione (uno per ticker)
    _template.json              Template documentato per nuove analisi
  scripts/                      Script di utilita'
    run_analysis.py             Analisi completa (config -> report)
    md_to_pdf.py                Conversione report MD -> PDF
  output/                       Report generati
    markdown/                   Report .md
    pdf/                        Report .pdf
  data/
    cache/                      Cache dati Damodaran
    logs/                       prompt_log.md
  .claude/
    agents/                     8 agenti specializzati
    skills/                     10 skill di valutazione
    commands/                   Comandi slash (/status, /demo)
  tests/                        165 test (unit + integration)
  demos/                        8 script demo (01-08)
  docs/                         Documentazione tecnica
```

## Flow di Analisi

1. **Config**: creare/popolare `configs/{TICKER}.json` (copiare da `_template.json`)
2. **Analisi**: `python scripts/run_analysis.py {TICKER}`
3. **PDF**: `python scripts/md_to_pdf.py {TICKER}`
4. Output in `output/markdown/` e `output/pdf/`

**IMPORTANTE**: NON creare script .py ad-hoc per singole analisi. Usare SEMPRE `run_analysis.py`.
Il flow gestisce sia aziende profittevoli che in perdita (EBIT/EPS negativi).

## Naming Convention Output

- Markdown: `{TICKER}_{YYYY-MM-DD}_valuation.md`
- PDF: `{TICKER}_{YYYY-MM-DD}_valuation.pdf`

## Report: 10 Sezioni Standard

1. Executive Summary (valore, prezzo, raccomandazione)
2. Panoramica Aziendale
3. Costo del Capitale (WACC)
4. Valutazione DCF (FCFF)
5. Valutazione Relativa (Multipli)
6. Analisi di Sensitivita'
7. Analisi per Scenari
8. Simulazione Monte Carlo
9. Sintesi e Raccomandazione
10. Rischi e Disclaimer

## Agenti Disponibili

1. **orchestrator** - Coordina tutti gli agenti
2. **dcf-analyst** - Valutazione DCF (FCFF/FCFE)
3. **relative-analyst** - Multipli e comparabili
4. **cost-of-capital** - WACC/CAPM/Beta
5. **option-pricing** - Black-Scholes, equity come opzione
6. **private-valuation** - Societa' private, sconti illiquidita'
7. **ma-analyst** - M&A e sinergie
8. **risk-analyst** - Sensitivity e Monte Carlo

## Logging Prompt

Ogni interazione significativa va loggata in `data/logs/prompt_log.md` usando `utils/logging_utils.py`.

## Formule Chiave (Damodaran)

- **FCFF** = EBIT(1-t) + Depr - CapEx - DeltaWC
- **CAPM**: Re = Rf + Beta * ERP + CRP
- **WACC**: WACC = (E/V)*Re + (D/V)*Rd*(1-t)
- **Terminal Value**: TV = FCF*(1+g)/(r-g)
- **Black-Scholes**: Equity = V*N(d1) - K*e^(-rT)*N(d2)

## Comandi Utili

```bash
pip install -e ".[dev]"                # Installazione
pytest tests/                           # 165 test
python scripts/run_analysis.py AAPL     # Analisi completa
python scripts/md_to_pdf.py AAPL        # Genera PDF
```
