---
name: fsi-comps-analysis-italy
description: |
  Costruzione di analisi di società comparabili (comparable company analysis) di qualità istituzionale per il mercato italiano/europeo, con metriche operative, multipli di valutazione e benchmarking statistico in formato Excel. Fonti dati: Refinitiv, Bureau van Dijk/AIDA, CONSOB, Borsa Italiana. Universo peer su FTSE MIB, FTSE Italia Mid Cap, STAR, Euronext. Valuta EUR con convenzioni europee.

  **Ideale per:**
  - Valutazione società quotate su Borsa Italiana / Euronext (M&A, analisi di investimento)
  - Benchmarking performance vs peer di settore italiani/europei
  - Pricing IPO o aumenti di capitale
  - Identificazione outlier di valutazione (sopra/sotto-valutate)
  - Supporto a presentazioni per comitato investimenti
  - Report di overview settoriale

  **Non ideale per:**
  - Società private senza peer pubblici comparabili
  - Conglomerati altamente diversificati
  - Società in dissesto/procedure concorsuali
  - Startup pre-revenue
  - Società con modelli di business unici
---

# Comparable Company Analysis — Contesto Italiano/Europeo

## ⚠️ CRITICO: Priorità Fonti Dati (LEGGERE PRIMA)

**Seguire SEMPRE questa gerarchia di fonti dati:**

1. **PRIMA: Verificare fonti dati MCP** — Se Refinitiv MCP, Bureau van Dijk MCP, o altri provider MCP sono disponibili, usarli esclusivamente per informazioni finanziarie e di trading
2. **NON usare ricerca web** se le fonti MCP sopra sono disponibili
3. **SOLO se gli MCP non sono disponibili:** Usare Refinitiv/LSEG, Bloomberg Terminal, bilanci CONSOB/Borsa Italiana, AIDA/Bureau van Dijk, o altre fonti istituzionali
4. **MAI usare la ricerca web come fonte dati primaria** — manca l'accuratezza, la tracciabilità e l'affidabilità richieste per analisi di grado istituzionale

**Fonti dati specifiche per il contesto italiano/europeo:**

| Fonte | Copertura | Contenuto |
|-------|-----------|-----------|
| **Refinitiv / LSEG** | Globale, forte EU | Consensus, stime, dati di mercato, beta, multipli |
| **Bureau van Dijk / AIDA** | Italia + EU | Bilanci strutturati, indici, confronti settoriali |
| **CONSOB** | Italia quotate | Comunicazioni, partecipazioni, prospetti |
| **Borsa Italiana** | Italia quotate | Prezzi, volumi, schede società, bilanci |
| **Bloomberg** | Globale | Dati di mercato, consensus, screening |
| **FactSet** | Globale, forte EU | Multipli, stime, screening peer |
| **S&P Capital IQ** | Globale | Financials, comparables, screening |
| **Registro Imprese** | Italia tutte | Bilanci depositati (quotate e non) |

---

## Panoramica

Questo skill guida la costruzione di analisi di comparabili di qualità istituzionale che combinano metriche operative, multipli di valutazione e benchmarking statistico, adattate al contesto del mercato italiano ed europeo.

**Differenze chiave rispetto al contesto US:**
- **Universo peer**: Borsa Italiana (~350 quotate vs 5.000+ US), Euronext, borse europee
- **Segmenti di mercato**: FTSE MIB (40 large cap), FTSE Italia Mid Cap (~60), STAR (~70 mid cap ad alti requisiti), EGM/AIM (~170 small cap)
- **Principi contabili**: IFRS (non US GAAP) — impatto su EBITDA, D&A, leasing, goodwill
- **Valuta**: EUR con formattazione europea (punto migliaia, virgola decimali)
- **Fonti filing**: Bilanci IFRS da CONSOB/Borsa Italiana (non 10-K/10-Q da SEC EDGAR)
- **Fiscalità**: IRES 24% + IRAP ~3.9% = ~27.9% (non 21% US)
- **Dimensioni**: Market cap italiane tipicamente più piccole — large cap italiane ≈ mid cap US
- **Concentrazione settoriale**: Borsa Italiana dominata da banche, utilities, lusso, industriali

**Materiale di Riferimento:**

Un esempio di analisi comparabili è fornito in `examples/comps_example.xlsx`. Quando si usano file esempio:

