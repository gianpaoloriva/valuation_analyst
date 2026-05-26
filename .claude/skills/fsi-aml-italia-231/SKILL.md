---
name: fsi-aml-italia-231
description: Adeguata verifica della clientela e obblighi antiriciclaggio ai sensi del D.Lgs. 231/2007 per intermediari finanziari italiani. Copre i tre livelli di verifica (semplificata, ordinaria, rafforzata), identificazione del titolare effettivo, valutazione del rischio, conservazione dei dati, segnalazione di operazioni sospette alla UIF e obblighi di astensione. Triggers su "antiriciclaggio", "AML", "adeguata verifica", "due diligence clientela", "titolare effettivo", "UBO", "UIF", "segnalazione operazione sospetta", "SOS", "D.Lgs. 231", "riciclaggio", "KYC Italia", "PEP Italia", "onboarding cliente Italia".
---

# Antiriciclaggio — Adeguata verifica della clientela

Riferimenti normativi: D.Lgs. 231/2007 (attuazione IV e V Direttiva Antiriciclaggio UE — Dir. 2015/849 e Dir. 2018/843), Provvedimento Banca d'Italia del 30/07/2019 (disposizioni attuative per intermediari), Provvedimento UIF del 04/05/2023 (indicatori di anomalia), D.Lgs. 90/2017 (modifiche al 231/2007), Reg. UE 2024/1624 (nuovo pacchetto AML/CFT — applicabile dal 2027).

## Ambito di applicazione

### Soggetti obbligati (art. 3 D.Lgs. 231/2007)

| Categoria | Esempi |
|-----------|--------|
| Intermediari bancari e finanziari | Banche, SIM, SGR, SICAV/SICAF, istituti di pagamento, IMEL, intermediari ex art. 106 TUB |
| Imprese di assicurazione | Ramo vita (I, III, V) |
| Intermediari assicurativi | Agenti, broker (per prodotti vita) |
| Professionisti | Notai, avvocati, commercialisti, consulenti del lavoro, revisori |
| Operatori non finanziari | Operatori in oro, case da gioco, operatori in beni di lusso (>€10.000 in contanti) |

### Quando scatta l'obbligo di adeguata verifica (art. 17 D.Lgs. 231/2007)

| Evento | Obbligo |
|--------|---------|
| Instaurazione di un rapporto continuativo | Sempre (apertura conto, mandato di gestione, contratto di consulenza) |
| Operazione occasionale ≥€15.000 | Sempre (anche se frazionata in più operazioni apparentemente collegate) |
| Trasferimento di fondi >€1.000 | Sempre |
| Sospetto di riciclaggio o finanziamento del terrorismo | Sempre, indipendentemente da soglie o deroghe |
| Dubbi sulla veridicità dei dati identificativi già acquisiti | Sempre (aggiornamento) |

## I tre livelli di adeguata verifica

### Livello 1 — Verifica semplificata (art. 23 D.Lgs. 231/2007)

Applicabile quando il rischio di riciclaggio è **basso**, sulla base della valutazione del rischio dell'intermediario.

| Condizione | Esempi |
|------------|--------|
| Cliente a basso rischio | Ente pubblico italiano, società quotata su mercato regolamentato UE, intermediario vigilato UE |
| Prodotto a basso rischio | Polizza vita con premio annuo <€1.000, pensione integrativa con contributi da lavoro |
| Area geografica a basso rischio | Italia, UE/SEE (salvo Paesi ad alto rischio) |

**Cosa si può semplificare:**
- Riduzione della frequenza di aggiornamento dei dati
- Riduzione dell'intensità del controllo costante
- **Non** si può omettere l'identificazione del cliente e del titolare effettivo

### Livello 2 — Verifica ordinaria (artt. 18-20 D.Lgs. 231/2007)

Il livello standard. Si applica alla maggior parte dei rapporti.

#### Step 1: Identificazione del cliente

**Persona fisica:**

