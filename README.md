# Valuation Analyst

**Sistema multi-agente per equity valuation basato sulle metodologie di Aswath Damodaran (NYU Stern).**

Toolkit professionale che combina 8 agenti Claude Code specializzati con moduli di calcolo Python per produrre report di valutazione completi, dalla raccolta dati alla raccomandazione finale.

## Scopo

1. **Strumento di lavoro** per analisti finanziari: genera report di valutazione riproducibili e audit-friendly
2. **Demo** per mostrare come Claude Code puo' orchestrare analisi finanziarie complesse

## Metodologie

| Metodologia | Modulo | Output |
| --- | --- | --- |
| DCF multi-stage (FCFF/FCFE) | `tools/dcf_fcff.py`, `dcf_fcfe.py` | Valore intrinseco per azione |
| CAPM / WACC | `tools/capm.py`, `wacc.py` | Costo del capitale |
| Valutazione relativa | `tools/multiples.py` | Range da multipli comparabili |
| Black-Scholes | `tools/black_scholes.py`, `equity_as_option.py` | Equity come opzione (distress) |
| Societa' private | `tools/illiquidity_discount.py`, `control_premium.py` | Sconti/premi per non quotate |
| M&A | `tools/synergy_valuation.py`, `acquisition_value.py` | Valore con sinergie |
| Risk analysis | `tools/sensitivity_table.py`, `monte_carlo.py`, `scenario_analysis.py` | Distribuzione valori |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env    # Inserisci la tua MASSIVE_API_KEY
pytest tests/           # Verifica installazione (165 test)
```

Requisiti: Python 3.11+, API key [Massive.com](https://massive.com).

## Come funziona

### Flow di analisi (3 step)

```text
Step 1: CONFIG          Step 2: ANALISI              Step 3: PDF
configs/NVDA.json  -->  run_analysis.py NVDA  -->  md_to_pdf.py NVDA
(parametri analista)    (calcoli + report .md)     (report .pdf)
```

**Step 1 - Configura.** Copia il template e popola i parametri dell'analista:

```bash
cp configs/_template.json configs/NVDA.json
# Modifica: ticker, rating, crescita, comparabili, scenari, rischi
```

**Step 2 - Analizza.** Lo script legge il config, recupera i dati live da Massive.com, esegue tutti i calcoli e genera il report markdown:

```bash
python scripts/run_analysis.py NVDA
# Output: output/markdown/NVDA_2026-03-18_valuation.md
```

**Step 3 - PDF.** Converte il report in PDF con layout professionale:

```bash
python scripts/md_to_pdf.py NVDA
# Output: output/pdf/NVDA_2026-03-18_valuation.pdf
```

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
    _template.json              Template documentato per nuove analisi
    AAPL.json                   Apple Inc.
    GOOGL.json                  Alphabet Inc.
    MSFT.json                   Microsoft Corporation
    ORCL.json                   Oracle Corporation
    RBLX.json                   Roblox Corporation
  scripts/                      Script di utilita'
    run_analysis.py             Analisi completa (config -> report)
    md_to_pdf.py                Conversione Markdown -> PDF
  src/valuation_analyst/        Package Python principale
    config/                     Impostazioni, costanti, URL
    models/                     Dataclass (Company, CashFlow, Comparable, etc.)
    tools/                      Moduli di calcolo + data fetching
    utils/                      Formatting, math helpers, logging, validazione
  output/                       Report generati
    markdown/                   Report .md
    pdf/                        Report .pdf
  data/
    cache/                      Cache dati Damodaran scaricati
    logs/                       Log delle interazioni (prompt_log.md)
  .claude/
    agents/                     8 agenti specializzati
    skills/                     10 skill di valutazione
    commands/                   Comandi slash (/status, /demo)
  tests/                        165 test (unit + integration)
  demos/                        8 script demo con dati di esempio
  docs/                         Documentazione tecnica
```

## Configurazione JSON

Il file `configs/{TICKER}.json` contiene solo i parametri che l'analista decide, non i dati di mercato (recuperati automaticamente da API).

### Campi principali

| Campo | Tipo | Esempio | Descrizione |
| --- | --- | --- | --- |
| `ticker` | string | `"AAPL"` | Simbolo azionario |
| `erp` | float | `0.055` | Equity Risk Premium |
| `rating_credito` | string | `"AA+"` | Rating S&P per il costo del debito |
| `crescita_alta` | float | `0.12` | Tasso crescita fase 1 DCF |
| `crescita_stabile` | float | `0.025` | Tasso crescita perpetua (terminale) |
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

### Skill disponibili

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

## Fonti dati

| Fonte | Utilizzo | Accesso |
| --- | --- | --- |
| [Massive.com](https://massive.com) | Prezzi, bilanci, ratios, profili aziendali | API key (`.env`) |
| [Dataset Damodaran](https://pages.stern.nyu.edu/~adamodar/) | Beta settoriali, ERP, WACC, multipli medi | Download automatico + cache |

## Demo

8 script nella cartella `demos/` dimostrano ogni funzionalita' con dati di esempio (nessuna API richiesta):

```bash
python demos/01_cost_of_capital.py      # WACC e CAPM
python demos/02_dcf_valuation.py        # DCF FCFF/FCFE multi-stage
python demos/03_comparable_analysis.py  # Screening e multipli
python demos/04_option_pricing.py       # Black-Scholes
python demos/05_private_valuation.py    # Sconti illiquidita'
python demos/06_ma_synergy.py           # Sinergie M&A
python demos/07_sensitivity_analysis.py # Monte Carlo e scenari
python demos/08_full_report.py          # Report completo
```

## Test

```bash
pytest tests/                     # 165 test, tutti i moduli
pytest tests/unit/                # 161 unit test
pytest tests/integration/         # 4 integration test
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
3. Carica i file di riferimento: `configs/_template.json`, `docs/methodology.md`
4. Condividi con il team (richiede piano Team o Enterprise)

## Documentazione

- [Architettura del sistema](docs/architecture.md)
- [Guida agli agenti](docs/agent_guide.md)
- [Metodologia Damodaran](docs/methodology.md)
- [Fonti dati](docs/data_sources.md)
- [Walkthrough demo](docs/demo_walkthrough.md)
- [Valutazione progetto](docs/project_evaluation.md)

## Formule chiave (Damodaran)

```text
FCFF  = EBIT(1-t) + Deprezzamento - CapEx - Delta WC
CAPM  = Rf + Beta * ERP + CRP
WACC  = (E/V) * Re + (D/V) * Rd * (1-t)
TV    = FCF * (1+g) / (r-g)
BS    = V * N(d1) - K * e^(-rT) * N(d2)
```

## Licenza

MIT
