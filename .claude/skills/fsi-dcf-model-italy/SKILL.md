---
name: fsi-dcf-model-italy
description: Modello DCF (Discounted Cash Flow) per la valutazione di società quotate e non quotate nel contesto italiano/europeo. Recupera dati finanziari da bilanci IFRS (CONSOB, Borsa Italiana, Bureau van Dijk), costruisce proiezioni di cash flow con WACC calcolato su parametri italiani (BTP 10Y, ERP italiano, Euribor), esegue analisi di sensitività e produce modelli Excel professionali. Attivare quando l'utente chiede una valutazione DCF, un'analisi del valore intrinseco, o un modello finanziario dettagliato con proiezioni di crescita e terminal value per società italiane o europee.
---

# DCF Model Builder — Contesto Italiano/Europeo

## Panoramica

Questo skill crea modelli DCF di qualità istituzionale per la valutazione azionaria secondo standard di investment banking, adattati al contesto italiano ed europeo. Ogni analisi produce un modello Excel dettagliato (con analisi di sensitività inclusa in fondo al foglio DCF).

**Differenze chiave rispetto al contesto US:**
- **Principi contabili**: IFRS (non US GAAP) — impatto su goodwill, leasing, revenue recognition
- **WACC**: risk-free rate su BTP 10Y, ERP italiano (6-8%), costo del debito su Euribor
- **Aliquota fiscale**: IRES 24% + IRAP ~3.9% = ~27.9% (non flat 21% US)
- **Terminal growth**: PIL Eurozona/Italia (~1-2%, non 2.5-3.5% US)
- **Fonti dati**: CONSOB, Borsa Italiana, Bureau van Dijk/AIDA (non SEC EDGAR)
- **Valuta**: EUR con separatori europei
- **Working capital**: DSO/DPO italiani più lunghi (60-90 gg vs 30-45 US)

## Strumenti

- Utilizzare tutte le informazioni fornite dall'utente e i server MCP disponibili per il sourcing dati.

## Vincoli Critici — Leggere Prima di Iniziare

Questi vincoli si applicano a tutto il processo di costruzione del DCF. Rivedere prima di iniziare:

**Ambiente: Office JS vs Python/openpyxl:**
- **Se in esecuzione dentro Excel (Office Add-in / Office JS):** Usare Office JS direttamente — NON usare Python/openpyxl. Scrivere formule via `range.formulas = [["=D19*(1+$B$8)"]]`. Nessun passo di ricalcolo necessario; Excel calcola nativamente. Usare `range.format.*` per lo stile. La stessa regola formule-sopra-valori-fissi si applica: impostare `.formulas`, mai `.values` per celle derivate.
- **Se si genera un file .xlsx standalone (nessuna sessione Excel attiva):** Usare Python/openpyxl come descritto sotto, poi eseguire `recalc.py` prima della consegna.
- Il resto di questo skill usa esempi openpyxl — tradurre in chiamate Office JS API quando nell'ambiente corrispondente, ma tutti i principi (stringhe formula, commenti cella, checkpoint di sezione, loop sensitivity table) si applicano identicamente.

**⚠️ Trappola merged cell in Office JS:** Quando si costruiscono intestazioni di sezione con celle unite, NON chiamare `.merge()` poi impostare `.values` sull'intervallo unito — Office JS riporta ancora le dimensioni originali dell'intervallo e lancia `InvalidArgument: The number of rows or columns in the input array doesn't match the size or dimensions of the range`. Invece, scrivere il valore sulla cella in alto a sinistra da sola, poi unire e formattare l'intervallo completo:

```js
// SBAGLIATO — lancia InvalidArgument:
const hdr = ws.getRange("A7:H7");
hdr.merge();
hdr.values = [["DATI DI MERCATO & INPUT CHIAVE"]];  // array 1×1 vs range 1×8 → errore

// CORRETTO — valore prima sulla singola cella, poi merge + formato sul range:
ws.getRange("A7").values = [["DATI DI MERCATO & INPUT CHIAVE"]];
const hdr = ws.getRange("A7:H7");
hdr.merge();
hdr.format.fill.color = "#1F4E79";
hdr.format.font.bold = true;
hdr.format.font.color = "#FFFFFF";
```

**Formule Sopra Valori Fissi (NON NEGOZIABILE):**
- Ogni proiezione, margine, fattore di sconto, PV e cella di sensitività DEVE essere una formula Excel viva — mai un valore calcolato in Python e scritto come numero
- Con openpyxl: `ws["D20"] = "=D19*(1+$B$8)"` è corretto; `ws["D20"] = calculated_revenue` è SBAGLIATO
- Gli unici numeri fissi permessi sono: (1) input storici grezzi, (2) driver di assunzione (tassi di crescita, input WACC, terminal g), (3) dati di mercato attuali (prezzo azione, debito)
- Se ci si ritrova a calcolare qualcosa in Python e scrivere il risultato — FERMARSI. Il modello deve flettersi quando l'utente cambia un'assunzione.

**Verificare Passo-Passo Con l'Utente (NON costruire end-to-end):**
- Dopo il recupero dati → mostrare all'utente il blocco input grezzi (ricavi, margini, azioni, posizione finanziaria netta) e confermare prima di proiettare
- Dopo le proiezioni di ricavo → mostrare il top line proiettato e i tassi di crescita, confermare prima di costruire il margine
- Dopo il build FCF → mostrare l'intero prospetto FCF, confermare la logica prima di calcolare il WACC
- Dopo il WACC → mostrare il calcolo e gli input, confermare prima dello sconto
- Dopo terminal value + PV → mostrare il ponte equity (EV → equity value → per share), confermare prima delle sensitivity table
- Individuare errori a ogni fase — un'assunzione di margine sbagliata scoperta dopo le sensitivity table significa ricostruire tutto a valle

**Sensitivity Tables:**
- **Usare un numero DISPARI di righe e colonne** (standard: 5×5, talvolta 7×7) — questo garantisce una vera cella centrale
- **Cella centrale = caso base.** Costruire i valori degli assi in modo che l'intestazione di riga centrale e l'intestazione di colonna centrale equivalgano esattamente alle assunzioni reali del modello (es. se WACC base = 9.5%, la riga centrale è 9.5%; se terminal g = 1.5%, la colonna centrale è 1.5%). L'output della cella centrale deve quindi eguagliare il prezzo implicito per azione del modello — questo è il sanity check che la tabella è costruita correttamente.
- **Evidenziare la cella centrale** con il riempimento blu medio (`#BDD7EE`) + font bold così è immediatamente visibile quale cella è il caso base.
- Popolare TUTTE le celle (tipicamente 3 tabelle × 25 celle = 75) con formule di ricalcolo DCF complete
- Usare loop openpyxl (o Office JS) per scrivere formule programmaticamente
- NESSUN testo placeholder, NESSUNA approssimazione lineare, NESSUN passaggio manuale richiesto
- Ogni cella deve ricalcolare il DCF completo per quella combinazione di assunzioni

