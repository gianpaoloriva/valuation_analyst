---
name: fsi-earnings-analysis-italy
description: >
  Report di aggiornamento utili (earnings update, 8-12 pagine) per società
  quotate su Borsa Italiana già in copertura. Analisi beat/miss su bilancio
  IFRS, metriche chiave, stime aggiornate, impatto sulla tesi.
  Fonti: CONSOB, Borsa Italiana, relazione semestrale IAS 34, conference call.
  Triggers on "earnings update", "aggiornamento utili", "analisi trimestrale",
  "risultati trimestrali", "risultati semestrali", "post-earnings",
  "Q1/Q2/Q3/Q4 results", "analisi bilancio".
---

# Equity Research Earnings Update — Contesto Italiano

Adapt dello skill US `earnings-analysis`. Il framework beat/miss e la struttura del report sono universali. Adattate le fonti dati, i riferimenti contabili (IFRS vs GAAP), il calendario earnings, e il formato di citazione.

**Caratteristiche report:**
- **Lunghezza**: 8-12 pagine
- **Parole**: 3.000-5.000
- **Tabelle**: 1-3 riassuntive
- **Grafici**: 8-12
- **Turnaround**: 1-2 giorni dalla pubblicazione risultati
- **Audience**: clienti che già conoscono la società (già in copertura)
- **Focus**: cosa c'è di NUOVO — beat/miss, stime aggiornate, impatto sulla tesi
- **Standard**: JPMorgan, Goldman Sachs, Morgan Stanley + **Mediobanca, Equita, Intesa Sanpaolo IMI**

## Adattamenti al Contesto Italiano

### Fonti Dati — Sostituzione

| Fonte US (da NON usare) | Fonte Italiana/Europea (da usare) |
|--------------------------|-----------------------------------|
| SEC EDGAR | **CONSOB** (consob.it → Emittenti → Documenti) |
| 10-Q (trimestrale) | **Resoconto intermedio di gestione** (se pubblicato) o **Relazione semestrale** (IAS 34) |
| 10-K (annuale) | **Bilancio consolidato IFRS** (Relazione annuale) |
| 8-K (current report) | **Comunicazione price sensitive** (CONSOB / Borsa Italiana) |
| Earnings release | **Comunicato stampa risultati** (sito IR della società) |
| Earnings call transcript | **Trascrizione conference call** (Refinitiv, Bloomberg, sito società) |
| DEF 14A proxy | **Relazione governo societario** + **Relazione remunerazione** |
| Bloomberg / FactSet consensus (US-centric) | **Refinitiv IBES**, **Bloomberg**, **FactSet** (con copertura EU) |

### Calendario Earnings Italiano

| Periodo | Documento | Timing pubblicazione | Note |
|---------|-----------|---------------------|------|
| Q4 / FY | Bilancio consolidato IFRS | Febbraio-Aprile (60-120 gg dopo 31/12) | Più lento che in US |
| H1 | Relazione semestrale (IAS 34) | Luglio-Settembre | Obbligatoria, revisionata |
| Q1 / Q3 | Resoconto intermedio di gestione | 45-60 gg dopo fine trimestre | **Non obbligatorio dal 2014** — molte società non lo pubblicano |

**Attenzione**: molte mid/small cap italiane pubblicano solo semestrali e annuali (no trimestrali). In quel caso, l'earnings update copre il semestre, non il trimestre.

**Conference call**: le large cap (FTSE MIB) fanno sempre conference call in inglese. Le mid cap (STAR, Mid Cap) spesso solo in italiano o con partecipazione limitata. Le small cap raramente fanno conference call pubblica.

### Principi Contabili — IFRS vs GAAP

| Voce US | Voce IFRS italiana | Differenza chiave |
|---------|-------------------|-------------------|
| Revenue (ASC 606) | Ricavi (IFRS 15) | Simile, differenze in contratti complessi |
| EPS (GAAP) | Utile per azione (IAS 33) | Base e diluito, stessa logica |
| Goodwill (ammortizzato) | Avviamento (IAS 36 — impairment test) | Nessun ammortamento, rischio svalutazione improvvisa |
| Operating lease (off-balance pre-ASC 842) | Leasing (IFRS 16 — tutti capitalizzati) | Sempre on-balance, impatto su EBITDA e debito |
| Adjusted EBITDA | EBITDA Adjusted / EBITDA reported | Società italiane spesso riportano "EBITDA adjusted" con add-back diversi |
| Non-GAAP measures | Misure alternative di performance (MAP) | ESMA Guidelines: le società devono riconciliare le MAP con le voci IFRS |

