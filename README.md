# Valuation Analyst

**Sistema multi-agente per equity valuation e credit risk con tre modalita' operative: Damodaran (Python, report markdown/PDF), FSI Excel (modelli Excel con formule vive, compliance normativa italiana) e Rating & Valuation (PMI non quotate, credit risk forward-looking).**

Toolkit professionale che combina 24 agenti Claude Code specializzati con moduli di calcolo Python per produrre report di valutazione completi, modelli Excel di qualita' istituzionale e stime di credit risk forward-looking per PMI.

## Scopo

1. **Strumento di lavoro** per analisti finanziari: genera report di valutazione riproducibili e audit-friendly
2. **Modelli Excel istituzionali** per il mercato italiano/europeo con compliance CONSOB, AGCM, MiFID II
3. **Stima credit risk forward-looking** per PMI non quotate: BMS settoriale, DCF con TV coerente, Agentic Credit Risk Monte Carlo, rating implicito
4. **Demo** per mostrare come Claude Code puo' orchestrare analisi finanziarie complesse

## Tre Modalita' Operative

| Aspetto | Damodaran (Python) | FSI Excel (Italia) | Rating & Valuation (PMI) |
| --- | --- | --- | --- |
| **Output** | Report Markdown/PDF | Workbook Excel con formule vive | Report Python + rating implicito |
| **Calcolo** | Python automatizzato | Claude guida la costruzione Excel | Python (Monte Carlo 20K trial) |
| **Interazione** | Batch (config -> report) | Step-by-step con review utente | Pipeline a checkpoint con gate |
| **Target** | Quotate (dati di mercato) | Quotate italiane/europee | PMI non quotate (bilancio riclassificato) |
| **Cash flow** | FCFF/FCFE (Damodaran) | FCFF (IFRS) | Capital cash flow (Ruback 2002) |
| **Parametri** | Damodaran datasets, US Treasury | IFRS, BTP 10Y, Euribor, IRES+IRAP | CSV normalizzati (AIDA/BvD) |
| **Credit risk** | Non incluso | Non incluso | PD/LGD/EL/UL Monte Carlo |
| **Compliance** | Standard Damodaran | CONSOB, AGCM, MiFID II | Paper accademici (AIAF, RAPD) |
| **Comando** | `python scripts/run_analysis.py TICKER` | `/fsi-valuation TICKER.MI` | `python examples/rating_valuation/02_*.py` |

## Metodologie

### Modalita' Damodaran (Python)

| Metodologia | Modulo | Output |
| --- | --- | --- |
| DCF multi-stage (FCFF/FCFE) | `tools/dcf_fcff.py`, `dcf_fcfe.py` | Valore intrinseco per azione |
| CAPM / WACC | `tools/capm.py`, `wacc.py` | Costo del capitale |
| Valutazione relativa | `tools/multiples.py` | Range da multipli comparabili |
| Black-Scholes | `tools/black_scholes.py`, `equity_as_option.py` | Equity come opzione (distress) |
| Societa' private | `tools/illiquidity_discount.py`, `control_premium.py` | Sconti/premi per non quotate |
| M&A | `tools/synergy_valuation.py`, `acquisition_value.py` | Valore con sinergie |
| Risk analysis | `tools/sensitivity_table.py`, `monte_carlo.py`, `scenario_analysis.py` | Distribuzione valori |

### Modalita' FSI Excel (Italia/Europa)

| Metodologia | Skill FSI | Output |
| --- | --- | --- |
| DCF (BTP, ERP italiano, IRES+IRAP) | `fsi-dcf-model-italy` | Workbook Excel DCF + WACC + sensitivity |
| LBO (Euribor, leverage 3-4.5x, PEX) | `fsi-lbo-model-italy` | Sources & Uses, debt schedule, returns |
| Three-statement (IFRS) | `fsi-3-statement-model-italy` | IS/BS/CF integrato con formule vive |
| Trading comps (Borsa Italiana, Euronext) | `fsi-comps-analysis-italy` | Multipli, statistiche, outlier |
| Pitch completo | `fsi-pitch-agent-italy` | Excel + deck PowerPoint |
| Merger model (IFRS 3, art. 176 TUIR) | `fsi-merger-model-italy` | Accretion/dilution, sinergie |

### Modalita' Rating & Valuation (PMI non quotate)

Basata su tre paper accademici integrati:

| Paper | Autori | Metodologia | Modulo Python |
| --- | --- | --- | --- |
| BMS (AIAF n.65, 2008) | Scarano/Brughera | Bilancio Medio Standardizzato settoriale | `rating_valuation.bms` |
| TV coerente (AIAF n.66, 2008) | Scarano/Di Napoli | DCF 2/3 stadi con reinvestimento esplicito + 7 check | `rating_valuation.dcf` |
| Agentic Credit Risk (RAPD, 2014) | Montesi/Papiro | PD forward-looking via Monte Carlo (Weibull, copula) | `rating_valuation.agentic_credit_risk` |

