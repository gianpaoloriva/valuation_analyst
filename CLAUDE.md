# Valuation Analyst - Istruzioni per Claude Code

## Panoramica Progetto

Toolkit multi-agente per equity valuation con due modalita' operative:
- **Modalita' Damodaran**: pipeline Python automatizzata (Damodaran, NYU Stern), report markdown/PDF
- **Modalita' FSI Excel**: modelli Excel interattivi con formule vive, compliance normativa italiana

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
    _template.json              Template per analisi US/internazionali
    _template_italia.json       Template per analisi societa' italiane/europee
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
    agents/                     8 agenti Damodaran + 10 agenti FSI Italy
    skills/                     10 skill Damodaran + 59 skill FSI Italy (prefisso fsi-)
    commands/                   Comandi slash (/status, /demo)
  tests/                        165 test (unit + integration)
  demos/                        8 script demo (01-08)
  docs/                         Documentazione tecnica
```

## Flow di Analisi

### Modalita' Damodaran (report markdown/PDF)
1. **Config**: creare/popolare `configs/{TICKER}.json` (copiare da `_template.json` o `_template_italia.json`)
2. **Analisi**: `python scripts/run_analysis.py {TICKER}`
3. **PDF**: `python scripts/md_to_pdf.py {TICKER}`
4. Output in `output/markdown/` e `output/pdf/`

**IMPORTANTE**: NON creare script .py ad-hoc per singole analisi. Usare SEMPRE `run_analysis.py`.
Il flow gestisce sia aziende profittevoli che in perdita (EBIT/EPS negativi).

### Modalita' FSI Excel (modelli Excel interattivi)
1. **Invoca**: `/fsi-valuation TICKER.MI` (o `/fsi-valuation TICKER.MI --tipo dcf|lbo|comps|pitch`)
2. Claude costruisce il modello Excel step-by-step con formule vive
3. Review interattiva a ogni fase (input -> proiezioni -> WACC -> DCF -> sensitivity)
4. Output: file .xlsx con formule vive in EUR

Parametri italiani: BTP 10Y (risk-free), ERP 6-8%, Euribor (costo debito), IRES 24% + IRAP 3.9%, IFRS.

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

### Agenti Damodaran (Python, report markdown/PDF)
1. **orchestrator** - Coordina tutti gli agenti
2. **dcf-analyst** - Valutazione DCF (FCFF/FCFE)
3. **relative-analyst** - Multipli e comparabili
4. **cost-of-capital** - WACC/CAPM/Beta
5. **option-pricing** - Black-Scholes, equity come opzione
6. **private-valuation** - Societa' private, sconti illiquidita'
7. **ma-analyst** - M&A e sinergie
8. **risk-analyst** - Sensitivity e Monte Carlo

### Agenti FSI Italy (Excel con formule vive, contesto italiano/europeo)
9. **fsi-model-builder-italy** - Modelli DCF, LBO, 3-statement, comps Excel (IFRS, BTP, Euribor, IRES+IRAP)
10. **fsi-pitch-agent-italy** - Pitch completo: workbook Excel + deck PowerPoint
11. **fsi-earnings-reviewer-italy** - Revisione utili e aggiornamento modelli
12. **fsi-market-researcher-italy** - Ricerca di mercato e analisi settoriale
13. **fsi-valuation-reviewer-italy** - Review valutazioni per LP reporting
14. **fsi-meeting-prep-agent-italy** - Preparazione briefing MiFID II-compliant
15. **fsi-kyc-screener-italy** - KYC/AML screening (D.Lgs. 231/2007)
16. **fsi-gl-reconciler-italy** - Riconciliazione contabile
17. **fsi-month-end-closer-italy** - Chiusura mensile (assestamento, TFR)
18. **fsi-statement-auditor-italy** - Verifica estratti conto LP/NAV

## Logging Prompt

Ogni interazione significativa va loggata in `data/logs/prompt_log.md` usando `utils/logging_utils.py`.

## Formule Chiave (Damodaran)

- **FCFF** = EBIT(1-t) + Depr - CapEx - DeltaWC
- **CAPM**: Re = Rf + Beta * ERP + CRP
- **WACC**: WACC = (E/V)*Re + (D/V)*Rd*(1-t)
- **Terminal Value**: TV = FCF*(1+g)/(r-g)
- **Black-Scholes**: Equity = V*N(d1) - K*e^(-rT)*N(d2)

## Skill FSI Italy per Verticale

Le 58 skill FSI Italy (prefisso `fsi-`) coprono 6 verticali:

| Verticale | Skills | Esempi |
|-----------|--------|--------|
| Financial Analysis | 13 | fsi-dcf-model-italy, fsi-comps-analysis-italy, fsi-lbo-model-italy |
| Equity Research | 9 | fsi-initiating-coverage-italy, fsi-earnings-analysis-italy |
| Investment Banking | 10 | fsi-golden-power-check, fsi-merger-model-italy |
| Private Equity | 10 | fsi-returns-analysis-italy, fsi-dd-checklist-italy |
| Wealth Management | 12 | fsi-mifid-ii-adeguatezza, fsi-regime-fiscale-italia |
| Operations | 4 | fsi-kyc-rules-italy, fsi-aml-italia-231, fsi-dora-compliance |

Compliance normativa: CONSOB, AGCM, MiFID II, Golden Power, KYC/AML (D.Lgs. 231/2007), SFDR, DORA.

## Comandi Utili

```bash
pip install -e ".[dev]"                # Installazione
pytest tests/                           # 165 test
python scripts/run_analysis.py AAPL     # Analisi Damodaran (US)
python scripts/run_analysis.py ENEL.MI  # Analisi Damodaran (Italia)
python scripts/md_to_pdf.py AAPL        # Genera PDF
/fsi-valuation ENEL.MI                  # Modello Excel FSI Italy
/fsi-valuation ENEL.MI --tipo pitch     # Pitch completo (Excel + deck)
```