**Usare gli esempi per:**
- Capire la gerarchia strutturale (come fluiscono le sezioni)
- Comprendere il livello di rigore atteso
- Apprendere i principi (intestazioni chiare, formule trasparenti, tracciabilità)

**NON usare gli esempi per:**
- Riproduzione esatta di formato o metriche
- Copiare il layout senza considerare il contesto
- Applicare lo stesso stile visivo indipendentemente dal pubblico

**SEMPRE chiedersi prima:**
1. **"Hai un formato preferito o devo adattare lo stile del template?"**
2. **"Chi è il pubblico?"** (Comitato investimenti, presentazione CdA, riferimento rapido, memo dettagliato)
3. **"Qual è la domanda chiave?"** (Valutazione, analisi crescita, posizionamento competitivo, efficienza)
4. **"Qual è il contesto?"** (Valutazione M&A, decisione di investimento, benchmarking settoriale, performance review)

**Adattare in base alle specificità:**
- **Contesto settoriale**: Le banche italiane richiedono metriche diverse dalle mid cap industriali dello STAR
- **Dimensione peer group**: Con ~350 quotate, il pool di comparabili italiani puri è spesso limitato — considerare peer europei
- **Familiarità**: Società note (Enel, Intesa) richiedono meno background, più focus su analisi differenziale
- **Tipo di decisione**: M&A richiede enfasi diversa dal monitoraggio di portafoglio

---

## ⚠️ CRITICO: Formule Sopra Valori Fissi + Verifica Passo-Passo

**Ambiente — Office JS vs Python:**
- **Se in esecuzione dentro Excel (Office Add-in / Office JS):** Usare Office JS direttamente. Scrivere formule via `range.formulas = [["=E7/C7"]]`, non `range.values`. Nessun ricalcolo separato — Excel gestisce nativamente.
- **Se si genera un file .xlsx standalone:** Usare Python/openpyxl. Scrivere `cell.value = "=E7/C7"` (stringa formula).
- **Trappola merged cell in Office JS:** NON chiamare `.merge()` poi impostare `.values`. Scrivere il valore sulla cella in alto a sinistra, poi unire e formattare.

**Formule, non valori fissi:**
- Ogni valore derivato (margine, multiplo, statistica) DEVE essere una formula Excel che referenzia celle input
- Gli unici valori fissi devono essere dati grezzi (ricavi, EBITDA, prezzo azione, ecc.) — e ognuno richiede un commento cella con la fonte

**Verificare passo-passo con l'utente:**
- Dopo la struttura → mostrare il layout intestazioni prima di inserire dati
- Dopo gli input grezzi → mostrare il blocco input e confermare fonti/periodi
- Dopo le metriche operative → mostrare margini calcolati e sanity-check
- Dopo i multipli di valutazione → mostrare i multipli e confermare ragionevolezza
- NON costruire l'intero foglio end-to-end

---

## Sezione 1: Struttura Documento & Setup

### Blocco Intestazione (Righe 1-3)
```
Riga 1: [TITOLO ANALISI] — ANALISI SOCIETÀ COMPARABILI
Riga 2: [Lista Società con Ticker] • [Società 1 (TICK1.MI)] • [Società 2 (TICK2.MI)] • [Società 3 (TICK3.MI)]
Riga 3: Al [Periodo] | Tutti i valori in EUR Milioni salvo importi per azione e rapporti
```

**Nota ticker italiani:** I ticker su Borsa Italiana usano il suffisso `.MI` (es. `ENEL.MI`, `ISP.MI`, `UCG.MI`). Su Euronext il suffisso varia (`.PA` Parigi, `.AS` Amsterdam). Specificare sempre la borsa di quotazione.

### Standard Convenzioni Visive (OPZIONALE — Le preferenze utente hanno sempre priorità)

**Colori & Sfondo — Palette Blu/Grigio Professionale:**
- **Intestazioni sezione**: Blu scuro (`#1F4E79`) sfondo, testo bianco bold
- **Intestazioni colonna**: Blu chiaro (`#D9E1F2`) sfondo, testo nero bold
- **Righe dati**: Sfondo bianco, testo nero per formule, testo blu per input
- **Righe statistiche**: Grigio chiaro (`#F2F2F2`) sfondo

