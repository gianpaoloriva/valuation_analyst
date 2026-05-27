# Skill: Backtest Comparator — Confronto Modelli Credit Risk

Confronto tra modelli di credit risk (Agentic Credit Risk vs Altman Z-score
vs Merton/KMV vs CDS-implied PD vs rating S&P) su campioni di imprese
defaulted e performing, con metriche AUROC/Gini/KS.

## Vincoli Critici

- Il confronto richiede **PD sullo stesso orizzonte** per tutti i modelli.
  Tipicamente 1 anno. Convertire prima di confrontare.
- Il campione deve includere sia **defaulted** che **performing** per calcolare
  il potere discriminante.
- I modelli hanno output diversi (Z-score, PD, rating, CDS spread):
  normalizzare tutto a PD 1y prima del confronto.
- Gini = 2*AUROC - 1. AUROC > 0.5 = meglio del caso. AUROC > 0.7 = buono.

## Metriche Standard

| Metrica | Formula | Interpretazione |
|---------|---------|-----------------|
| AUROC | Area Under ROC | > 0.7 buono, > 0.9 eccellente |
| Gini | 2*AUROC - 1 | > 0.4 buono, > 0.8 eccellente |
| KS | max distanza CDF defaulted vs performing | > 0.3 buono |

## Modelli Supportati

| Modello | Tipo | Input PD | Forza | Debolezza |
|---------|------|----------|-------|-----------|
| Agentic Credit Risk | Strutturale, stocastico | Monte Carlo fondamentali | Early warning, PMI private | Assunzioni forecast |
| Altman Z-score | Scoring ratio-based | Z → rating → PD | Semplice, stabile | Backward-looking |
| Moody's KMV | Strutturale, Merton | Market cap + vol | Segnale rapido | Solo quotate, market-dep |
| S&P rating | Expert judgment | Master scale | Consolidato | Lagging, cliff effect |
| CDS implied | Market pricing | 1-exp(-CDS/LGD) | Real-time | Illiquido per PMI |

## Workflow

### Step 1: Preparazione campione

Il campione deve contenere:
- Imprese **defaulted**: con data di default nota
- Imprese **performing**: mai defaulted nell'orizzonte

Per ciascuna, servono i bilanci a 1, 2 e 3 anni prima della data di riferimento.

```python
from rating_valuation.backtest.comparator import run_backtest
```

**CHECKPOINT**: Mostrare composizione campione (n_defaulted, n_performing,
settori, anni coperti).

### Step 2: Calcolo PD per modello

Per ogni impresa e ogni orizzonte:

**Agentic Credit Risk:**
```python
from rating_valuation.agentic_credit_risk import AgenticCreditRiskSimulator
sim = AgenticCreditRiskSimulator.from_company(row, sectors, macro)
result = sim.run(seed=42)
pd_1y = result.metrics.cumulative_pd[0]
```

**Altman Z-score:**
```python
from rating_valuation.rating.mapper import altman_z_to_rating, RatingLookup
z = altman_z(...)
rating = altman_z_to_rating(z)
lookup = RatingLookup.from_csv()
pd_1y = lookup.pd_of_rating(rating)
```

**CDS implied:**
```python
from rating_valuation.rating.mapper import cds_to_pd
pd_1y = cds_to_pd(cds_bps=spread, lgd=0.60)
```

**CHECKPOINT**: Mostrare tabella riepilogativa con PD per modello per le
prime 5 imprese del campione, come sanity check.

### Step 3: Calcolo metriche discriminanti

```python
result = run_backtest(defaulted_pds, performing_pds)
print(result.metrics_table())
```

Calcola per ogni modello:
- AUROC, Gini, KS sul campione completo
- PD mediana 1/2/3 anni prima del default (solo defaulted)
- PD mediana sulle performing (check bias upward)

**CHECKPOINT**: Mostrare tabella comparativa modelli x metriche.

### Step 4: Interpretazione

Risultati attesi dal paper Montesi/Papiro (Section 5, 46 defaulted + 100 performing):
- Agentic Credit Risk: PD mediana > 60% un anno prima del default
- Altman Z: secondo per early detection
- S&P: PD mediana solo 2.6% un anno prima (lagging)
- KMV/DRSK: PD bassa fino a quando il mercato non realizza
- Sulle performing: Agentic Credit Risk non ha bias upward (mediana ~0.06%)

Se i risultati divergono significativamente, investigare l'implementazione.

**CHECKPOINT**: Confronto con benchmark del paper. Flag se anomalie.

## Errori Comuni

| Errore | Gravita' | Soluzione |
|--------|----------|-----------|
| Confrontare PD su orizzonti diversi | CRITICO | Normalizzare tutto a 1y |
| Campione solo defaulted (no performing) | CRITICO | Serve il campione negativo per AUROC/Gini |
| Look-ahead bias (usare dati post-default) | CRITICO | Usare solo bilanci ante-default |
| Campione troppo piccolo (< 30 defaulted) | ALTO | Metriche instabili |
| Non convertire Z-score → PD prima del confronto | ALTO | Z e PD non sono confrontabili direttamente |
| Ignorare il time horizon dei modelli | MEDIO | Specificare sempre: 1y, 2y, 3y prima del default |

## Risultati Empirici di Riferimento (Paper RAPD)

| Metrica | Agentic Credit Risk | Altman Z | S&P | KMV |
|---------|----------|----------|-----|-----|
| PD mediana 1y pre-default | > 60% | ~20-30% | ~2.6% | ~5-10% |
| PD mediana performing | ~0.06% | ~0.1-0.3% | N/A | ~0.3% |
| Early warning | 1-3 anni | 1-2 anni | Lagging | Tardo |
| Applicabile PMI private | Si' | Si' | Si' (se rated) | No |

Recovery rate medio campione: 37.96% (mediana 33.65%).
Correlazione PD-Recovery: -0.704 (Pearson).

Riferimento: `docs/rating_valuation/RAPD.pdf`, Section 5
