---
name: fsi-3-statement-model-italy
description: Completamento e popolamento di template per modelli finanziari a 3 prospetti integrati (Conto Economico, Stato Patrimoniale, Rendiconto Finanziario) nel contesto italiano/IFRS. Attivare quando viene chiesto di compilare template di modello, completare framework esistenti, popolare modelli finanziari con dati da bilanci IFRS/OIC italiani, completare un framework IS/BS/CF parzialmente compilato, o collegare prospetti finanziari integrati. Include gestione TFR, IRES+IRAP, perdite fiscali art. 84 TUIR, IFRS 16 leasing, e convenzioni contabili italiane.
---

# Completamento Template Modello Finanziario a 3 Prospetti — Contesto Italiano/IFRS

Completare e popolare template di modelli finanziari integrati con linkage corretti tra Conto Economico, Stato Patrimoniale e Rendiconto Finanziario, adattati al contesto contabile e fiscale italiano.

**Differenze chiave rispetto al contesto US:**
- **Principi contabili**: IFRS per quotate, OIC per non quotate (non US GAAP)
- **Fonti dati**: CONSOB, Borsa Italiana, AIDA/Bureau van Dijk (non SEC EDGAR)
- **Imposte**: IRES 24% + IRAP 3.9% su basi imponibili diverse (non flat 21%)
- **TFR**: Passività specifica italiana per benefici ai dipendenti (IAS 19)
- **Perdite fiscali**: Art. 84 TUIR — riporto illimitato, limite utilizzo 80% (primi 3 esercizi 100%)
- **Leasing**: IFRS 16 capitalizza tutti i leasing (impatto su D&A, debito, oneri finanziari)
- **Goodwill**: IAS 36 — no ammortamento, impairment test annuale
- **Working capital**: DSO/DPO italiani 60-90 gg (vs 30-45 US)
- **Valuta**: EUR con separatori europei (punto migliaia, virgola decimali)

## ⚠️ PRINCIPI CRITICI — Leggere Prima di Popolare Qualsiasi Template

**Ambiente — Office JS vs Python:**
- **Se in esecuzione dentro Excel (Office Add-in / Office JS):** Usare Office JS direttamente. Scrivere formule via `range.formulas = [["=D14*(1+Assunzioni!$B$5)"]]` — mai `range.values` per celle derivate. Nessun ricalcolo separato; Excel calcola nativamente. Usare `context.workbook.worksheets.getItem(...)` per navigare i tab.
- **Se si genera un file .xlsx standalone:** Usare Python/openpyxl. Scrivere `ws["D15"] = "=D14*(1+Assunzioni!$B$5)"`, poi eseguire `recalc.py` prima della consegna.
- **Trappola merged cell in Office JS:** NON chiamare `.merge()` poi impostare `.values` sull'intervallo unito — lancia `InvalidArgument`. Scrivere il valore sulla cella in alto a sinistra, poi unire e formattare il range completo.
- Tutti i principi seguenti si applicano identicamente in entrambi gli ambienti.

**Formule sopra valori fissi (non negoziabile):**
- Ogni cella di proiezione, roll-forward, linkage e subtotale DEVE essere una formula Excel — mai un valore pre-calcolato
- Con Python/openpyxl: scrivere stringhe formula, NON risultati calcolati
- Le UNICHE celle che possono contenere numeri fissi sono: (1) dati storici effettivi, (2) driver di assunzione nel tab Assunzioni
- Il modello deve flettersi quando gli scenari si alternano o le assunzioni cambiano

**Verificare passo-passo con l'utente:**
1. **Dopo la mappatura del template** → mostrare all'utente quali tab/sezioni sono stati identificati e confermare prima di toccare celle
2. **Dopo il popolamento degli storici** → mostrare il blocco storico e confermare che valori/periodi corrispondano ai dati fonte
3. **Dopo la costruzione proiezioni CE** → eseguire i check subtotali, mostrare il CE proiettato, confermare prima di passare allo SP
4. **Dopo la costruzione SP** → mostrare il check di bilancio (Attivo = Passivo + PN) per ogni periodo, confermare prima di passare al RF
5. **Dopo la costruzione RF** → mostrare il cash tie-out (Cassa finale RF = Cassa SP), confermare prima di finalizzare
6. **NON popolare l'intero modello end-to-end** — procedere prospetto per prospetto, mostrare il lavoro, individuare errori presto

## Formattazione — Palette Blu/Grigio Professionale

**Mantenere i colori minimali.** Usare solo blu e grigio per i riempimenti cella.

