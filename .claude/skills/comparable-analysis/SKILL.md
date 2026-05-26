---
name: comparable-analysis
description: Esegue analisi dei comparabili e valutazione relativa tramite multipli di mercato secondo Damodaran
user_invocable: true
---

# Skill: Analisi Comparabili e Valutazione Relativa (Damodaran)

Stima il valore di un'azienda attraverso multipli di mercato e confronto con societa'
comparabili, seguendo il framework di valutazione relativa di Aswath Damodaran:
i multipli non sono scorciatoie ma sono guidati da fondamentali (crescita, rischio, payout).

## Utilizzo

```
/comparable-analysis AAPL
/comparable-analysis ENEL.MI
/comparable-analysis AAPL --multipli "PE,EV_EBITDA,PB"
```

---

## Vincoli Critici

Leggere PRIMA di iniziare qualsiasi analisi:

1. **Minimo 5 comparabili** — con meno di 5, i risultati sono statisticamente inaffidabili
2. **MAI usare P/E per aziende in perdita** — usare EV/EBITDA, EV/Sales, o P/B
3. **Mediana preferita alla media** — la mediana e' robusta agli outlier
4. **Escludere outlier > 2 deviazioni standard** dalla mediana prima di calcolare le statistiche
5. **Non mescolare GAAP e IFRS** senza aggiustamenti — principi contabili diversi producono multipli non confrontabili
6. **Specificare sempre trailing vs forward** — un P/E trailing non e' confrontabile con un P/E forward
7. **Enterprise Value multipli richiedono ponte** — da EV si passa a Equity sottraendo Debito Netto
8. **Multipli non sono scorciatoie**: ogni multiplo ha un fondamentale sottostante (g, rischio, payout)

---

## Processo di Valutazione Relativa

### Step 1: Selezione dei Comparabili