Pipeline completa: BMS settoriale -> analisi differenziale -> DCF con TV coerente -> Agentic Credit Risk Monte Carlo -> rating implicito.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env    # Inserisci la tua MASSIVE_API_KEY
pytest tests/           # Verifica installazione (348 test)
```

Requisiti: Python 3.11+, API key [Massive.com](https://massive.com).

## Come funziona

### Flow Damodaran (3 step)

```text
Step 1: CONFIG          Step 2: ANALISI              Step 3: PDF
configs/NVDA.json  -->  run_analysis.py NVDA  -->  md_to_pdf.py NVDA
(parametri analista)    (calcoli + report .md)     (report .pdf)
```

**Step 1 - Configura.** Copia il template e popola i parametri dell'analista:

```bash
# Societa' US/internazionali
cp configs/_template.json configs/NVDA.json

# Societa' italiane/europee (defaults: BTP, ERP 7%, IRES+IRAP 27.9%)
cp configs/_template_italia.json configs/ENEL.MI.json
```

**Step 2 - Analizza.** Lo script legge il config, recupera i dati live da Massive.com, esegue tutti i calcoli e genera il report markdown:

```bash
python scripts/run_analysis.py NVDA       # Societa' US
python scripts/run_analysis.py ENEL.MI    # Societa' italiana (defaults IRES+IRAP)
```

**Step 3 - PDF.** Converte il report in PDF con layout professionale:

```bash
python scripts/md_to_pdf.py NVDA
```

### Flow FSI Excel (interattivo)

**Cosa NON e':** non e' uno script Python che esporta un `.xlsx`. Non esiste un comando shell tipo `run_analysis.py` per la modalita' FSI.

**Cos'e':** e' un workflow conversazionale in cui **Claude stesso costruisce il workbook Excel cella per cella**, in modo interattivo, fermandosi a checkpoint per farsi validare ogni fase. Il risultato e' un modello Excel con **formule vive** che ricalcola da solo quando modifichi un'assunzione.

#### Due ambienti di esecuzione

| Ambiente | Quando si attiva | Come Claude scrive le celle |
| --- | --- | --- |
| **Office JS (Add-in)** | Sei dentro Excel con l'Add-in Claude collegato | Scrittura diretta nel workbook aperto, ricalcolo nativo Excel |
| **Python / openpyxl** | Sessione standard (es. Claude Code, claude.ai) | Genera file `.xlsx` su disco, ricalcolo via `recalc.py` prima della consegna |

In entrambi i casi i principi sono identici: formule sopra valori fissi, commenti cella con fonte, sensitivity table 5x5 con celle centrali = caso base.

#### Step 1: invocazione

Scegli il tipo di modello che ti serve:

```text
/fsi-valuation ENEL.MI                  # DCF Excel (default)
/fsi-valuation ENEL.MI --tipo dcf       # DCF esplicito
/fsi-valuation ENEL.MI --tipo lbo       # LBO model (Sources & Uses, debt schedule, returns)
/fsi-valuation ENEL.MI --tipo comps     # Trading comparables (Borsa Italiana / Euronext)
/fsi-valuation ENEL.MI --tipo pitch     # Pitch completo: workbook Excel + deck PowerPoint
```

Queste sono **invocazioni di skill**, non comandi shell — vanno digitate nella conversazione con Claude.

#### Step 2: identificazione target e raccolta dati

Claude ti chiede ticker/ISIN e tipo di modello, poi recupera i dati seguendo questa priorita':

1. **MCP servers** (CapIQ, Daloopa, Refinitiv) se configurati nell'ambiente
2. **Dati forniti da te** (bilanci, stime, management guidance)
3. **Ricerca web pubblica** (CONSOB, Borsa Italiana, bilanci IFRS) come fallback

Per societa' italiane si usano bilanci IFRS consolidati (non US GAAP), fonti CONSOB/Borsa Italiana/Bureau van Dijk (non SEC EDGAR).

#### Step 3: costruzione interattiva con checkpoint

Claude **non costruisce il modello end-to-end**. Si ferma a ogni fase e ti chiede di confermare:

```text
Fase 1: INPUT GREZZI
  Mostra: ricavi storici, margini, azioni, posizione finanziaria netta
  Checkpoint: "Confermi gli input prima di proiettare?"

Fase 2: PROIEZIONI RICAVI
  Mostra: top line proiettato, tassi di crescita anno per anno
  Checkpoint: "Confermi la curva di crescita prima di costruire i margini?"

Fase 3: BUILD FCF
  Mostra: prospetto FCF completo (EBIT, tax, D&A, CapEx, Delta WC)
  Checkpoint: "Confermi la logica FCF prima del WACC?"