| Elemento | Riempimento | Font |
|----------|-------------|------|
| Intestazioni sezione (CE / SP / RF) | Blu scuro `#1F4E79` | Bianco bold |
| Intestazioni colonna (FY2024A, FY2025E, ecc.) | Blu chiaro `#D9E1F2` | Nero bold |
| Celle input (storici, driver assunzioni) | Grigio chiaro `#F2F2F2` o bianco | Blu `#0000FF` |
| Celle formula | Bianco | Nero |
| Link cross-tab | Bianco | Verde `#008000` |
| Righe check / totali chiave | Blu medio `#BDD7EE` | Nero bold |

Il colore del font segnala *cosa* è una cella (input/formula/link). Il colore di riempimento segnala *dove* ci si trova (intestazione/dati/check).

## Struttura del Modello

### Identificare l'Organizzazione dei Tab del Template

I template variano nelle convenzioni di naming e organizzazione. Prima di popolare, rivedere tutti i tab per capire la struttura del template:

| Nomi Tab Comuni (IT) | Nomi Tab Comuni (EN) | Contenuto |
|----------------------|---------------------|-----------|
| CE, Conto Economico, P&L | IS, P&L, Income Statement | Conto Economico |
| SP, Stato Patrimoniale | BS, Balance Sheet | Stato Patrimoniale |
| RF, Rendiconto Finanziario | CF, CFS, Cash Flow | Rendiconto Finanziario |
| CCN, Capitale Circolante | WC, Working Capital | Schedule Capitale Circolante |
| D&A, Ammortamenti, PP&E | DA, D&A, Depreciation | Schedule Ammortamenti |
| Debito, Schedule Debito | Debt, Debt Schedule | Schedule Debito Finanziario |
| TFR | (n/a — specifico Italia) | Schedule TFR |
| Perdite Fiscali | NOL, Tax, DTA | Schedule Perdite Fiscali Riportabili |
| Assunzioni, Input, Driver | Assumptions, Inputs | Driver di assunzione e input |
| Controlli, Audit | Checks, Audit, Validation | Dashboard di controllo errori |

**Checklist Revisione Template:**
- Identificare quali tab esistono nel template (non tutti i template includono ogni schedule)
- Notare tab specifici non elencati sopra
- Comprendere le dipendenze tra tab (es. Assunzioni → CE → SP → RF)
- Localizzare celle input vs celle formula su ogni tab
- **Verificare se il template è in formato IFRS o OIC** — la struttura delle voci può differire

### Periodo di Proiezione
- I template tipicamente proiettano 5 anni in avanti dall'ultimo anno storico
- Verificare che le colonne storiche (A) vs proiettate (E) siano chiaramente separate
- Confermare che le colonne usino la notazione dell'esercizio fiscale (es. FY2024A, FY2025E)

## Analisi dei Margini

**Nota: L'analisi dei margini va eseguita solo se richiesta dall'utente o se il template la richiede esplicitamente.**

| Margine | Formula | Cosa Misura |
|---------|---------|-------------|
| Margine Lordo | Utile Lordo / Ricavi | Pricing power, efficienza produttiva |
| Margine EBITDA | EBITDA / Ricavi | Profittabilità operativa core |
| Margine EBIT | EBIT / Ricavi | Profittabilità operativa dopo D&A |
| Margine Utile Netto | Utile Netto / Ricavi | Profittabilità bottom-line |

## Metriche Creditizie

**Nota: L'analisi creditizia va eseguita solo se richiesta dall'utente o se il template la richiede esplicitamente.**

| Metrica | Formula | Cosa Misura |
|---------|---------|-------------|
| Debito Totale / EBITDA | Debito Totale / LTM EBITDA | Multiplo di leva |
| PFN / EBITDA | (Debito Totale - Cassa) / LTM EBITDA | Leva al netto della cassa |
| Interest Coverage | EBITDA / Oneri Finanziari | Capacità di servizio del debito |
| Debito / Cap. Totale | Debito Totale / (Debito Totale + PN) | Struttura del capitale |
| Debito / PN | Debito Totale / Patrimonio Netto | Leva finanziaria |
| Current Ratio | Attività Correnti / Passività Correnti | Liquidità a breve |
| Quick Ratio | (Attività Correnti - Rimanenze) / Passività Correnti | Liquidità immediata |

**Nota PFN italiana:** La Posizione Finanziaria Netta (PFN) è la metrica standard per la leva in Italia. Include: debiti finanziari correnti + non correnti - cassa - titoli a breve. Post IFRS 16, specificare se include o esclude le passività per leasing (ESMA raccomanda di includerle).