**Convenzioni di Formattazione:**
- **Precisione decimale**:
  - Percentuali: 1 decimale (12,3%)
  - Multipli: 1 decimale (13,5x)
  - Importi in euro: Nessun decimale, separatore migliaia con punto (69.632)
  - Margini come percentuali: 1 decimale (68,7%)
- **Bordi**: Nessun bordo (aspetto pulito, minimale)
- **Allineamento**: Tutte le metriche centrate
- **Dimensioni celle**: Larghezze colonna uniformi, altezze riga consistenti

---

## Sezione 2: Statistiche Operative & Metriche Finanziarie

### Colonne Core (Partire da queste)
1. **Società** — Nomi con formattazione coerente
2. **Ricavi** — Metrica dimensionale (LTM, trimestrale, o annuale)
3. **Crescita Ricavi** — Variazione percentuale anno su anno
4. **Utile Lordo** — Ricavi meno costo del venduto
5. **Margine Lordo** — UL/Ricavi (profittabilità fondamentale)
6. **EBITDA** — Utile prima di interessi, imposte, ammortamenti e svalutazioni
7. **Margine EBITDA** — EBITDA/Ricavi (efficienza operativa)

**Nota IFRS:** L'EBITDA non è una metrica IFRS standard. Le società italiane possono riportare EBITDA adjusted con diverse rettifiche (costi non ricorrenti, SBC, ristrutturazioni). Verificare la definizione usata da ciascuna società e normalizzare se necessario per confrontabilità.

### Aggiunte Opzionali (Scegliere in base a settore/scopo)
- **Trimestrale vs LTM** — Includere entrambi se la stagionalità conta
- **Free Cash Flow** — Per settori capital-intensive o SaaS
- **Margine FCF** — FCF/Ricavi
- **Utile Netto** — Per società mature e profittevoli
- **Risultato Operativo** — Per business con D&A variabile
- **Metriche CapEx** — Per settori asset-heavy
- **ROIC** — Return on invested capital (particolarmente rilevante in Europa)
- **Dividend Yield** — Più rilevante che in US (società italiane hanno payout più alti)
- **Payout Ratio** — Dividendi / Utile Netto

### Esempi Formula (Usando Riga 7 come esempio)
```excel
// Rapporti core — sempre calcolati
Margine Lordo (F7): =E7/C7
Margine EBITDA (H7): =G7/C7

// Rapporti opzionali — includere se rilevanti
Margine FCF: =[FCF]/[Ricavi]
Margine Utile Netto: =[Utile Netto]/[Ricavi]
Dividend Yield: =[DPS]/[Prezzo Azione]
```

### Blocco Statistiche (Dopo i dati delle società)

**CRITICO: Aggiungere formule statistiche per tutte le metriche comparabili.**

```
[Lasciare una riga vuota per separazione visiva]
- Massimo: =MAX(B7:B9)
- 75° Percentile: =QUARTILE(B7:B9,3)
- Mediana: =MEDIAN(B7:B9)
- 25° Percentile: =QUARTILE(B7:B9,1)
- Minimo: =MIN(B7:B9)
```

**Colonne che NECESSITANO statistiche (metriche comparabili):**
- Crescita Ricavi %, Margine Lordo %, Margine EBITDA %, EPS, Dividend Yield %
- EV/Ricavi, EV/EBITDA, P/E, P/BV, Beta

**Colonne che NON necessitano statistiche (metriche dimensionali):**
- Ricavi, EBITDA, Utile Netto (la dimensione assoluta varia per scala)
- Market Cap, Enterprise Value

---

## Sezione 3: Multipli di Valutazione & Metriche di Investimento

### Colonne Core di Valutazione
1. **Società** — Stesso ordine della sezione operativa
2. **Market Cap** — Capitalizzazione di mercato corrente
3. **Enterprise Value** — Market Cap ± PFN (Posizione Finanziaria Netta)
4. **EV/Ricavi** — Quanto il mercato paga per euro di ricavi
5. **EV/EBITDA** — Quanto il mercato paga per euro di EBITDA
6. **P/E** — Prezzo relativo all'utile netto
7. **P/BV** — Prezzo / Book Value (particolarmente rilevante per banche italiane)

