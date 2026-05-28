# Skill: Agentic Credit Risk — Simulazione Stocastica PD

Stima forward-looking della probabilita' di default (PD), LGD, Expected Loss
e Unexpected Loss via simulazione Monte Carlo sui fondamentali aziendali,
secondo il modello Montesi/Papiro (2014).

## Vincoli Critici

- Il cash flow usato e' il **capital cash flow** (Ruback 2002):
  `OCF = NOPAT - DELTA_NIC + tau*INT`. Il tax shield e' gia' nel flusso.
- Il WACC deve essere **pre-tax**: `w_e*k_e + w_d*r_d` senza `(1-t)` sul
  debito. Applicare after-tax WACC al capital cash flow significherebbe
  contare il tax shield due volte.
- Il debito e' **endogeno e ricorsivo** (eq. [7] del paper): non e' un input
  fisso ma viene risolto in forma chiusa per ogni scenario imponendo
  l'equilibrio finanziario.
- La condizione di default e': `EV_t < D_t - CASH_t`.
- Il Terminal Value include l'Interest Tax Shield: `TV = NOPAT_T/k + tau*INT_T`.
- Minimo **20.000 trial** Monte Carlo (paper). Per debug/test: 5.000.
- Le distribuzioni sono **Weibull** (non normali): i ricavi hanno asimmetria
  positiva, i costi sono piu' simmetrici ma comunque asimmetrici.

## Equazioni Fondamentali

```
[1]  NOPAT_t = REV_{t-1} * (1 + g_t) * m_t * (1 - tau)
[2]  NIC_t   = (f_t + w_t) * REV_{t-1} * (1 + g_t)
[3]  OCF_t   = NOPAT_t - DELTA_NIC_t + tau * INT_t        (capital cash flow)
[4]  INT_t   = r_d * (D_{t-1} + D_t) / 2
[7]  D_t     = max(0, (2*(NOPAT - DELTA_NIC + DELTA_CAP - 2*D_{t-1}) / (r_d*(1-tau) - 2)) - D_{t-1})
[12] EV_t    = SUM OCF / (1+k)^t  +  TV      (k = pre-tax WACC)
[13] Default iff EV_t < D_t - CASH_t
```

### Tre tipi di PD

| Tipo | Formula | Uso |
|------|---------|-----|
| Yearly Default Frequency | P(EV_t < D_t) | Fragilita' nel singolo anno |
| Marginal PD | P(default in t \| sopravvissuto a t-1) | Pricing del debito |
| Cumulative PD | P(default entro t) = 1 - PROD(1 - marg_i) | Comitato crediti, Basel IRB |

## Workflow

### Step 1: Preparazione dati

```python
from rating_valuation.common.data_loader import load_all, target_row
bundle = load_all()
target = target_row(bundle.companies, fiscal_year=2024).iloc[0]
```

Verificare che il target soddisfi gli invarianti di bilancio.
Leggere `sectors.csv` per i parametri Weibull e le correlazioni.
Leggere `macro.csv` per Rf, MRP, crescita PIL.

**CHECKPOINT**: Mostrare i dati del target (NOPAT, NIC, debito, cash, D/E)
e i parametri Weibull del settore. Chiedere conferma.

### Step 2: Costruzione simulatore

```python
from rating_valuation.agentic_credit_risk import AgenticCreditRiskSimulator

sim = AgenticCreditRiskSimulator.from_company(
    target, bundle.sectors, bundle.macro,
    n_trials=20_000, n_years=3,
)
```

Il factory `from_company()` costruisce automaticamente:
- `InitialState` con pre-tax WACC
- `StochasticParameters` con shape Weibull, autocorrelazioni e cross-correlazioni
  dal settore
- Flip segno su correlazioni (`OpCost/Sales → EBITDA_margin`)

**CHECKPOINT**: Mostrare WACC pre-tax, NIC iniziale, debito iniziale,
parametri Weibull. Verificare che siano ragionevoli per il settore.

### Step 3: Esecuzione simulazione

```python
result = sim.run(seed=42)
```

La simulazione produce matrici diagnostiche per trial:
`nopat`, `ocf`, `debt`, `cash`, `ev`, `interest` — disponibili per audit.

**CHECKPOINT**: Mostrare tabella PD per anno (yearly freq, marginal, cumulative).
Mostrare numero scenari di default su totale trial.

### Step 4: Metriche di credito

```python
m = result.metrics
# m.cumulative_pd, m.lgd_mean, m.lgd_median, m.recovery_rate_mean
# m.expected_loss, m.unexpected_loss_95, m.unexpected_loss_99
```