### Valuta e Formato

- **Valuta**: EUR (€), non USD ($)
- **Separatore migliaia**: punto (1.000.000)
- **Separatore decimali**: virgola (3,50%)
- **EPS**: €X,XX (non $X.XX)
- **Unità**: EUR Milioni (€M)

### Formato Citazioni

**Fonti da citare in ogni earnings update:**
- ✅ Comunicato stampa risultati (con data e link al sito IR)
- ✅ Relazione semestrale o bilancio consolidato (con data e link CONSOB o sito società)
- ✅ Trascrizione conference call (con data)
- ✅ Presentazione investitori / supplemental materials (se disponibile)
- ✅ Consensus stime (Refinitiv IBES / Bloomberg / FactSet con data)
- ✅ Guidance precedente (dal comunicato del trimestre/semestre precedente)

**Sezione SOURCES a fine report:**

```
FONTI E RIFERIMENTI

Materiali Risultati (H1 2024):
• Comunicato stampa risultati (25 luglio 2024)
  [Link al sito IR della società]

• Relazione semestrale consolidata (25 luglio 2024)
  [Link a CONSOB o sito società sezione Bilanci]

• Trascrizione conference call (26 luglio 2024)
  [Link a Refinitiv o sito società]

• Presentazione investitori H1 2024 (25 luglio 2024)
  [Link al sito IR]
```

**NON linkare a SEC EDGAR** — usare CONSOB (consob.it) o il sito IR della società per i documenti ufficiali.

## Workflow

Il workflow segue le stesse 5 fasi dello skill US. Applicare gli adattamenti sopra in ogni fase.

### Fase 1: Raccolta Dati (30-60 minuti)

**Procedura di ricerca adattata per società italiane:**

1. **Sito IR della società** → sezione "Risultati finanziari" / "Financial Results" / "Bilanci e Relazioni"
2. **Borsa Italiana** (borsaitaliana.it) → scheda società → documenti
3. **CONSOB** (consob.it) → Emittenti → Documenti → cercare per denominazione
4. **Refinitiv / Bloomberg** → consensus stime, trascrizione conference call

**Verifiche obbligatorie:**
- [ ] Data comunicato stampa verificata (entro ultimi 3 mesi)
- [ ] Relazione semestrale / bilancio disponibile su CONSOB o sito società
- [ ] Conference call transcript disponibile e della stessa data
- [ ] Consensus pre-risultati (Refinitiv IBES o Bloomberg) con data

**Per dettagli procedurali**: riferirsi a `references/workflow.md` dello skill US, sostituendo SEC EDGAR con CONSOB e 10-Q con relazione semestrale.

### Fase 2: Analisi (2-3 ore)

Stessa struttura analitica dello skill US. Adattamenti:

**Beat/miss analysis:**
- Confrontare con consensus Refinitiv IBES (non solo Bloomberg US)
- Metriche chiave: Ricavi, EBITDA, EBIT, Utile netto, EPS, FCF
- Se società bancaria: NII (Margine d'interesse), Commissioni nette, Cost/Income, CET1, NPL ratio
- Se utility: RAB, EBITDA regolato, FFO/Debt

**Guidance:**
- Società italiane danno guidance meno frequentemente e meno dettagliata che le US
- Molte danno solo "outlook qualitativo" anziché numeri specifici
- Verificare se la società ha aggiornato la guidance nel comunicato

**Metriche IFRS specifiche da monitorare:**
- Svalutazione avviamento (IAS 36) — impatto one-off significativo
- Impatto IFRS 16 su EBITDA e debito
- TFR e altri fondi (IAS 19) — variazioni attuariali in OCI
- Misure Alternative di Performance (MAP) e loro riconciliazione IFRS

### Fase 3: Generazione Grafici (1-2 ore)

8-12 grafici, stessa tipologia dello skill US. Adattamenti:

| Grafico | Adattamento |
|---------|-------------|
| Revenue progression | Valori in €M, eventuale breakdown Italia/Europa/Globale |
| EPS progression | €/azione, formato X,XX |
| Margin trends | EBITDA margin, EBIT margin (non "operating margin" generico) |
| Revenue by segment | Usare segmenti IFRS 8 come riportati dalla società |
| Beat/miss summary | Consensus Refinitiv IBES |
| Valuation | Multipli vs FTSE MIB / settore italiano, non S&P 500 |

### Fase 4: Creazione Report (2-3 ore)

Struttura identica allo skill US (8-12 pagine). Adattamenti:

- **Pagina 1**: Rating (COMPRARE/MANTENERE/VENDERE o BUY/HOLD/SELL), prezzo target in €, benchmark FTSE MIB
- **Pagine 2-3**: Analisi risultati con voci IFRS
- **Pagine 4-5**: Metriche chiave — usare la terminologia IFRS italiana
- **Pagine 6-7**: Aggiornamento tesi — includere catalizzatori italiani/europei (PNRR, BCE, regolamentazione settoriale)
- **Pagine 8-10**: Valutazione con multipli vs peer europei, WACC italiano
- **Disclaimer CONSOB** a fine report (non SEC)

**Per template dettagliati**: riferirsi a `references/report-structure.md` dello skill US, applicando le sostituzioni valuta/formato/fonti.

### Fase 5: Quality Check & Consegna (30 minuti)

**Checklist di verifica adattata:**
- [ ] Ogni grafico ha fonte con documento specifico e data
- [ ] Ogni tabella ha fonte con riferimento documento
- [ ] Beat/miss cita fonte consensus con data (Refinitiv IBES / Bloomberg)
- [ ] Variazioni guidance citano comunicati corrente e precedente
- [ ] Sezione Fonti elenca tutti i materiali con link
- [ ] **NESSUN link a SEC EDGAR** — solo CONSOB / sito IR società
- [ ] Valori in EUR con formato europeo (punto migliaia, virgola decimali)
- [ ] EPS in €X,XX
- [ ] Multipli confrontati con peer europei (non S&P 500)
- [ ] Disclaimer CONSOB incluso

**Per checklist completa**: riferirsi a `references/best-practices.md` dello skill US, applicando le sostituzioni fonti/formato.

## Output

**Deliverable principale**: report DOCX (8-12 pagine)
**Nome file**: `[Società]_H1_[Anno]_Earnings_Update.docx` o `[Società]_Q[Trimestre]_[Anno]_Earnings_Update.docx`
**Esempio**: `Enel_H1_2024_Earnings_Update.docx`

**Contenuti:**
- Pagina 1: Sintesi con rating, prezzo target in €, key takeaways
- Pagine 2-3: Analisi risultati dettagliata (IFRS)
- Pagine 4-5: Metriche chiave e guidance
- Pagine 6-7: Aggiornamento tesi
- Pagine 8-10: Valutazione e stime
- Pagine 11-12: Appendice (opzionale)
- 8-12 grafici embedded
- 1-3 tabelle riassuntive
- Sezione Fonti con link (CONSOB / sito IR)
- Disclaimer CONSOB

**Deliverable opzionale**: aggiornamento modello XLS

## Errori Comuni da Evitare

### ❌ Cercare il 10-Q su SEC EDGAR
Le società italiane non depositano 10-Q. Il documento equivalente è la relazione semestrale (IAS 34), depositata su CONSOB e pubblicata sul sito IR. Per i trimestrali (Q1/Q3): verificare se la società pubblica il resoconto intermedio — dal 2014 non è obbligatorio.

### ❌ Usare "GAAP EPS" e "Non-GAAP EPS"
In IFRS non esiste la distinzione GAAP/Non-GAAP. Usare: "Utile per azione" (IAS 33) e "Utile per azione adjusted" (MAP della società). Verificare sempre la riconciliazione MAP → IFRS come richiesto da ESMA Guidelines.

### ❌ Confrontare con S&P 500 o peer US
Il benchmark è il FTSE MIB (o EURO STOXX 50 per società pan-europee). I peer nella tabella comparativa devono essere europei del medesimo settore.

### ❌ Aspettarsi trimestrali da tutte le società
Molte mid/small cap italiane pubblicano solo semestrali e annuali. L'earnings update in quel caso copre il semestre (H1 o FY), non il singolo trimestre.

### ❌ Ignorare le svalutazioni di avviamento
In IFRS l'avviamento non si ammortizza ma è soggetto a impairment test annuale (IAS 36). Svalutazioni improvvise possono avere impatto significativo e sono un catalizzatore negativo da monitorare sempre.