### Metriche di Valutazione Opzionali
- **FCF Yield** — FCF/Market Cap (per analisi focalizzate sulla cassa)
- **PEG Ratio** — P/E/Tasso di Crescita (per società in crescita)
- **Price/Book** — Valore di mercato vs valore contabile (asset-heavy e banche)
- **ROE/ROA** — Metriche di rendimento
- **CAGR Ricavi/EBITDA** — Tassi di crescita storici
- **Dividend Yield** — DPS/Prezzo (molto rilevante per investitori italiani)
- **Payout Ratio** — Dividendi/Utile Netto
- **Debito/PN** — Leva finanziaria

**Nota PFN:** Per il calcolo dell'Enterprise Value in contesto italiano/europeo, la Posizione Finanziaria Netta (PFN) è la metrica standard:
```
PFN = Debiti Finanziari Correnti + Debiti Finanziari Non Correnti 
      + Passività Leasing IFRS 16 (se incluse)
      - Disponibilità Liquide - Investimenti Finanziari a Breve
EV = Market Cap + PFN
```
Post IFRS 16, specificare se la PFN include o esclude le passività per leasing (ESMA raccomanda di includerle per confrontabilità).

### Esempi Formula
```excel
// Multipli core — sempre includere
EV/Ricavi: =[Enterprise Value]/[Ricavi LTM]
EV/EBITDA: =[Enterprise Value]/[EBITDA LTM]
P/E: =[Market Cap]/[Utile Netto]
P/BV: =[Market Cap]/[Patrimonio Netto]

// Multipli opzionali — includere se dati disponibili
FCF Yield: =[FCF LTM]/[Market Cap]
Dividend Yield: =[DPS Annuale]/[Prezzo Azione]
```

### Regola Cross-Reference
**CRITICO:** I multipli di valutazione DEVONO referenziare la sezione metriche operative. Mai inserire gli stessi dati grezzi due volte.

### Considerazioni Multipli nel Contesto Italiano/Europeo

| Multiplo | Range Tipico Italia/EU | Note |
|----------|----------------------|------|
| EV/Ricavi | 0,5-10x | Più basso che in US per assenza mega-cap tech |
| EV/EBITDA | 6-15x | Range più stretto, meno tech ad alta crescita |
| P/E | 8-25x | Generalmente più basso che in US |
| P/BV | 0,3-3,0x | Particolarmente rilevante per banche (molte <1x) |
| Dividend Yield | 2-6% | Significativamente più alto che in US |

**Attenzione al "discount italiano":** Le società italiane quotate tradano storicamente a sconto del 10-20% rispetto ai peer europei su multipli EV/EBITDA e P/E, per fattori di rischio paese, governance e liquidità. Non usare multipli US come benchmark diretto.

---

## Sezione 4: Note & Documentazione Metodologica

### Componenti Obbligatorie

**Fonti Dati & Qualità:**
- Da dove vengono i dati? (Refinitiv MCP, Bureau van Dijk MCP, Bloomberg, bilanci CONSOB)
- Quale periodo coprono? (FY2024, dati certificati / relazione semestrale)
- Come sono stati verificati? (Cross-check con bilancio IFRS consolidato)
- Nota: Dare priorità a fonti MCP (Refinitiv, BvD) se disponibili

**Definizioni Chiave:**
- Metodo di calcolo EBITDA (Utile Lordo + D&A, o Risultato Operativo + D&A)
- **Specificare se EBITDA adjusted e quali rettifiche** (costi non ricorrenti, SBC, impairment)
- Formula Free Cash Flow (CF Operativo - CapEx)
- Definizioni periodi (LTM, periodi di calcolo CAGR)
- **Definizione PFN usata** (con/senza IFRS 16, con/senza TFR)

**Metodologia di Valutazione:**
- Come è stato calcolato l'Enterprise Value? (Market Cap + PFN)
- Quali tassi di crescita sono stati usati? (CAGR storico, stime forward)
- Aggiustamenti effettuati? (Voci non ricorrenti escluse, margini normalizzati)
- **Principi contabili**: tutti IFRS? Eventuali società OIC nel peer group?

---

## Sezione 5: Scegliere le Metriche Giuste (Framework Decisionale)

### Partire da "Quale domanda sto rispondendo?"

**"Quale società è sottovalutata?"**
→ Focus su: EV/Ricavi, EV/EBITDA, P/E, P/BV, Market Cap
→ Saltare: Dettagli operativi, metriche di crescita

