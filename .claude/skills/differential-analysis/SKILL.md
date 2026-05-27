# Skill: Analisi Differenziale Target vs Impresa Media Standard

Confronto strutturato tra l'impresa target e il Bilancio Medio Standardizzato
(BMS) del settore, con scomposizione del premio/sconto per driver (margine,
crescita, leva, capital intensity).

## Vincoli Critici

- L'analisi differenziale **richiede un BMS gia' costruito** come input.
  Invocare prima la skill `bms-builder`.
- Il confronto e' per anno fiscale singolo. Per analisi multi-anno,
  costruire BMS per piu' anni e confrontare separatamente.
- La somma dei contributi dei 4 driver **non coincide esattamente** con il
  gap totale di equity value (gli effetti interagiscono). Le direzioni
  sono comunque informative.
- Il target deve avere lo stesso `gics_sub_industry` del BMS.

## Driver di Scomposizione

| Driver | KPI | Interpretazione |
|--------|-----|-----------------|
| Margine operativo | EBITDA/Revenues target vs BMS | Efficienza operativa |
| Crescita attesa | CAGR ricavi target vs BMS | Dinamica top-line |
| Leva finanziaria | Debt/Equity target vs BMS | Rischio finanziario |
| Capital intensity | NIC/Revenues target vs BMS | Efficienza del capitale |

## Workflow

### Step 1: Preparazione input

```python
from rating_valuation.bms import BMSBuilder
from rating_valuation.common.data_loader import load_companies, peer_sample, target_row
from rating_valuation.differential import DifferentialAnalyzer

companies = load_companies()
peers = peer_sample(companies, "Industrial Machinery", fiscal_year=2024)
bms = BMSBuilder(peers, min_sample_size=15).build()
target = target_row(companies, fiscal_year=2024).iloc[0]
```

**CHECKPOINT**: Confermare che target e BMS siano dello stesso settore e anno.

### Step 2: Esecuzione analisi

```python
analyzer = DifferentialAnalyzer(bms)
diff = analyzer.analyze(target)
```

Output `DifferentialResult` contiene:
- `comparisons`: lista di confronti (label, target, bms, delta, unit, favorable)
- `summary_line()`: riga sintetica
- `as_dataframe()`: tabella completa
- `favorable_count()`: numero indicatori favorevoli al target

**CHECKPOINT**: Mostrare tabella completa con indicatori, valori target vs BMS,
delta, e flag favorevole/sfavorevole.

### Step 3: Interpretazione

Per ogni driver, spiegare:
- **Direzione**: il target batte o perde contro il settore?
- **Entita'**: quanto e' significativo il delta?
- **Implicazione**: cosa significa per la valutazione?

Esempio: "Riva Meccanica ha margine 17% vs settore 14% (+3 p.p. favorevole):
il premio di valutazione e' giustificato dalla superiore efficienza operativa."

**CHECKPOINT**: Mostrare commento per driver e verdict complessivo:
"X su Y indicatori favorevoli".

### Step 4: Passaggio downstream

I risultati alimentano:
- La narrativa del `valuation-reporter` (sezione 3: posizionamento differenziale)
- La calibrazione del DCF (se il target ha margini superiori al BMS, le proiezioni
  esplicite possono giustificare un ROIC sopra WACC)
- L'interpretazione della PD (se la leva e' superiore al settore, la PD sara'
  elevata per ragioni strutturali)

## Errori Comuni

| Errore | Gravita' | Soluzione |
|--------|----------|-----------|
| Confrontare target con BMS di settore diverso | CRITICO | Stessa `gics_sub_industry` |
| Confrontare anni fiscali diversi | ALTO | Stesso `fiscal_year` per entrambi |
| Interpretare il delta come causale | MEDIO | E' correlazione, non causalita' |
| Sommare i driver per ottenere il gap totale | MEDIO | I driver interagiscono, la somma e' approssimata |
| Non contestualizzare con la ciclicita' | BASSO | Un anno buono del target vs BMS medio puo' essere temporaneo |

## Metriche di Confronto

L'analyzer produce confronti su queste dimensioni:

| Metrica | Tipo | Formula |
|---------|------|---------|
| Fatturato | Assoluto (M) | `target.revenues` vs `bms.average_revenues` |
| EBITDA margin | Percentuale | `ebitda/revenues` |
| EBIT margin | Percentuale | `ebit/revenues` |
| NOPAT margin | Percentuale | `nopat/revenues` |
| Debito/Attivo | Percentuale | `gross_debt/total_assets` |
| Equity/Attivo | Percentuale | `equity/total_assets` |
| NIC/Fatturato | Ratio | `net_invested_capital/revenues` |
| D/E | Ratio | `gross_debt/equity` |

## Metodologia (Scarano/Brughera 2008)

L'approccio settoriale prevede:
1. Costruire il BMS → profilo dell'Impresa Media Standard (IMS)
2. Valutare l'IMS con DCF → valore di riferimento del settore
3. **Analizzare il differenziale** della singola PMI rispetto al BMS
4. Attribuire le differenze ai singoli driver (margine, crescita, leva, CI)

Il differenziale isola le peculiarita' (positive e negative) della target
rispetto al settore e quantifica il loro peso sul valore.

Riferimento: `docs/rating_valuation/2008 n.-65 Bilancio Madio Standard.pdf`