| Dato | Fonte | Documento |
|------|-------|-----------|
| Nome e cognome | Documento d'identità in corso di validità | Carta d'identità, passaporto, patente (quest'ultima solo in combinazione con codice fiscale) |
| Data e luogo di nascita | Documento d'identità | |
| Residenza anagrafica | Documento + autocertificazione | Certificato di residenza o autocertificazione |
| Codice fiscale | Tessera sanitaria / tesserino CF | Obbligatorio per l'identificazione in Italia |
| Cittadinanza | Documento d'identità | Rilevante per valutazione rischio |

**Persona giuridica / ente:**

| Dato | Fonte | Documento |
|------|-------|-----------|
| Denominazione | Visura camerale | Visura CCIAA aggiornata |
| Sede legale | Visura camerale | |
| Codice fiscale / Partita IVA | Visura camerale | |
| Forma giuridica | Visura camerale | S.r.l., S.p.A., S.a.s., associazione, fondazione, trust |
| Legale rappresentante | Visura camerale + documento d'identità del rappresentante | Identificazione come persona fisica |
| Oggetto sociale | Statuto / visura | Rilevante per coerenza con operatività |

#### Step 2: Identificazione del titolare effettivo (artt. 19-20 D.Lgs. 231/2007)

Il titolare effettivo è la persona fisica che possiede o controlla il cliente.

**Criteri di individuazione (in ordine di priorità):**

| Criterio | Soglia | Dettaglio |
|----------|--------|-----------|
| 1. Proprietà diretta | >25% del capitale / diritti di voto | Persona fisica che detiene direttamente >25% |
| 2. Proprietà indiretta | >25% tramite catena societaria | Ricostruire la catena fino alla persona fisica che controlla |
| 3. Controllo tramite altri mezzi | Qualsiasi | Patti parasociali, diritti speciali, accordi che conferiscono il controllo |
| 4. Titolare effettivo residuale | — | Se nessuno dei criteri precedenti identifica una persona fisica: il legale rappresentante o chi esercita poteri di amministrazione/direzione |

**Fonti per la verifica:**

| Fonte | Disponibilità |
|-------|--------------|
| Registro dei Titolari Effettivi (CCIAA) | Operativo dal 2023 — consultabile dagli intermediari |
| Visura camerale con assetto proprietario | Sempre disponibile, ma mostra solo la proprietà diretta |
| Dichiarazione del cliente (autocertificazione) | Obbligatoria — il cliente deve dichiarare il titolare effettivo |
| Bilancio e nota integrativa | Per le partecipazioni rilevanti |
| Banche dati commerciali | Bureau van Dijk (Orbis), InfoCamere |

**Strutture complesse — punti di attenzione:**

| Struttura | Rischio | Azione |
|-----------|---------|--------|
| Trust | Elevato — identificare disponente, trustee, beneficiari, guardiano | Acquisire atto istitutivo e letter of wishes (se disponibile) |
| Fondazioni | Medio-alto — identificare fondatore, beneficiari, organi di gestione | Acquisire statuto e atto costitutivo |
| Catene societarie multi-livello | Elevato — opacità proprietaria | Ricostruire l'intera catena fino alla persona fisica. Se la catena attraversa Paesi ad alto rischio: verifica rafforzata |
| Società fiduciarie | Elevato — intestazione fiduciaria | Acquisire dichiarazione della fiduciaria sull'identità del fiduciante |

#### Step 3: Informazioni su scopo e natura del rapporto

| Informazione | Come raccoglierla |
|-------------|-------------------|
| Scopo del rapporto | Perché il cliente apre il rapporto? (investimento, gestione liquidità, copertura, previdenza) |
| Natura del rapporto | Tipo di servizio richiesto (consulenza, gestione, deposito titoli, RTO) |
| Origine dei fondi | Da dove provengono i fondi? (reddito da lavoro, vendita immobile, eredità, attività d'impresa, donazione) |
| Operatività prevista | Volumi e frequenza attesi, strumenti utilizzati, mercati |
| Coerenza con il profilo | L'operatività dichiarata è coerente con il profilo economico-patrimoniale? |

#### Step 4: Controllo costante (art. 20 D.Lgs. 231/2007)

| Attività | Frequenza | Dettaglio |
|----------|-----------|-----------|
| Monitoraggio delle transazioni | Continua | Verificare che le operazioni siano coerenti con il profilo di rischio e l'operatività dichiarata |
| Aggiornamento dati identificativi | Periodica (in base al rischio) | Almeno ogni 2-3 anni per rischio medio, annuale per rischio alto |
| Screening liste sanzionatorie | A ogni transazione + periodicamente | Liste UE, ONU, e nazionali — automatizzare con screening MCP |
| Verifica PEP | All'onboarding + periodicamente | Verificare se il cliente o il titolare effettivo è diventato PEP |
| Analisi operatività anomala | Continua | Operazioni incoerenti, frazionamenti, importi anomali |

### Livello 3 — Verifica rafforzata (art. 24-25 D.Lgs. 231/2007)

Obbligatoria quando il rischio è **elevato**. Si aggiunge alla verifica ordinaria.

| Fattore di rischio elevato | Misure rafforzate |
|---------------------------|-------------------|
| **PEP** (Persone Politicamente Esposte) | Autorizzazione del responsabile o dell'alta dirigenza per instaurare/proseguire il rapporto. Misure adeguate per stabilire l'origine del patrimonio e dei fondi. Controllo costante rafforzato |
| **Paese ad alto rischio** (lista UE ex art. 9 Dir. 2015/849) | Acquisizione di informazioni aggiuntive sul cliente, sul titolare effettivo, sulla natura del rapporto. Misure aggiuntive per verificare la fonte dei fondi |
| **Struttura proprietaria complessa o opaca** | Ricostruzione completa della catena proprietaria. Acquisizione di documentazione aggiuntiva (atti costitutivi, patti parasociali, bilanci di ogni livello) |
| **Operatività insolita o anomala** | Approfondimento specifico. Richiesta di giustificazione al cliente. Valutazione per eventuale segnalazione |
| **Rapporti a distanza** (senza presenza fisica) | Misure aggiuntive di identificazione (video-identificazione conforme alle disposizioni Banca d'Italia, doppio documento, bonifico da conto intestato al cliente) |

### PEP — Persone Politicamente Esposte (art. 1(2)(dd) D.Lgs. 231/2007)

| Categoria | Esempi |
|-----------|--------|
| Cariche pubbliche nazionali | Presidente della Repubblica, Presidente del Consiglio, Ministri, Sottosegretari, parlamentari, membri Corte Costituzionale, magistrati di Cassazione e Corte dei Conti, ambasciatori |
| Cariche pubbliche regionali/locali | Presidenti di Regione, sindaci di capoluogo di provincia (>15.000 abitanti) |
| Cariche in organismi internazionali | Membri di parlamenti UE, dirigenti di organizzazioni internazionali (ONU, NATO, BEI, BCE) |
| Alte cariche militari | Ufficiali con grado ≥ generale di corpo d'armata |
| Organi di imprese pubbliche | Amministratori, sindaci, direttori generali di società a partecipazione pubblica significativa |
| **Familiari e stretti collaboratori** | Coniuge/convivente, figli e loro coniugi, genitori. Persone fisiche legate da rapporti d'affari stretti. Si applicano le **stesse misure rafforzate** |

La qualifica di PEP persiste per **5 anni** dopo la cessazione della carica.

## Valutazione del rischio

### Approccio basato sul rischio (art. 15-16 D.Lgs. 231/2007)

L'intermediario deve classificare ogni rapporto su una scala di rischio:

| Fattore | Rischio basso | Rischio medio | Rischio alto |
|---------|-------------|--------------|-------------|
| **Cliente** | Ente pubblico, società quotata, intermediario vigilato UE | Persona fisica residente UE, società con struttura chiara | PEP, società con struttura opaca, trust non regolamentato, settori ad alto rischio (gioco, contanti, cripto) |
| **Prodotto/servizio** | Polizza vita a premio basso, fondo pensione | Conto deposito, consulenza, gestione patrimoniale | Private banking, trasferimenti internazionali frequenti, operazioni in contanti, cambio valuta |
| **Area geografica** | Italia, UE/SEE (maggior parte) | Paesi terzi con regime AML adeguato | Paesi ad alto rischio (lista UE), paradisi fiscali, Paesi sotto embargo |
| **Canale** | Rapporto in presenza con identificazione documentale | Rapporto a distanza con video-identificazione | Intermediazione tramite terzi in Paesi a rischio |
| **Operatività** | Coerente con profilo dichiarato | Alcune operazioni di importo significativo, giustificate | Operatività incoerente, frazionamento, importi anomali, uso intensivo di contanti |

### Matrice rischio → livello di verifica

| Rischio complessivo | Livello di verifica | Frequenza aggiornamento | Monitoraggio |
|--------------------|--------------------|-----------------------|-------------|
| Basso | Semplificata | Ogni 5 anni | Ordinario |
| Medio | Ordinaria | Ogni 2-3 anni | Ordinario |
| Alto | Rafforzata | Annuale | Rafforzato |
| Molto alto | Rafforzata + valutazione per astensione | Semestrale | Continuo + reporting interno |

## Segnalazione di operazione sospetta (SOS)

### Quando segnalare (art. 35 D.Lgs. 231/2007)

L'intermediario segnala alla UIF quando **sa, sospetta o ha motivi ragionevoli per sospettare** che:
- Siano in corso o siano stati compiuti o tentati atti di riciclaggio o finanziamento del terrorismo
- I fondi provengano da attività criminosa

Il sospetto può derivare da:
- Operatività incoerente con il profilo del cliente
- Riscontri sulle liste sanzionatorie o adverse media
- Indicatori di anomalia (Provvedimento UIF 04/05/2023)
- Informazioni acquisite nell'esercizio dell'attività

### Indicatori di anomalia (selezione)

| Categoria | Indicatori |
|-----------|-----------|
| **Comportamento del cliente** | Riluttanza a fornire informazioni, fretta ingiustificata, accompagnamento da parte di terzi che influenzano le risposte, richiesta di trattamento preferenziale per evitare controlli |
| **Operatività in contanti** | Versamenti/prelievi frequenti appena sotto la soglia di €10.000, operazioni frazionate in più giorni, cambio di banconote di piccolo taglio in taglio grande |
| **Operatività finanziaria** | Trasferimenti frequenti verso/da Paesi a rischio, giroconti ripetuti senza apparente finalità economica, acquisto/vendita rapida di strumenti finanziari senza logica di investimento |
| **Strutture societarie** | Uso di società veicolo in Paesi opachi, catene proprietarie complesse senza giustificazione economica, cambio frequente di titolare effettivo |
| **Incongruenze** | Operatività incompatibile con il reddito/patrimonio dichiarato, fonte dei fondi non verificabile, documentazione insufficiente o contraddittoria |

### Procedura di segnalazione

| Step | Azione | Responsabile |
|------|--------|-------------|
| 1 | Rilevazione dell'anomalia | Operatore di front-office / sistema di monitoraggio |
| 2 | Prima valutazione | Responsabile dell'unità organizzativa |
| 3 | Analisi approfondita | Funzione antiriciclaggio / Responsabile SOS |
| 4 | Decisione di segnalare | Responsabile SOS (delegato dal legale rappresentante) |
| 5 | Invio alla UIF | Tramite portale INFOSTAT-UIF, entro tempi ragionevoli (senza ritardo) |
| 6 | Conservazione | Conservare tutta la documentazione per 10 anni dalla segnalazione |

### Divieto di comunicazione (tipping-off) — art. 39 D.Lgs. 231/2007

| Regola | Dettaglio |
|--------|-----------|
| A chi si applica | A chiunque sia coinvolto nella segnalazione (operatore, responsabile, funzione AML) |
| Cosa è vietato | Comunicare al cliente o a terzi che è stata effettuata (o si sta valutando) una segnalazione |
| Eccezioni | Comunicazione tra intermediari coinvolti nella stessa operazione, scambio di informazioni tra funzioni AML di un gruppo |
| Sanzioni | Penali: da 1 a 5 anni di reclusione (art. 55(4) D.Lgs. 231/2007) |

## Obbligo di astensione (art. 42 D.Lgs. 231/2007)

| Quando | Azione |
|--------|--------|
| Impossibilità di adeguata verifica | L'intermediario **non può** instaurare il rapporto / eseguire l'operazione / deve valutare se porre fine al rapporto |
| Sospetto di riciclaggio + impossibilità di astensione | Se l'astensione non è possibile o potrebbe ostacolare le indagini: eseguire l'operazione e segnalare immediatamente alla UIF |

## Conservazione dei dati (art. 31-32 D.Lgs. 231/2007)

| Dato | Durata di conservazione | Decorrenza |
|------|------------------------|-----------|
| Documenti identificativi, dati del titolare effettivo | **10 anni** | Dalla cessazione del rapporto |
| Registrazioni delle operazioni | **10 anni** | Dall'esecuzione dell'operazione |
| Corrispondenza e documentazione di supporto | **10 anni** | Dalla data del documento |
| Segnalazioni di operazioni sospette | **10 anni** | Dalla data della segnalazione |

I dati devono essere conservati in modo da consentire la ricostruzione dell'operazione e la tempestiva risposta alle richieste dell'autorità giudiziaria o della UIF.

## Sanzioni

| Violazione | Sanzione amministrativa | Sanzione penale |
|------------|------------------------|----------------|
| Omessa adeguata verifica | Da €2.000 a €50.000 | — |
| Omessa segnalazione operazione sospetta | Da €30.000 a €300.000 | — |
| Violazione obblighi di conservazione | Da €2.000 a €50.000 | — |
| Violazione divieto di comunicazione (tipping-off) | — | Reclusione da 1 a 5 anni |
| Omessa istituzione di presidi organizzativi AML | Da €10.000 a €200.000 (a carico dell'ente) | — |
| Riciclaggio (art. 648-bis c.p.) | — | Reclusione da 4 a 12 anni + multa da €5.000 a €25.000 |
| Autoriciclaggio (art. 648-ter.1 c.p.) | — | Reclusione da 2 a 8 anni + multa da €5.000 a €25.000 |

## Workflow

### Step 1: Valutazione preliminare del rischio

Prima dell'onboarding, classificare il rischio atteso sulla base delle informazioni disponibili:
- Tipo di cliente (persona fisica/giuridica, residente/non residente)
- Settore di attività
- Area geografica
- Servizio richiesto

### Step 2: Adeguata verifica

In base al livello di rischio, applicare la verifica appropriata (semplificata, ordinaria, rafforzata):
1. Identificazione del cliente (Step 1 della verifica ordinaria)
2. Identificazione del titolare effettivo (Step 2)
3. Scopo e natura del rapporto (Step 3)
4. Attivazione del controllo costante (Step 4)

### Step 3: Screening

Eseguire verifiche su:
- Liste sanzionatorie UE e ONU
- Liste PEP
- Adverse media (notizie negative da fonti pubbliche)
- Registro Titolari Effettivi (CCIAA)

### Step 4: Decisione

| Esito | Azione |
|-------|--------|
| Rischio accettabile, verifica completata | Apertura rapporto, fascicolo cliente archiviato |
| Rischio elevato ma gestibile | Apertura con misure rafforzate, autorizzazione dirigenza |
| Verifica impossibile (documenti mancanti, incoerenze) | **Astensione** — non aprire il rapporto |
| Sospetto di riciclaggio | **Astensione** + valutazione SOS alla UIF |

### Step 5: Output

Produrre:
1. **Fascicolo di adeguata verifica** — Documenti identificativi, dichiarazione titolare effettivo, profilo di rischio, scopo del rapporto
2. **Scheda di valutazione del rischio** — Punteggio per ogni fattore, rischio complessivo, livello di verifica applicato
3. **Esito screening** — Liste sanzionatorie, PEP, adverse media — con data e fonte
4. **Piano di monitoraggio** — Frequenza aggiornamento, soglie di alert, prossima revisione
5. **Eventuale SOS** — Se emerge sospetto, documentazione per la funzione AML

## Note importanti

- L'adeguata verifica non è un adempimento burocratico: è un presidio penale. L'omessa verifica espone l'intermediario e i suoi esponenti a sanzioni significative
- Il principio del **rischio-based approach** non autorizza a omettere la verifica: autorizza a calibrare l'intensità. Anche per i clienti a basso rischio, l'identificazione e la verifica del titolare effettivo restano obbligatorie
- La UIF (Unità di Informazione Finanziaria) è un organismo indipendente presso la Banca d'Italia — non è un'autorità di polizia. La segnalazione SOS non è una denuncia penale ma un'informativa di intelligence finanziaria
- Il Registro dei Titolari Effettivi presso le CCIAA è operativo dal 2023 ma la copertura è ancora parziale per alcune categorie. Non esime dall'obbligo di acquisire la dichiarazione del cliente
- Il pacchetto AML/CFT europeo (Reg. UE 2024/1624 + Dir. UE 2024/1640 + Reg. AMLA) entrerà in vigore progressivamente dal 2027 e introdurrà un'autorità di vigilanza AML europea (AMLA, con sede a Francoforte), un regolamento direttamente applicabile (senza recepimento nazionale) e soglie armonizzate a livello UE