**"Quale società è più efficiente?"**
→ Focus su: Margine Lordo, Margine EBITDA, Margine FCF, ROIC
→ Saltare: Metriche dimensionali, importi assoluti

**"Quale società cresce più velocemente?"**
→ Focus su: Crescita Ricavi %, CAGR EBITDA, Crescita organica
→ Saltare: Metriche di margine, rapporti di leva

**"Quale genera più cassa?"**
→ Focus su: FCF, Margine FCF, FCF Conversion, CapEx intensity, Dividend Yield
→ Saltare: EBITDA, rapporti P/E

### Selezione Metriche per Settore — Contesto Italiano

**Banche & Servizi Finanziari** (settore dominante su Borsa Italiana):
Obbligatorie: ROE, ROTE, CET1 Ratio, Cost/Income, P/BV, P/E
Opzionali: NIM (Net Interest Margin), NPL Ratio, Coverage Ratio, Dividend Yield
Saltare: Margine Lordo, EBITDA, EV/Ricavi (non significativi per banche)

**Utilities** (Enel, Terna, Snam, Italgas, A2A, Hera):
Obbligatorie: EBITDA, Margine EBITDA, RAB (Regulated Asset Base), Dividend Yield
Opzionali: EV/RAB, Debito Netto/EBITDA, CapEx/Ricavi, FFO/Debito Netto
Saltare: Crescita ricavi aggressiva (settore regolato)

**Lusso & Moda** (Ferrari, Moncler, Brunello Cucinelli, Prada):
Obbligatorie: Crescita Ricavi (organica), Margine EBITDA, EV/EBITDA
Opzionali: Same-store sales, Crescita per area geografica, Margine lordo >65%
Saltare: Metriche heavy-asset

**Industriali & Manifatturiero** (Leonardo, Prysmian, Interpump):
Obbligatorie: Margine EBITDA, ROIC, Backlog (se applicabile), CapEx/Ricavi
Opzionali: Book-to-bill, Crescita organica vs acquisizioni, Asset Turnover
Saltare: Metriche SaaS

**Infrastrutture & Concessioni** (Atlantia/Mundys, ENAV):
Obbligatorie: EBITDA, EV/EBITDA, Dividend Yield, Durata concessione residua
Opzionali: Traffico/volumi, RAB, FFO/Debito
Saltare: Metriche di crescita aggressiva

**Software/Tech Italia** (piccolo segmento):
Obbligatorie: Crescita Ricavi, Margine EBITDA, ARR (se SaaS)
Opzionali: Rule of 40, Net Dollar Retention
Saltare: Confronti diretti con mega-cap tech US

### La Regola "5-10"

**5 metriche operative** — Ricavi, Crescita, 2-3 margini/metriche di efficienza
**5 metriche di valutazione** — Market Cap, EV, 3 multipli
**= 10 colonne totali** — Sufficiente per raccontare la storia

Se si hanno più di 15 metriche, probabilmente si sta includendo rumore.

---

## Sezione 6: Best Practice & Controlli di Qualità

### Prima di Iniziare
1. **Definire il peer group** — Le società devono essere veramente comparabili (modello di business, scala, geografia simili)
   - **Contesto italiano**: Con ~350 quotate, il pool di comparabili italiani puri è spesso limitato
   - Considerare peer europei dello stesso settore (CAC 40, DAX, IBEX, AEX)
   - Specificare se il peer group è "domestico puro" o "pan-europeo"
2. **Scegliere il periodo giusto** — LTM appiana la stagionalità; trimestrale mostra i trend
3. **Standardizzare le unità** — Decidere milioni vs miliardi upfront (EUR M è lo standard italiano)
4. **Mappare le fonti dati** — Sapere da dove viene ogni numero
5. **Verificare principi contabili** — Tutte IFRS? Eventuali OIC nel gruppo?

### Durante la Costruzione
1. **Inserire prima tutti i dati grezzi** — Completare il testo blu prima di scrivere formule
2. **Aggiungere commenti cella a TUTTI gli input fissi**

   **Per dati da fonte, citare esattamente la provenienza:**
   - Esempio: "Refinitiv LSEG — ENEL.MI Equity, accesso 2025-10-02"
   - Esempio: "Bilancio consolidato IFRS FY2024, pag. 42, voce 'Ricavi'"
   - Esempio: "Consensus FactSet al 2025-10-02"
   - Esempio: "Bureau van Dijk / AIDA — ultimo bilancio disponibile FY2024"
   - **Includere hyperlink quando possibile** al bilancio su CONSOB/Borsa Italiana

   **Per assunzioni, spiegare il razionale:**
   - Esempio: "Margine EBITDA stimato 15% basato su mediana peer, la società non lo espone"
   - Esempio: "EV stimato come Market Cap + PFN €50M (da SP H1, FY non ancora disponibile)"