### Gerarchia Metriche Creditizie

Validare che lo scenario Upside mostri il profilo creditizio più forte:
- Leva: Upside < Base < Downside (più basso è meglio)
- Copertura: Upside > Base > Downside (più alto è meglio)
- Liquidità: Upside > Base > Downside (più alto è meglio)

## Analisi per Scenari (Base / Upside / Downside)

Usare un selettore scenario (dropdown) nel tab Assunzioni con formule CHOOSE o INDEX/MATCH.

| Scenario | Descrizione |
|----------|-------------|
| Caso Base | Guidance management o stime consensus |
| Caso Upside | Crescita sopra guidance, espansione margini |
| Caso Downside | Crescita sotto trend, compressione margini |

**Driver Chiave da Sensitizzare**: Crescita ricavi, Margine lordo, % Costi operativi, DSO/DIO/DPO, % CapEx, Tasso di interesse (Euribor + spread), Aliquota fiscale effettiva (IRES+IRAP).

## Estrazione Dati da Bilanci IFRS

Se il template richiede specificamente l'estrazione di dati da bilanci di società italiane (relazione annuale IFRS, bilancio d'esercizio OIC), vedere [references/consob-ifrs-filings.md](references/consob-ifrs-filings.md) per la guida dettagliata all'estrazione. Questo riferimento è necessario solo quando si popolano template con dati di società pubbliche da bilanci depositati.

## Completamento dei Template

### Step 1: Analizzare la Struttura del Template

Prima di inserire qualsiasi dato, rivedere a fondo il template per comprenderne l'architettura:

**Identificare Celle Input vs Formula**
- Cercare indicatori visivi (colore font, sfondo cella) che distinguano celle input da celle formula
- Convenzioni comuni: Font blu = input, Font nero = formule, Font verde = link ad altri fogli
- Usare Traccia Precedenti/Dipendenti per capire le relazioni tra celle
- Controllare intervalli denominati che possano controllare input chiave

**Mappare il Flusso del Template**
- Identificare quali tab alimentano gli altri (es. Assunzioni → CE → SP → RF)
- Notare eventuali schedule di supporto e i loro linkage ai prospetti principali
- Documentare le voci specifiche e la struttura del template prima di popolare
- **Verificare se include Schedule TFR** (specifico per società italiane)
- **Verificare trattamento leasing** (IFRS 16 vs operating lease off-balance pre-IFRS 16)

### Step 2: Inserimento Dati Senza Rompere le Formule

**Regole d'Oro per l'Inserimento Dati**

| Regola | Descrizione |
|--------|-------------|
| Modificare solo celle input | Non sovrascrivere mai celle contenenti formule salvo sostituzione intenzionale |
| Preservare i riferimenti | Quando si copiano dati, usare Incolla Valori per evitare di sovrascrivere formule |
| Rispettare le unità del template | Verificare se il template usa migliaia, milioni o valori effettivi |
| Rispettare le convenzioni di segno | Seguire la convenzione di segno esistente del template |
| Controllare riferimenti circolari | Se il template usa calcoli iterativi, assicurarsi che il calcolo iterativo sia abilitato |

**Processo di Inserimento Dati Sicuro**
1. Identificare le celle esatte designate per l'input
2. Inserire prima i dati storici, poi verificare che le formule calcolino correttamente
3. Inserire i driver di assunzione che alimentano i calcoli previsionali
4. Rivedere gli output calcolati per confermare che le formule funzionino

### Step 3: Validazione Formule

**Controlli di Integrità Formula**

| Tipo Check | Metodo |
|------------|--------|
| Traccia precedenti | Verificare che la formula referenzi gli input corretti |
| Traccia dipendenti | Verificare che gli input chiave fluiscano alle celle output attese |
| Valuta formula | Usare Valuta Formula per percorrere calcoli complessi |
| Check valori fissi | Le formule di proiezione devono referenziare le assunzioni, non contenere valori fissi |
| Test con valori noti | Inserire valori test semplici per verificare risultati attesi |
| Coerenza cross-tab | Assicurarsi che la stessa logica formula si applichi a tutti i periodi |

### Step 4: Controlli di Qualità per Prospetto

**Conto Economico — Controlli Qualità**
- I ricavi corrispondono ai dati fonte per i periodi storici
- Tutte le voci di costo sommano ai totali riportati
- I subtotali (Utile Lordo, EBIT, EBT, Utile Netto) calcolano correttamente
- La logica fiscale è appropriata:
  - **IRES**: 24% sul reddito imponibile (con aggiustamenti fiscali)
  - **IRAP**: 3.9% sul valore della produzione netta (base imponibile diversa — non deducibili interessi e costo del lavoro)
  - Verificare che il modello gestisca le perdite correttamente (IRES e IRAP separatamente)