**CHECKPOINT**: Mostrare:
- PD cumulata 3y e rating implicito
- LGD media e mediana
- Recovery rate medio
- Expected Loss e Unexpected Loss (95%, 99%)

### Step 5: Rating implicito

```python
rating = result.implied_rating  # es. "BBB+/BBB (0.42)"
```

Il rating e' **interpolato log-linearmente** sulla master scale (22 classi).
Non quantizzato su classi discrete — il comitato crediti ha un segnale
piu' preciso.

**CHECKPOINT**: Mostrare rating con posizionamento tra classi adiacenti.

### Step 6: Estensioni opt-in (Appendice A)

Tutte retrocompatibili (default neutri = modello ridotto del paper):

| Estensione | Parametro | Default |
|------------|-----------|---------|
| Interessi attivi sul cash | `cash_yield` | 0 |
| Tax rate stocastico | `tax_stochastic` | False |
| Dividendi / payout | `payout_ratio` | 0.0 |
| Debt floor / covenant | `debt_floor` | 0.0 |
| Collateral coverage LGD | `collateral_coverage` | 0.0 |

Per riprodurre esattamente i numeri del paper, lasciare i default.
Attivare uno alla volta e osservare la derivata della PD cumulata.

## Errori Comuni

| Errore | Gravita' | Soluzione |
|--------|----------|-----------|
| Usare after-tax WACC con capital cash flow | CRITICO | Doppio counting tax shield. Usare pre-tax WACC |
| Debito esogeno statico | CRITICO | Il modello richiede debito endogeno (eq. [7]) |
| Distribuzioni normali invece di Weibull | ALTO | Ricavi asimmetrici; Weibull cattura l'asimmetria |
| < 20.000 trial per uso produzione | ALTO | Margine errore PD > 50 bps con pochi trial |
| Ignorare il flip di segno correlazioni | ALTO | Il factory lo fa automaticamente, ma attenzione se si creano parametri manualmente |
| Interpretare P(default) come previsione puntuale | MEDIO | E' frequenza empirica su scenari, non probabilita' bayesiana |
| Non verificare stabilita' al cambio seed | MEDIO | Se rating cambia > 2 notch, aumentare n_trials |
| Omettere ITS nel Terminal Value | MEDIO | TV = NOPAT/k + tau*INT (paper Appendice A) |

## Parametri per Paese

| Parametro | Italia | US |
|-----------|--------|-----|
| Risk-free | BTP 10Y | US Treasury 10Y |
| MRP | 5% (paper default) | 5% (paper default) |
| Tax rate nominale | 27.9% | 25% |
| Tax range stocastico | 70-150% del nominale | 70-150% del nominale |
| Crescita PIL nominale (centro Weibull) | ~3% | ~4-5% |
| Procedure concorsuali | 3-7 anni (piu' lunghe) | 12-18 mesi (Chapter 11) |
| Fonte bilanci PMI | AIDA / Bureau van Dijk | Compustat |

## Differenza vs Modelli Option/Contingent (Merton, KMV)

| Aspetto | Agentic Credit Risk | Merton / KMV |
|---------|----------|-------------|
| EV | Da fondamentali (DCF stocastico) | Da prezzi di mercato + volatilita' |
| Debito | Endogeno, ricorsivo | Esogeno, statico |
| Applicabile a PMI private | Si' | No (richiede market cap) |
| Orizzonte > 1 anno | Si' (multi-anno coerente) | Limitato (<2 anni) |
| Bolle di mercato | Immune | Influenzato |

## Parametri Default (Paper, Appendice A)

| Parametro | Valore | Fonte |
|-----------|--------|-------|
| Trial MC | 20.000 | paper |
| Orizzonte | 3 anni | paper |
| Weibull ricavi shape | 2 | paper |
| Weibull OpCost/Sales shape | 3.5 | paper |
| Weibull NFA/Sales shape | 3.5 | paper |
| Weibull NWC/Sales shape | 3 | paper |
| Autocorr Sales | 0.2 | paper |
| Autocorr OpCost | 0.3 | paper |
| Autocorr NFA | 0.5 | paper |
| Autocorr NWC | 0.4 | paper |
| Corr Sales x OpCost | -0.4 | paper |
| Corr Sales x NFA | +0.2 | paper |
| Corr Sales x NWC | -0.3 | paper |
| Corr NFA x OpCost | -0.2 | paper |

Riferimento: `docs/rating_valuation/RAPD.pdf`