3. **Costruire formule riga per riga** — Testare ogni calcolo prima di procedere
4. **Formattare in modo coerente** — Percentuali come percentuali, non decimali
5. **Usare formattazione condizionale** — Evidenziare outlier automaticamente

### Sanity Check
- **Test margini**: Margine lordo > Margine EBITDA > Margine utile netto
- **Ragionevolezza multipli** (contesto italiano/europeo):
  - EV/Ricavi: tipicamente 0,5-10x (varia molto per settore)
  - EV/EBITDA: tipicamente 6-15x (più contenuto che in US)
  - P/E: tipicamente 8-25x (più basso che in US)
  - P/BV: tipicamente 0,3-3,0x (banche italiane spesso <1x)
- **Correlazione crescita-multiplo**: Crescita più alta di solito significa multipli più alti
- **Trade-off dimensione-efficienza**: Società più grandi hanno spesso margini migliori
- **Dividend yield**: Società italiane tipicamente 3-5% vs 1-2% US — non è segnale di distress

### Errori Comuni da Evitare
- Mescolare market cap ed enterprise value nelle formule
- Usare periodi temporali diversi per numeratore e denominatore
- Inserire valori fissi nelle formule invece di riferimenti cella
- **Input fissi senza commenti cella che citino la fonte**
- Includere troppe metriche senza scopo chiaro
- **Includere società non comparabili** (modelli di business diversi, geografie diverse)
- **Confrontare multipli di società italiane con benchmark US** senza aggiustare per il "discount italiano"
- Usare dati obsoleti senza disclosure
- **Mescolare dati IFRS e OIC** senza normalizzazione
- **Ignorare le differenze IFRS 16** nella definizione di PFN/EBITDA

---

## Sezione 7: Costruzione del Peer Group — Contesto Italiano

### Segmenti di Mercato Borsa Italiana

| Segmento | # Società | Caratteristiche | Quando Usare |
|----------|-----------|-----------------|--------------|
| **FTSE MIB** | ~40 | Large cap, alta liquidità | Peer group per large cap italiane |
| **FTSE Italia Mid Cap** | ~60 | Mid cap | Peer group per medie imprese |
| **STAR** | ~70 | Mid cap con alti requisiti di trasparenza e governance | Peer group per PMI eccellenti |
| **EGM (ex AIM Italia)** | ~170 | Small/micro cap, listing semplificato | Peer group per small cap |

### Strategie di Composizione Peer Group

**Scenario 1: Società italiana large cap (es. Enel, Intesa)**
- Peer group: 5-8 peer europei dello stesso settore
- Fonti: FTSE MIB + equivalenti su CAC 40, DAX, IBEX
- Nota: i comparabili US sono informativi ma non direttamente applicabili per valutazione

**Scenario 2: Mid cap italiana (es. Interpump, Reply)**
- Peer group: 3-5 italiane + 3-5 europee di dimensione simile
- Fonti: FTSE Italia Mid Cap / STAR + small/mid cap europee
- Nota: la liquidità può essere un fattore — verificare volumi medi giornalieri

**Scenario 3: Small cap / EGM**
- Peer group più ristretto: 3-5 società italiane o europee simili
- Nota: dati meno disponibili, consensus limitato, bassa coverage analitica
- Considerare: multipli di transazione come complemento

**Scenario 4: Società italiana con business globale (es. Ferrari, Prysmian)**
- Peer group internazionale: globale nel settore specifico
- La quotazione italiana non deve limitare il peer group

### Fattori di Confrontabilità

Oltre a modello di business e dimensione, considerare:
- **Esposizione geografica**: società con ricavi prevalentemente italiani vs export
- **Governance**: società a controllo familiare (frequente in Italia) vs public company pura
- **Flottante**: il flottante basso (comune in Italia) impatta i multipli per premio/sconto liquidità
- **Settore regolato vs non regolato**: le utilities/concessioni hanno multipli strutturalmente diversi