Fase 4: WACC (parametri italiani)
  Mostra: Rf=BTP 10Y, ERP=6-8%, Beta, Costo debito=Euribor+spread, IRES+IRAP=27.9%
  Checkpoint: "Confermi il WACC prima dello sconto?"

Fase 5: TERMINAL VALUE + EQUITY BRIDGE
  Mostra: TV, PV cash flow, EV -> equity value -> prezzo per azione
  Checkpoint: "Confermi prima delle sensitivity table?"

Fase 6: SENSITIVITY TABLES + AUDIT
  Costruisce: 3 tabelle 5x5 (WACC vs g, crescita vs margine, etc.)
  Esegue: fsi-audit-xls-italy (controllo formule, balance check, errori)
  Consegna: file .xlsx finale
```

Ogni checkpoint serve a intercettare errori prima che si propaghino — una proiezione di margine sbagliata scoperta dopo le sensitivity costringe a rifare tutto a valle.

#### Step 4: check regolamentari (solo M&A / pitch)

Se il `--tipo` e' `pitch` o si tratta di un'operazione M&A, Claude esegue automaticamente i check di compliance:

- **AGCM** — soglie concentrazione (fatturato aggregato >532M EUR, target >32M EUR)
- **Golden Power** — verifica settori strategici (D.L. 21/2012: energia, telco, difesa, infrastrutture critiche, banche)
- **CONSOB** — comunicazioni obbligatorie per target quotate (OPA, comunicati price-sensitive)

#### Step 5: consegna

Output:

- **DCF / LBO / 3-statement / comps** — un file `.xlsx` con formule vive in EUR
- **Pitch** — file `.xlsx` + file `.pptx` (deck con executive summary, valuation football field, analisi competitiva)

Puoi aprire il workbook in Excel/Google Sheets, modificare qualsiasi assunzione (crescita, margini, WACC, terminal g) e tutto il modello ricalcola in tempo reale grazie alle formule vive.

#### Perche' "formule vive" e' la differenza chiave

| | Modello con valori hardcoded | Modello FSI con formule vive |
| --- | --- | --- |
| `D20` (ricavo anno 1) | `1.234.567` | `=D19*(1+$B$8)` |
| Cambi crescita in `B8` | Niente succede, devi rifare i calcoli | L'intero modello si aggiorna istantaneamente |
| Sensitivity 5x5 | 25 numeri statici | 25 formule che ricalcolano DCF completo |
| Audit / review | Difficile capire da dove viene un numero | Click su cella -> vedi formula e fonte |

Tutti gli input grezzi (numeri blu) hanno commenti cella con fonte e data, cosi' il modello e' audit-friendly.

#### Parametri italiani di default (FSI Excel)

| Parametro | Valore | Fonte |
| --- | --- | --- |
| Risk-free rate | BTP 10Y (~4%) | Banca d'Italia |
| ERP | 6-8% | Damodaran + CRP Italia |
| Costo debito base | Euribor 3M/6M + spread (250-450 bps) | BCE |
| Aliquota fiscale | IRES 24% + IRAP 3.9% = 27.9% | D.P.R. 917/1986 + D.Lgs. 446/1997 |
| Terminal growth | 1-2% | PIL nominale Eurozona |
| Leverage tipico LBO | 3-4.5x EBITDA | Mercato italiano |
| DSO / DPO | 60-90 giorni | Prassi italiana |
| Esenzione plusvalenze | PEX 95% (art. 87 TUIR) | TUIR |
| Limite deducibilita' interessi | 30% del ROL (art. 96 TUIR) | TUIR |

#### Quando usare FSI Excel vs Damodaran vs Rating & Valuation

| Caso d'uso | Modalita' consigliata |
| --- | --- |
| Analisi quotata USA, report PDF/MD batch, riproducibile | **Damodaran** (`run_analysis.py`) |
| Valutazione di una quotata italiana, voglio un Excel da modificare a mano | **FSI Excel** (`/fsi-valuation`) |
| Pitch a comitato investimenti con Excel + deck | **FSI Excel** `--tipo pitch` |
| LBO con Euribor, PEX exit, art. 96 TUIR | **FSI Excel** `--tipo lbo` |
| PMI non quotata, credit risk forward-looking, rating implicito | **Rating & Valuation** |

### Flow Rating & Valuation (PMI, credit risk)

Pipeline Python per PMI non quotate, basata su tre paper accademici AIAF/RAPD:

```text
Step 1: DATASET         Step 2: BMS            Step 3: DCF           Step 4: CREDIT RISK
CSV normalizzati  -->   BMS settoriale   -->   DCF 2/3 stadi  -->   Monte Carlo PD/LGD
(bilanci AIDA/BvD)     (IMS di settore)       (TV coerente)         (20K trial, rating)
```

```bash
# Pipeline completa su Riva Meccanica SpA (dataset demo)
python examples/rating_valuation/02_full_pipeline_riva_meccanica.py

