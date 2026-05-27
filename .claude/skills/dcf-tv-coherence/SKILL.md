# Skill: DCF con Terminal Value Coerente

Valutazione DCF a 2 e 3 stadi con check di coerenza del Terminal Value,
secondo la metodologia Scarano/Di Napoli (Rivista AIAF n. 66, 2008).

## Vincoli Critici

- Il TV pesa in media il **64% dell'Enterprise Value** (studio Univ. Bergamo
  su ~800 report). Il **10% dei report ha un TV incoerente**. Questa skill
  impone i check per eliminare il problema alla radice.
- `g` (crescita lungo periodo) **non puo' superare la crescita del PIL
  nominale** del paese (Eurozona ~1.5-3%, US ~3-4%).
- Il vincolo micro di coerenza e': `g = ROIC_NI * h_T` dove `h_T` e' la
  quota di NOPAT reinvestita. Se `h_T > 1` la crescita e' insostenibile.
- Quando `ROIC_NI = WACC` (steady state), il TV collassa a `NOPAT/WACC` —
  la crescita non genera valore aggiuntivo.
- Il cash flow usato e' il **capital cash flow** (Ruback 2002):
  `OCF = NOPAT - DELTA_NIC + tau*INT`. Il tax shield e' nel flusso,
  quindi usare **pre-tax WACC** con capital cash flow (Agentic Credit Risk),
  oppure FCFF con after-tax WACC (DCF classico). MAI mescolare.

## Formule Fondamentali

### DCF 2 stadi

```
EV = SUM_{t=1..T} FCFF_t / (1+wacc)^t  +  TV / (1+wacc)^T
```

### Terminal Value con reinvestimento esplicito (formula coerente)

```
TV = NOPAT_{T+1} * (1 - g/ROIC_NI) / (wacc - g)
```

### Caso speciale: ROIC_NI = WACC (steady state)

```
TV = NOPAT_{T+1} / wacc
```

### DCF 3 stadi — convergenza geometrica

```
Stadio 1: previsione esplicita (5-8 anni), FCFF dettagliati
Stadio 2: convergenza ROIC_marginale → WACC
           tasso_decay = (WACC / ROIC_residuo)^(1/n) - 1
Stadio 3: steady state con ROIC_NI = WACC → TV = NOPAT/WACC
```

### Vincolo di coerenza

```
g = ROIC_NI * h_T
h_T = g / ROIC_NI = DELTA_CI / NOPAT
h_T in [0, 1]   (altrimenti crescita insostenibile)
```

## Workflow

### Step 1: Raccolta parametri

- Leggere `data/rating_valuation/macro.csv` per il paese target:
  `risk_free_rate_10y`, `market_risk_premium`, `gdp_nominal_growth_5y_avg`
- Leggere `data/rating_valuation/sectors.csv` per `beta_unlevered`
- Calcolare WACC (after-tax per FCFF, pre-tax per capital cash flow)

```python
from rating_valuation.common.financial import WACCInputs, wacc_after_tax
from rating_valuation.common.data_loader import load_all

bundle = load_all()
macro = bundle.macro[(bundle.macro["country"] == "IT") & (bundle.macro["year"] == 2024)].iloc[0]
```

**CHECKPOINT**: Mostrare WACC calcolato con componenti (Rf, beta, MRP, Kd, pesi).
Confrontare con il `gdp_nominal_growth_5y_avg` per verificare che `g < WACC`.

### Step 2: Proiezione cash flow espliciti

- Proiettare NOPAT, CapEx, NWC per l'orizzonte esplicito (5-8 anni)
- Calcolare FCFF = NOPAT - DELTA_NIC (o dal BMS se analisi settoriale)

**CHECKPOINT**: Mostrare tabella proiezione anno per anno. Verificare coerenza
tra crescita dichiarata e reinvestimento implicito.

### Step 3: Scelta del modello (2 o 3 stadi)

**Usare 2 stadi** quando:
- Il forecast esplicito arriva gia' al ROIC ≈ WACC (settori maturi)
- La crescita e' bassa e stabile

**Usare 3 stadi** quando:
- Il ROIC marginale alla fine del forecast e' ancora >> WACC
- Senza convergenza il TV sarebbe troppo alto
- Settori con extra-rendimenti temporanei (tech, pharma, luxury)

```python
from rating_valuation.dcf import value_two_stage_coherent, value_three_stage

# 2 stadi
result = value_two_stage_coherent(
    fcff_explicit=fcff_list,
    nopat_t_plus_1=nopat_terminal,
    wacc=wacc,
    terminal_growth=g,
    roic_new_investments=roic_ni,
    net_debt_today=net_debt,
)

# 3 stadi
from rating_valuation.dcf.three_stage import ThreeStageInputs, value_three_stage
inputs = ThreeStageInputs(
    nopat_explicit=[...],
    nic_explicit=[...],
    wacc=wacc,
    roic_initial=roic_0,
    convergence_years=5,
    terminal_growth=g,
    net_debt=net_debt,
    gdp_nominal_5y_avg=gdp_growth,
)
result = value_three_stage(inputs)
```

