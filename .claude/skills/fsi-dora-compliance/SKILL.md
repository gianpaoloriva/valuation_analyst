---
name: fsi-dora-compliance
description: Checklist e workflow di conformità al Regolamento DORA (Digital Operational Resilience Act) per operatori finanziari. Copre gestione del rischio ICT, classificazione e segnalazione degli incidenti, test di resilienza operativa digitale, rischio di terze parti ICT e accordi di condivisione delle informazioni. Triggers su "DORA", "resilienza operativa digitale", "rischio ICT", "incidenti ICT", "test resilienza", "terze parti ICT", "fornitori critici", "TLPT", "threat-led penetration testing", "registro informazioni ICT", "continuità operativa ICT".
---

# DORA — Digital Operational Resilience Act

Riferimenti normativi: Reg. UE 2022/2554 (DORA), applicabile dal 17 gennaio 2025. RTS e ITS delle ESA (EBA, ESMA, EIOPA): RTS sulla gestione del rischio ICT (art. 15), RTS sulla classificazione degli incidenti (art. 18), RTS sulla segnalazione degli incidenti (art. 20), RTS sui test di resilienza (art. 26), RTS sul rischio di terze parti (art. 28), ITS sul registro delle informazioni (art. 28(3)).

## Ambito di applicazione (art. 2)

| Soggetti obbligati | Esempi |
|-------------------|--------|
| Enti creditizi | Banche, gruppi bancari |
| Imprese di investimento | SIM |
| Istituti di pagamento | Anche istituti di moneta elettronica |
| Imprese di assicurazione e riassicurazione | Tutti i rami |
| Fondi pensione (IORP) | Fondi pensione negoziali, aperti |
| Gestori di fondi di investimento alternativi | SGR, GEFIA |
| Società di gestione OICVM | SGR armonizzate |
| Fornitori di servizi di cripto-attività | Come definiti dal Reg. MiCA |
| CCP, depositari centrali, sedi di negoziazione | Infrastrutture di mercato |
| Fornitori di servizi ICT critici per il settore finanziario | Designati dalle ESA (cloud provider, core banking vendor, ecc.) |

**Principio di proporzionalità (art. 4):** gli obblighi si applicano in modo proporzionale alla dimensione, al profilo di rischio e alla complessità dell'entità finanziaria. Le microimprese hanno un regime semplificato (art. 16).

## I cinque pilastri di DORA

### Pilastro 1 — Gestione del rischio ICT (artt. 5-16)

#### Quadro di gestione del rischio ICT

L'organo di gestione (CdA o equivalente) è **direttamente responsabile** della definizione e della supervisione del quadro di gestione del rischio ICT.

**Responsabilità dell'organo di gestione (art. 5(2)):**

| Obbligo | Dettaglio |
|---------|-----------|
| Definire la strategia di resilienza operativa digitale | Inclusi livelli di tolleranza al rischio ICT |
| Approvare la politica di sicurezza delle informazioni | E rivederla almeno annualmente |
| Approvare i piani di continuità operativa ICT | E i piani di ripristino |
| Approvare la politica sulle terze parti ICT | Inclusa la strategia multi-vendor |
| Allocare budget adeguato | Per la resilienza operativa digitale |
| Formazione obbligatoria | I membri dell'organo di gestione devono ricevere formazione periodica sui rischi ICT |

#### Framework di gestione del rischio ICT (art. 6)

| Componente | Contenuto | Frequenza revisione |
|-----------|-----------|-------------------|
| Strategia di resilienza operativa digitale | Obiettivi, tolleranza al rischio, KPI, architettura ICT target | Annuale |
| Policy di sicurezza delle informazioni | Classificazione dati, controlli di accesso, cifratura, gestione identità | Annuale |
| Procedure di gestione degli incidenti ICT | Classificazione, escalation, comunicazione, post-mortem | Annuale + dopo ogni incidente rilevante |
| Piani di continuità operativa ICT | RTO, RPO, scenari, test periodici | Annuale + dopo cambiamenti significativi |
| Piani di ripristino (disaster recovery) | Procedure di recovery, siti alternativi, test | Annuale |

#### Identificazione (art. 8)

| Obbligo | Dettaglio |
|---------|-----------|
| Inventario degli asset ICT | Hardware, software, reti, dati, con classificazione di criticità |
| Mappatura delle funzioni critiche | Quali funzioni aziendali dipendono da quali sistemi ICT |
| Mappatura delle dipendenze da terze parti | Quali servizi critici sono forniti da provider esterni |
| Valutazione del rischio ICT | Per ogni asset e funzione critica: probabilità × impatto |
| Aggiornamento | L'inventario e la mappatura vanno aggiornati almeno annualmente e dopo ogni cambiamento significativo |

