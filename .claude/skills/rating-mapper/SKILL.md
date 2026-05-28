# Skill: Rating Mapper — PD, Rating, CDS, Altman Z

Conversioni tra PD, rating S&P, CDS spread e Altman Z-score usando la
master scale del paper Montesi/Papiro (2014) con interpolazione log-lineare.

## Vincoli Critici

- La master scale ha **22 classi** (AAA → D) con PD esponenzialmente crescenti.
- L'interpolazione e' **log-lineare** — non quantizza il rating su classi
  discrete. Output: `"BBB+/BBB (0.42)"` (piu' preciso di un "BBB" secco).
- La conversione CDS → PD usa `PD = 1 - exp(-CDS/LGD)` con **LGD = 60%**
  (recovery 40%) come default.
- L'Altman Z-score ha varianti diverse per manufacturing e non-manufacturing.
  Per PMI italiane usare `altman_z_double_prime_non_manufacturing()`.
- La PD della master scale e' a **1 anno**. Per confronti con PD cumulate
  multi-anno, convertire o specificare l'orizzonte.

## Master Scale Rating ↔ PD 1y

| Rating | PD 1y | Rating | PD 1y |
|--------|-------|--------|-------|
| AAA | 0.000% | BB+ | 0.550% |
| AA+ | 0.010% | BB | 0.800% |
| AA | 0.020% | BB- | 1.300% |
| AA- | 0.040% | B+ | 2.600% |
| A+ | 0.070% | B | 5.880% |
| A | 0.090% | B- | 9.120% |
| A- | 0.120% | CCC+ | 15.805% |
| BBB+ | 0.160% | CCC | 27.390% |
| BBB | 0.230% | CCC- | 37.861% |
| BBB- | 0.380% | CC | 52.335% |
| | | C | 72.343% |
| | | D | 100.000% |

Fonte: `data/rating_valuation/rating_master_scale.csv`

## Workflow

### Step 1: Inizializzazione

```python
from rating_valuation.rating import RatingLookup

lookup = RatingLookup.from_csv()  # carica master scale dal CSV
```

### Step 2: Conversioni

**PD → Rating interpolato:**
```python
rating, lower, upper, fraction = lookup.rating_of_pd_interpolated(pd_value)
# Es: ("BBB+", "BBB", 0.42) → tra BBB+ e BBB, 42% verso BBB
```

**Rating → PD:**
```python
pd = lookup.pd_of_rating("BBB+")  # 0.0016
```

**CDS spread → PD:**
```python
from rating_valuation.rating.mapper import cds_to_pd
pd = cds_to_pd(cds_bps=150, lgd=0.60)  # PD = 1 - exp(-CDS/LGD)
```

**Altman Z-score → Rating:**
```python
from rating_valuation.rating.mapper import altman_z_to_rating
rating = altman_z_to_rating(z_score=2.3)

# Per PMI non-manufacturing italiane:
from rating_valuation.rating.mapper import altman_z_double_prime_non_manufacturing
z = altman_z_double_prime_non_manufacturing(
    working_capital=wc, retained_earnings=re,
    ebit=ebit, book_equity=eq, total_assets=ta, total_liabilities=tl
)
```

**CHECKPOINT**: Mostrare il rating risultante con posizionamento sulla scala.
Se PD di input e' da Agentic Credit Risk, specificare l'orizzonte.

### Step 3: Interpretazione

| Classe | PD 1y | Interpretazione | Azione tipica |
|--------|-------|-----------------|---------------|
| AAA-A | < 0.12% | Investment grade alto | Green light |
| BBB+ - BBB- | 0.16-0.38% | Investment grade basso | Monitoraggio |
| BB+ - BB- | 0.55-1.30% | Speculative grade | Attenzione |
| B+ - B- | 2.60-9.12% | High yield | Rischio elevato |
| CCC+ e sotto | > 15.8% | Distress | Intervento immediato |

## Errori Comuni

| Errore | Gravita' | Soluzione |
|--------|----------|-----------|
| Confrontare PD 1y (master scale) con PD 3y cumulata | CRITICO | Specificare sempre l'orizzonte |
| Usare LGD = 100% nella conversione CDS | ALTO | Default paper: LGD = 60% (recovery 40%) |
| Usare Altman Z originale per non-manufacturing | ALTO | Usare Z'' (double prime) per servizi e PMI italiane |
| Quantizzare il rating su classi discrete | MEDIO | L'interpolazione log-lineare e' piu' informativa |
| Interpretare il rating come previsione | BASSO | E' un posizionamento sulla scala, non una previsione |

## Altman Z-Score Buckets

| Z-score | Rating equivalente |
|---------|-------------------|
| > 8.15 | AAA |
| 7.60 - 8.15 | AA+ |
| 7.30 - 7.60 | AA |
| 7.00 - 7.30 | AA- |
| 6.85 - 7.00 | A+ |
| 6.65 - 6.85 | A |
| 6.40 - 6.65 | A- |
| 6.25 - 6.40 | BBB+ |
| 5.85 - 6.25 | BBB |
| 5.65 - 5.85 | BBB- |
| ... | ... |
| < 1.75 | D |

Fonte: `rating/mapper.py`, ALTMAN_Z_BUCKETS

## Parametri per Paese

| Parametro | Italia | US |
|-----------|--------|-----|
| Variante Altman | Z'' (non-manufacturing, PMI) | Z originale (manufacturing) |
| Recovery rate medio | 35-40% (procedure lunghe) | 40-45% |
| LGD default | 60% | 60% |
| Master scale | Stessa (S&P globale) | Stessa |

Riferimento: `docs/rating_valuation/RAPD.pdf`, Appendice A (Master Scale)