**CHECKPOINT**: Mostrare EV, Equity Value, peso TV su EV, decomposizione
valore esplicito vs TV scontato.

### Step 4: Check di coerenza (7 controlli)

Il `coherence_report` e' integrato automaticamente nel risultato del 3 stadi.
Per il 2 stadi, invocarlo esplicitamente:

```python
from rating_valuation.dcf import check_coherence, Severity

report = check_coherence(
    wacc=wacc, growth=g, roic_new_investments=roic_ni,
    implied_reinvestment=g/roic_ni,
    tv_weight=result.tv_weight,
    roic_marginal_final=roic_ni,
    nopat_t_plus_1=nopat_terminal,
    gdp_nominal_5y_avg=gdp_growth,
    used_coherent_formula=True,
    inflation=inflation,
)
```

I 7 check:

| Check | Cosa verifica | Gravita' se fallisce |
|-------|---------------|---------------------|
| C1 | `g <= g_PIL` (cap macro) | ERROR |
| C2 | `g = ROIC_NI * h_T` (identita' reinvestimento) | ERROR |
| C3 | Formula coerente usata (non Gordon naive) | WARNING |
| C4 | `TV_weight <= 80%` | WARNING |
| C5 | `ROIC_marginale → WACC` (convergenza) | WARNING |
| C6 | Segni e bounds (`wacc > g > -inflation`, ROIC > 0) | ERROR |
| C7 | `h_T in [0, 1]` (reinvestimento ragionevole) | ERROR |

Verdetti: `PASS` (tutto ok), `WARNING` (usare con cautela), `ERROR` (non usare).

**CHECKPOINT**: Mostrare tabella 7 check con esito. Se ERROR, spiegare il fix.

### Step 5: Validazione e output

- Confronto EV/Equity con valutazione Damodaran (se disponibile)
- Confronto con multipli di mercato (se disponibili)

## Errori Comuni

| Errore | Gravita' | Soluzione |
|--------|----------|-----------|
| Usare Gordon naive senza check coerenza | CRITICO | Usare formula con `(1 - g/ROIC_NI)` |
| g > crescita PIL nominale | CRITICO | Cap: 1.5-3% Eurozona, 3-4% US |
| h_T > 1 (reinvestimento > NOPAT) | CRITICO | Ridurre g o aumentare ROIC_NI |
| Mescolare capital cash flow con after-tax WACC | CRITICO | CCF → pre-tax WACC; FCFF → after-tax WACC |
| TV > 80% di EV senza giustificazione | ALTO | Allungare forecast o usare 3 stadi |
| ROIC_marginale >> WACC alla fine del forecast | ALTO | Aggiungere stadio di convergenza |
| Non verificare `g = ROIC * h` | ALTO | Check C2 lo cattura automaticamente |
| Dimenticare net_debt nel ponte EV→Equity | MEDIO | `Equity = EV - Net_Debt` |

## Parametri per Paese

| Parametro | Italia | US |
|-----------|--------|-----|
| Risk-free | BTP 10Y | US Treasury 10Y |
| MRP | 5-7% (include CRP) | 5-6% |
| Tax rate | 27.9% (IRES 24% + IRAP 3.9%) | 25% federale |
| g cap (PIL nominale) | 1.5-3% | 3-4% |
| Fonte macro | `macro.csv` country=IT | `macro.csv` country=US |
| WACC tipico PMI | 8-12% | 8-11% |

## Metodologia (Scarano/Di Napoli 2008)

Studio Universita' di Bergamo su ~800 report di valutazione di quotate europee:
- Il TV pesa in media il **64%** dell'Enterprise Value
- Il **10%** dei report ha un TV incoerente con la logica DCF sottostante
- Gli errori derivano da `g`, `h_T` e `ROIC_NI` non compatibili tra loro

Il modello a **3 stadi** elimina il problema alla radice:
1. **Stadio 1** — previsione esplicita (5-8 anni): NOPAT, CapEx, NWC dettagliati
2. **Stadio 2** — convergenza: `ROIC_marginale` decresce geometricamente verso WACC
3. **Stadio 3** — steady state: `ROIC_NI = WACC` → `TV = NOPAT/WACC`

Il tasso di convergenza geometrica:
```
decay = (WACC / ROIC_residuo)^(1/n) - 1
```

Riferimento: `docs/rating_valuation/2008 n.-66 Calcolo del Terminal Value.pdf`