**Criteri di selezione (in ordine di priorita' — Damodaran):**

| Priorita' | Criterio | Dettaglio |
|-----------|----------|-----------|
| 1 | Stesso settore/industria | Business model simile, stessi driver di valore |
| 2 | Dimensione | Market cap nella stessa fascia (small/mid/large cap) |
| 3 | Crescita | Tasso crescita ricavi simile (±5 pp) |
| 4 | Profittabilita' | Margini operativi simili (±5 pp) |
| 5 | Rischio | Beta e leverage simili |
| 6 | Geografia | Stesso mercato principale |

**Numero di comparabili:**
- Ideale: 7-10
- Minimo accettabile: 5
- Con meno di 5: segnalare esplicitamente la limitazione nei risultati

**Dove trovare i comparabili:**
- Config `configs/{TICKER}.json` sezione `comparabili` (fonte primaria)
- Dataset Damodaran per mediane settoriali
- Se non in config, chiedere all'utente o proporre un set basato sul settore

**Multipli specifici per settore:**

| Settore | Multipli chiave | Metriche aggiuntive |
|---------|----------------|---------------------|
| Tech / Software | EV/Sales, EV/EBITDA | Rule of 40 (crescita + margine) |
| Banche | P/B, P/E | ROE, CET1 ratio |
| Assicurazioni | P/B, P/Embedded Value | Combined ratio |
| Utilities | EV/EBITDA, Dividend Yield | RAB (Regulated Asset Base) |
| Industriali | EV/EBIT, EV/EBITDA | ROIC, CapEx intensity |
| Healthcare | EV/EBITDA, P/E | Pipeline, patent cliff |
| Real Estate | P/NAV, P/FFO | Cap rate, occupancy |
| Retail | EV/Sales, EV/EBITDA | Same-store sales growth |

> **CHECKPOINT**: Mostrare la lista comparabili proposta con settore, market cap,
> e crescita ricavi. Chiedere conferma o sostituzione prima di procedere.

---

### Step 2: Raccolta e Validazione Multipli

**Multipli da calcolare per ogni comparabile:**

| Multiplo | Formula | Uso principale |
|----------|---------|---------------|
| P/E | Prezzo / EPS | Aziende profittevoli, utili stabili |
| EV/EBITDA | Enterprise Value / EBITDA | Cross-border, capital-intensive |
| P/B | Market Cap / Book Value Equity | Banche, asset-heavy |
| EV/Sales | Enterprise Value / Ricavi | Aziende in perdita, startup, confronti margini |
| EV/EBIT | Enterprise Value / EBIT | Simile a EV/EBITDA ma considera D&A |
| PEG | P/E / Crescita EPS (%) | Aggiustamento P/E per crescita |

**Fondamentali che guidano ogni multiplo (Damodaran):**

| Multiplo | Drivers fondamentali | Formula intrinseca |
|----------|---------------------|--------------------|
| P/E | Crescita, rischio, payout | `P/E = Payout * (1+g) / (Re - g)` |
| EV/EBITDA | Crescita, rischio, tax, reinvestimento | `EV/EBITDA = (1-t)(1 - RIR/...) / (WACC - g)` |
| P/B | ROE, crescita, rischio | `P/B = (ROE - g) / (Re - g)` |
| EV/Sales | Margine, crescita, rischio | `EV/Sales = Margine_after_tax * (1+g) / (WACC - g)` |

Comprendere i driver evita di applicare ciecamente la mediana: se il target ha crescita
superiore ai peer, merita un multiplo piu' alto.

**Pulizia dati:**
- Escludere P/E per aziende con utili negativi
- Rimuovere outlier > 2 sigma dalla mediana
- Normalizzare per voci straordinarie se possibile
- Verificare coerenza GAAP vs IFRS tra i comparabili

> **CHECKPOINT**: Mostrare tabella completa dei multipli per tutti i comparabili.
> Evidenziare outlier e valori esclusi.

---

### Step 3: Calcolo Statistiche

**Statistiche di riferimento:**

| Statistica | Quando usarla |
|-----------|--------------|
| **Mediana** | Default — robusta a outlier |
| **Media** | Solo se distribuzione simmetrica e no outlier estremi |
| **Media armonica** | Per P/E — gestisce meglio valori estremi alti |
| **25° percentile** | Limite inferiore del range ragionevole |
| **75° percentile** | Limite superiore del range ragionevole |

**Analisi dispersione:**
- Deviazione standard / Mediana > 50%: dispersione eccessiva, i risultati sono poco informativi
- Range interquartile ampio: segnalare all'utente la bassa affidabilita' della stima puntuale

**Tabella output:**

| Multiplo | Media | Mediana | Q1 | Q3 | Std Dev | N |
|----------|-------|---------|----|----|---------|---|
| P/E | ... | ... | ... | ... | ... | ... |
| EV/EBITDA | ... | ... | ... | ... | ... | ... |
| P/B | ... | ... | ... | ... | ... | ... |
| EV/Sales | ... | ... | ... | ... | ... | ... |

> **CHECKPOINT**: Mostrare tabella statistiche. Se dispersione eccessiva su un multiplo,
> segnalare e valutare se escluderlo dalla valutazione.

---

### Step 4: Aggiustamenti per Differenze Fondamentali

**Aggiustamento per crescita:**
Se il target cresce piu' (o meno) dei comparabili:
```
Multiplo_aggiustato = Multiplo_mediano * (1 + g_target) / (1 + g_mediano)
```

**Aggiustamento per rischio:**
Se il target ha rischio diverso (beta piu' alto/basso):
```
Multiplo_aggiustato = Multiplo_mediano * Re_mediano / Re_target
```

**Aggiustamento per margini (EV/Sales):**
```
Multiplo_aggiustato = Multiplo_mediano * Margine_target / Margine_mediano
```

**Conglomerate discount:**
Aziende diversificate in piu' settori possono meritare uno sconto (10-20%)
rispetto a peer pure-play. Applicare solo se giustificato dalla struttura.

Gli aggiustamenti sono opzionali ma importanti quando il target differisce
significativamente dai peer. Specificare sempre se i multipli sono aggiustati o grezzi.

> **CHECKPOINT**: Se si applicano aggiustamenti, mostrare multiplo grezzo vs aggiustato
> con la motivazione.

---

### Step 5: Valutazione del Target

**Applicazione multipli al target:**

Per multipli equity-based (P/E, P/B):
```
Valore Equity = Metrica_target * Multiplo_mediano
Valore Per Azione = Valore Equity / Azioni Outstanding
```

Per multipli enterprise (EV/EBITDA, EV/Sales, EV/EBIT):
```
Enterprise Value implicito = Metrica_target * Multiplo_mediano
Equity Value = EV implicito - Debito Netto
Valore Per Azione = Equity Value / Azioni Outstanding
```

**Tabella valutazione:**

| Multiplo | Metrica Target | Multiplo Mediano | Valore Implicito | Per Azione |
|----------|---------------|-----------------|-----------------|------------|
| P/E | EPS = ... | ... | ... | ... |
| EV/EBITDA | EBITDA = ... | ... | EV = ... | ... |
| P/B | BV = ... | ... | ... | ... |
| EV/Sales | Ricavi = ... | ... | EV = ... | ... |

**Range di valutazione:**
```
Range stretto: [Valore al Q1, Valore al Q3]   (50% dei comparabili)
Range largo:   [Valore al Min, Valore al Max]  (esclusi outlier)
Punto centrale: Valore alla Mediana
```

**Sintesi multi-multiplo (pesi suggeriti per settore):**

| Settore | P/E | EV/EBITDA | P/B | EV/Sales |
|---------|-----|-----------|-----|----------|
| Tech | 25% | 35% | - | 40% |
| Banche | 30% | - | 50% | 20% |
| Utilities | 20% | 50% | 15% | 15% |
| Industriali | 30% | 40% | 15% | 15% |
| Default | 30% | 35% | 15% | 20% |

> **CHECKPOINT FINALE**: Mostrare tabella valutazione completa, range, e valore medio ponderato.
> Confrontare con prezzo di mercato (upside/downside).

---

## Errori Comuni

| Errore | Perche' e' grave | Come evitarlo |
|--------|-----------------|---------------|
| Usare P/E per aziende in perdita | P/E negativo non ha senso economico | Usare EV/EBITDA o EV/Sales |
| Mescolare trailing e forward | Non confrontabili | Specificare e usare un solo approccio |
| Mescolare GAAP e IFRS | Trattamento diverso di lease, R&D, goodwill | Verificare principi contabili dei peer |
| Usare media con outlier estremi | La media e' distorta da valori estremi | Usare mediana o media harmonica |
| Dimenticare ponte EV -> Equity | Applicare EV/EBITDA direttamente al prezzo | Sempre sottrarre Debito Netto |
| Ignorare differenze di crescita | Un'azienda che cresce il doppio merita multiplo piu' alto | Aggiustare o almeno segnalare |
| Troppi pochi comparabili (< 5) | Risultati statisticamente non significativi | Allargare criteri o dichiarare limitazione |
| Ignorare lease operativi (IFRS 16) | EV/EBITDA distorto per aziende con molti lease | Aggiustare EBITDA e EV coerentemente |
| Conglomerato senza sconto | Mix di business diversi deprime i multipli | Sum-of-the-parts o sconto esplicito |

---

## Parametri per Paese

| Parametro | US | Italia |
|-----------|-----|--------|
| Universo quotate | ~5,000 (NYSE, NASDAQ) | ~350 (Borsa Italiana) |
| Indici principali | S&P 500, Russell 2000 | FTSE MIB, Mid Cap, STAR |
| Principi contabili | US GAAP | IFRS |
| Lease accounting | ASC 842 | IFRS 16 |
| Valuta | USD | EUR |
| Fonte multipli settore | Damodaran (US-centric) | Damodaran + aggiustamento per paese |
| Problemi specifici | Buyback inflazionano EPS | Partecipazioni incrociate, patto parasociale |
| P/E mediano mercato | ~18-22x | ~12-16x (sconto per crescita e rischio) |

**Nota Italia:**
Il mercato italiano ha meno quotate — spesso necessario allargare i peer all'Europa
(Euronext, Xetra, BME). Specificare se il set e' domestico o pan-europeo.
Le mid-cap italiane nel segmento STAR hanno obblighi di trasparenza maggiori.

---

## Metodologia Valutazione Relativa — Riferimento (Damodaran)

### Principio Base

Il valore di un asset puo' essere stimato guardando come il mercato prezza asset simili.
I multipli sono il ponte tra valore e fondamentali — non numeri arbitrari.

Ogni multiplo ha una formula intrinseca che lo lega a variabili fondamentali:
- **P/E** = f(crescita, rischio, payout)
- **EV/EBITDA** = f(crescita, tax, reinvestimento, rischio)
- **P/B** = f(ROE, crescita, rischio)
- **EV/Sales** = f(margini, crescita, rischio)

### Quattro Test per un Buon Multiplo (Damodaran)

1. **Definizione coerente**: numeratore e denominatore devono essere coerenti
   (P/E: equity/equity; EV/EBITDA: firm/firm)
2. **Uniformita'**: calcolato allo stesso modo per target e peer
3. **Distribuzione nota**: conoscere media, mediana, dispersione del multiplo nel settore
4. **Driver fondamentali**: sapere quali variabili lo guidano per interpretare le differenze

### Fonti Dati Damodaran per Multipli Settoriali

| Dataset | Contenuto |
|---------|-----------|
| `pedata.xlsx` | P/E per settore |
| `vebitda.xlsx` | EV/EBITDA per settore |
| `pbvdata.xlsx` | P/B per settore |
| `psdata.xlsx` | Price/Sales per settore |

### Regressione Cross-Settoriale (Avanzato)

Per universi ampi, Damodaran suggerisce la regressione:
```
Multiplo = a + b1*Crescita + b2*Rischio + b3*Payout
```
Il valore intrinseco del multiplo per il target si ottiene inserendo i suoi fondamentali.
Utile quando i peer diretti sono pochi.

---

## Note Operative

- **MAI creare script .py ad-hoc**. Usare SEMPRE `run_analysis.py`
- I comparabili vanno configurati in `configs/{TICKER}.json` sezione `comparabili`
- Per aziende italiane: considerare peer pan-europei se il set domestico e' insufficiente
- Il risultato della valutazione relativa e' la sezione 5 del report standard
- Loggare l'analisi in `data/logs/prompt_log.md` tramite `utils/logging_utils.py`
