---
name: fsi-process-letter-italy
description: >
  Lettere di processo e istruzioni per offerte in operazioni M&A sell-side in Italia:
  IOI, offerte vincolanti, management meeting. Tempistiche AGCM/Golden Power,
  esclusività 45-90gg, contratto di cessione partecipazioni, atto notarile S.r.l.,
  diritto civile italiano.
  Triggers on "process letter", "lettera di processo", "bid instructions",
  "istruzioni per offerta", "IOI letter", "lettera secondo round",
  "final bid procedures", "management meeting invite".
---

# Process Letter — Contesto Italiano

Adapt dello skill US `process-letter`. La struttura della lettera e il workflow sono universali. Adattati: framework legale, tempistiche, antitrust, documentazione.

**Per il workflow completo** (Step 1-5, tipologie lettera, output): riferirsi allo skill US `process-letter`. Qui si documentano gli adattamenti.

## Adattamenti al Contesto Italiano

### 1. Lingua della Lettera

- **Deal domestici** (buyer e seller italiani): italiano
- **Deal cross-border** (buyer estero): inglese, con eventuale traduzione italiana per documenti legali
- **Prassi**: la process letter è tipicamente in inglese anche tra parti italiane per deal mid-market+, per uniformità con standard internazionali. Per deal small-cap o con buyer industriali italiani, può essere in italiano.

### 2. IOI Instructions — Integrazioni Italiane

Oltre ai requisiti standard dello skill US, la IOI deve richiedere:

- **Struttura proposta**: cessione partecipazioni (share deal) vs cessione d'azienda/ramo (asset deal) — specificare quale è preferita dal venditore
- **Forma societaria del veicolo acquirente**: S.p.A., S.r.l., NewCo, veicolo estero
- **Analisi regolamentare**:
  - **AGCM (Autorità Garante della Concorrenza e del Mercato)**: il buyer supera le soglie di notifica? (fatturato aggregato Italia >€532M E fatturato Italia dell'acquisita >€32M)
  - **Golden Power**: l'operazione ricade in settori strategici (D.L. 21/2012)? Il buyer è soggetto extra-UE?
  - **Regolatori settoriali**: Banca d'Italia, IVASS, AGCOM, ARERA — serve autorizzazione?
- **Fonte del finanziamento**: equity commitment, debito (su base Euribor), vendor loan
- **Trattamento del management**: conferma/sostituzione, eventuale rollover equity, patti di non concorrenza

### 3. Final Bid / Secondo Round — Integrazioni Italiane

**Contratto di acquisizione:**
- Share deal: **contratto di cessione di partecipazioni** (non SPA/APA nel senso US)
- Asset deal: **contratto di cessione d'azienda** (o ramo d'azienda)
- Richiedere markup del draft contratto preparato dal venditore
- Per cessioni di quote di **S.r.l.**: l'atto richiede **forma notarile** (art. 2470 c.c.) — inserire nota su tempistiche notaio nel cronoprogramma

**Garanzie (Representations & Warranties):**
- Framework italiano: garanzie convenzionali ex art. 1490-1497 c.c. + clausole contrattuali specifiche
- Richiedere posizione del buyer su: clausola di indennizzo, cap (tipico 15-30% del prezzo), basket/deductible, durata garanzie (12-24 mesi, fiscali/lavoro fino a prescrizione)
- Meccanismo di aggiustamento prezzo: locked box (prevalente in Italia) vs completion accounts

**Esclusività:**
- Durata tipica Italia: **45-90 giorni** (vs 30-45 US)
- Motivazione: tempistiche notarili, autorizzazioni regolamentari AGCM, due diligence più estesa su aspetti giuslavoristici e fiscali

**Analisi antitrust — tempistiche:**

| Procedura | Termine | Note |
|-----------|---------|------|
| AGCM — Fase I | 30 giorni dalla notifica completa | Approvazione semplice o avvio Fase II |
| AGCM — Fase II | 45 giorni aggiuntivi | Indagine approfondita (raro per mid-market) |
| EUMR (Commissione UE) | Fase I: 25 gg lavorativi | Se soglie UE superate (€5Mld aggregato + €250M ciascuna in UE) |
| Golden Power | 45 giorni dalla notifica | Estendibili; obbligo di notifica pre-closing |

**Condizioni sospensive (Conditions Precedent) tipiche:**
- Autorizzazione AGCM / Commissione UE
- Esito Golden Power (se applicabile)
- Autorizzazione regolatore settoriale
- Delibera CdA / Assemblea del buyer
- Ottenimento financing
- Assenza MAC (Material Adverse Change)

### 4. Management Meeting — Integrazioni

Stessa struttura dello skill US, con aggiunte:
- **Lingua**: se buyer estero, presentazione in inglese; prevedere interprete se management non anglofono
- **Sede**: tipicamente presso gli uffici della società target o dell'advisor — non è prassi comune il video per primo incontro in Italia
- **Partecipanti lato target**: AD/CEO, CFO, eventualmente Presidente CdA o soci (se azienda familiare — frequente in Italia)
- **Nota culturale**: nel mid-market italiano il rapporto personale con il fondatore/famiglia è spesso determinante. La management presentation non è solo un esercizio finanziario.

### 5. Tempistiche Tipiche — Processo M&A Italiano

| Fase | Durata tipica |
|------|--------------|
| Teaser + NDA | 2-3 settimane |
| CIM + IOI | 3-4 settimane |
| Selezione shortlist | 1-2 settimane |
| Due diligence + management meeting | 6-10 settimane |
| Offerte vincolanti | 3-4 settimane |
| Negoziazione contratto + signing | 4-8 settimane |
| Autorizzazioni (AGCM, Golden Power) | 4-8 settimane |
| Closing | 2-4 settimane post-autorizzazioni |
| **Totale indicativo** | **6-10 mesi** |

Nota: i deal italiani tendono a essere più lunghi di quelli US per via di: complessità fiscale, tempistiche notarili, autorizzazioni regolamentari, negoziazione garanzie, gestione della transizione familiare.

## Errori Comuni da Evitare

### ❌ Usare tempistiche HSR (30 giorni)
L'antitrust italiano (AGCM) ha tempistiche e soglie proprie. L'HSR Act non esiste in Italia. Usare le tempistiche AGCM o EUMR.

### ❌ Riferirsi a SPA/APA senza adattamento
In Italia il contratto è una "cessione di partecipazioni" (share deal) o "cessione d'azienda" (asset deal). La struttura delle garanzie segue il diritto civile italiano, non il common law.

### ❌ Dimenticare l'atto notarile per S.r.l.
La cessione di quote di S.r.l. richiede obbligatoriamente atto notarile (o firma digitale con deposito al Registro Imprese). Non prevedere questa fase nel cronoprogramma è un errore che causa ritardi.

### ❌ Non menzionare Golden Power
Per acquisizioni in settori strategici (energia, TLC, difesa, finanza, AI, semiconduttori, agroalimentare), la notifica Golden Power è obbligatoria. Omettere questa verifica nella process letter è una lacuna significativa.

### ❌ Sottostimare i tempi di esclusività
45-90 giorni è la norma italiana. Proporre 30 giorni come nel mercato US rischia di essere irrealistico e di mettere pressione inutile sul processo.