- I driver previsionali referenziano il tab assunzioni (nessun valore fisso)
- Le variazioni periodo-su-periodo sono direzionalmente ragionevoli

**Stato Patrimoniale — Controlli Qualità**
- **Attivo = Passivo + Patrimonio Netto** per ogni periodo (check primario)
- La cassa corrisponde alla cassa finale del Rendiconto Finanziario
- Le voci di capitale circolante legano alle schedule di supporto
- Gli utili portati a nuovo si sviluppano correttamente: UPN prec. + Utile Netto - Dividendi +/- Rettifiche = UPN finale
- I debiti finanziari legano alla schedule debito
- **Il TFR lega alla schedule TFR** (specifico Italia)
- **Le passività per leasing legano alla schedule IFRS 16** (se applicabile)
- Tutti gli elementi hanno segni appropriati

**Rendiconto Finanziario — Controlli Qualità**
- L'Utile Netto in testa al CFO corrisponde all'Utile Netto del CE
- Gli add-back non monetari (D&A, SBC, accantonamento TFR) legano alle fonti
- Le variazioni di capitale circolante hanno segni corretti (aumento attivo = uso cassa = negativo)
- CapEx lega alla schedule PP&E
- Le attività di finanziamento legano alle variazioni di debito e equity dello SP
- **I pagamenti TFR sono in CFO** (non CFF)
- **I pagamenti leasing IFRS 16 (quota capitale) sono in CFF, gli interessi in CFO**
- La Cassa Finale corrisponde alla Cassa dello SP
- La Cassa Iniziale equivale alla Cassa Finale del periodo precedente

### Step 5: Controlli di Integrità Cross-Prospetto

| Check | Formula | Risultato Atteso |
|-------|---------|-----------------|
| Bilancio SP | Attivo - Passivo - PN | = 0 |
| Cash Tie-Out | Cassa Finale RF - Cassa SP | = 0 |
| Link Utile Netto | UN dal CE - UN iniziale RF | = 0 |
| Utili Portati a Nuovo | UPN prec. + UN - Dividendi - UPN SP finale | = 0 |
| TFR Tie-Out | TFR Schedule - TFR SP | = 0 |

### Step 6: Revisione Finale

Prima di considerare il modello completo:
- Alternare tutti gli scenari (se applicabile) per verificare che i check passino in ogni caso
- Rivedere tutti gli errori #REF!, #DIV/0!, #VALUE!, #NAME? e risolvere o documentare
- Confermare che tutte le celle input siano state popolate
- Verificare che le unità siano coerenti su tutti i tab (€ milioni)
- **Verificare che l'aliquota fiscale rifletta IRES+IRAP (~27.9%), non l'aliquota US (21%)**
- **Verificare che il TFR sia trattato correttamente (accantonamento in CE/CFO, stock in SP)**
- Salvare una versione pulita prima di ulteriori modifiche

## Validazione e Audit del Modello

### Linkage Fondamentali (Devono Sempre Valere)

Vedere [references/formulas.md](references/formulas.md) per tutti i dettagli sulle formule.

| Check | Formula | Risultato Atteso |
|-------|---------|-----------------|
| Bilancio SP | Attivo - Passivo - PN | = 0 |
| Cash Tie-Out | Cassa SP - Cassa Finale RF | = 0 |
| Link Utile Netto | UN CE - UN iniziale RF | = 0 |
| Utili Portati a Nuovo | UPN prec. + UN - Dividendi - UPN SP | = 0 |
| Finanziamento Equity | ΔCapitale/Sovrapprezzo (SP) - Emissione (CFF) | = 0 |
| TFR Tie-Out | TFR Schedule - TFR SP | = 0 |
| IFRS 16 Tie-Out | Passività Leasing Schedule - Passività Leasing SP | = 0 |

### Convenzione Segni

| Prospetto | Voce | Convenzione Segno |
|-----------|------|-------------------|
| CFO | D&A, SBC, Acc. TFR | Positivo (add-back) |
| CFO | ΔCrediti commerciali (aumento) | Negativo (uso cassa) |
| CFO | ΔDebiti commerciali (aumento) | Positivo (fonte cassa) |
| CFO | Pagamenti TFR | Negativo (uso cassa) |
| CFI | CapEx | Negativo |
| CFF | Accensione debiti | Positivo |
| CFF | Rimborso debiti | Negativo |
| CFF | Pagamento canoni leasing IFRS 16 (quota capitale) | Negativo |
| CFF | Dividendi | Negativo |