# Solo BMS settoriale
python examples/rating_valuation/01_bms_industrial_machinery.py
```

Convenzione cash flow: capital cash flow (Ruback 2002) con pre-tax WACC. I dati risiedono in `data/rating_valuation/` (CSV normalizzati con schema in `data/rating_valuation/schema.md`).

### Cosa genera il report

Ogni report contiene 10 sezioni standardizzate:

| # | Sezione | Contenuto |
| --- | --- | --- |
| 1 | Executive Summary | Valore stimato, prezzo, upside/downside, raccomandazione |
| 2 | Panoramica Aziendale | Market cap, ricavi, EBIT, EPS, debito, beta |
| 3 | Costo del Capitale | CAPM, costo debito, WACC |
| 4 | Valutazione DCF | FCFF base, proiezione 3-stage, enterprise/equity value |
| 5 | Valutazione Relativa | Campione comparabili, statistiche multipli, valori impliciti |
| 6 | Analisi di Sensitivita' | WACC vs growth, crescita vs margine (tabelle 2D) |
| 7 | Analisi per Scenari | Best/base/worst case con probabilita' ponderate |
| 8 | Simulazione Monte Carlo | 10.000 iterazioni, percentili, istogramma |
| 9 | Sintesi e Raccomandazione | Media ponderata multi-metodo, rating BUY/HOLD/SELL |
| 10 | Rischi e Disclaimer | Fattori di rischio al rialzo e al ribasso |

### Aziende in perdita

Il flow gestisce automaticamente aziende con EBIT/EPS negativi (es. Roblox, Unity):

- I multipli P/E e EV/EBITDA vengono segnalati come N/A
- Il DCF funziona anche con FCFF negativo (proiezione convergenza a profitto)
- Divisioni per zero protette su tutti i multipli
- Note automatiche nel report che spiegano le limitazioni

## Struttura del progetto

```text
valuation_analyst/
  configs/                      Parametri analista per ogni ticker
    _template.json              Template per societa' US/internazionali
    _template_italia.json       Template per societa' italiane/europee
    AAPL.json                   Apple Inc.
    ENEL.MI.json                ENEL S.p.A. (esempio italiano)
    GOOGL.json                  Alphabet Inc.
    MSFT.json                   Microsoft Corporation
    ORCL.json                   Oracle Corporation
    RBLX.json                   Roblox Corporation
  scripts/                      Script di utilita'
    run_analysis.py             Analisi completa (config -> report)
    md_to_pdf.py                Conversione Markdown -> PDF
  src/valuation_analyst/        Package Python Damodaran
    config/                     Impostazioni, costanti, URL
    models/                     Dataclass (Company, CashFlow, Comparable, etc.)
    tools/                      Moduli di calcolo + data fetching
    utils/                      Formatting, math helpers, logging, validazione
  src/rating_valuation/         Package Python Rating & Valuation
    common/                     Data loader, financial math, invarianti bilancio
    bms/                        BMSBuilder — Bilancio Medio Standardizzato
    dcf/                        DCF 2/3 stadi con Terminal Value coerente + check coerenza
    agentic_credit_risk/        Simulatore Monte Carlo PD/LGD/EL/UL
    differential/               Analisi differenziale target vs IMS
    rating/                     Rating Mapper (master scale, CDS, Altman Z)
    backtest/                   Backtest Comparator (AUROC/Gini/KS)
  output/                       Report generati
    markdown/                   Report .md
    pdf/                        Report .pdf
  data/
    cache/                      Cache dati Damodaran scaricati
    logs/                       Log delle interazioni (prompt_log.md)
    rating_valuation/           CSV normalizzati per Rating & Valuation
      companies.csv             Bilanci riclassificati (1 riga per company x anno)
      sectors.csv               Parametri settoriali (Weibull, correlazioni, beta)
      macro.csv                 Parametri macro per paese (Rf, MRP, PIL)
      rating_master_scale.csv   Master scale S&P Rating ↔ PD
      schema.md                 Schema autoritativo dei CSV
  .claude/
    agents/                     8 agenti Damodaran + 10 agenti FSI Italy + 6 agenti Rating & Valuation
    skills/                     10 skill Damodaran + 59 skill FSI Italy + 7 skill Rating & Valuation
    commands/                   Comandi slash (/status, /demo)
  tests/                        348 test totali
    unit/                       Unit test Damodaran
    integration/                Integration test Damodaran
    rating_valuation/           Test Rating & Valuation (183 test)
  examples/
    damodaran/                  8 script demo Damodaran (01-08)
    rating_valuation/           2 esempi pipeline Rating & Valuation
  docs/
    damodaran/                  Architettura, metodologia, agent guide, demo walkthrough
    fsi_italy/                  Documentazione modalita' FSI Excel (indice skill)
    rating_valuation/           overview.md, TODO.md, 3 PDF paper accademici
