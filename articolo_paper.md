# L'Intelligenza Artificiale Generativa nella Valutazione d'Azienda: un Cambio di Paradigma per l'Analista Finanziario

## Abstract

Il presente lavoro illustra la progettazione e la realizzazione di un sistema multi-agente basato su intelligenza artificiale generativa per la valutazione d'azienda (*equity valuation*). Il toolkit, denominato **Valuation Analyst**, impiega otto agenti specializzati coordinati da un orchestratore centrale, ciascuno incaricato di una specifica metodologia valutativa secondo l'impianto teorico di Aswath Damodaran (NYU Stern). Il sistema rappresenta un cambiamento fondamentale nel modo in cui l'analista finanziario interagisce con i modelli di valutazione: non piu' fogli di calcolo isolati e processi manuali, bensi' un'infrastruttura intelligente capace di eseguire analisi complesse, coordinare flussi di lavoro interdipendenti e produrre report strutturati in linguaggio naturale. L'articolo esamina l'architettura del sistema, le metodologie implementate, le implicazioni operative per la professione dell'analista e le prospettive di evoluzione di questo nuovo paradigma.

---

## 1. Introduzione: il Contesto di Riferimento

La valutazione d'azienda costituisce una delle attivita' fondamentali della finanza aziendale. Che si tratti di determinare il valore intrinseco di una societa' quotata, di stimare il prezzo equo in un'operazione di M&A, o di valutare una partecipazione in una societa' non quotata, l'analista finanziario si trova quotidianamente a confrontarsi con modelli matematici articolati, fonti dati eterogenee e un volume considerevole di assunzioni da formulare, documentare e giustificare.

Tradizionalmente, questo lavoro si svolge attraverso fogli di calcolo costruiti manualmente, alimentati da dati raccolti da terminali finanziari, e integrati con il giudizio professionale dell'analista. Il processo e' intrinsecamente sequenziale: si parte dal costo del capitale, si costruisce il modello DCF, si verificano i risultati con i multipli di mercato, si conducono analisi di sensitivita'. Ogni passaggio richiede la costruzione manuale di formule, la verifica della coerenza dei dati e l'interpretazione critica dei risultati.

L'avvento dell'intelligenza artificiale generativa, e in particolare dei modelli linguistici di grandi dimensioni (*Large Language Models*, LLM), introduce per la prima volta la possibilita' di ripensare radicalmente questo flusso di lavoro. Non si tratta di un semplice strumento di automazione -- come potrebbe essere una macro di Excel -- ma di un sistema capace di comprendere il contesto della richiesta, selezionare autonomamente le metodologie appropriate, eseguire calcoli complessi e comunicare i risultati in modo strutturato e comprensibile.

Il progetto qui descritto, **Valuation Analyst**, rappresenta un caso di studio concreto di questa trasformazione: un toolkit multi-agente che porta le metodologie consolidate di Aswath Damodaran -- il riferimento mondiale nella disciplina della valutazione -- all'interno di un'architettura intelligente governata da agenti AI specializzati.

---

## 2. Il Cambio di Paradigma: dall'Analista che Calcola all'Analista che Dirige

### 2.1 Il Modello Tradizionale

Nel modello operativo convenzionale, l'analista finanziario riveste simultaneamente il ruolo di progettista del modello, operatore di calcolo, controllore qualita' e redattore del report. Costruisce personalmente ogni formula nel foglio di calcolo, verifica manualmente la coerenza tra i moduli (ad esempio, che il WACC calcolato nella scheda dedicata sia correttamente referenziato nel modello DCF), e infine trasferisce i risultati in un documento narrativo.

Questo approccio presenta limiti strutturali ben noti:

- **Rischio di errore**: la costruzione manuale di modelli complessi espone a errori di formula, riferimenti circolari e incongruenze tra fogli
- **Scarsa riproducibilita'**: ogni analista costruisce i propri modelli con convenzioni diverse, rendendo difficile la revisione e il riutilizzo
- **Rigidita'**: modificare un'assunzione fondamentale (ad esempio, il modello di crescita) puo' richiedere la ristrutturazione di interi segmenti del foglio di calcolo
- **Costo temporale**: una valutazione completa con DCF, multipli, sensitivity e report finale richiede tipicamente diversi giorni di lavoro

### 2.2 Il Nuovo Paradigma

