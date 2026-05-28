---
name: fsi-initiating-coverage-italy
description: Creazione di report di initiation coverage di qualità istituzionale per società quotate su Borsa Italiana e borse europee, attraverso un workflow a 5 task. I task devono essere eseguiti singolarmente con prerequisiti verificati — (1) ricerca qualitativa, (2) modellistica finanziaria IFRS, (3) analisi di valutazione con WACC italiano, (4) generazione grafici, (5) assemblaggio report finale. Ogni task produce deliverable specifici. Adattato al contesto italiano: bilanci IFRS, fonti CONSOB/Borsa Italiana, WACC con BTP/ERP/Euribor, aliquota IRES+IRAP, comparabili europei.
---

# Initiating Coverage — Contesto Italiano/Europeo

Creazione di report di initiation coverage di qualità istituzionale per società quotate su Borsa Italiana e borse europee, attraverso un workflow strutturato a 5 task. Ogni task deve essere eseguito separatamente con prerequisiti verificati.

## Panoramica

Questo skill produce report di prima copertura seguendo standard istituzionali (JPMorgan, Goldman Sachs, Morgan Stanley, Mediobanca, Intesa Sanpaolo IMI, Equita). I task vengono eseguiti singolarmente, ciascuno verificando i prerequisiti prima di procedere.

**Differenze chiave rispetto al contesto US:**
- **Fonti dati**: CONSOB, Borsa Italiana, Bureau van Dijk/AIDA (non SEC EDGAR, 10-K/10-Q)
- **Principi contabili**: IFRS obbligatorio per quotate (non US GAAP)
- **WACC**: BTP 10Y, ERP italiano 6-8%, Euribor (non Treasury, ERP 5-6%, SOFR)
- **Fiscalità**: IRES 24% + IRAP 3,9% = ~27,9% (non 21% US)
- **Terminal growth**: 1,0-2,0% (non 2,5-3,5% US)
- **Valuta**: EUR con formattazione europea
- **Mercato**: ~350 quotate su Borsa Italiana (FTSE MIB, Mid Cap, STAR, EGM)
- **Governance**: CdA + Collegio Sindacale, frequente azionista di controllo
- **Comparabili**: peer italiani + europei (non US)

**LEGGERE PRIMA**: Il file [references/italy-context.md](references/italy-context.md) contiene tutti gli adattamenti specifici per ogni task. Caricarlo prima di iniziare qualsiasi task.

