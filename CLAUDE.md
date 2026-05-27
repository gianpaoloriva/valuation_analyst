# Valuation Analyst - Istruzioni per Claude Code

## Panoramica Progetto

Toolkit multi-agente per equity valuation e credit risk con tre modalita' operative:
- **Modalita' Damodaran**: pipeline Python automatizzata (Damodaran, NYU Stern), report markdown/PDF
- **Modalita' FSI Excel**: modelli Excel interattivi con formule vive, compliance normativa italiana
- **Modalita' Rating & Valuation**: valutazione PMI con approccio settoriale (BMS), DCF con TV coerente, credit risk forward-looking (Agentic Credit Risk Monte Carlo), rating implicito

Triplo scopo: (1) strumento di lavoro per analisti finanziari, (2) demo per mostrare Claude Code, (3) stima credit risk forward-looking per PMI non quotate.

## Convenzioni

- **Lingua**: Tutto in italiano (commenti, docstring, README, docs, skill descriptions)
- **Python**: 3.11+, type hints ovunque, dataclass per modelli dati
- **Stile**: ruff per formatting, mypy per type checking
- **Test**: pytest, 348 test (165 valuation_analyst + 183 rating_valuation)

## Data Provider

- **Massive.com** (https://massive.com) per dati aziendali reali (modalita' Damodaran)
- **Damodaran datasets** (https://pages.stern.nyu.edu/~adamodar/) per parametri di settore (modalita' Damodaran)
- **CSV normalizzati** in `data/rating_valuation/` per bilanci riclassificati (modalita' Rating & Valuation)
- API key in `.env` (mai committare)

## Struttura

```
valuation_analyst/
  src/valuation_analyst/        Package Python Damodaran
    config/                     Impostazioni, costanti, URL Damodaran
    models/                     Dataclass (Company, CashFlow, Comparable, etc.)
    tools/                      Moduli di calcolo + fetch_dati.py
    utils/                      Math, formatting, logging, validazione
  src/rating_valuation/         Package Python Rating & Valuation (BMS, DCF TV coerente, Agentic Credit Risk)
    common/                     Data loader, financial math, invarianti bilancio
    bms/                        BMSBuilder — Bilancio Medio Standardizzato
    dcf/                        DCF 2/3 stadi con Terminal Value coerente + check coerenza
    agentic_credit_risk/        Simulatore Monte Carlo PD/LGD/EL/UL
    differential/               Analisi differenziale target vs IMS
    rating/                     Rating Mapper (master scale, CDS, Altman Z)
    backtest/                   Backtest Comparator (AUROC/Gini/KS)
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
    rating_valuation/           CSV normalizzati per Rating & Valuation
      companies.csv             Bilanci riclassificati (1 riga per company x anno)
      sectors.csv               Parametri settoriali (Weibull, correlazioni, beta)
      macro.csv                 Parametri macro per paese (Rf, MRP, PIL)
      rating_master_scale.csv   Master scale S&P Rating ↔ PD
      schema.md                 Schema autoritativo dei CSV
      generators/               Generatore dataset demo (seed fisso)
  .claude/
    agents/                     8 agenti Damodaran + 10 agenti FSI Italy + 6 agenti Rating & Valuation
    skills/                     10 skill Damodaran + 59 skill FSI Italy + 7 skill Rating & Valuation
    commands/                   Comandi slash (/status, /demo)
  tests/                        348 test (165 valuation_analyst + 183 rating_valuation)
  demos/                        8 script demo (01-08)
  examples/rating_valuation/    2 esempi pipeline Rating & Valuation
  docs/
    rating_valuation/           overview.md, TODO.md, 3 PDF paper originali
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

### Modalita' Rating & Valuation (PMI, credit risk)

Pipeline Python per PMI non quotate basata su tre paper accademici:
1. **BMS** (Scarano/Brughera, AIAF n.65): costruzione Impresa Media Standard del settore
2. **DCF con TV coerente** (Scarano/Di Napoli, AIAF n.66): formula con reinvestimento esplicito + 7 check coerenza
3. **Agentic Credit Risk** (Montesi/Papiro, 2014): PD forward-looking via Monte Carlo (20.000 trial, Weibull, debito endogeno)

```bash
python examples/rating_valuation/02_full_pipeline_riva_meccanica.py  # Pipeline completa
```

Cash flow: capital cash flow (Ruback 2002) `OCF = NOPAT - DELTA_NIC + tau*INT`.
WACC: pre-tax con CCF, after-tax con FCFF. MAI mescolare.
Dati: CSV normalizzati in `data/rating_valuation/` (schema in `data/rating_valuation/schema.md`).

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

### Agenti Rating & Valuation (Python, PMI, credit risk)
19. **bms-analyst** - Costruzione e validazione BMS settoriale
20. **dcf-validator** - Validazione DCF con check coerenza TV (7 controlli)
21. **agentic-credit-risk-simulator** - Simulazione Monte Carlo PD/LGD/EL/UL
22. **data-curator** - Validazione e curatela dataset CSV
23. **backtest-analyst** - Confronto modelli credit risk (AUROC/Gini/KS)
24. **valuation-reporter** - Report narrativo in italiano (stile AIAF)

## Logging Prompt

Ogni interazione significativa va loggata in `data/logs/prompt_log.md` usando `utils/logging_utils.py`.

## Formule Chiave (Damodaran)

- **FCFF** = EBIT(1-t) + Depr - CapEx - DeltaWC
- **CAPM**: Re = Rf + Beta * ERP + CRP
- **WACC**: WACC = (E/V)*Re + (D/V)*Rd*(1-t)
- **Terminal Value**: TV = FCF*(1+g)/(r-g)
- **Black-Scholes**: Equity = V*N(d1) - K*e^(-rT)*N(d2)

## Formule Chiave (Rating & Valuation)

- **Capital Cash Flow** (Ruback): OCF = NOPAT - DELTA_NIC + tau*INT
- **Pre-tax WACC**: w_e*k_e + w_d*r_d (senza (1-t) sul debito)
- **TV coerente**: TV = NOPAT*(1 - g/ROIC_NI) / (wacc - g)
- **TV steady state** (ROIC=WACC): TV = NOPAT/wacc
- **Coerenza**: g = ROIC_NI * h_T, h_T in [0,1]
- **Debito endogeno** (eq.[7]): D_t = max(0, f(NOPAT, DELTA_NIC, r_d, tau, D_{t-1}))
- **Default**: EV_t < D_t - CASH_t
- **CDS → PD**: PD = 1 - exp(-CDS/LGD), LGD = 60%

## Skill Rating & Valuation

Le 7 skill Rating & Valuation coprono la pipeline completa:

| Skill | Modulo Python | Funzione |
|-------|---------------|----------|
| bms-builder | bms/builder.py | Costruzione BMS settoriale |
| dcf-tv-coherence | dcf/ (3 file) | DCF 2/3 stadi + 7 check coerenza TV |
| differential-analysis | differential/analyzer.py | Target vs IMS, 4 driver |
| agentic-credit-risk | agentic_credit_risk/ (6 file) | Monte Carlo PD/LGD/EL/UL |
| rating-mapper | rating/mapper.py | Master scale, CDS→PD, Altman Z |
| backtest-comparator | backtest/comparator.py | AUROC/Gini/KS multi-modello |
| rating-valuation-pipeline | Orchestrazione | Pipeline end-to-end |

Paper di riferimento: `docs/rating_valuation/overview.md`

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
pytest tests/                           # 348 test (valuation_analyst + rating_valuation)
python scripts/run_analysis.py AAPL     # Analisi Damodaran (US)
python scripts/run_analysis.py ENEL.MI  # Analisi Damodaran (Italia)
python scripts/md_to_pdf.py AAPL        # Genera PDF
/fsi-valuation ENEL.MI                  # Modello Excel FSI Italy
/fsi-valuation ENEL.MI --tipo pitch     # Pitch completo (Excel + deck)

# Rating & Valuation (PMI)
python examples/rating_valuation/01_bms_industrial_machinery.py    # BMS settoriale
python examples/rating_valuation/02_full_pipeline_riva_meccanica.py  # Pipeline completa
python data/rating_valuation/generators/seed_companies.py          # Rigenera dataset demo
```