---

## Sezione 8: Template Layout Esempio

**Versione Semplice (Partire da qui):**
```
┌──────────────────────────────────────────────────────────────────┐
│ UTILITIES ITALIA — ANALISI SOCIETÀ COMPARABILI                   │
│ Enel • Terna • Snam • Italgas • A2A                             │
│ Al FY2024 | Tutti i valori in EUR Milioni                        │
├──────────────────────────────────────────────────────────────────┤
│ METRICHE OPERATIVE                                               │
├──────────┬─────────┬─────────┬──────────┬──────────┬────────────┤
│ Società  │ Ricavi  │ Crescita│ Margine  │ EBITDA   │ Margine    │
│          │ (LTM)   │ (YoY)   │ Lordo    │ (LTM)    │ EBITDA     │
├──────────┼─────────┼─────────┼──────────┼──────────┼────────────┤
│ ENEL     │ 82.350  │  3,2%   │  42,1%   │  22.650  │  27,5%     │
│ TERNA    │  3.280  │  5,1%   │  68,3%   │   2.510  │  76,5%     │
│ SNAM     │  3.650  │  4,8%   │  55,2%   │   2.780  │  76,2%     │
│ ITALGAS  │  1.870  │  6,3%   │  61,5%   │   1.250  │  66,8%     │
│ A2A      │ 12.450  │  1,8%   │  28,6%   │   1.980  │  15,9%     │
│          │         │         │          │          │            │ [riga vuota]
│ Mediana  │ =MEDIAN │ =MEDIAN │ =MEDIAN  │ =MEDIAN  │ =MEDIAN    │
│ 75° %    │ =QUART  │ =QUART  │ =QUART   │ =QUART   │ =QUART     │
│ 25° %    │ =QUART  │ =QUART  │ =QUART   │ =QUART   │ =QUART     │
├──────────────────────────────────────────────────────────────────┤
│ MULTIPLI DI VALUTAZIONE                                          │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┤
│ Società  │ Mkt Cap  │ EV       │ EV/Ric.  │ EV/EBITDA│ P/E  │DY%│
├──────────┼──────────┼──────────┼──────────┼──────────┼──────┼───┤
│ ENEL     │  68.500  │  98.200  │  1,2x    │  4,3x    │ 11,2 │5,8│
│ TERNA    │  16.800  │  26.100  │  8,0x    │ 10,4x    │ 16,5 │3,9│
│ SNAM     │  15.200  │  30.800  │  8,4x    │ 11,1x    │ 14,8 │5,2│
│ ITALGAS  │   5.650  │  10.200  │  5,5x    │  8,2x    │ 12,1 │4,5│
│ A2A      │   5.800  │  11.300  │  0,9x    │  5,7x    │  9,8 │6,1│
│          │          │          │          │          │      │   │
│ Mediana  │ =MEDIAN  │ =MEDIAN  │ =MEDIAN  │ =MEDIAN  │=MED  │=MD│
│ 75° %    │ =QUART   │ =QUART   │ =QUART   │ =QUART   │=QRT  │=QR│
│ 25° %    │ =QUART   │ =QUART   │ =QUART   │ =QUART   │=QRT  │=QR│
└──────────┴──────────┴──────────┴──────────┴──────────┴──────┴───┘
```

**Nota:** L'esempio sopra è illustrativo con dati fittizi. I dati reali vanno estratti dalle fonti istituzionali.

---

## Sezione 9: Aggiunte Settoriali (Opzionale)

Aggiungere solo se critiche per l'analisi.

**Banche & Assicurazioni (settore dominante Borsa Italiana):**
Aggiungere: ROE, ROTE, CET1 Ratio, Cost/Income, NIM, NPL Ratio, Coverage Ratio, P/BV
NON usare: EV/EBITDA, Margine Lordo (non significativi per banche)

**Utilities & Infrastrutture (forte presenza italiana):**
Aggiungere: RAB, EV/RAB, FFO/Debito Netto, Dividend Yield, Durata concessioni

**Lusso & Moda:**
Aggiungere: Crescita organica, Like-for-like sales, Margine lordo (>65% tipico)

**Industriali:**
Aggiungere: ROIC, Asset Turnover, Backlog, Book-to-bill