### Gestione Riferimenti Circolari

Gli oneri finanziari creano circolarità: Interessi → Utile Netto → Cassa → Saldo Debito → Interessi

Abilitare calcolo iterativo in Excel: File → Opzioni → Formule → Abilita calcolo iterativo. Impostare iterazioni massime a 100, variazione massima a 0,001. Aggiungere un interruttore nel tab Assunzioni.

### Categorie di Check

**Sezione 1: Coerenza Valuta**
- Valuta identificata e documentata nelle Assunzioni (EUR)
- Tutti i tab usano simbolo e scala valuta coerenti
- La riga unità corrisponde alla valuta del modello

**Sezione 2: Integrità Stato Patrimoniale**
- Attivo = Passivo + PN (per ogni periodo)

**Sezione 3: Integrità Rendiconto Finanziario**
- Cassa lega allo SP (Cassa Finale RF = Cassa SP)
- UN lega al CE (UN RF = UN CE)
- D&A lega alla schedule
- Variazioni CCN legano alla schedule
- CapEx lega alla schedule D&A
- **Accantonamento e pagamenti TFR legano alla schedule TFR**
- **Pagamenti leasing IFRS 16 separati correttamente (interessi in CFO, capitale in CFF)**

**Sezione 4: Utili Portati a Nuovo**
- Check roll-forward UPN: UPN prec. + UN - Dividendi = UPN finale
- Mostrare scomposizione componenti per debugging

**Sezione 5: Capitale Circolante**
- Crediti, Rimanenze, Debiti legano allo SP
- Check ragionevolezza DSO, DIO, DPO:
  - **DSO Italia**: 60-90 giorni (segnalare se fuori range)
  - **DPO Italia**: 60-75 giorni (segnalare se fuori range)
  - DIO: dipende dal settore

**Sezione 6: Schedule Debito**
- Debito Totale lega allo SP (Corrente + Non Corrente)
- Calcolo interessi lega al CE
- **Costo del debito coerente con Euribor + spread** (non SOFR/LIBOR)

**Sezione 6b: Schedule TFR (Specifico Italia)**
- Fondo TFR SP = Fondo TFR Schedule
- Accantonamento TFR nel CE coerente con la dimensione dell'organico
- Pagamenti TFR nel RF coerenti con turnover del personale
- Per aziende >50 dipendenti: la maggior parte del TFR maturando va a INPS/fondi pensione

**Sezione 6c: Perdite Fiscali (Art. 84 TUIR)**
- Saldo iniziale perdite (Anno 1 / Costituzione) = 0 (nuova società parte con zero perdite)
- Le perdite aumentano solo quando il reddito imponibile IRES < 0
- DTA lega allo SP (DTA Schedule = DTA SP)
- Utilizzo perdite ≤ 80% del reddito imponibile (limite generale art. 84 TUIR)
- **Eccezione**: perdite dei primi 3 esercizi utilizzabili al 100%
- Saldo perdite non negativo
- **IRAP**: perdite IRAP seguono regole proprie, separate da perdite IRES
- Imposte = 0 quando reddito tassabile ≤ 0

**Sezione 7: Gerarchia Scenari**
- Metriche assolute: Upside > Base > Downside (UN, EBITDA, FCF)
- Margini: Upside > Base > Downside
- Metriche creditizie: Upside < Base < Downside per la leva (invertite)

**Sezione 8: Integrità Formula**
- COGS, Costi commerciali, G&A, R&D guidati da % dei Ricavi (nessun valore fisso)
- Formule coerenti attraverso gli anni di proiezione
- Nessun errore #REF!, #DIV/0!, #VALUE!
- **Aliquota fiscale ~27.9% (IRES 24% + IRAP 3.9%), NON 21%**

### Formula Check Master

Aggregare tutti gli stati delle sezioni in un unico check master:
- Se tutte le sezioni passano → "✓ TUTTI I CHECK SUPERATI"
- Se qualsiasi sezione fallisce → "✗ ERRORI RILEVATI - VERIFICARE SOTTO"

### Workflow di Debug Rapido

Quando lo Status Master mostra errori:
1. Scorrere per trovare le sezioni evidenziate in rosso
2. Identificare quale categoria di check ha fallimenti
3. Navigare al tab fonte per investigare
4. Correggere il problema sottostante
5. Tornare al tab Controlli per verificare la risoluzione