Il sistema Valuation Analyst introduce un modello operativo radicalmente diverso. L'analista non costruisce piu' il modello: lo dirige. Invece di scrivere formule, esprime in linguaggio naturale l'analisi che desidera condurre. Invece di assemblare manualmente i risultati di diversi approcci valutativi, delega a un orchestratore intelligente il coordinamento dei flussi di lavoro.

In termini concreti, l'analista puo' richiedere:

> *"Valuta Apple Inc. utilizzando il DCF con FCFF a tre stadi, verifica il risultato con i multipli di settore e conduci un'analisi di sensitivita' su WACC e tasso di crescita terminale."*

Il sistema, autonomamente:

1. Calcola il costo del capitale (WACC) tramite il CAPM con beta bottom-up
2. Costruisce il modello DCF con proiezione dei flussi di cassa a tre fasi
3. Seleziona le societa' comparabili e calcola i multipli di mercato
4. Conduce l'analisi di sensitivita' bidimensionale
5. Produce un report strutturato con tutti i risultati, le assunzioni documentate e i range di valutazione

L'analista conserva il pieno controllo sulle assunzioni e sul giudizio finale, ma viene liberato dall'onere della costruzione meccanica del modello. Il suo ruolo si eleva: da operatore di calcolo a supervisore critico, da costruttore di fogli di calcolo a decisore informato.

---

## 3. Architettura del Sistema

### 3.1 Visione d'Insieme

Il sistema si articola su quattro livelli architetturali, ciascuno con una responsabilita' distinta:

```
+---------------------------------------------------+
|              LIVELLO AGENTI                        |
|  orchestrator | dcf-analyst | relative-analyst     |
|  cost-of-capital | option-pricing | risk-analyst   |
|  private-valuation | ma-analyst                    |
+---------------------------------------------------+
|              LIVELLO SKILLS                        |
|  Interfacce utente invocabili in linguaggio        |
|  naturale per ogni tipologia di analisi            |
+---------------------------------------------------+
|           LIVELLO STRUMENTI DI CALCOLO             |
|  25 moduli Python (DCF, WACC, multipli,            |
|  Black-Scholes, Monte Carlo, sinergie...)          |
+---------------------------------------------------+
|              LIVELLO FONDAMENTA                    |
|  Modelli dati | Configurazione | Utilita'          |
|  Cache dati | Fonti esterne (API, dataset)         |
+---------------------------------------------------+
```

### 3.2 Il Livello Agenti: Intelligenza Specializzata

Il cuore concettuale del sistema risiede negli otto agenti specializzati. Ciascun agente e' un'istanza del modello linguistico Claude, dotata di un *system prompt* che ne definisce il ruolo, le competenze, il flusso di lavoro e i vincoli operativi. Gli agenti non sono generici: ognuno incorpora la conoscenza metodologica specifica del proprio dominio.

**Orchestrator** -- Il coordinatore centrale riceve la richiesta dell'analista e determina quali agenti attivare, in quale sequenza e con quali dipendenze. Gestisce quattro workflow predefiniti: valutazione standard di societa' quotate, valutazione di societa' in distress, valutazione di societa' private e analisi M&A. Quando possibile, l'orchestratore avvia agenti in parallelo (ad esempio, il DCF e l'analisi dei comparabili) per ridurre i tempi di esecuzione.