**Font di default**: Times New Roman per tutti i documenti (salvo diversa indicazione dell'utente).

---

## ⚠️ CRITICO: Un Task alla Volta

**QUESTO SKILL OPERA IN MODALITÀ SINGOLO TASK.**

### Se l'Utente Richiede la Pipeline Completa

Quando l'utente richiede:
- "Crea un report di initiation per [Società]"
- "Scrivi un report di coverage per [Società]"
- "Fai l'intero processo di equity research per [Società]"
- Qualsiasi richiesta che implichi eseguire più task

**RISPOSTA OBBLIGATORIA:**

1. **Chiedere quale task specifico eseguire:**
   ```
   Posso aiutarti a creare un report di initiation coverage per [Società].
   Questo prevede 5 task separati da completare individualmente:

   1. Ricerca Qualitativa — Business, management, settore, rischi
   2. Modellistica Finanziaria — Modello con proiezioni da bilancio IFRS
   3. Analisi di Valutazione — DCF (WACC italiano) e comparabili europei
   4. Generazione Grafici — 25-35 grafici professionali
   5. Assemblaggio Report — Report finale 30-50 pagine

   Con quale task vuoi iniziare?
   ```

2. **Mai eseguire automaticamente più task** — completare un task, consegnare, attendere.

### Regole di Esecuzione Task

- ✅ Eseguire esattamente UN task per richiesta utente
- ✅ Sempre verificare i prerequisiti prima di iniziare
- ✅ Consegnare gli output del task e confermare il completamento
- ✅ Attendere che l'utente richieda esplicitamente il task successivo
- ✅ **Caricare references/italy-context.md** prima di ogni task
- ❌ Mai concatenare più task automaticamente
- ❌ Mai assumere che l'utente voglia procedere al task successivo
- ❌ Mai eseguire Task 3-5 senza verificare che gli input richiesti esistano

### ⚠️ Politica Deliverable: NESSUNA SCORCIATOIA

**CONSEGNARE SOLO GLI OUTPUT SPECIFICATI. NON CREARE DOCUMENTI EXTRA.**

- ✅ Task 1: Documento di ricerca (.md) — **NIENT'ALTRO**
- ✅ Task 2: Modello finanziario (.xlsx) — **NIENT'ALTRO**
- ✅ Task 3: Analisi di valutazione (.md) + tab Excel aggiunti al file Task 2 — **NIENT'ALTRO**
- ✅ Task 4: File zip grafici (.zip) — **NIENT'ALTRO**
- ✅ Task 5: Report finale (.docx) — **NIENT'ALTRO**

---

## Selezione Task

| Task | Nome | Prerequisiti | Output |
|------|------|-------------|--------|
| **1** | Ricerca Qualitativa | Nome/ticker società | Documento 6-8K parole |
| **2** | Modellistica Finanziaria | Bilancio IFRS o dati finanziari | Modello Excel (6 tab) |
| **3** | Analisi di Valutazione | Modello finanziario (Task 2) | Valutazione + prezzo target |
| **4** | Generazione Grafici | Task 1, 2, 3 + dati esterni | 25-35 grafici PNG/JPG |
| **5** | Assemblaggio Report | TUTTI i task precedenti (1-4) | Report DOCX 30-50 pagine |

---

## Ordine di Esecuzione Task

```
Richiesta 1: Task 1 — Ricerca Qualitativa (indipendente)
             ↓ [L'utente rivede e richiede il task successivo]
Richiesta 2: Task 2 — Modellistica Finanziaria (indipendente)
             ↓ [L'utente rivede e richiede il task successivo]
Richiesta 3: Task 3 — Analisi di Valutazione (richiede Task 2)
             ↓ [L'utente rivede e richiede il task successivo]
Richiesta 4: Task 4 — Generazione Grafici (richiede Task 2 & 3)
             ↓ [L'utente rivede e richiede il task successivo]
Richiesta 5: Task 5 — Assemblaggio Report (richiede TUTTI i task 1-4)
```

**Nota**: I Task 1 e 2 possono essere eseguiti in qualsiasi ordine. I Task 3-5 hanno dipendenze strette.

---

## Task 1: Ricerca Qualitativa

**Scopo**: Ricercare il business dell'azienda, il management, la posizione competitiva, il settore e i rischi.

**Prerequisiti**: ✅ Nessuno (completamente indipendente)
- Nome società o ticker (es. ENEL.MI, ISP.MI, UCG.MI)

**Processo**:
1. Verificare nome/ticker fornito
2. **Caricare references/italy-context.md** per le fonti dati italiane
3. Eseguire il workflow di ricerca qualitativa
4. Consegnare il documento di ricerca

**Fonti dati specifiche Italia:**
- CONSOB → comunicazioni, partecipazioni, prospetti
- Borsa Italiana → scheda società, bilanci, prezzi
- Relazione sul governo societario → governance, CdA, Collegio Sindacale
- Relazione sulla remunerazione → compensi management
- AIDA/Bureau van Dijk → bilanci strutturati, confronti settoriali

**Output**: Documento di Ricerca (6.000-8.000 parole)
- Panoramica società e storia
- Biografie management (300-400 parole × 3-4 dirigenti) + struttura governance italiana
- Analisi prodotti e servizi
- Panoramica settore (contesto italiano/europeo)
- Analisi competitiva (5-10 concorrenti, italiani + europei)
- Dimensionamento TAM (mercato italiano + europeo + globale)
- Valutazione rischi (8-12 rischi, includendo rischi regolatori italiani)

**Sezioni aggiuntive per contesto italiano:**
- **Governance**: modello (tradizionale/monistico/dualistico), Collegio Sindacale, azionista di controllo, patti parasociali
- **Contesto regolatorio**: regolatori settoriali rilevanti (CONSOB, Banca d'Italia, AGCM, ARERA, AGCOM)
- **ESG**: rating ESG, classificazione SFDR, obiettivi sostenibilità

**File name**: `[Società]_Research_Document_[Data].md`

**⚠️ CONSEGNARE SOLO QUESTO 1 FILE. Nessun riassunto di completamento, nessun documento extra.**

---

## Task 2: Modellistica Finanziaria

**Scopo**: Estrarre dati storici da bilanci IFRS e costruire un modello finanziario Excel completo con proiezioni e scenari.

**Prerequisiti**: ⚠️ Verificare prima di iniziare
- **Obbligatorio**: Accesso ai dati finanziari della società
  - Per società quotate: **Bilancio consolidato IFRS** (Relazione annuale) da CONSOB/Borsa Italiana
  - Per società non quotate: Bilancio OIC da Registro Imprese o dati disponibili
  - OPPURE: Dati storici pre-estratti forniti dall'utente
- **Opzionale**: Ricerca qualitativa (Task 1) per contesto

**Verifica Input**:
```
PRIMA DI INIZIARE — Selezionare approccio:

Opzione A: Estrarre dati dal bilancio (più comune)
- [ ] Accesso al bilancio consolidato IFRS (relazione annuale)?
- [ ] Pronti a estrarre 3-5 anni di dati?

Opzione B: Dati pre-estratti forniti dall'utente
- [ ] File con dati storici ricevuto?
- [ ] Contiene CE, SP, RF (3-5 anni)?

Opzionale:
- [ ] Ricerca qualitativa (Task 1) completata?
```

**Processo**:
1. Verificare accesso ai dati finanziari
2. **Caricare references/italy-context.md** per gli adattamenti IFRS
3. **Step 1**: Estrarre dati storici dal bilancio IFRS (se necessario)
4. **Step 2+**: Costruire modello con 6 tab essenziali
5. Consegnare modello Excel

**Note IFRS critiche per il modello:**
- **TFR**: modellare come passività separata (IAS 19), accantonamento in CFO
- **IFRS 16**: RoU assets in PP&E, passività leasing separate, D&A + interessi
- **Goodwill**: no ammortamento, impairment test annuale (IAS 36)
- **Imposte**: IRES 24% + IRAP 3,9% su basi imponibili diverse
- **Working capital**: DSO 60-90 gg, DPO 60-75 gg (più lunghi che US)

**Output**: Modello Finanziario Excel (.xlsx) — 6 tab:
1. **Revenue Model** — Breakdown per prodotto (20-30 righe) + Geografia (Italia/Europa/Global)
2. **Income Statement** — P&L completo IFRS con 40-50 voci, storico (3-5 anni) + proiezioni (5 anni)
3. **Cash Flow Statement** — CFO/CFI/CFF, storico + proiezioni (include TFR, IFRS 16)
4. **Balance Sheet** — Attivo/Passivo/PN IFRS, storico + proiezioni
5. **Scenarios** — Tabella comparativa Bull/Base/Bear
6. **DCF Inputs** — Preparato per Task 3 con **parametri WACC italiani**

**File name**: `[Società]_Financial_Model_[Data].xlsx`

**⚠️ CONSEGNARE SOLO QUESTO 1 FILE.**

---

## Task 3: Analisi di Valutazione

**Scopo**: Eseguire valutazione completa usando DCF (WACC italiano), comparabili europei e transazioni precedenti.

**Prerequisiti**: ⚠️ Verificare prima di iniziare
- **Obbligatorio**: Modello finanziario dal Task 2
- **⚠️ CRITICO: NON INIZIARE SE IL TASK 2 NON È COMPLETO**

**Processo**:
1. Verificare che il modello finanziario sia accessibile
2. **Caricare references/italy-context.md** per parametri WACC e multipli italiani
3. Eseguire workflow di valutazione con parametri italiani
4. Consegnare analisi di valutazione

**Parametri WACC Italia (NON usare parametri US):**
- Risk-Free: BTP 10Y (~3,5-4,5%), NON Treasury US
- ERP: 6,0-8,0% (include CRP italiano), NON 5,0-5,5%
- Beta: vs FTSE MIB o EURO STOXX 50
- Costo debito: Euribor 6M + spread, NON SOFR
- Aliquota: ~27,9% (IRES+IRAP), NON 21%
- Terminal growth: 1,0-2,0%, NON 2,5-3,5%

**Comparabili:**
- 5-10 peer, mix italiano + europeo
- Multipli: EV/Ricavi, EV/EBITDA, P/E, P/BV, Dividend Yield
- Range italiani: EV/EBITDA 6-15x, P/E 8-25x (più bassi che US)
- Nota "discount italiano" (~10-20% vs peer europei core)
- **PFN** per Enterprise Value (con nota IFRS 16)

**Settori speciali:**
- **Banche**: usare DDM / Excess Return Model, NON DCF standard. Metriche: ROE, P/BV, CET1
- **Utilities regolate**: considerare EV/RAB
- **Concessioni**: DCF su durata concessione residua

**Output**: Analisi di Valutazione (4-6 pagine + tab Excel)
- DCF con sensitivity tables (WACC italiano)
- Comparabili europei (5-10 peer con riepilogo statistico)
- Transazioni precedenti (se applicabile, fonti: Mergermarket, BvD Zephyr)
- Valuation football field
- **Prezzo target**: €XX,XX
- **Raccomandazione**: COMPRARE / MANTENERE / VENDERE
- **Upside**: XX%
- Catalizzatori chiave (3-5, includere specifici italiani)

**Files**:
- `[Società]_Valuation_Analysis_[Data].md`
- Tab Excel aggiunti a `[Società]_Financial_Model_[Data].xlsx`:
  - Tab DCF con calcoli (parametri italiani)
  - Tab Sensitivity analysis
  - Tab Comparable companies (peer europei)
  - Tab Valuation summary

**⚠️ CONSEGNARE SOLO: 1 file markdown + 4 tab aggiunti all'Excel esistente.**

---

## Task 4: Generazione Grafici

**Scopo**: Generare 25-35 grafici finanziari professionali per il report.

**Prerequisiti**: ⚠️ Verificare prima di iniziare
- **Obbligatorio**: Ricerca da Task 1 + Modello da Task 2 (con tab Task 3)
- **Obbligatorio**: Dati di mercato esterni
- **⚠️ CRITICO: NON INIZIARE SE I TASK 1, 2, E 3 NON SONO COMPLETI**

**Adattamenti per grafici italiani:**
- chart_01 (Stock price): prezzo in EUR, benchmark FTSE MIB (non S&P 500)
- chart_04 (Revenue by geography): focus Italia/Europa/Global
- chart_28 (DCF sensitivity): WACC 8-13%, terminal growth 0,5-2,5%
- chart_30 (Comps): peer europei, multipli in range italiano
- chart_32 (Football field): prezzo target in EUR
- chart_34 (Historical multiples): vs FTSE MIB / settore italiano

**Fonti dati per grafici:**
- Prezzo storico: Borsa Italiana, Refinitiv, Bloomberg (non Yahoo Finance US)
- Benchmark: FTSE MIB, EURO STOXX 50 (non S&P 500, Nasdaq)
- Multipli storici: Refinitiv, Bloomberg consensus

**Output**: 25-35 file grafici professionali (PNG/JPG, 300 DPI) in zip

**4 grafici OBBLIGATORI** ⭐:
- chart_03: Ricavi per prodotto (stacked area)
- chart_04: Ricavi per area geografica (stacked bar)
- chart_28: DCF sensitivity (heatmap 2-way)
- chart_32: Valuation football field (barre orizzontali)

**File name**: `[Società]_Charts_[Data].zip`

**⚠️ CONSEGNARE SOLO QUESTO 1 FILE ZIP.**

---

## Task 5: Assemblaggio Report

**Scopo**: Scrivere e assemblare il report finale DOCX completo.

**Prerequisiti**: ⚠️ Verificare prima di iniziare
- **Obbligatorio**: TUTTI i task 1-4 completi
- **⚠️ CRITICO: NON INIZIARE SE QUALSIASI TASK 1-4 NON È COMPLETO**

**Processo**:
1. **CRITICO**: Verificare TUTTI i prerequisiti
2. **Caricare references/italy-context.md** per disclaimer CONSOB e adattamenti report
3. Assemblare report usando skill DOCX e XLSX
4. Includere tutti i 25-35 grafici dal Task 4
5. Aggiungere disclaimer CONSOB
6. Salvare e consegnare report finale

**Adattamenti report per contesto italiano:**
- Valuta: tutti i valori in EUR
- Governance: sezione dedicata (CdA, Collegio Sindacale, azionista di controllo)
- WACC: mostrare calcolo completo con parametri italiani
- Comparabili: tabella con peer europei
- Disclaimer: conformità CONSOB (non SEC)
- ESG/Sostenibilità: sezione dedicata se rilevante

**Output**: Report Equity Research Completo (.docx)

**Specifiche**:
- **Lunghezza**: 30-50 pagine (MINIMO 30)
- **Word count**: 10.000-15.000 parole (MINIMO 10.000)
- **Grafici**: 25-35 immagini embedded
- **Tabelle**: 12-20 tabelle complete
- **Formato**: DOCX professionale con hyperlink cliccabili

**Struttura**:
- Pagina 1: Investment Summary (formato INITIATING COVERAGE)
- Pagine 2-5: Tesi di investimento & rischi
- Pagine 6-17: Company 101 (include governance italiana)
- Pagine 18-30: Analisi finanziaria & proiezioni (IFRS, IRES+IRAP)
- Pagine 31-40: Analisi di valutazione (WACC italiano, comps europei)
- Pagine 41-50: Appendici + disclaimer CONSOB

**File name**: `[Società]_Initiation_Report_[Data].docx`

**⚠️ CONSEGNARE SOLO QUESTO 1 FILE DOCX.**

**🔥 CRITICO: QUESTO È IL DELIVERABLE FINALE. NESSUNA SCORCIATOIA.**
- ✅ Scrivere ogni sezione completamente
- ✅ Raggiungere TUTTI i requisiti minimi
- ✅ Inserire TUTTI i grafici dal Task 4
- ✅ Creare TUTTE le tabelle da Task 2/3
- ✅ Qualità professionale — indistinguibile da research Mediobanca/JPMorgan

---

## Standard di Qualità

Tutti gli output soddisfano standard istituzionali:

- **Completi**: Raggiungere tutti i requisiti minimi
- **Dettagliati**: Dati specifici ed esempi, non affermazioni generiche
- **Quantificati**: Guidare con numeri e metriche
- **Citati**: Fonti appropriate con hyperlink (CONSOB, Borsa Italiana, bilanci)
- **Professionali**: Formattazione di qualità istituzionale
- **Accurati**: Tutti i numeri verificati e cross-checked
- **Contestualizzati**: Parametri e benchmark italiani/europei (non US)

---

## Note Importanti

### Indipendenza dei Task
- **Task 1** può essere eseguito in qualsiasi momento
- **Task 2** può essere eseguito in qualsiasi momento (necessita solo dati storici)
- **Task 1 & 2** possono essere eseguiti in parallelo
- **Task 3** richiede Task 2
- **Task 4** richiede Task 2 & 3
- **Task 5** richiede Task 1, 2, 3 & 4

### File di Riferimento

Istruzioni dettagliate per ogni task nei file di riferimento:

- **references/italy-context.md** — ⚠️ CARICARE SEMPRE — Adattamenti italiani per tutti i task
- Per il workflow dettagliato di ogni task, fare riferimento ai reference files dello skill US `initiating-coverage` (la meccanica del workflow è identica, solo il contesto finanziario cambia)

### Criteri di Successo

Un workflow di initiation report di successo deve:
1. Completare tutti i 5 task in ordine
2. Passare tutte le verifiche input
3. Soddisfare tutti gli standard di qualità
4. **Usare parametri WACC italiani** (BTP, ERP 6-8%, Euribor)
5. **Usare aliquota ~27,9%** (IRES+IRAP), non 21%
6. **Usare terminal growth 1,0-2,0%**, non 2,5-3,5%
7. **Usare fonti CONSOB/Borsa Italiana**, non SEC EDGAR
8. **Usare principi contabili IFRS**, non US GAAP
9. **Usare comparabili europei**, non US
10. Il report finale deve essere publication-ready
