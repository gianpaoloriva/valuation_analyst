# Skill: Rating & Valuation Pipeline — Analisi End-to-End

Pipeline completa di valutazione PMI e stima credit risk forward-looking:
BMS settoriale → DCF con TV coerente → Analisi differenziale → Agentic Credit
Risk Monte Carlo → Rating implicito. Basata su tre paper accademici integrati.

## Vincoli Critici

- I tre tool (BMS, DCF, Agentic Credit Risk) condividono la **stessa definizione
  di cash flow**: capital cash flow (Ruback 2002). Non mescolare con FCFF post-tasse.
- Il **pre-tax WACC** e' usato dall'Agentic Credit Risk e dal DCF con capital
  cash flow. L'after-tax WACC e' usato dal DCF classico con FCFF.
- Il campione BMS e' anche il campione per i parametri Weibull dell'Agentic Credit
  Risk. Mantenere coerenza tra i due.
- La coerenza del TV (paper n. 66) e' **prerequisito** per la robustezza della
  stima di PD (paper RAPD).
- I dati devono rispettare lo schema in `data/rating_valuation/schema.md`.

## Paper di Riferimento

| # | Paper | Autori | Tool |
|---|-------|--------|------|
| 1 | Bilancio Medio Standardizzato | Scarano/Brughera, AIAF n.65 (2008) | BMS Builder |
| 2 | Terminal Value coerente | Scarano/Di Napoli, AIAF n.66 (2008) | DCF 2/3 stadi |
| 3 | Agentic Credit Risk (RAPD) | Montesi/Papiro (2014) | Agentic Credit Risk Simulator |

Quadro comune: `docs/rating_valuation/overview.md`

## Workflow Completo

### Step 1: Validazione dataset

Invocare skill `data-curator` (agente) o verificare manualmente:

```python
from rating_valuation.common.data_loader import load_all
from rating_valuation.common.invariants import check_invariants

bundle = load_all()
violations = check_invariants(bundle.companies)
```

Verificare:
- Schema compliant (colonne, tipi, unita')
- Invarianti bilancio soddisfatti
- Target identificato (`is_target=1`)
- Peer sufficienti (>= 20) nel settore

**GATE**: "Dataset validato: X aziende, Y peer nel settore Z, anno W.
Invarianti: [OK/N violazioni]. Procedo con BMS?"

### Step 2: BMS settoriale

Invocare skill `bms-builder`:

```python
from rating_valuation.bms import BMSBuilder
from rating_valuation.common.data_loader import peer_sample, target_row

peers = peer_sample(bundle.companies, sub_industry, fiscal_year=year)
bms = BMSBuilder(peers).build()
target = target_row(bundle.companies, fiscal_year=year).iloc[0]
```

**GATE**: "BMS costruito: N peer, margine EBITDA XX%, EBIT XX%, leva D/TA XX%.
Campione [rappresentativo/sotto soglia]. Procedo con analisi differenziale?"

### Step 3: Analisi differenziale

Invocare skill `differential-analysis`:

```python
from rating_valuation.differential import DifferentialAnalyzer

diff = DifferentialAnalyzer(bms).analyze(target)
print(diff.summary_line())
```

**GATE**: "Target vs BMS: X/Y indicatori favorevoli. Principali delta:
margine +X p.p., leva -X p.p. Procedo con DCF?"

### Step 4: DCF con Terminal Value coerente

Invocare skill `dcf-tv-coherence`:

```python
from rating_valuation.common.financial import WACCInputs, wacc_after_tax
from rating_valuation.dcf import value_two_stage_coherent, check_coherence

wacc = wacc_after_tax(wacc_inputs)
dcf = value_two_stage_coherent(
    fcff_explicit=fcff_list,
    nopat_t_plus_1=nopat_terminal,
    wacc=wacc, terminal_growth=g,
    roic_new_investments=roic_ni,
    net_debt_today=net_debt,
)
report = check_coherence(...)
```

**GATE**: "EV = EUR X M, Equity = EUR X M. TV peso XX%. Coerenza: [PASS/WARNING/ERROR].
Procedo con Agentic Credit Risk?"

### Step 5: Agentic Credit Risk Monte Carlo

Invocare skill `agentic-credit-risk`:

```python
from rating_valuation.agentic_credit_risk import AgenticCreditRiskSimulator

sim = AgenticCreditRiskSimulator.from_company(
    target, bundle.sectors, bundle.macro,
    n_trials=20_000, n_years=3,
)
result = sim.run(seed=42)
```

**GATE**: "PD cumulata 3y = X.XX%. Rating implicito: [rating].
EL = EUR X M, UL 95% = EUR X M. Procedo con il report?"

### Step 6: Rating e sintesi

Invocare skill `rating-mapper`:

```python
from rating_valuation.rating import RatingLookup
lookup = RatingLookup.from_csv()
bracket = lookup.rating_of_pd_interpolated(pd_cumulated)
```

### Step 7: Report finale

Invocare agente `valuation-reporter` per la narrativa in italiano.

Struttura report:
1. Executive Summary (valore, PD, rating, verdict coerenza)
2. Contesto settoriale (BMS)
3. Posizionamento differenziale target vs IMS
4. Valutazione DCF (EV, Equity, decomposizione TV, 7 check)
5. Profilo di rischio (PD, LGD, EL, UL, driver)
6. Giudizio conclusivo (range, affidabilita', sensitivita')

## Esempio End-to-End

```bash
python examples/rating_valuation/02_full_pipeline_riva_meccanica.py
```

Esegue la pipeline completa su Riva Meccanica SpA (target del dataset demo):
BMS → Differential → DCF 2-stage → Agentic Credit Risk 5K trial → Rating.

## Quando Usare Quale Paradigma

| Criterio | Rating & Valuation (questa pipeline) | Damodaran | FSI Excel |
|----------|--------------------------------------|-----------|-----------|
| Target | PMI non quotate, bilancio riclassificato | Quotate, dati di mercato | Quotate italiane |
| Cash flow | Capital cash flow (Ruback) | FCFF/FCFE (Damodaran) | FCFF (IFRS) |
| WACC | Pre-tax (con CCF) o after-tax (con FCFF) | After-tax | After-tax |
| TV | Formula coerente (g = ROIC*h) | Gordon growth | Gordon growth |
| Credit risk | Agentic Credit Risk Monte Carlo (PD/LGD) | Non incluso | Non incluso |
| Approccio settoriale | BMS + differenziale | Comparabili di mercato | Comps quotati |
| Output | Python + report markdown | Python + report markdown/PDF | Excel + PowerPoint |
| Fonte dati | CSV normalizzati (AIDA/BvD) | Massive.com + Damodaran NYU | CapIQ/FactSet |

## Errori Comuni

| Errore | Gravita' | Soluzione |
|--------|----------|-----------|
| Mescolare pre-tax e after-tax WACC nella stessa pipeline | CRITICO | CCF → pre-tax; FCFF → after-tax. Scegliere uno |
| Usare BMS di un settore per l'ACR di un altro | CRITICO | Stesso gics_sub_industry ovunque |
| TV incoerente come input per ACR | ALTO | Verificare coerenza (7 check) prima |
| Saltare la validazione dati | ALTO | Gli invarianti catturano errori di riclassificazione |
| Non documentare le assunzioni | MEDIO | Ogni gate chiede conferma — usarli |