#### Protezione e prevenzione (art. 9)

| Misura | Requisito minimo |
|--------|-----------------|
| Gestione degli accessi | Principio del minimo privilegio, autenticazione forte, revisione periodica |
| Cifratura | Dati a riposo e in transito, gestione delle chiavi |
| Gestione delle vulnerabilità | Scansioni periodiche, patch management con SLA definiti |
| Sicurezza della rete | Segmentazione, firewall, IDS/IPS, monitoraggio |
| Gestione dei cambiamenti | Change management formale per ogni modifica a sistemi critici |
| Sicurezza fisica | Controllo accessi ai data center, protezione ambientale |

#### Rilevamento (art. 10)

| Misura | Requisito minimo |
|--------|-----------------|
| Monitoraggio continuo | Log management, SIEM, correlazione eventi, SOC |
| Rilevamento anomalie | Alert su comportamenti anomali, baseline di normalità |
| Test dei meccanismi di rilevamento | Verifiche periodiche dell'efficacia della detection |

#### Risposta e ripristino (artt. 11-12)

| Fase | Azioni |
|------|--------|
| Contenimento | Isolare i sistemi compromessi, limitare la propagazione |
| Eradicazione | Rimuovere la causa dell'incidente |
| Ripristino | Riportare i sistemi allo stato operativo secondo i piani di DR |
| Comunicazione | Notificare alle autorità competenti (Banca d'Italia, CONSOB, IVASS), ai clienti se impattati |
| Lezioni apprese | Post-incident review, aggiornamento dei piani e delle procedure |

#### Regime semplificato per microimprese (art. 16)

| Semplificazione | Dettaglio |
|----------------|-----------|
| Framework di rischio ICT | Può essere meno formalizzato, ma deve comunque esistere |
| Policy di sicurezza | Può essere più sintetica |
| Test di resilienza | Obblighi ridotti (no TLPT) |
| Segnalazione incidenti | Stessi obblighi delle entità maggiori (nessuna esenzione) |

### Pilastro 2 — Gestione, classificazione e segnalazione degli incidenti ICT (artt. 17-23)

#### Classificazione degli incidenti (art. 18)

| Criterio | Come valutare |
|----------|-------------|
| Clienti, controparti e transazioni impattate | Numero e tipo di clienti colpiti, transazioni bloccate/compromesse |
| Durata dell'incidente | Tempo di indisponibilità o degradazione del servizio |
| Estensione geografica | Aree e giurisdizioni coinvolte |
| Perdite di dati | Volume e sensibilità dei dati compromessi |
| Criticità dei servizi impattati | Servizi core vs. accessori |
| Impatto economico | Costi diretti (ripristino) e indiretti (reputazione, clienti persi) |

#### Incidenti rilevanti — soglie

Un incidente è **rilevante** (e va segnalato) se supera le soglie definite nei RTS per almeno uno dei criteri sopra. Indicativamente:

| Criterio | Soglia indicativa di rilevanza |
|----------|-------------------------------|
| Clienti impattati | >10% della base clienti O >100.000 clienti |
| Durata | >2 ore per servizi critici |
| Perdita di dati | Dati personali di >5.000 persone O dati classificati come riservati |
| Impatto economico | >€100.000 costi diretti O perdita di ricavi significativa |
| Transazioni impattate | >10% delle transazioni giornaliere medie |

#### Procedura di segnalazione (art. 19)

| Step | Tempistica | Destinatario | Contenuto |
|------|-----------|-------------|-----------|
| Notifica iniziale | **Entro 4 ore** dalla classificazione come rilevante (max 24 ore dal rilevamento) | Autorità competente (Banca d'Italia / CONSOB / IVASS) | Informazioni essenziali: cosa è successo, impatto stimato, primi interventi |
| Report intermedio | **Entro 72 ore** dalla notifica iniziale (o prima, se nuove informazioni rilevanti) | Stessa autorità | Aggiornamento su causa, impatto effettivo, misure di contenimento |
| Report finale | **Entro 1 mese** dalla risoluzione dell'incidente | Stessa autorità | Analisi completa: causa radice, impatto totale, lezioni apprese, azioni correttive |

#### Incidenti significativi legati a minacce cyber (art. 19(2))

Per gli incidenti derivanti da attacchi informatici: notifica volontaria anche delle **minacce cyber significative** (non solo degli incidenti effettivi).

### Pilastro 3 — Test di resilienza operativa digitale (artt. 24-27)

#### Test ordinari (art. 25) — per tutte le entità

| Tipo di test | Frequenza minima | Dettaglio |
|-------------|-----------------|-----------|
| Vulnerability assessment | Almeno annuale | Scansione sistemi e applicazioni per vulnerabilità note |
| Test di sicurezza della rete | Almeno annuale | Penetration test di base su perimetro esterno e segmenti critici |
| Gap analysis | Almeno annuale | Confronto con framework di riferimento (ISO 27001, NIST) |
| Test di continuità operativa | Almeno annuale | Simulazione di scenario di indisponibilità, verifica RTO/RPO |
| Test dei piani di ripristino | Almeno annuale | Ripristino effettivo da backup, failover su sito DR |
| Source code review | In base al rischio | Per applicazioni critiche sviluppate internamente |
| Scenario-based testing | In base al rischio | Simulazione di scenari specifici (ransomware, data breach, outage provider) |

#### TLPT — Threat-Led Penetration Testing (art. 26) — solo per entità significative

| Aspetto | Dettaglio |
|---------|-----------|
| Chi è obbligato | Entità identificate dall'autorità competente come significative (grandi banche, SIM sistemiche, CCP, depositari centrali) |
| Frequenza | Almeno ogni **3 anni** |
| Metodologia | Basata sul framework TIBER-EU (adottato in Italia come TIBER-IT dalla Banca d'Italia) |
| Ambito | Funzioni critiche in produzione (non ambienti di test) |
| Esecutore | Team di red teaming esterno qualificato + threat intelligence provider esterno |
| Supervisione | L'autorità competente valida l'ambito e riceve il report |
| Pooled testing | Più entità possono condividere un test se usano lo stesso provider ICT critico |

### Pilastro 4 — Rischio di terze parti ICT (artt. 28-30)

#### Principi generali (art. 28)

| Obbligo | Dettaglio |
|---------|-----------|
| Strategia sul rischio di terze parti ICT | Approvata dall'organo di gestione, include politica multi-vendor e piano di uscita |
| Registro delle informazioni | Registro di **tutti** gli accordi contrattuali con fornitori ICT terzi (art. 28(3)) — obbligo di comunicazione alle autorità |
| Due diligence pre-contrattuale | Valutare capacità, affidabilità, resilienza del fornitore prima della stipula |
| Valutazione del rischio di concentrazione | Identificare dipendenze eccessive da un singolo fornitore o da fornitori non sostituibili |

#### Registro delle informazioni (art. 28(3))

Ogni entità finanziaria deve mantenere un registro aggiornato con:

| Dato | Dettaglio |
|------|-----------|
| Identificazione del fornitore | Nome, LEI, Paese, gruppo di appartenenza |
| Tipo di servizio ICT | Descrizione, classificazione (critico/importante o meno) |
| Funzioni aziendali supportate | Mapping servizio → funzione critica |
| Data di inizio e durata del contratto | Incluse clausole di rinnovo automatico |
| Ubicazione dei dati e del trattamento | Paese di elaborazione, Paese di storage, eventuale sub-outsourcing |
| Livelli di servizio (SLA) | RTO, RPO, disponibilità, tempo di risoluzione |
| Piano di uscita | Esiste? È stato testato? Tempi stimati di migrazione |

Il registro deve essere comunicato alle autorità competenti su richiesta e, per i fornitori critici designati, proattivamente.

#### Clausole contrattuali obbligatorie (art. 30)

Ogni contratto con fornitori ICT di servizi critici o importanti deve includere:

| Clausola | Contenuto |
|----------|-----------|
| Descrizione del servizio | Dettagliata, con SLA quantitativi |
| Ubicazione dati | Paesi di elaborazione e conservazione, obbligo di notifica in caso di cambiamento |
| Disponibilità, autenticità, integrità, riservatezza dei dati | Obblighi specifici del fornitore |
| Diritto di accesso e audit | L'entità finanziaria e le autorità competenti possono effettuare audit (anche tramite terzi) |
| Cooperazione in caso di incidente | Obbligo del fornitore di assistere nella gestione e segnalazione degli incidenti |
| Piano di uscita | Obblighi di assistenza alla migrazione, restituzione dati, periodo di transizione |
| Risoluzione del contratto | Diritto di recesso in caso di violazioni gravi o cambiamenti che impattano il rischio |
| Sub-outsourcing | Notifica preventiva, diritto di opposizione, catena di responsabilità |

#### Fornitori ICT critici designati (artt. 31-37)

Le ESA (tramite il Joint Committee) designano i fornitori ICT critici per il settore finanziario europeo (tipicamente: grandi cloud provider, core banking vendor).

| Obbligo | Per il fornitore critico |
|---------|------------------------|
| Supervisione diretta delle ESA | Lead Overseer designato (EBA, ESMA o EIOPA) |
| Ispezioni | Le ESA possono ispezionare direttamente il fornitore |
| Raccomandazioni vincolanti | Le ESA possono emettere raccomandazioni, e il fornitore deve conformarsi o spiegare |
| Penalità periodiche | In caso di non conformità, fino a **1% del fatturato medio giornaliero mondiale** per ogni giorno di violazione |

### Pilastro 5 — Accordi di condivisione delle informazioni (art. 45)

| Aspetto | Dettaglio |
|---------|-----------|
| Cosa | Scambio di informazioni su minacce cyber, vulnerabilità, indicatori di compromissione (IoC), TTP (tattiche, tecniche e procedure degli attaccanti) |
| Con chi | Altre entità finanziarie, autorità, CERT nazionali (CSIRT Italia) |
| Base giuridica | DORA autorizza esplicitamente la condivisione, nel rispetto del GDPR e della riservatezza commerciale |
| Forma | Accordi bilaterali o multilaterali, trusted communities, ISAC (Information Sharing and Analysis Centers) |

## Workflow di compliance

### Step 1: Gap analysis

Confrontare lo stato attuale dell'entità con i requisiti DORA:

| Area | Requisito DORA | Stato attuale | Gap | Priorità |
|------|---------------|--------------|-----|----------|
| Governance ICT | Responsabilità CdA, strategia, budget | | | |
| Framework rischio ICT | Policy, procedure, inventario asset | | | |
| Gestione incidenti | Classificazione, segnalazione 4h/72h/1m | | | |
| Continuità operativa | BCP, DR, test annuali | | | |
| Test di resilienza | VA, pentest, TLPT (se applicabile) | | | |
| Terze parti ICT | Registro, clausole contrattuali, piani uscita | | | |
| Condivisione informazioni | Accordi, community, CSIRT | | | |

### Step 2: Piano di rimedio

Per ogni gap identificato:

| Gap | Azione correttiva | Responsabile | Scadenza | Budget |
|-----|-------------------|-------------|----------|--------|
| | | | | |

### Step 3: Implementazione e monitoraggio

| Attività | Frequenza |
|----------|-----------|
| Revisione framework rischio ICT | Annuale |
| Test di resilienza (VA, pentest, BCP) | Annuale |
| Aggiornamento registro terze parti ICT | Continuo (a ogni variazione) + report annuale |
| Formazione organo di gestione su rischi ICT | Almeno annuale |
| Esercitazione di gestione crisi ICT | Almeno annuale |
| TLPT (se entità significativa) | Ogni 3 anni |

### Step 4: Output

Produrre:
1. **Gap analysis DORA** — Tabella requisiti vs. stato attuale, con prioritizzazione
2. **Piano di rimedio** — Azioni, responsabili, scadenze, budget
3. **Registro informazioni terze parti ICT** — Formato conforme all'ITS art. 28(3)
4. **Piano di test annuale** — Calendario VA, pentest, BCP/DR test, scenario testing
5. **Template di segnalazione incidenti** — Notifica iniziale (4h), report intermedio (72h), report finale (1 mese)
6. **Checklist clausole contrattuali** — Per la revisione dei contratti con fornitori ICT critici

## Note importanti

- DORA è un **regolamento** (non una direttiva): è direttamente applicabile in tutti gli Stati membri UE senza necessità di recepimento nazionale. In vigore dal 17 gennaio 2025
- Le autorità italiane competenti per la vigilanza DORA sono Banca d'Italia (per banche e intermediari finanziari), CONSOB (per SIM e mercati), IVASS (per assicurazioni), COVIP (per fondi pensione)
- L'organo di gestione ha responsabilità **personale** sulla resilienza operativa digitale — non è delegabile interamente alla funzione IT
- I contratti con fornitori ICT già in essere devono essere adeguati alle clausole obbligatorie DORA entro il periodo transitorio
- Per i gruppi bancari: il framework di gestione del rischio ICT si applica a livello consolidato, ma ogni entità deve avere la propria capacità di segnalazione degli incidenti
- DORA si coordina con NIS2 (Dir. UE 2022/2555) sulla cybersecurity — le entità finanziarie che rispettano DORA sono considerate conformi ai requisiti NIS2 per la parte di gestione del rischio ICT (art. 4 NIS2)
- Il registro delle informazioni sulle terze parti ICT sarà uno degli strumenti principali di vigilanza: le autorità lo useranno per identificare rischi di concentrazione a livello di sistema finanziario