**Real Estate / SIIQ:**
Aggiungere: NAV, P/NAV, FFO, Dividend Yield, Occupancy Rate, Cap Rate

---

## Sezione 10: Red Flag & Segnali di Attenzione

### Problemi Qualità Dati
- Periodi temporali incoerenti (mescolare trimestrale e annuale)
- Dati mancanti senza spiegazione
- Differenze significative tra fonti dati (>10% varianza)
- **Definizioni EBITDA diverse tra le società del peer group**

### Red Flag Valutazione
- Società con EBITDA negativo valutate su multipli EBITDA (usare multipli su ricavi)
- P/E >50x senza storia di crescita forte
- Margini che non hanno senso per il settore
- **Multipli applicati senza aggiustamento per "discount italiano"**

### Problemi di Confrontabilità
- Fine esercizio fiscale diversi (causa problemi di timing)
- Mescolare pure-play e conglomerati
- Modelli di business materialmente diversi etichettati come "comps"
- **Mescolare società con flottante alto e basso** senza nota sulla liquidità
- **Confrontare multipli di società a controllo familiare con public company pure**

**In caso di dubbio, escludere la società.** Meglio 3 comparabili perfetti che 6 discutibili.

---

## Sezione 11: Guida Riferimento Formule

### Formule Excel Essenziali
```excel
// Funzioni Statistiche
=MEDIA(range)             // Media semplice
=MEDIANA(range)           // Valore mediano
=QUARTILE(range, 1)       // 25° percentile
=QUARTILE(range, 3)       // 75° percentile
=MAX(range)               // Valore massimo
=MIN(range)               // Valore minimo

// Calcoli Finanziari
=B7/C7                    // Rapporto semplice (Margine)
=SE(B7>0, C7/B7, "N/D")  // Calcolo condizionale
=SE.ERRORE(C7/D7, 0)     // Gestione divisione per zero
```

### Formule Rapporti Comuni
```excel
Margine Lordo = Utile Lordo / Ricavi
Margine EBITDA = EBITDA / Ricavi
Margine FCF = Free Cash Flow / Ricavi
ROE = Utile Netto / Patrimonio Netto
ROIC = NOPAT / Capitale Investito
PFN/EBITDA = Posizione Finanziaria Netta / EBITDA
Dividend Yield = DPS / Prezzo Azione
```

---

## Principi Chiave — Riepilogo

1. **La struttura guida l'insight** — Le intestazioni giuste forzano il pensiero giusto
2. **Meno è meglio** — 5-10 metriche che contano battono 20 che non contano
3. **Scegliere le metriche per la domanda** — Analisi di valutazione ≠ analisi di efficienza
4. **Le statistiche mostrano pattern** — Mediana/quartili rivelano più della media
5. **Trasparenza batte complessità** — Formule semplici che tutti capiscono
6. **La confrontabilità è sovrana** — Meglio escludere che forzare un comparabile sbagliato
7. **Documentare le scelte** — Spiegare quali metriche e perché nella sezione note
8. **Contestualizzare per l'Italia** — Non applicare benchmark US a società italiane

---

## Checklist Output

Prima di consegnare un'analisi di comparabili, verificare:
- [ ] Tutte le società sono veramente comparabili (settore, dimensione, geografia)
- [ ] I dati provengono da periodi coerenti
- [ ] Le unità sono chiaramente indicate (EUR milioni)
- [ ] Le formule referenziano celle, non valori fissi
- [ ] **Tutti gli input fissi hanno commenti con: (1) fonte dati esatta, O (2) spiegazione assunzione**
- [ ] **Hyperlink aggiunti dove rilevante** (bilanci CONSOB, Borsa Italiana, report)
- [ ] Le statistiche includono almeno 5 metriche (Max, 75°, Med, 25°, Min)
- [ ] La sezione note documenta fonti e metodologia
- [ ] La formattazione visiva segue le convenzioni (blu = input, nero = formula)
- [ ] I sanity check passano (margini logici, multipli ragionevoli per contesto italiano)
- [ ] Il date stamp è corrente ("Al [Data]")
- [ ] L'auditing formule non mostra errori (#DIV/0!, #REF!, #N/D)
- [ ] **La PFN è definita chiaramente** (con/senza IFRS 16, con/senza TFR)
- [ ] **I multipli sono contestualizzati** per il mercato italiano/europeo (non confrontati con range US)