```

## Configurazione JSON

Il file `configs/{TICKER}.json` contiene solo i parametri che l'analista decide, non i dati di mercato (recuperati automaticamente da API).

Due template disponibili:

- `_template.json` - Societa' US/internazionali (ERP 5.5%, tax 25%, terminal growth 2.5%)
- `_template_italia.json` - Societa' italiane/europee (ERP 7%, IRES+IRAP 27.9%, terminal growth 1.5%)

### Campi principali

| Campo | Tipo | Esempio | Descrizione |
| --- | --- | --- | --- |
| `ticker` | string | `"AAPL"` o `"ENEL.MI"` | Simbolo azionario |
| `paese` | string | `"US"` o `"IT"` | Paese (attiva defaults italiani se `"IT"`) |
| `modalita` | string | `"damodaran"` | Modalita' di analisi |
| `erp` | float | `0.055` (US) / `0.07` (IT) | Equity Risk Premium |
| `rating_credito` | string | `"AA+"` | Rating S&P per il costo del debito |
| `crescita_alta` | float | `0.12` | Tasso crescita fase 1 DCF |
| `crescita_stabile` | float | `0.025` (US) / `0.015` (IT) | Tasso crescita perpetua (terminale) |
| `anni_alta` | int | `5` | Durata fase alta crescita |
| `anni_transizione` | int | `5` | Durata convergenza a crescita stabile |
| `comparabili` | array | vedi sotto | Lista di 5-7 societa' peer |
| `sensitivity` | object | vedi sotto | Range per le tabelle di sensitivita' |
| `scenari` | object | vedi sotto | Parametri best/base/worst |
| `monte_carlo` | object | vedi sotto | Deviazioni standard per la simulazione |
| `rischi_rialzo` | array | `["..."]` | Fattori di rischio qualitativi |
| `rischi_ribasso` | array | `["..."]` | Fattori di rischio qualitativi |
| `fondamentali_fallback` | object | vedi sotto | Dati di bilancio se API non disponibile |

### Esempio comparabile

```json
{
  "ticker": "MSFT",
  "nome": "Microsoft Corporation",
  "settore": "Technology",
  "market_cap": 3083000,
  "pe_ratio": 31.7,
  "ev_ebitda": 22.7,
  "pb_ratio": 11.5,
  "ev_sales": 11.7,
  "ev_ebit": 26.0,
  "margine_operativo": 0.45,
  "crescita_ricavi": 0.16,
  "paese": "US"
}
```

### Dati di mercato

Lo script recupera i dati in due modi:

- **Sempre live** (Massive.com API): prezzo, market cap, shares outstanding, risk-free rate
- **Fondamentali** (bilancio, conto economico, cash flow):
  - Piano API con `/stocks/financials/*`: dati live
  - Piano free: usa `fondamentali_fallback` dal JSON config (valori in milioni USD)

## Agenti Claude Code

### Agenti Damodaran (Python, report markdown/PDF)

| Agente | Ruolo | Tool principali |
| --- | --- | --- |
| **orchestrator** | Coordina tutti gli agenti, sintetizza i risultati | Task, Agent |
| **dcf-analyst** | DCF multi-stage (FCFF/FCFE) | dcf_fcff, dcf_fcfe, terminal_value |
| **relative-analyst** | Multipli e screening comparabili | multiples, comparable_screen |
| **cost-of-capital** | WACC, CAPM, beta, risk premium | capm, wacc, beta_estimation |
| **option-pricing** | Black-Scholes, equity come opzione | black_scholes, equity_as_option |
| **private-valuation** | Sconti illiquidita', premio controllo | illiquidity_discount, control_premium |
| **ma-analyst** | Sinergie e valore di acquisizione | synergy_valuation, acquisition_value |
| **risk-analyst** | Sensitivity, scenari, Monte Carlo | sensitivity_table, monte_carlo, scenario_analysis |

### Agenti FSI Italy (Excel con formule vive, contesto italiano/europeo)

| Agente | Ruolo | Parametri |
| --- | --- | --- |
| **fsi-model-builder-italy** | DCF, LBO, 3-statement, comps in Excel | BTP, Euribor, IRES+IRAP, IFRS |
| **fsi-pitch-agent-italy** | Pitch completo: workbook + deck PowerPoint | AGCM, Golden Power, CONSOB |
| **fsi-earnings-reviewer-italy** | Revisione utili e aggiornamento modelli | Bilancio semestrale/annuale |
| **fsi-market-researcher-italy** | Ricerca di mercato e analisi settoriale | Borsa Italiana, Euronext |
| **fsi-valuation-reviewer-italy** | Review valutazioni per LP reporting | PEX, AIFMD |
| **fsi-meeting-prep-agent-italy** | Briefing MiFID II-compliant | MiFID II, adeguatezza |
| **fsi-kyc-screener-italy** | KYC/AML screening | D.Lgs. 231/2007, UIF |
| **fsi-gl-reconciler-italy** | Riconciliazione contabile | OIC, IFRS |
| **fsi-month-end-closer-italy** | Chiusura mensile | TFR, assestamento |
| **fsi-statement-auditor-italy** | Verifica estratti conto LP/NAV | SGR/GEFIA |

### Skill Damodaran

| Skill | Comando | Descrizione |
| --- | --- | --- |
| Nuova analisi | `/new-analysis NVDA` | Setup config per un nuovo ticker |
| Report completo | `/valuation-report AAPL` | Orchestrazione completa |
| DCF | `/dcf-valuation AAPL` | Solo valutazione DCF |
| Comparabili | `/comparable-analysis AAPL` | Solo valutazione relativa |
| Costo capitale | `/cost-of-capital AAPL` | Solo WACC/CAPM |
| Sensitivita' | `/sensitivity-analysis AAPL` | Solo risk analysis |
| Option pricing | `/option-valuation AAPL` | Solo Black-Scholes |
| Privata | `/private-valuation AAPL` | Solo societa' privata |
| M&A | `/ma-valuation AAPL` | Solo M&A e sinergie |
| Dati Damodaran | `/fetch-damodaran-data` | Aggiorna dataset settoriali |

### Skill FSI Italy (59 skill, prefisso `fsi-`)

| Verticale | Skill (n.) | Esempi |
| --- | --- | --- |
| Financial Analysis | 14 | `fsi-dcf-model-italy`, `fsi-comps-analysis-italy`, `fsi-lbo-model-italy`, `fsi-3-statement-model-italy` |
| Equity Research | 9 | `fsi-initiating-coverage-italy`, `fsi-earnings-analysis-italy`, `fsi-sector-overview-italy` |
| Investment Banking | 10 | `fsi-golden-power-check`, `fsi-merger-model-italy`, `fsi-buyer-list-italy`, `fsi-process-letter-italy` |
| Private Equity | 10 | `fsi-returns-analysis-italy`, `fsi-dd-checklist-italy`, `fsi-ic-memo-italy` |
| Wealth Management | 12 | `fsi-mifid-ii-adeguatezza`, `fsi-regime-fiscale-italia`, `fsi-fondi-pensione-italia`, `fsi-pir-pianificazione` |
| Operations | 4 | `fsi-kyc-rules-italy`, `fsi-aml-italia-231`, `fsi-dora-compliance` |

Entry point: `/fsi-valuation ENEL.MI` per avviare il workflow FSI Excel.

### Agenti Rating & Valuation (Python, PMI, credit risk)

| Agente | Ruolo | Skill invocata |
| --- | --- | --- |
| **bms-analyst** | Costruzione e validazione BMS settoriale | `bms-builder` |
| **dcf-validator** | DCF 2/3 stadi + 7 check coerenza TV | `dcf-tv-coherence` |
| **agentic-credit-risk-simulator** | Monte Carlo PD/LGD/EL/UL (20K trial) | `agentic-credit-risk` |
| **data-curator** | Validazione e curatela dataset CSV | — |
| **backtest-analyst** | Confronto modelli credit risk (AUROC/Gini/KS) | `backtest-comparator` |
| **valuation-reporter** | Report narrativo in italiano (stile AIAF) | — |

### Skill Rating & Valuation (7 skill)

| Skill | Modulo Python | Funzione |
| --- | --- | --- |
| `bms-builder` | `rating_valuation.bms` | Bilancio Medio Standardizzato settoriale |
| `dcf-tv-coherence` | `rating_valuation.dcf` | DCF 2/3 stadi + 7 check coerenza TV |
| `differential-analysis` | `rating_valuation.differential` | Target vs IMS, 4 driver |
| `agentic-credit-risk` | `rating_valuation.agentic_credit_risk` | Monte Carlo PD/LGD/EL/UL |
| `rating-mapper` | `rating_valuation.rating` | Master scale, CDS→PD, Altman Z |
| `backtest-comparator` | `rating_valuation.backtest` | AUROC/Gini/KS multi-modello |
| `rating-valuation-pipeline` | Orchestrazione | Pipeline end-to-end |

## Fonti dati

### Modalita' Damodaran

| Fonte | Utilizzo | Accesso |
| --- | --- | --- |
| [Massive.com](https://massive.com) | Prezzi, bilanci, ratios, profili aziendali | API key (`.env`) |
| [Dataset Damodaran](https://pages.stern.nyu.edu/~adamodar/) | Beta settoriali, ERP, WACC, multipli medi | Download automatico + cache |

### Modalita' FSI Excel (Italia)

| Fonte | Utilizzo | Accesso |
| --- | --- | --- |
| MCP servers (CapIQ, Daloopa, Refinitiv) | Financials, consensus, multipli | MCP configurati (opzionale) |
| CONSOB / Borsa Italiana | Bilanci IFRS societa' quotate italiane | Pubblico |
| Bureau van Dijk / AIDA | Bilanci strutturati, comparabili italiani | Licenza (opzionale) |
| Dati utente | Bilanci, stime, management guidance | Forniti manualmente |

### Modalita' Rating & Valuation (PMI)

| Fonte | Utilizzo | Accesso |
| --- | --- | --- |
| CSV normalizzati (`data/rating_valuation/`) | Bilanci riclassificati, parametri settoriali, macro | Inclusi (dataset demo) |
| Bureau van Dijk / AIDA | Bilanci strutturati per campione settoriale | Licenza (per dati reali) |
| Master scale S&P | Conversione PD ↔ rating | Inclusa nel CSV |
| Paper AIAF/RAPD | Parametri Weibull, correlazioni, recovery rate | Inclusi in `docs/rating_valuation/` |

## Demo

8 script nella cartella `examples/damodaran/` dimostrano ogni funzionalita' con dati di esempio (nessuna API richiesta):

```bash
python examples/damodaran/01_cost_of_capital.py      # WACC e CAPM
python examples/damodaran/02_dcf_valuation.py        # DCF FCFF/FCFE multi-stage
python examples/damodaran/03_comparable_analysis.py  # Screening e multipli
python examples/damodaran/04_option_pricing.py       # Black-Scholes
python examples/damodaran/05_private_valuation.py    # Sconti illiquidita'
python examples/damodaran/06_ma_synergy.py           # Sinergie M&A
python examples/damodaran/07_sensitivity_analysis.py # Monte Carlo e scenari
python examples/damodaran/08_full_report.py          # Report completo

# Rating & Valuation (PMI, credit risk)
python examples/rating_valuation/01_bms_industrial_machinery.py    # BMS settoriale
python examples/rating_valuation/02_full_pipeline_riva_meccanica.py  # Pipeline completa
```

## Test

```bash
pytest tests/                     # 348 test (valuation_analyst + rating_valuation)
pytest tests/unit/                # 161 unit test Damodaran
pytest tests/integration/         # 4 integration test Damodaran
pytest tests/test_bms_*.py        # Test BMS
pytest tests/test_dcf_*.py        # Test DCF (Damodaran + Rating & Valuation)
pytest tests/test_agentic_*.py    # Test Agentic Credit Risk
pytest tests/ --cov               # Con coverage report
```

## Uso con Claude Cowork

Il progetto e' strutturato per funzionare nativamente con [Claude Cowork](https://claude.com/blog/cowork-research-preview), la feature collaborativa di Claude (disponibile su piani Pro, Max, Team, Enterprise).

### Setup su Cowork

1. **Apri Cowork** dalla tab dedicata su Claude Desktop o claude.ai
2. **Connetti il progetto** dando accesso alla cartella locale del repository
3. **Claude legge automaticamente** `CLAUDE.md` dalla root come istruzioni di progetto
4. **Tutti gli agenti e le skill** in `.claude/` sono disponibili immediatamente

### Cosa funziona out-of-the-box

| Feature | Come funziona in Cowork |
| --- | --- |
| Analisi nuova | Chiedi "analizza Oracle" e Claude usa `/new-analysis` + `run_analysis.py` |
| Config condivisi | I file `configs/*.json` sono visibili e modificabili da tutti i collaboratori |
| Report uniformi | Ogni analisi produce le stesse 10 sezioni, indipendentemente da chi la lancia |
| Skill e agenti | `/valuation-report`, `/dcf-valuation`, etc. sono invocabili da qualsiasi membro |
| Storico | I report in `output/` e i log in `data/logs/` restano accessibili a tutto il team |

### Workflow collaborativo tipico

```text
Analista A                          Analista B
    |                                   |
    +-- /new-analysis TSLA              +-- /new-analysis AMZN
    |   (crea configs/TSLA.json)        |   (crea configs/AMZN.json)
    |                                   |
    +-- run_analysis.py TSLA            +-- run_analysis.py AMZN
    |   (genera report)                 |   (genera report)
    |                                   |
    +-- review e commenti        <----->+-- review e commenti
    |                                   |
    +-- md_to_pdf.py TSLA              +-- md_to_pdf.py AMZN
```

### Alternativa: Claude Projects (claude.ai)

Se Cowork non e' disponibile, puoi usare Claude Projects:

1. Vai su claude.ai > Projects > New Project
2. Nelle istruzioni di progetto, incolla il contenuto di `CLAUDE.md`
3. Carica i file di riferimento: `configs/_template.json`, `docs/damodaran/methodology.md`
4. Condividi con il team (richiede piano Team o Enterprise)

## Compliance Normativa Italiana

Le skill FSI Italy includono verifiche e conformita' per:

| Ambito | Normativa | Skill |
| --- | --- | --- |
| Antitrust | AGCM (soglie: fatturato >532M EUR, target >32M EUR) | `fsi-golden-power-check`, `fsi-buyer-list-italy` |
| Settori strategici | Golden Power (D.L. 21/2012) | `fsi-golden-power-check` |
| Quotate | CONSOB, Regolamento Emittenti | `fsi-pitch-agent-italy` |
| Adeguatezza | MiFID II (profiling, target market, ESG) | `fsi-mifid-ii-adeguatezza` |
| Costi | MiFID II ex-ante/ex-post | `fsi-costi-mifid-exante-expost` |
| AML/KYC | D.Lgs. 231/2007 (3 livelli adeguata verifica) | `fsi-kyc-rules-italy`, `fsi-aml-italia-231` |
| Sostenibilita' | SFDR art. 6/8/9 | `fsi-sfdr-disclosure` |
| Resilienza operativa | DORA (Reg. UE 2022/2554) | `fsi-dora-compliance` |
| Fiscalita' | IRES 24% + IRAP 3.9%, PEX art. 87 TUIR, art. 96 TUIR | `fsi-regime-fiscale-italia`, `fsi-returns-analysis-italy` |
| Previdenza | Fondi pensione, TFR, PIR | `fsi-fondi-pensione-italia`, `fsi-pir-pianificazione` |

## Documentazione

### Damodaran (Python, report markdown/PDF)

- [Architettura del sistema](docs/damodaran/architecture.md)
- [Guida agli agenti](docs/damodaran/agent_guide.md)
- [Metodologia Damodaran](docs/damodaran/methodology.md)
- [Fonti dati](docs/damodaran/data_sources.md)
- [Walkthrough demo](docs/damodaran/demo_walkthrough.md)
- [Valutazione progetto](docs/damodaran/project_evaluation.md)

### FSI Excel (Italia/Europa)

- [Documentazione modalita' FSI Excel](docs/fsi_italy/README.md) (indice delle 59 skill `fsi-*`)

### Rating & Valuation (PMI, credit risk)

- [Quadro d'insieme](docs/rating_valuation/overview.md)
- [Paper: BMS - Bilancio Medio Standardizzato (AIAF n.65)](docs/rating_valuation/2008%20n.-65%20Bilancio%20Medio%20Standard.pdf)
- [Paper: Terminal Value coerente (AIAF n.66)](docs/rating_valuation/2008%20n.-66%20Calcolo%20del%20Terminal%20Value.pdf)
- [Paper: Agentic Credit Risk (RAPD)](docs/rating_valuation/RAPD.pdf)

## Formule chiave

### Formule Damodaran (US/internazionale)

```text
FCFF  = EBIT(1-t) + Deprezzamento - CapEx - Delta WC
CAPM  = Rf + Beta * ERP + CRP
WACC  = (E/V) * Re + (D/V) * Rd * (1-t)
TV    = FCF * (1+g) / (r-g)
BS    = V * N(d1) - K * e^(-rT) * N(d2)
```

### Parametri italiani (FSI Excel)

```text
Rf    = BTP 10Y (~4%)
ERP   = 6-8% (include CRP Italia)
t     = IRES 24% + IRAP 3.9% = 27.9%
Rd    = Euribor 3M/6M + spread (250-450 bps)
TV_g  = 1-2% (PIL nominale Eurozona)
PEX   = 95% esenzione plusvalenze (art. 87 TUIR)
ROL   = 30% limite deducibilita' interessi (art. 96 TUIR)
```

### Formule Rating & Valuation (PMI, credit risk)

```text
CCF   = NOPAT - DELTA_NIC + tau * INT        (Capital Cash Flow, Ruback 2002)
WACC  = w_e * k_e + w_d * r_d                (pre-tax, con CCF)
TV    = NOPAT * (1 - g/ROIC_NI) / (wacc - g) (Terminal Value coerente)
TV_ss = NOPAT / wacc                          (steady state, ROIC = WACC)
g     = ROIC_NI * h_T                         (vincolo coerenza, h_T in [0,1])
D_t   = max(0, f(NOPAT, DELTA_NIC, r_d, tau, D_{t-1}))  (debito endogeno, eq.[7])
PD    = 1 - exp(-CDS / LGD)                  (CDS -> PD, LGD = 60%)
```

## Licenza

MIT