**Commenti Cella:**
- Aggiungere commenti cella MAN MANO che ogni valore fisso viene creato
- Formato: "Fonte: [Sistema/Documento], [Data], [Riferimento], [URL se applicabile]"
- Ogni input blu deve avere un commento prima di passare alla sezione successiva
- Non rimandare alla fine o scrivere "TODO: aggiungere fonte"

**Pianificazione Layout Modello:**
- Definire TUTTE le posizioni di riga delle sezioni PRIMA di scrivere qualsiasi formula
- Scrivere TUTTE le intestazioni e le etichette per prime
- Scrivere TUTTI i separatori di sezione e le righe vuote per secondi
- POI scrivere le formule usando le posizioni di riga bloccate
- Testare le formule immediatamente dopo la creazione

**Ricalcolo Formule:**
- Eseguire `python recalc.py model.xlsx 30` prima della consegna
- Correggere TUTTI gli errori fino a stato "success"
- Zero errori formula richiesti (#REF!, #DIV/0!, #VALUE!, ecc.)

**Blocchi Scenario:**
- Creare blocchi separati per i casi Bear/Base/Bull
- Mostrare le assunzioni orizzontalmente attraverso gli anni di proiezione all'interno di ogni blocco
- Usare formule IF: `=IF($B$6=1,[cella Bear],IF($B$6=2,[cella Base],[cella Bull]))`
- Verificare che le formule referenzino le celle corrette del blocco scenario

## Processo DCF

### Step 1: Recupero e Validazione Dati

Recuperare dati da server MCP, dati forniti dall'utente e dal web.

**Priorità Fonti Dati:**
1. **Server MCP** (se configurati) — Dati finanziari strutturati da provider (Refinitiv, Bloomberg, Bureau van Dijk/AIDA)
2. **Dati Forniti dall'Utente** — Bilanci storici dalla loro ricerca
3. **Ricerca/Fetch Web** — Prezzi correnti, beta, debito e cassa quando necessario

**Fonti Dati Specifiche per l'Italia:**
- **CONSOB** — Comunicazioni price sensitive, prospetti, OPA, partecipazioni rilevanti
- **Borsa Italiana** — Prezzi, volumi, indici (FTSE MIB, FTSE Italia Mid Cap, STAR)
- **Bureau van Dijk / AIDA** — Bilanci società italiane quotate e non quotate
- **Refinitiv / LSEG** — Consensus estimates, dati di mercato, beta
- **Bilancio consolidato IFRS** — Relazione annuale e semestrale (non 10-K/10-Q)
- **InfoCamere / Registro Imprese** — Visure camerali, dati societari

**Checklist di Validazione:**
- Verificare posizione finanziaria netta vs cassa netta (critico per la valutazione)
- Confermare numero azioni diluite (controllare recenti buyback/aumenti di capitale)
- Validare che i margini storici siano coerenti con il modello di business
- Cross-check tassi di crescita ricavi con benchmark di settore
- Verificare che l'aliquota fiscale sia ragionevole (~27.9%: IRES 24% + IRAP 3.9%)
- Per IRAP: verificare aliquota regionale (base 3.9%, varia per regione e settore — settore finanziario 4.65%)
- Verificare principi contabili: IFRS obbligatorio per quotate, OIC per non quotate

### Step 2: Analisi Storica (3-5 anni)

Analizzare e documentare:
- **Trend crescita ricavi**: Calcolare CAGR, identificare driver
- **Progressione margini**: Tracciare margine lordo, margine EBIT, margine FCF
- **Intensità di capitale**: D&A e CapEx come % dei ricavi
- **Efficienza capitale circolante**: Variazioni NWC come % della crescita ricavi
- **Metriche di rendimento**: ROIC, ROE trends

**Nota IFRS vs GAAP:**
- Goodwill: in IFRS non si ammortizza, si fa impairment test annuale (IAS 36)
- Leasing: IFRS 16 capitalizza tutti i leasing (impatto su EBITDA, debito, D&A)
- Ricavi: IFRS 15 — riconoscimento per performance obligation
- Attività immateriali: criteri di capitalizzazione R&D diversi (IAS 38)
- Verificare se la società riporta per segmento (IFRS 8) e utilizzare i dati segmentali

Creare tabelle riepilogative:
```
Metriche Storiche (LTM):
Ricavi: €X milioni
Crescita ricavi: X% CAGR
Margine lordo: X%
Margine EBIT: X%
D&A % dei ricavi: X%
CapEx % dei ricavi: X%
Margine FCF: X%
```

### Step 3: Costruzione Proiezioni di Ricavo

**Metodologia:**
1. Partire dall'ultimo ricavo effettivo (LTM o esercizio fiscale più recente)
2. Applicare tassi di crescita per ogni anno di proiezione
3. Mostrare sia importi in euro CHE percentuali di crescita calcolate

**Framework Tassi di Crescita:**
- Anno 1-2: Crescita più alta riflettendo visibilità di breve termine
- Anno 3-4: Moderazione graduale verso la media di settore
- Anno 5+: Avvicinamento al tasso di crescita terminale

**Contesto italiano:** La crescita del PIL italiano è strutturalmente più bassa di quella US (~0.5-1.5% reale). Le proiezioni di crescita per società italiane mature dovrebbero riflettere questo contesto macro. Le PMI innovative possono avere tassi superiori ma il mercato domestico è più piccolo.

**Struttura formule:**
- Ricavi(Anno N) = Ricavi(Anno N-1) × (1 + Tasso di Crescita)
- Crescita %(Anno N) = Ricavi(Anno N) / Ricavi(Anno N-1) - 1

**Approccio a tre scenari:**
```
Caso Bear: Crescita conservativa (es. 3-6% per large cap italiana)
Caso Base: Scenario più probabile (es. 5-10%)
Caso Bull: Crescita ottimistica (es. 8-14%)
```

### Step 4: Modellazione Costi Operativi

**Analisi Costi Fissi/Variabili:**

I costi operativi dovrebbero modellare una leva operativa realistica:
- **Costi commerciali e di vendita**: Tipicamente 10-30% dei ricavi a seconda del modello di business
- **Ricerca e Sviluppo**: Tipicamente 3-15% (le aziende italiane investono mediamente meno in R&D rispetto a quelle US)
- **Costi generali e amministrativi**: Tipicamente 8-15% dei ricavi, mostra leva al crescere della scala
- **Costo del lavoro**: In Italia incide di più per TFR, contributi INPS e INAIL — prestare attenzione alla struttura dei costi del personale nel bilancio IFRS

**Principi chiave:**
- TUTTE le percentuali basate sui RICAVI, non sull'utile lordo
- Modellare la leva operativa: % dovrebbe diminuire al crescere dei ricavi
- Mantenere voci separate per Commerciali, R&D, G&A
- Calcolare EBIT = Utile Lordo - Totale OpEx

**Framework espansione margini:**
```
Stato Attuale → Stato Target (Anno 5)
Margine Lordo: X% → Y% (giustificare in base a scala, efficienza)
Margine EBIT: X% → Y% (risultato di crescita ricavi + leva opex)
```

### Step 5: Calcolo Free Cash Flow

**Costruire FCF nella sequenza corretta:**

```
EBIT
(-) Imposte (EBIT × Aliquota Fiscale Effettiva)
= NOPAT (Net Operating Profit After Tax)
(+) D&A (costi non monetari, % dei ricavi)
(-) CapEx (% dei ricavi, tipicamente 3-8%)
(-) Δ NWC (variazione del capitale circolante netto)
= Unlevered Free Cash Flow
```

**Aliquota Fiscale per l'Italia:**
- **IRES**: 24% (imposta sul reddito delle società)
- **IRAP**: 3.9% base (varia per regione; settore bancario/finanziario: 4.65%; assicurazioni: 5.90%)
- **Aliquota combinata standard**: ~27.9% (usare come default per società non finanziarie)
- **Attenzione**: IRAP ha base imponibile diversa da IRES (non deducibili interessi passivi e costo del lavoro). Per modelli di dettaglio, calcolare IRES e IRAP separatamente. Per il DCF standard, l'aliquota combinata ~28% è un'approssimazione accettabile applicata all'EBIT.

**Modellazione Capitale Circolante:**
- Calcolare come % della variazione dei ricavi (delta ricavi)
- **Range tipico Italia: 3-8% della variazione dei ricavi** (più alto che in US per DSO/DPO più lunghi)
- DSO italiani medi: 60-90 giorni (vs 30-45 US) — particolarmente lunghi nel B2B e nel settore pubblico
- DPO italiani medi: 60-75 giorni
- Numero negativo = fonte di cassa (rilascio capitale circolante)
- Numero positivo = uso di cassa (assorbimento capitale circolante)

**CapEx di Mantenimento vs Crescita:**
- CapEx di mantenimento: Sostiene le operazioni correnti (~2-3% ricavi)
- CapEx di crescita: Supporta l'espansione (2-5% addizionale)
- Il CapEx totale dovrebbe allinearsi alla strategia di crescita dell'azienda

### Step 6: Costo del Capitale (WACC) — Parametri Italiani

**Metodologia CAPM per il Costo dell'Equity:**

```
Costo dell'Equity = Risk-Free Rate + Beta × ERP + CRP (se applicabile)

Dove:
- Risk-Free Rate = Rendimento BTP 10 anni (titolo di Stato italiano)
- Beta = Beta mensile a 5 anni vs indice di mercato (FTSE MIB o EURO STOXX 50)
- ERP = Equity Risk Premium italiano: 6.0-8.0%
  (include premio per rischio paese rispetto a mercati core come Germania/US)
- CRP = Country Risk Premium (opzionale, se si usa risk-free tedesco + CRP separato)
```

**Due approcci per il risk-free rate:**

| Approccio | Risk-Free | CRP | Quando usare |
|-----------|-----------|-----|--------------|
| **A — BTP diretto** | Rendimento BTP 10Y (~3.5-4.5%) | Incorporato nel BTP | Più semplice, standard per analisti italiani |
| **B — Bund + CRP** | Rendimento Bund 10Y (~2.0-2.5%) + spread BTP-Bund (~1.0-2.0%) | Esplicito | Più analitico, preferito da advisory internazionali |

Entrambi convergono sullo stesso risultato. Usare l'approccio A come default, l'approccio B quando si vuole isolare il rischio paese.

**Equity Risk Premium (ERP) — Contesto Italiano:**
- ERP Italia (Damodaran, ultimo aggiornamento): ~6.5-7.5%
- Composto da: ERP maturo (~5.0-5.5%) + Country Risk Premium Italia (~1.5-2.0%)
- Lo spread BTP-Bund è un proxy del rischio paese percepito dal mercato
- Per società con ricavi prevalentemente internazionali, considerare un ERP ponderato per geografia dei ricavi

**Costo del Debito:**

```
Costo del Debito After-Tax = Costo del Debito Pre-Tax × (1 - Aliquota Fiscale)

Determinare il Costo del Debito Pre-Tax da:
- Rendimento obbligazioni corporate della società (se quotate)
- Spread creditizio su Euribor/€STR in base al rating
- Interessi passivi / Debito Totale dal bilancio
- Rating creditizio Moody's / S&P / Fitch / DBRS
```

**Benchmark costo del debito (Italia, 2024-2025):**
- Investment grade (BBB): Euribor 6M (~3.5%) + spread 100-200 bps = ~4.5-5.5%
- High yield (BB): Euribor 6M + spread 300-500 bps = ~6.5-8.5%
- Unrated mid-cap: stimare in base a copertura interessi e leva, tipicamente 5-7%

**Pesi della Struttura del Capitale:**

```
Market Cap = Prezzo Corrente × Azioni in Circolazione
Posizione Finanziaria Netta (PFN) = Debito Totale - Cassa & Equivalenti
Enterprise Value = Market Cap + PFN

Peso Equity = Market Cap / Enterprise Value
Peso Debito = PFN / Enterprise Value

WACC = (Costo Equity × Peso Equity) + (Costo Debito After-Tax × Peso Debito)
```

**Casi Speciali:**
- **Posizione di Cassa Netta**: Se Cassa > Debito, PFN è NEGATIVA
  - Il Peso del Debito può essere negativo
  - Il calcolo WACC si aggiusta di conseguenza
- **Nessun Debito**: WACC = Costo dell'Equity

**Range WACC Tipici (contesto italiano):**
- Large Cap stabile (FTSE MIB): 8-10%
- Mid Cap in crescita (STAR): 10-13%
- Small Cap / Alta crescita: 13-16%
- Settore bancario: usare modello DDM, non DCF (regolamentazione capitale)

### Step 7: Applicazione Tasso di Sconto (5-10 Anni di Previsione)

**Convenzione Mid-Year:**
- I flussi di cassa si assumono generati a metà anno
- Periodo di Sconto: 0.5, 1.5, 2.5, 3.5, 4.5, ecc.
- Fattore di Sconto = 1 / (1 + WACC)^Periodo

**Calcolo del Valore Attuale:**
```
Per ogni anno di proiezione:
PV del FCF = FCF Unlevered × Fattore di Sconto

Esempio (Anno 1):
FCF = €1.000
WACC = 10%
Periodo = 0.5
Fattore di Sconto = 1 / (1.10)^0.5 = 0.9535
PV = €1.000 × 0.9535 = €954
```

**Selezione Periodo di Proiezione:**
- **5 anni**: Standard per la maggior parte delle analisi
- **7-10 anni**: Società ad alta crescita con pista più lunga
- **3 anni**: Business maturi e stabili

### Step 8: Calcolo Terminal Value

**Metodo della Crescita Perpetua (Preferito):**

```
FCF Terminale = FCF Ultimo Anno × (1 + Tasso di Crescita Terminale)
Terminal Value = FCF Terminale / (WACC - Tasso di Crescita Terminale)

Vincolo Critico: Crescita Terminale < WACC (altrimenti valore infinito)
```

**Selezione Tasso di Crescita Terminale (contesto italiano/europeo):**
- Conservativo: 1.0-1.5% (crescita PIL reale Italia a lungo termine)
- Moderato: 1.5-2.0% (PIL nominale Eurozona, target inflazione BCE 2%)
- Aggressivo: 2.0-2.5% (solo per leader di mercato con pricing power)

**Non superare**: Il tasso risk-free o la crescita nominale del PIL a lungo termine. L'Italia ha un PIL reale a lungo termine di ~0.5-1.0%, quindi con inflazione target 2% il PIL nominale è ~2.5-3.0%. Un terminal growth sopra il 2.5% richiede giustificazione forte.

**Metodo del Multiplo di Uscita (Alternativo):**
```
Terminal Value = EBITDA Ultimo Anno × Multiplo di Uscita

Dove il Multiplo di Uscita viene da:
- Multipli di trading dei comparabili su Borsa Italiana / Euronext
- Multipli di transazioni precedenti
- Range tipico: 6-12x EBITDA (più basso del mercato US per multiple compression)
```

**Valore Attuale del Terminal Value:**
```
PV del Terminal Value = Terminal Value / (1 + WACC)^Ultimo Periodo

Dove l'Ultimo Periodo considera la temporizzazione:
Modello 5 anni con convenzione mid-year: Periodo = 4.5
```

**Sanity Check Terminal Value:**
- Dovrebbe rappresentare 50-70% dell'Enterprise Value
- Se >75%, il modello potrebbe essere troppo dipendente dalle assunzioni terminali
- Se <40%, verificare se le assunzioni terminali sono troppo conservative

### Step 9: Ponte da Enterprise Value a Equity Value

**Struttura Riepilogo Valutazione:**

```
(+) Somma PV degli FCF Proiettati = €X milioni
(+) PV del Terminal Value = €Y milioni
= Enterprise Value = €Z milioni

(-) Posizione Finanziaria Netta [o + Cassa Netta se negativa] = €A milioni
= Equity Value = €B milioni

÷ Azioni Diluite in Circolazione = C milioni di azioni
= Prezzo Implicito per Azione = €XX,XX

Prezzo Corrente dell'Azione = €YY,YY
Rendimento Implicito = (Prezzo Implicito / Prezzo Corrente) - 1 = XX%
```

**Aggiustamenti Critici:**
- **PFN = Debito Totale - Cassa & Equivalenti**
  - Se positiva: Sottrarre dall'EV (riduce equity value)
  - Se negativa (Cassa Netta): Aggiungere all'EV (aumenta equity value)
- **Usare Azioni Diluite**: Include stock option, piani di incentivazione, convertibili
- **Attenzione TFR**: Il TFR (Trattamento di Fine Rapporto) in bilancio IFRS è una passività per benefici ai dipendenti (IAS 19). Considerare se includerlo nella PFN o trattarlo separatamente come debt-like item.
- **Altri aggiustamenti** (se applicabili):
  - Interessi di minoranza
  - Fondi rischi e oneri significativi
  - Passività per leasing (IFRS 16)
  - Partecipazioni non consolidate (equity method) — aggiungere al valore

**Formato Output Valutazione:**
```csv
Componente Valutazione,Importo (€M)
PV FCF Espliciti,X,X
PV Terminal Value,Y,Y
Enterprise Value,Z,Z
(-) PFN,A,A
Equity Value,B,B
,,
Azioni in Circolazione (M),C,C
Prezzo Implicito per Azione,€XX.XX
Prezzo Corrente dell'Azione,€YY.YY
Upside/(Downside) Implicito,+XX%
```

### Step 10: Analisi di Sensitività

Costruire **tre tabelle di sensitività** in fondo al foglio DCF mostrando come la valutazione cambia con diverse assunzioni:

1. **WACC vs Terminal Growth** — Mostra la sensitività dell'enterprise value al tasso di sconto e alla crescita perpetua
2. **Crescita Ricavi vs Margine EBIT** — Mostra l'impatto della crescita del top-line e della leva operativa
3. **Beta vs Risk-Free Rate** — Mostra la sensitività alle componenti del costo dell'equity

**Implementazione**: Queste sono semplici griglie 2D (NON la funzionalità "Data Table" di Excel) con formule in ogni cella. Ogni cella deve contenere un ricalcolo completo del DCF per quella specifica combinazione di assunzioni. Vedere la sezione Vincoli Critici per i requisiti dettagliati sul popolamento programmato di tutte le 75 celle.

<correct_patterns>

Questa sezione contiene tutti i pattern CORRETTI da seguire nella costruzione di modelli DCF.

### Pattern di Selezione Blocco Scenario — Seguire Questo Approccio

**Le assunzioni sono organizzate in blocchi separati per ogni scenario:**

**STRUTTURA CRITICA — Tre righe per ogni intestazione di sezione:**

```csv
ASSUNZIONI CASO BEAR (intestazione sezione, merge celle)
Assunzione,FY1,FY2,FY3,FY4,FY5
Crescita Ricavi (%),5%,4%,3%,3%,2%
Margine EBIT (%),18%,17%,17%,16%,16%

ASSUNZIONI CASO BASE (intestazione sezione, merge celle)
Assunzione,FY1,FY2,FY3,FY4,FY5
Crescita Ricavi (%),8%,7%,6%,5%,4%
Margine EBIT (%),20%,21%,22%,22%,23%

ASSUNZIONI CASO BULL (intestazione sezione, merge celle)
Assunzione,FY1,FY2,FY3,FY4,FY5
Crescita Ricavi (%),12%,11%,9%,8%,6%
Margine EBIT (%),22%,23%,24%,25%,26%
```

**Ogni blocco scenario DEVE avere una riga intestazione colonna** che mostra gli anni di proiezione (FY2025E, FY2026E, ecc.) immediatamente sotto il titolo della sezione. Senza questo, gli utenti non possono dire quale valore corrisponde a quale anno.

**Come referenziare le assunzioni — Creare una colonna di consolidamento:**
1. Cella selettore caso (es. B6) contiene 1=Bear, 2=Base, o 3=Bull
2. Creare una colonna di consolidamento con formule INDEX o OFFSET per estrarre dal blocco scenario corretto
3. Le formule di proiezione referenziano la colonna di consolidamento (riferimenti cella puliti)
4. Ogni blocco scenario contiene l'insieme completo delle assunzioni DCF attraverso gli anni di proiezione

**Pattern colonna consolidamento raccomandato (usando INDEX):**
`=INDEX(B10:D10, 1, $B$6)`

**NON questo — istruzioni IF sparse ovunque:**
`=IF($B$6=1,[cella blocco Bear],IF($B$6=2,[cella blocco Base],[cella blocco Bull]))`

L'approccio colonna di consolidamento centralizza la logica e rende il modello più facile da auditare.

### Pattern Corretto di Proiezione Ricavi

**Creare una colonna di consolidamento con formule INDEX, poi referenziarla nelle proiezioni:**

**Step 1 - Colonna consolidamento per crescita FY1:**
`=INDEX([crescita FY1 Bear]:[crescita FY1 Bull], 1, $B$6)`

**Step 2 - Proiezione ricavi referenzia la colonna di consolidamento:**
`Ricavi Anno 1: =D29*(1+$E$10)`

Dove:
- D29 = Ricavi anno precedente
- $E$10 = Cella colonna di consolidamento per crescita FY1 (contiene formula INDEX)
- $B$6 = Selettore caso (1=Bear, 2=Base, 3=Bull)

### Pattern Corretto Formula FCF

**Usare colonne di consolidamento con formule INDEX, poi referenziarle nei calcoli FCF:**

**Approccio colonna consolidamento:**
```csv
Voce,Formula,Riferimento
D&A,=E29*$E$21,$E$21 = colonna consolidamento per D&A %
CapEx,=E29*$E$22,$E$22 = colonna consolidamento per CapEx %
Δ NWC,=(E29-D29)*$E$23,$E$23 = colonna consolidamento per NWC %
FCF Unlevered,=E57+E58-E60-E62,E57=NOPAT E58=D&A E60=CapEx E62=Δ NWC
```

### Formato Corretto Commenti Cella

**Ogni valore fisso necessita di questo formato:**

"Fonte: [Sistema/Documento], [Data], [Riferimento], [URL se applicabile]"

**Esempi:**
```csv
Voce,Commento Fonte
Prezzo azione,Fonte: Borsa Italiana 2025-10-12 Prezzo chiusura
Azioni in circolazione,Fonte: Relazione annuale FY2024 Pag. 45 Nota 12
Ricavi storici,Fonte: Bilancio consolidato IFRS FY2024 Conto Economico
Beta,Fonte: Refinitiv 2025-10-12 Beta mensile 5 anni vs FTSE MIB
Stime consensus,Fonte: Guidance management Q3 2024 conference call
Rendimento BTP,Fonte: Banca d'Italia / Bloomberg 2025-10-12
```

### Struttura Corretta Tabella Assunzioni

**CRITICO: Ogni blocco scenario richiede TRE elementi strutturali:**

1. **Riga intestazione sezione** (celle unite): es. "ASSUNZIONI CASO BEAR"
2. **Riga intestazione colonna** che mostra gli anni — OBBLIGATORIA, NON SALTARE
3. **Righe dati** con valori delle assunzioni

### Processo Corretto di Pianificazione Righe

**1. Scrivere TUTTE le intestazioni e le etichette PER PRIME**
**2. Scrivere TUTTI i separatori di sezione e le righe vuote**
**3. POI scrivere le formule usando le posizioni di riga bloccate**
**4. Testare le formule immediatamente dopo la creazione**

### Implementazione Corretta Sensitivity Table

**IMPORTANTE**: Queste NON sono la funzionalità "Data Table" di Excel. Sono semplici griglie dove si scrivono formule regolari usando openpyxl. Sì, questo significa ~75 formule totali (3 tabelle × 25 celle ciascuna), ma è diretto e obbligatorio.

**Struttura Tabella — griglia 5×5 (dimensioni DISPARI, caso base centrato):**

Se il WACC base del modello = 9.5% e la crescita terminale base = 1.5%, costruire gli assi simmetricamente attorno a quei valori:

```csv
WACC vs Terminal Growth,  0.5%,  1.0%,  1.5%,  2.0%,  2.5%
              8.5%,       [fml], [fml], [fml], [fml], [fml]
              9.0%,       [fml], [fml], [fml], [fml], [fml]
              9.5%,       [fml], [fml], [★  ], [fml], [fml]   ← riga centrale = WACC base
             10.0%,       [fml], [fml], [fml], [fml], [fml]
             10.5%,       [fml], [fml], [fml], [fml], [fml]
                                   ↑
                          colonna centrale = terminal g base
```

**★ = la cella centrale.** Il suo output formula DEVE eguagliare il prezzo per azione implicito del modello (dal riepilogo valutazione). Applicare il riempimento blu medio (`#BDD7EE`) e font bold a questa cella così il caso base è visivamente ancorato.

**Regola per i valori degli assi:** `axis_values = [base - 2*step, base - step, base, base + step, base + 2*step]` — simmetrico attorno alla base, conteggio dispari garantisce un centro.

**Pattern Formula — Cella B88 (WACC=8.5%, Terminal Growth=0.5%):**

La formula in B88 dovrebbe ricalcolare il prezzo implicito usando:
- WACC dall'intestazione di riga: `$A88` (8.5%)
- Terminal Growth dall'intestazione di colonna: `B$87` (0.5%)

**Approccio raccomandato:** Referenziare il calcolo DCF principale ma sostituire questi valori.

**Struttura formula esempio:**
`=([SOMMA dei PV FCF usando $A88 come tasso di sconto] + [Terminal Value usando B$87 come tasso di crescita e $A88 come WACC] - [PFN]) / [Azioni]`

**CRITICO — Scrivere una formula per OGNI cella nella griglia 5x5 (25 celle per tabella, 75 celle totali).** Usare openpyxl per scrivere queste formule programmaticamente in un loop.

```python
# Pseudocodice per popolare la sensitivity table
for row_idx, wacc_value in enumerate(wacc_range):
    for col_idx, term_growth_value in enumerate(term_growth_range):
        formula = f"=<DCF ricalcolo usando {wacc_value} e {term_growth_value}>"
        ws.cell(row=start_row+row_idx, column=start_col+col_idx).value = formula
```

</correct_patterns>

<common_mistakes>

Questa sezione contiene tutti i pattern SBAGLIATI da evitare nella costruzione di modelli DCF.

### SBAGLIATO: Approssimazioni Semplificate Sensitivity Table o Testo Placeholder

**Non usare approssimazioni lineari:**

```
// SBAGLIATO - Approssimazione lineare
B97: =B88*(1+(0.096-0.116))    // Assume relazione lineare

// SBAGLIATO - Scorciatoia divisione
B105: =B88/(1+(E48-0.07))      // Non ricalcola il DCF completo
```

**Non lasciare testo placeholder:**
```
// SBAGLIATO - Nota placeholder
"Nota: Usare la funzionalità Data Table di Excel per popolare le sensitivity tables."

// SBAGLIATO - Celle vuote
[lasciare celle vuote perché "è complesso"]
```

### SBAGLIATO: Commenti Cella Mancanti

**Non fare questo:**
- Creare tutti gli input fissi senza commenti
- Pensare "li aggiungerò dopo"
- Scrivere "TODO: aggiungere fonte"

**Invece:** Aggiungere il commento cella MAN MANO che ogni valore fisso viene creato

### SBAGLIATO: Riferimenti Riga Formula Spostati

**Sintomo:**
La sezione FCF referenzia le righe di assunzione sbagliate:
`D&A:  =E29*$E$34    // Dovrebbe essere $E$21, ma referenzia riga sbagliata`

**Invece:** Bloccare il layout delle righe PRIMA, poi scrivere le formule

### SBAGLIATO: Aliquota Fiscale US Applicata al Contesto Italiano

**Non fare questo:**
- Usare 21% come aliquota (è l'aliquota corporate US, non italiana)
- Ignorare IRAP
- Dimenticare che IRAP ha base imponibile diversa

**Invece:** Usare ~27.9% (IRES 24% + IRAP 3.9%) come default, verificare l'aliquota IRAP regionale/settoriale

### SBAGLIATO: Risk-Free Rate su Treasury US

**Non fare questo:**
- Usare il rendimento del Treasury 10Y US come risk-free rate
- Usare ERP del 5.0-5.5% (è l'ERP del mercato US maturo, non include il CRP italiano)

**Invece:** Usare BTP 10Y o Bund 10Y + spread BTP-Bund, con ERP 6.0-8.0%

### SBAGLIATO: Terminal Growth Troppo Alto

**Non fare questo:**
- Usare 2.5-3.0% come terminal growth "conservativo" (è il range US)
- Giustificarlo con "crescita GDP" senza specificare quale GDP

**Invece:** Per l'Italia, terminal growth 1.0-2.0%. La crescita del PIL nominale italiano a lungo termine è ~2.5-3.0%, quindi il terminal growth non dovrebbe superare il 2.0-2.5% nemmeno nel caso più ottimistico.

### SBAGLIATO: Fonti Dati US

**Non fare questo:**
- Referenziare SEC EDGAR per i bilanci
- Cercare 10-K o 10-Q
- Usare SOFR come riferimento per il costo del debito

**Invece:** Bilancio consolidato IFRS da CONSOB/Borsa Italiana, Euribor per il costo del debito

### TOP 5 ERRORI — RIEPILOGO

1. **Riferimenti riga formula spostati** → Definire TUTTE le posizioni riga PRIMA di scrivere formule
2. **Commenti cella mancanti** → Aggiungere commenti MAN MANO che le celle vengono create
3. **Sensitivity tables semplificate** → Popolare tutte le celle con formule di ricalcolo DCF completo
4. **Parametri WACC US** → Usare BTP 10Y, ERP italiano 6-8%, Euribor, aliquota ~28%
5. **Terminal growth troppo alto** → 1.0-2.0% per l'Italia, non 2.5-3.5%

### Errori Calcolo WACC — Contesto Italiano
- Usare Treasury US invece di BTP 10Y
- Non includere il Country Risk Premium italiano nell'ERP
- Usare SOFR/LIBOR invece di Euribor per il costo del debito
- Applicare aliquota fiscale US (21%) invece di italiana (~28%)
- Non considerare IRAP nella struttura fiscale
- Mixing book e market values nella struttura del capitale

### Errori Assunzioni di Crescita
- Terminal growth > WACC (crea valore infinito)
- Terminal growth > 2.5% senza giustificazione per contesto italiano
- Tassi di crescita proiettati incoerenti con il track record
- Crescita non allineata con le dinamiche del mercato italiano (più piccolo, più maturo)

### Errori Terminal Value
- Usare metodo di crescita sbagliato (perpetuità vs multiplo di uscita)
- Terminal value >80% dell'enterprise value (suggerisce eccessiva dipendenza)
- Multipli di uscita basati su comparabili US anziché europei
- Periodo di sconto sbagliato per il terminal value

### Errori Proiezioni Cash Flow
- Costi operativi basati sull'utile lordo invece che sui ricavi
- Percentuali D&A/CapEx disallineate dal modello di business
- NWC sottostimato (non tenere conto dei DSO/DPO più lunghi italiani)
- Incoerenza aliquota fiscale tra anni
- Non considerare TFR come passività debt-like

</common_mistakes>

## Creazione File Excel

**Questo skill usa lo skill `xlsx` per tutte le operazioni su fogli di calcolo.** Lo skill xlsx fornisce:
- Regole standardizzate di costruzione formule
- Convenzioni di formattazione numerica
- Ricalcolo automatizzato formule via script `recalc.py`
- Controllo e validazione errori completa

Tutti i file Excel creati da questo skill devono seguire i requisiti dello skill xlsx, inclusi zero errori formula e ricalcolo corretto.

## Rubrica di Qualità

Ogni modello DCF deve massimizzare per:
1. **Assunzioni realistiche di ricavi e margini** basate sulla performance storica e il contesto macro italiano
2. **Calcolo appropriato del costo del capitale** con metodologia CAPM e parametri italiani
3. **Analisi di sensitività completa** che mostra range di valutazione
4. **Calcolo terminal value chiaro** con razionale a supporto e crescita coerente con PIL europeo
5. **Struttura modello professionale** che abilita l'analisi per scenari
6. **Documentazione trasparente** di tutte le assunzioni chiave

## Requisiti di Input

### Input Minimi Richiesti
1. **Identificativo società**: Ticker o nome società (Borsa Italiana, Euronext, o non quotata)
2. **Assunzioni di crescita**: Tassi di crescita ricavi per il periodo di proiezione (o "usa consensus")
3. **Parametri opzionali**:
   - Periodo di proiezione (default: 5 anni)
   - Casi scenario (assunzioni crescita e margine Bear/Base/Bull)
   - Tasso di crescita terminale (default: 1.5-2.0%)
   - Input WACC specifici se non si usa CAPM
   - Quotata vs non quotata (impatta fonti dati e liquidità)

## Struttura Modello Excel

### Architettura Fogli

Creare **due fogli**:

1. **DCF** — Modello di valutazione principale con analisi di sensitività in fondo
2. **WACC** — Calcolo del costo del capitale

**CRITICO**: Le sensitivity tables vanno IN FONDO al foglio DCF (non su un foglio separato).

### Ricalcolo Formule (OBBLIGATORIO)

Dopo aver creato o modificato il modello Excel, **ricalcolare tutte le formule** usando lo script recalc.py dallo skill xlsx:

```bash
python recalc.py [percorso_file_excel] [timeout_secondi]
```

Esempio:
```bash
python recalc.py ENEL_DCF_Model_2025-10-12.xlsx 30
```

### Standard di Formattazione

**IMPORTANTE**: Seguire lo skill xlsx per le regole di costruzione formule e le convenzioni di formattazione numerica.

**Schema Colori — Due Livelli**:

**Livello 1: Colori Font (OBBLIGATORIO)**
- **Testo blu (RGB: 0,0,255)**: TUTTI gli input fissi (prezzo azione, azioni, dati storici, assunzioni)
- **Testo nero (RGB: 0,0,0)**: TUTTE le formule e i calcoli
- **Testo verde (RGB: 0,128,0)**: Link ad altri fogli (riferimenti al foglio WACC)

**Livello 2: Colori Riempimento — Palette Blu/Grigio Professionale**
- **Intestazioni sezione**: Blu scuro (RGB: 31,78,121 / `#1F4E79`) sfondo con testo bianco bold
- **Sub-intestazioni/intestazioni colonna**: Blu chiaro (RGB: 217,225,242 / `#D9E1F2`) sfondo con testo nero bold
- **Celle input**: Grigio chiaro (RGB: 242,242,242 / `#F2F2F2`) sfondo con font blu
- **Celle calcolate**: Sfondo bianco con font nero
- **Righe output/riepilogo**: Blu medio (RGB: 189,215,238 / `#BDD7EE`) sfondo con font nero bold

**Formati Numerici:**
- **Anni**: Formattare come stringhe testo (es. "2024" non "2.024")
- **Percentuali**: `0,0%` (un decimale)
- **Valuta**: `€#.##0` per milioni; `€#.##0,00` per per-share — SEMPRE specificare unità nelle intestazioni ("Ricavi (€M)")
- **Zeri**: Usare formattazione numerica per rendere tutti gli zeri "-"
- **Numeri grandi**: `#.##0` con separatore migliaia (punto in italiano)
- **Numeri negativi**: `(#.##0)` tra parentesi (NON segno meno)

### Struttura Dettagliata Foglio DCF

**Sezione 1: Intestazione**
```csv
Riga,Contenuto
1,[Nome Società] Modello DCF
2,Ticker: [XXX.MI] | Data: [Data] | Fine Esercizio: [FYE]
3,Vuoto
4,Cella Selettore Caso (1=Bear 2=Base 3=Bull)
5,Visualizzazione Nome Caso (formula: =IF([Selettore]=1,"Bear",IF([Selettore]=2,"Base","Bull")))
```

**Sezione 2: Dati di Mercato (NON dipendenti dal caso)**
```csv
Voce,Valore
Prezzo Corrente Azione,€XX,XX
Azioni in Circolazione (M),XX,X
Market Cap (€M),[Formula]
Posizione Finanziaria Netta (€M),XXX [o Cassa Netta se negativa]
```

**Sezione 3: Assunzioni Scenario DCF**

Creare blocchi di assunzione separati per ogni scenario (Bear, Base, Bull) con assunzioni specifiche DCF (Crescita Ricavi %, Margine EBIT %, Aliquota Fiscale %, D&A % dei Ricavi, CapEx % dei Ricavi, Δ NWC % del ΔRicavi, Tasso Crescita Terminale, WACC) disposte orizzontalmente attraverso gli anni di proiezione.

**Sezione 4: Dati Storici & Proiettati**

```csv
Conto Economico (€M),2020A,2021A,2022A,2023A,2024E,2025E,2026E
Ricavi,XXX,XXX,XXX,XXX,[=E29*(1+$E$10)],[=F29*(1+$E$11)],[=G29*(1+$E$12)]
  % crescita,XX%,XX%,XX%,XX%,[=E29/D29-1],[=F29/E29-1],[=G29/F29-1]
```

**Sezione 5: Costruzione Free Cash Flow**

```csv
Cash Flow (€M),2020A,2021A,2022A,2023A,2024E,2025E,2026E
NOPAT,XXX,XXX,XXX,XXX,[=E45],[=F45],[=G45]
(+) D&A,XXX,XXX,XXX,XXX,[=E29*$E$21],[=F29*$E$21],[=G29*$E$21]
(-) CapEx,(XX),(XX),(XX),(XX),[=E29*$E$22],[=F29*$E$22],[=G29*$E$22]
(-) Δ NWC,(XX),(XX),(XX),(XX),[=(E29-D29)*$E$23],[=(F29-E29)*$E$23],[=(G29-F29)*$E$23]
FCF Unlevered,XXX,XXX,XXX,XXX,[=E57+E58-E60-E62],[=F57+F58-F60-F62],[=G57+G58-G60-G62]
```

**Sezione 6: Sconto & Valutazione**
```csv
Valutazione DCF,2024E,2025E,2026E,2027E,2028E,Terminale
FCF Unlevered (€M),XXX,XXX,XXX,XXX,XXX,
Periodo,0.5,1.5,2.5,3.5,4.5,
Fattore di Sconto,0.XX,0.XX,0.XX,0.XX,0.XX,
PV del FCF (€M),XXX,XXX,XXX,XXX,XXX,
,,,,,,
Riepilogo Valutazione (€M),,,,,,
Somma PV FCF,XXX,,,,,
PV Terminal Value,XXX,,,,,
Enterprise Value,XXX,,,,,
(-) PFN,(XX),,,,,
Equity Value,XXX,,,,,
,,,,,,
Azioni in Circolazione (M),XX.X,,,,,
PREZZO IMPLICITO PER AZIONE,€XX.XX,,,,,
Prezzo Corrente Azione,€XX.XX,,,,,
Upside/(Downside) Implicito,XX%,,,,,
```

### Struttura Foglio WACC — Parametri Italiani

```csv
CALCOLO COSTO DELL'EQUITY,,
Risk-Free Rate (BTP 10Y),X,XX%,[Input blu]
Beta (5 anni mensile vs FTSE MIB),X,XX,[Input blu]
Equity Risk Premium (Italia),X,XX%,[Input blu]
Costo dell'Equity,X,XX%,[Calcolato nero]
,,
CALCOLO COSTO DEL DEBITO,,
Rating Creditizio (Moody's/S&P/Fitch/DBRS),BBB,[Input blu]
Costo del Debito Pre-Tax (Euribor + spread),X,XX%,[Input blu]
Aliquota Fiscale (IRES + IRAP),XX,X%,[Link a foglio DCF]
Costo del Debito After-Tax,X,XX%,[Calcolato nero]
,,
STRUTTURA DEL CAPITALE,,
Prezzo Corrente Azione,€XX,XX,[Link a DCF]
Azioni in Circolazione (M),XX,X,[Link a DCF]
Capitalizzazione di Mercato (€M),"X.XXX",[Calcolato]
,,
Debito Totale (€M),XXX,[Input blu]
Cassa & Equivalenti (€M),XXX,[Input blu]
Posizione Finanziaria Netta (€M),XXX,[Calcolato]
,,
Enterprise Value (€M),"X.XXX",[Calcolato]
,,
CALCOLO WACC,Peso,Costo,Contribuzione
Equity,XX,X%,X,X%,X,XX%
Debito,XX,X%,X,X%,X,XX%
,,
COSTO MEDIO PONDERATO DEL CAPITALE (WACC),X,XX%,[Output verde]
```

**Formule Chiave WACC:**
```
Market Cap = Prezzo × Azioni
PFN = Debito Totale - Cassa
Enterprise Value = Market Cap + PFN
Peso Equity = Market Cap / EV
Peso Debito = PFN / EV
WACC = (Costo Equity × Peso Equity) + (Costo Debito After-Tax × Peso Debito)
```

**Note WACC Specifiche per l'Italia:**
- Risk-Free: rendimento BTP 10Y corrente (verificare su Banca d'Italia / Bloomberg)
- Beta: vs FTSE MIB per società italiane, vs EURO STOXX 50 per pan-europee
- ERP: usare Damodaran country-specific o stimare come ERP maturo (~5.0%) + CRP Italia (~1.5-2.0%)
- Costo debito: Euribor 6M + spread creditizio (NON SOFR o LIBOR)
- Aliquota: IRES 24% + IRAP 3.9% = 27.9% default (verificare settore/regione)

### Analisi di Sensitività (Fondo del Foglio DCF)

**Posizione**: Righe 87+ sul foglio DCF (NON un foglio separato)

**Tre sensitivity tables, impilate verticalmente:**

1. **WACC vs Terminal Growth** (righe 87-100) — griglia 5×5 = 25 celle con formule
2. **Crescita Ricavi vs Margine EBIT** (righe 102-115) — griglia 5×5 = 25 celle con formule
3. **Beta vs Risk-Free Rate** (righe 117-130) — griglia 5×5 = 25 celle con formule

**Totale formule da scrivere: 75** (obbligatorio)

**Range tipici per gli assi (contesto italiano):**
- WACC: step da 0.5%, range ±1.0% dal base (es. 8.5%-10.5% se base 9.5%)
- Terminal Growth: step da 0.5%, range ±1.0% dal base (es. 0.5%-2.5% se base 1.5%)
- Beta: step da 0.1, range ±0.2 dal base
- Risk-Free (BTP 10Y): step da 0.25%, range ±0.5% dal base

## Implementazione Selettore Caso

**Framework a Tre Casi:**

### Caso Bear
- Crescita ricavi conservativa (fascia bassa del range storico)
- Compressione margini o nessuna espansione
- WACC più alto (aumento premio al rischio, spread BTP-Bund più ampio)
- Tasso di crescita terminale più basso (1.0%)
- Assunzioni CapEx più alte

### Caso Base
- Crescita ricavi consensus o guidance management
- Espansione margini moderata basata su leva operativa
- WACC implicito dal mercato corrente
- Crescita terminale allineata al PIL (~1.5%)
- Assunzioni CapEx standard

### Caso Bull
- Crescita ricavi ottimistica (fascia alta delle proiezioni)
- Espansione margini significativa
- WACC più basso (riduzione premio al rischio, spread compresso)
- Crescita terminale più alta (2.0-2.5%)
- Intensità CapEx ridotta

## Struttura Deliverable

**Naming file**: `[Ticker]_DCF_Model_[Data].xlsx` (es. `ENEL_DCF_Model_2025-10-12.xlsx`)

**Due fogli**:
1. **DCF** — Modello completo con casi Bear/Base/Bull + tre sensitivity tables in fondo
2. **WACC** — Calcolo costo del capitale con parametri italiani

## Best Practice

### Costruzione Modello
1. **Costruire incrementalmente**: Completare ogni sezione prima di passare alla successiva
2. **Testare durante la costruzione**: Inserire numeri campione per verificare le formule
3. **Usare struttura coerente**: Calcoli simili seguono pattern simili
4. **Costruire controlli interni**: Somme di verifica e bilanci di controllo dove applicabile

### Documentazione
1. **Documentare tutte le assunzioni**: Spiegare il razionale dietro gli input chiave
2. **Citare le fonti dati**: Notare da dove viene ogni dato (CONSOB, Borsa Italiana, bilancio, Refinitiv)
3. **Spiegare la metodologia**: Descrivere approcci non standard
4. **Segnalare le incertezze**: Evidenziare aree con visibilità limitata

## Variazioni Comuni

### Società Tecnologiche ad Alta Crescita (Italia)
- Periodo di proiezione più lungo (7-10 anni)
- Tassi di crescita iniziali più alti (15-25%)
- Espansione margini significativa nel tempo
- WACC più alto (13-16%)
- Mercato domestico più piccolo — valutare % ricavi export

### Società Mature/Stabili (FTSE MIB)
- Periodo di proiezione più corto (3-5 anni)
- Crescita modesta (PIL +1-3%)
- Margini stabili
- WACC più basso (8-10%)
- Focus su generazione di cassa e allocazione del capitale
- Dividend yield tipicamente più alto che in US

### Società Cicliche
- Modellare attraverso il ciclo economico
- Normalizzare margini a metà ciclo
- Considerare scenari di picco e fondo
- Aggiustare beta per ciclicità

### Società Multi-Segmento
- DCF separati per ogni business unit
- Tassi di crescita e margini diversi per segmento
- Valutazione sum-of-parts
- Considerare sinergie

### Società Non Quotate (PMI Italiane)
- Beta da società quotate comparabili (unlever/relever)
- Applicare premio per illiquidità (+2-4% al costo dell'equity)
- Applicare sconto per dimensione se appropriato
- Bilancio OIC (non IFRS) — potrebbe necessitare aggiustamenti
- Governance: considerare rischio uomo chiave

## Integrazione nel Workflow

### All'Inizio della Costruzione DCF

1. **Raccogliere dati di mercato**:
   - Controllare server MCP disponibili per dati di mercato correnti
   - Usare ricerca/fetch web per prezzi azioni (Borsa Italiana), beta, BTP 10Y, Euribor
   - Richiedere all'utente se servono dati specifici

2. **Raccogliere bilanci storici**:
   - Controllare server MCP disponibili (Refinitiv, Bureau van Dijk)
   - Richiedere all'utente se non disponibili via MCP
   - Estrazione manuale da bilanci IFRS depositati in CONSOB se necessario

3. **Iniziare la costruzione del modello** usando la metodologia DCF descritta in questo skill

### Prima della Consegna del Modello (OBBLIGATORIO)

1. **Verificare la struttura**:
   - Blocchi scenario per Bear/Base/Bull con assunzioni attraverso gli anni
   - Selettore caso funzionale con formule che referenziano i blocchi corretti
   - Sensitivity tables in fondo al foglio DCF
   - Colori font: Input blu, formule nere, link fogli verdi
   - Commenti cella su TUTTI gli input fissi
   - Bordi professionali attorno alle sezioni principali
   - **WACC con parametri italiani** (BTP, ERP, Euribor, IRES+IRAP)

2. **Ricalcolare formule**: Eseguire `python recalc.py model.xlsx 30`

3. **Controllare output**:
   - Se `status` è `"success"` → Continuare al passo 4
   - Se `status` è `"errors_found"` → Controllare `error_summary` e correggere

4. **Correggere errori e rieseguire recalc.py** fino a status "success"

5. **Spot-check formule**:
   - Testare una formula FCF — referenzia le righe di assunzione corrette?
   - Cambiare selettore caso — la colonna di consolidamento si aggiorna correttamente?
   - Verificare che le formule dei ricavi referenzino la colonna di consolidamento
   - **Verificare che WACC usi BTP 10Y e non Treasury US**
   - **Verificare aliquota ~28% e non 21%**

6. **Consegnare modello**

## Checklist Finale

Prima di consegnare il modello DCF:

**Obbligatorio:**
- Eseguire `python recalc.py model.xlsx 30` fino a status "success" (zero errori formula)
- Due fogli: DCF (con sensitività in fondo), WACC
- Colori font: Blu=input, Nero=formule, Verde=link fogli
- Commenti cella su TUTTI gli input fissi
- Sensitivity tables completamente popolate con formule
- Bordi professionali attorno alle sezioni principali

**Validazione Specifica Italia:**
- Risk-free rate: BTP 10Y (NON Treasury US)
- ERP: 6.0-8.0% (NON 5.0-5.5%)
- Costo debito: su Euribor (NON SOFR/LIBOR)
- Aliquota fiscale: ~27.9% IRES+IRAP (NON 21%)
- Terminal growth: 1.0-2.0% (NON 2.5-3.5%)
- Valuta: EUR con formattazione europea
- Fonti dati: CONSOB/Borsa Italiana (NON SEC EDGAR)
- Principi contabili: IFRS (NON US GAAP)
- NWC: DSO/DPO italiani (60-90 gg, NON 30-45)
- Naming file: `[Ticker]_DCF_Model_[Data].xlsx`