**Cost of Capital** -- Questo agente e' sempre il primo a essere invocato, poiche' il costo del capitale rappresenta l'input fondamentale per tutti gli altri modelli. Implementa il CAPM con le estensioni di Damodaran: risk-free rate dal Treasury decennale nella valuta dell'azienda, beta bottom-up (preferito al beta di regressione per la maggiore stabilita'), Equity Risk Premium del mercato maturo con l'aggiunta del Country Risk Premium per i mercati emergenti, e costo del debito derivato dal rating creditizio o dall'interest coverage ratio.

**DCF Analyst** -- Lo specialista della valutazione intrinseca implementa modelli DCF sia FCFF (*Free Cash Flow to Firm*) che FCFE (*Free Cash Flow to Equity*) con architettura multi-stage a tre fasi: alta crescita (cinque anni), transizione (cinque anni con convergenza lineare) e crescita stabile in perpetuita'. Il Terminal Value viene calcolato con il Gordon Growth Model, con il vincolo che il tasso di crescita terminale non superi la crescita nominale dell'economia.

**Relative Analyst** -- Conduce analisi dei comparabili selezionando societa' peer per settore, dimensione, geografia e profilo di crescita. Calcola e confronta multipli equity (P/E, P/B, PEG ratio) e enterprise (EV/EBITDA, EV/EBIT, EV/Sales), utilizzando la mediana come statistica di riferimento per la robustezza rispetto agli outlier. Il range di valutazione viene derivato dal venticinquesimo e settantacinquesimo percentile.

**Option Pricing** -- Per le situazioni in cui il DCF tradizionale risulta inadeguato -- aziende in distress finanziario, con alto leverage o utili negativi -- questo agente applica il modello di Black-Scholes interpretando l'equity come un'opzione call sugli asset aziendali con prezzo di esercizio pari al valore nominale del debito. L'output include il valore stimato dell'equity, il valore implicito del debito e la probabilita' di default.

**Private Valuation** -- Specializzato nella valutazione di societa' non quotate, applica lo sconto di illiquidita' (calibrato su ricavi, profittabilita' e dimensione, tipicamente nel range 10-40%) e il premio di controllo per partecipazioni di maggioranza (15-30%). Implementa inoltre il concetto di *total beta* per investitori non diversificati.

**M&A Analyst** -- Dedicato alle operazioni straordinarie, stima il valore delle sinergie operative (risparmi di costo, crescita incrementale), finanziarie (tax shield, capacita' di debito) e il valore complessivo dell'acquisizione, inclusivo dei costi di integrazione. Produce l'analisi di accretion/dilution sull'EPS dell'acquirente.

**Risk Analyst** -- Interviene dopo gli altri agenti per quantificare l'incertezza. Offre tre strumenti: tabelle di sensitivita' bidimensionale (tipicamente WACC versus tasso di crescita terminale), analisi per scenari (best/base/worst con probabilita') e simulazione Monte Carlo con almeno 10.000 iterazioni, distribuzioni parametriche e correlazioni tra variabili.

### 3.3 Il Livello Strumenti: Calcolo Deterministico

Al di sotto degli agenti, venticinque moduli Python implementano le formule di calcolo come funzioni pure, prive di effetti collaterali. Questa separazione e' fondamentale: il ragionamento e il giudizio risiedono negli agenti (livello AI), mentre il calcolo numerico e' deterministico e testabile (livello software).

I moduli principali includono:

| Dominio | Moduli | Formule Implementate |
|---------|--------|---------------------|
| Costo del Capitale | `capm.py`, `wacc.py`, `beta_estimation.py`, `risk_premium.py` | Re = Rf + Beta * ERP + CRP; WACC = (E/V)*Re + (D/V)*Rd*(1-t) |
| DCF | `dcf_fcff.py`, `dcf_fcfe.py`, `terminal_value.py`, `growth_models.py` | FCFF = EBIT(1-t) - CapEx + D&A - DeltaWC; TV = FCF*(1+g)/(r-g) |
| Multipli | `multiples.py`, `comparable_screen.py` | P/E, EV/EBITDA, P/B, EV/Sales |
| Option Pricing | `black_scholes.py`, `equity_as_option.py` | E = V*N(d1) - K*e^(-rT)*N(d2) |
| Societa' Private | `illiquidity_discount.py`, `control_premium.py` | Sconti e premi calibrati su benchmark |
| M&A | `synergy_valuation.py`, `acquisition_value.py` | V_acq = V_standalone + V_sinergie - Costi |
| Risk Analysis | `sensitivity_table.py`, `scenario_analysis.py`, `monte_carlo.py` | Griglia 2D, scenari ponderati, simulazione stocastica |

Ogni modulo e' accompagnato da test unitari e di integrazione (139 test complessivi, tutti superati), a garanzia della correttezza numerica.

### 3.4 Le Fonti Dati

Il sistema si alimenta da due fonti principali:

**Massive.com** -- Un'API REST che fornisce dati aziendali in tempo reale: profili societari, conti economici, stati patrimoniali, rendiconti finanziari, indici di mercato e quotazioni storiche. L'integrazione avviene tramite un client dedicato con gestione della cache.

**Dataset Damodaran** -- I fogli di calcolo pubblicati annualmente dal Professor Damodaran sul sito della NYU Stern, contenenti parametri di settore per l'intero universo delle aziende quotate a livello globale: beta per settore, equity risk premium per paese, WACC, multipli (P/E, EV/EBITDA, P/B, Price/Sales), margini operativi, CapEx, aliquote fiscali effettive e altro ancora. Il sistema scarica, interpreta e memorizza in cache questi dataset con un meccanismo di aggiornamento automatico.

---

## 4. Metodologia: il Rigore Accademico di Damodaran nell'Architettura AI

Un aspetto che merita particolare enfasi e' la scelta di ancorare l'intero sistema alla metodologia di un singolo autore di riferimento: Aswath Damodaran. Questa decisione non e' casuale.

La valutazione d'azienda soffre storicamente di un problema di frammentazione: ogni analista, ogni banca d'investimento, ogni fondo adotta varianti proprie dei modelli classici, spesso con semplificazioni o approssimazioni non documentate. Il risultato e' una proliferazione di "dialetti" valutativi che rendono difficile il confronto e la verifica dei risultati.

Damodaran rappresenta il tentativo piu' riuscito e sistematico di codificare la valutazione d'azienda in un framework coerente, trasparente e riproducibile. Il suo approccio si distingue per:

- **Rigore nella definizione dei flussi di cassa**: la distinzione netta tra FCFF e FCFE, con criteri precisi per la scelta dell'uno o dell'altro
- **Coerenza interna dei modelli**: il vincolo che il tasso di crescita terminale non superi la crescita dell'economia, che il reinvestment rate sia coerente con il ROIC atteso, che la struttura capitale converga verso un target stabile
- **Trasparenza parametrica**: la pubblicazione annuale di dataset con i parametri di settore, consultabili e verificabili da chiunque
- **Preferenza per il beta bottom-up**: piu' stabile e fondato economicamente rispetto al beta di regressione

Il sistema Valuation Analyst incorpora queste scelte metodologiche non come opzioni configurabili, ma come vincoli strutturali. Gli agenti sono istruiti a seguire la tassonomia di Damodaran per i cash flow, a preferire il beta bottom-up, a verificare la coerenza del terminal value, a documentare ogni assunzione. In questo modo, il rigore accademico non dipende dalla disciplina individuale dell'analista, ma e' incorporato nell'architettura stessa del sistema.

---

## 5. Un Esempio Operativo: la Valutazione Completa di una Societa' Quotata

Per illustrare concretamente il funzionamento del sistema, si consideri una richiesta di valutazione completa di Apple Inc.

L'analista esprime la richiesta in linguaggio naturale. L'orchestratore avvia il seguente flusso:

**Fase 1 -- Costo del Capitale.** L'agente Cost of Capital recupera il risk-free rate dal Treasury decennale statunitense, identifica il settore di appartenenza (Technology) per ricavare il beta unlevered dal dataset Damodaran, lo rileva con il rapporto debito/equity di Apple, calcola l'Equity Risk Premium e determina il costo dell'equity tramite il CAPM. Successivamente, stima il costo del debito al netto delle imposte e compone il WACC ponderando per la struttura del capitale. Risultato indicativo: WACC nell'intorno del 9-10%.

**Fase 2 -- Valutazione DCF e Multipli (in parallelo).** Due agenti lavorano simultaneamente. Il DCF Analyst costruisce il modello FCFF a tre fasi: calcola il flusso di cassa base dai dati di bilancio, proietta cinque anni di alta crescita calibrata sul reinvestment rate storico, cinque anni di transizione lineare verso la crescita stabile e il terminal value con il Gordon Growth Model. Contemporaneamente, il Relative Analyst seleziona sette societa' comparabili del settore tecnologico e calcola i multipli P/E, EV/EBITDA, P/B ed EV/Sales, applicando la mediana al target.

**Fase 3 -- Analisi del Rischio.** Il Risk Analyst riceve i risultati del DCF e costruisce una tabella di sensitivita' bidimensionale variando WACC e tasso di crescita terminale, quindi esegue una simulazione Monte Carlo con distribuzioni parametriche per quantificare l'incertezza.

**Fase 4 -- Report Finale.** L'orchestratore sintetizza tutti i risultati in un report strutturato: range di valutazione per metodo, valore consigliato come media ponderata, confronto con il prezzo di mercato, parametri chiave e avvertenze.

L'intero processo, che nel modello tradizionale richiederebbe diversi giorni di lavoro manuale, viene completato in pochi minuti con piena tracciabilita' di ogni passaggio.

---

## 6. Implicazioni per la Professione dell'Analista Finanziario

### 6.1 Cio' che Cambia

L'introduzione di sistemi multi-agente nella valutazione d'azienda trasforma profondamente il profilo professionale dell'analista:

**Dalla costruzione alla supervisione.** L'analista non costruisce piu' modelli da zero. Li configura, li supervisiona e ne valuta criticamente i risultati. Il tempo risparmiato nella meccanica del calcolo puo' essere reinvestito nell'analisi qualitativa, nella comprensione del settore e nel dialogo con il management.

**Dalla serialita' alla parallelizzazione.** L'esecuzione simultanea di piu' approcci valutativi (DCF e multipli in parallelo, ad esempio) consente una visione multi-dimensionale del valore che nel modello tradizionale era ottenibile solo con un investimento di tempo considerevole.

**Dalla fragilita' alla riproducibilita'.** Un modello costruito da un sistema codificato e' intrinsecamente riproducibile. Le stesse assunzioni producono gli stessi risultati. La documentazione delle assunzioni non e' un'attivita' aggiuntiva, ma un prodotto automatico del processo.

**Dall'isolamento alla collaborazione.** Il sistema di logging integrato (ogni interazione viene tracciata con data, agente utilizzato, input e sintesi del risultato) crea un audit trail completo che facilita la revisione da parte di colleghi e supervisori.

### 6.2 Cio' che non Cambia

E' essenziale sottolineare che il sistema non sostituisce il giudizio dell'analista. L'intelligenza artificiale generativa eccelle nell'esecuzione strutturata di processi definiti e nella manipolazione di informazioni complesse, ma non possiede il senso economico, la comprensione del contesto competitivo e la capacita' di valutare la qualita' del management che contraddistinguono un analista esperto.

Il sistema produce valutazioni tecnicamente corrette *date le assunzioni fornite*. La scelta delle assunzioni -- quale tasso di crescita attendersi, quale premio per il rischio applicare, quali comparabili selezionare -- rimane una prerogativa esclusivamente umana. In questo senso, il sistema amplifica le capacita' dell'analista senza sostituirne il giudizio.

### 6.3 Le Nuove Competenze Richieste

Questo cambio di paradigma richiede all'analista finanziario di sviluppare competenze che prima non erano necessarie:

- **Prompt engineering finanziario**: la capacita' di formulare richieste precise e non ambigue al sistema, specificando metodologie, assunzioni e vincoli desiderati
- **Supervisione critica dei modelli AI**: la capacita' di valutare se il sistema ha interpretato correttamente la richiesta e ha selezionato le metodologie appropriate
- **Comprensione dell'architettura multi-agente**: la consapevolezza di come i diversi agenti interagiscono e si condizionano reciprocamente
- **Validazione dei risultati**: la capacita' di verificare la ragionevolezza dei risultati, identificare anomalie e intervenire con aggiustamenti manuali quando necessario

---

## 7. Aspetti Tecnici di Rilievo

### 7.1 La Separazione tra Ragionamento e Calcolo

Una scelta architetturale fondamentale del sistema e' la netta separazione tra il livello del ragionamento (agenti AI) e il livello del calcolo (moduli Python). Gli agenti decidono *cosa* calcolare e *come* interpretare i risultati; i moduli Python eseguono i calcoli in modo deterministico e verificabile.

Questa separazione offre due vantaggi cruciali:

1. **Testabilita'**: ogni modulo di calcolo e' coperto da test unitari che ne verificano la correttezza numerica indipendentemente dall'agente che lo invoca
2. **Trasparenza**: l'analista puo' sempre ispezionare il codice di calcolo per verificare che le formule implementate corrispondano alle formule attese

### 7.2 Il Modello dei Dati

Il sistema adotta un approccio rigorosamente tipizzato. Tutti i dati transitano attraverso *dataclass* Python con validazione integrata: `Company`, `ValuationResult`, `CashFlowProjection`, `CostoCapitale`, `Comparabile`, `InputBlackScholes`, `Scenario`, `RisultatoSensitivity`. Questo previene errori di tipo e garantisce che ogni modulo riceva dati nel formato atteso.

### 7.3 La Piattaforma: Claude Code

Il sistema e' costruito su Claude Code, l'interfaccia da linea di comando di Anthropic per il modello Claude. Claude Code offre nativamente il supporto per agenti specializzati (file `.md` con system prompt e strumenti), skill invocabili dall'utente (workflow predefiniti attivabili con comandi slash) e l'accesso a strumenti di sistema (lettura/scrittura file, esecuzione codice, ricerca nel codebase). Questa piattaforma consente di definire agenti con competenze verticali che possono essere orchestrati in workflow complessi -- una capacita' che non era disponibile nei sistemi AI di generazione precedente.

---

## 8. Limiti e Considerazioni

Il sistema presenta limiti che e' doveroso esplicitare:

**Dipendenza dalla qualita' dei dati.** La valutazione prodotta e' tanto affidabile quanto i dati di input. Errori o lacune nei dati finanziari di base si propagano inevitabilmente nei risultati.

**Necessita' di supervisione esperta.** Il sistema non e' progettato per l'uso autonomo da parte di non esperti. Un analista finanziario qualificato deve validare le assunzioni, verificare la ragionevolezza dei risultati e intervenire con il proprio giudizio professionale.

**Aggiornamento dei parametri.** I dataset di Damodaran vengono aggiornati annualmente. Il sistema riflette i parametri dell'ultimo aggiornamento disponibile e potrebbe non catturare variazioni intra-annuali significative.

**Complessita' non modellata.** Esistono aspetti della valutazione -- operazioni cross-border con regime fiscale complesso, strutture societarie a cascata, strumenti finanziari esotici -- che esulano dall'ambito attuale del sistema.

---

## 9. Prospettive di Evoluzione

Il sistema nella sua forma attuale rappresenta un punto di partenza, non un punto di arrivo. Le direttrici di evoluzione piu' promettenti includono:

**Integrazione con fonti dati aggiuntive.** L'estensione a data provider multipli (Bloomberg, Refinitiv, S&P Capital IQ) aumenterebbe la copertura e consentirebbe la verifica incrociata dei dati.

**Modelli settoriali specializzati.** Lo sviluppo di agenti dedicati a settori con dinamiche valutative peculiari -- banche (DDM e residual income), utilities (regulatory asset base), real estate (NAV), risorse naturali (reserve-based) -- amplierebbe il campo di applicazione.

**Apprendimento dalle revisioni.** Un sistema di feedback in cui le correzioni apportate dall'analista vengano utilizzate per raffinare il comportamento degli agenti nel tempo.

**Generazione automatica di presentazioni.** L'estensione dall'output testuale alla generazione di *pitch book* e presentazioni formattate per comitati investimento e consigli di amministrazione.

---

## 10. Conclusioni

Il progetto Valuation Analyst dimostra che l'intelligenza artificiale generativa, quando applicata con rigore metodologico e architettura appropriata, puo' trasformare radicalmente il flusso di lavoro della valutazione d'azienda. Il sistema non semplifica la valutazione: la rende piu' accessibile, riproducibile e trasparente, liberando l'analista dalla meccanica del calcolo per consentirgli di concentrarsi su cio' che realmente conta -- il giudizio professionale.

Il cambio di paradigma non risiede nella sostituzione dell'analista, ma nella ridefinizione del suo ruolo. L'analista del futuro non sara' colui che costruisce il modello migliore, ma colui che pone le domande migliori, seleziona le assunzioni piu' appropriate e interpreta i risultati con la maggiore profondita'. In questo senso, l'intelligenza artificiale non diminuisce il valore della competenza finanziaria: lo amplifica.

La disponibilita' di sistemi come Valuation Analyst pone tuttavia una responsabilita' nuova alla comunita' degli analisti finanziari: quella di comprendere la tecnologia sottostante, di apprendere a interagire efficacemente con essa e di mantenere sempre il controllo critico sui risultati prodotti. L'alternativa -- ignorare questa evoluzione -- non e' piu' sostenibile in un mercato che premia la velocita', la coerenza e la trasparenza dell'analisi.

---

## Riferimenti

- Damodaran, A. (2012). *Investment Valuation: Tools and Techniques for Determining the Value of Any Asset*. 3rd Edition, Wiley.
- Damodaran, A. *Damodaran Online*. https://pages.stern.nyu.edu/~adamodar/
- Anthropic. *Claude Code Documentation*. https://docs.anthropic.com/
- Black, F., & Scholes, M. (1973). The Pricing of Options and Corporate Liabilities. *Journal of Political Economy*, 81(3), 637-654.
- Gordon, M. J. (1959). Dividends, Earnings, and Stock Prices. *The Review of Economics and Statistics*, 41(2), 99-105.

---

*Questo articolo descrive il progetto Valuation Analyst, un toolkit multi-agente per equity valuation costruito su Claude Code (Anthropic). Il sistema implementa le metodologie di Aswath Damodaran attraverso otto agenti AI specializzati, venticinque moduli di calcolo Python e l'integrazione con fonti dati professionali.*
