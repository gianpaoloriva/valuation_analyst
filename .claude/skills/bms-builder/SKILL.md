# Skill: Bilancio Medio Standardizzato (BMS)

Costruzione del Bilancio Medio Standardizzato per valutazione PMI con approccio
settoriale, secondo la metodologia Scarano/Brughera (Rivista AIAF n. 65, 2008).

## Vincoli Critici

- Il BMS **NON e' la somma line-by-line** dei bilanci peer. E' la media delle
  quote normalizzate (CE su fatturato, SP su totale attivo) moltiplicata per
  la media delle grandezze assolute. La somma sarebbe dominata dall'impresa
  piu' grande — il BMS elimina l'effetto dimensionale.
- Campione minimo raccomandato: **20 imprese** (paper). Sotto soglia il builder
  emette `below_min_sample=True` ma non blocca — documentare la limitazione.
- **Un solo anno fiscale** per BMS. Per analisi multi-anno usare
  `build_bms_timeseries()`.
- Le righe con `is_target=1` vengono escluse automaticamente dal campione.
- Tutti i peer devono soddisfare i 5 invarianti di bilancio riclassificato
  (`common/invariants.py`).

## Formule Fondamentali

### Conto Economico (voce i-esima)

```
quota_i = (1/n) * SUM_j ( ce_{i,j} / Fatturato_j )
CE_BMS_i = quota_i * Fatturato_medio
```

dove `Fatturato_medio = (1/n) * SUM_j Fatturato_j`

### Stato Patrimoniale (voce i-esima)

```
quota_i = (1/n) * SUM_j ( sp_{i,j} / TotaleAttivo_j )
SP_BMS_i = quota_i * TotaleAttivo_medio
```

dove `TotaleAttivo_medio = (1/n) * SUM_j TotaleAttivo_j`

Ogni impresa contribuisce con **peso 1/n** indipendentemente dalla dimensione.

## Workflow

### Step 1: Selezione e validazione campione

- Filtrare `companies.csv` per `gics_sub_industry` e `fiscal_year`
- Escludere target (`is_target=1`)
- Verificare invarianti di bilancio su ogni peer
- Se outlier dimensionali evidenti, considerare `outlier_sigma` per escluderli

```python
from rating_valuation.common.data_loader import load_companies, peer_sample
from rating_valuation.common.invariants import check_invariants

companies = load_companies()
peers = peer_sample(companies, "Industrial Machinery", fiscal_year=2024)
violations = check_invariants(peers)
```

**CHECKPOINT**: Mostrare all'utente: numero peer, settore, anno, eventuali
violazioni di invarianti. Chiedere conferma prima di costruire il BMS.

### Step 2: Costruzione BMS

```python
from rating_valuation.bms import BMSBuilder

result = BMSBuilder(peers, min_sample_size=20).build()
```

Output `BMSResult` contiene:
- `income_statement`: valori assoluti CE del BMS (EUR M)
- `income_statement_shares`: quote normalizzate (percentuali)
- `balance_sheet`: valori assoluti SP del BMS (EUR M)
- `balance_sheet_shares`: quote normalizzate (percentuali)
- `average_revenues`, `average_total_assets`: medie campione
- `n_companies`, `below_min_sample`
- `income_statement_shares_median`, `_p25`, `_p75`: statistiche robuste

**CHECKPOINT**: Mostrare tabella CE e SP del BMS con quote percentuali.
Evidenziare margine EBITDA, EBIT, NOPAT e struttura patrimoniale.

### Step 3: Confronto BMS vs Somma (opzionale)

Il `BMSResult` include anche il bilancio "somma naive" per confronto.
La differenza tra BMS e somma quantifica l'effetto dimensionale.

**CHECKPOINT**: Mostrare la deviazione BMS vs somma sui KPI principali.

### Step 4: Serie storica (opzionale)

```python
from rating_valuation.bms.builder import build_bms_timeseries

timeseries = build_bms_timeseries(companies, "Industrial Machinery", min_sample_size=15)
for year, r in sorted(timeseries.items()):
    print(f"{year}: EBITDA margin = {r.income_statement_shares['ebitda']:.1%}")
```

**CHECKPOINT**: Mostrare trend dei KPI settoriali attraverso gli anni.
Segnalare variazioni >20% anno su anno come possibili anomalie.

### Step 5: Output e passaggio downstream

Il BMS e' input per:
- `DifferentialAnalyzer` (confronto target vs IMS)
- Parametrizzazione Weibull dell'Agentic Credit Risk (centroidi settoriali)
- DCF dell'Impresa Media Standard

## Errori Comuni

| Errore | Gravita' | Soluzione |
|--------|----------|-----------|
| Usare la somma line-by-line invece del BMS | CRITICO | Il BMS normalizza — la somma no. Sono due numeri diversi |
| Campione < 20 senza documentarlo | ALTO | Il builder non blocca ma setta `below_min_sample=True` |
| Mescolare anni fiscali diversi | ALTO | Un BMS per anno. Usare `fiscal_year=` nel filtro |
| Non escludere il target dal campione | MEDIO | `peer_sample(exclude_target=True)` e' il default |
| Peer con settori GICS diversi | MEDIO | Filtrare per `gics_sub_industry`, non `gics_sector` |
| Ignorare outlier dimensionali | MEDIO | Un peer 10x distorce le quote medie |
| Variazioni YoY > 20% non investigate | BASSO | Possibile errore di riclassificazione nel peer |

## Parametri per Paese

| Parametro | Italia | US |
|-----------|--------|-----|
| Fonte bilanci | AIDA / Bureau van Dijk | Compustat / SEC filings |
| Riclassificazione | IV Direttiva → schema BMS | US GAAP → schema BMS |
| Campione tipico PMI | 20-50 per sotto-settore | 50-200 per sotto-settore |
| Nota | Piu' PMI non quotate disponibili via AIDA | Prevalenza quotate su Compustat |

## Metodologia (Scarano/Brughera 2008)

L'approccio **rovescia la prospettiva**: invece di valutare direttamente la PMI
(bilancio volatile, poco rappresentativo), si costruisce prima un'**Impresa Media
Standard (IMS)** rappresentativa del settore, la si valuta con DCF, e poi si
valuta la PMI obiettivo **per differenziale** rispetto all'IMS.

Vantaggi:
1. La media settoriale e' piu' stabile del singolo bilancio
2. Le previsioni prospettiche sull'IMS sono piu' affidabili
3. L'analisi differenziale isola le peculiarita' della singola impresa
4. Il BMS storico rivela trend e punti di flesso del settore

Riferimento: `docs/rating_valuation/2008 n.-65 Bilancio Medio Standard.pdf`
