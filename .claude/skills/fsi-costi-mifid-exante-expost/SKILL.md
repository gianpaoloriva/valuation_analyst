---
name: fsi-costi-mifid-exante-expost
description: Generazione della reportistica costi e oneri ex-ante (prima dell'investimento) ed ex-post (rendicontazione annuale) obbligatoria ai sensi di MiFID II. Copre costi del servizio, costi del prodotto, incentivi (inducements), impatto cumulato su rendimento, e formato conforme agli Orientamenti ESMA. Triggers su "costi ex-ante", "costi ex-post", "rendicontazione costi", "costi e oneri MiFID", "cost disclosure", "impatto costi sul rendimento", "inducements", "incentivi", "costi del servizio", "costi del prodotto".
---

# Reportistica costi e oneri MiFID II

Riferimenti normativi: art. 24(4) Dir. 2014/65/UE (MiFID II), artt. 50-51 Reg. Delegato UE 2017/565, Orientamenti ESMA 35-43-3288 (costi e oneri), art. 52-54 Reg. Intermediari CONSOB (adottato con delibera n. 20307/2018), Comunicazione CONSOB n. 0097996 del 22/12/2017.

## Principio generale

L'intermediario deve fornire al cliente informazioni complete su tutti i costi e gli oneri in due momenti:

| Momento | Tipo | Obbligo | Riferimento |
|---------|------|---------|-------------|
| **Prima** dell'investimento | **Ex-ante** | Aggregazione di tutti i costi previsti, in modo che il cliente possa comprendere il costo complessivo e l'effetto cumulato sul rendimento | Art. 50(1)-(2) Reg. Delegato |
| **Dopo** (con cadenza annuale) | **Ex-post** | Rendicontazione dei costi effettivamente sostenuti nell'anno, confrontati con quanto comunicato ex-ante | Art. 50(9)-(10) Reg. Delegato |

L'informativa deve essere fornita sia in importo monetario (€) sia in percentuale (%).

## Informativa ex-ante

### Step 1: Identificare tutte le voci di costo

Le voci si dividono in quattro macro-categorie obbligatorie (art. 50(2) Reg. Delegato):

#### A. Costi del servizio di investimento

| Voce | Tipo | Come si calcola | Esempio |
|------|------|----------------|---------|
| Commissione di consulenza | Ricorrente | % annua sul controvalore gestito/consigliato | 1,00% annuo su AUM |
| Commissione di sottoscrizione / ingresso | Una tantum | % o importo fisso sul capitale investito | 1,50% alla sottoscrizione |
| Commissione di negoziazione / esecuzione ordini | Per operazione | Importo fisso o % per trade | €7 per eseguito oppure 0,19% |
| Commissione di switch / trasferimento | Per operazione | % o importo fisso | 0,50% per switch tra fondi |
| Commissione di uscita / rimborso | Una tantum | % sul capitale disinvestito | 1,00% (spesso decrescente nel tempo) |
| Costi di custodia e tenuta conto | Ricorrente | Importo fisso annuo o % | €30/anno oppure 0,10% |
| Costi di conversione valutaria | Per operazione | Spread sul cambio | 0,25% spread FX |

#### B. Costi del prodotto finanziario

| Voce | Tipo | Fonte dell'informazione | Esempio |
|------|------|------------------------|---------|
| Commissione di gestione del fondo/ETF (TER) | Ricorrente | KIID/KID del prodotto, factsheet | 1,50% annuo |
| Commissione di performance | Ricorrente (eventuale) | Regolamento del fondo | 20% dell'overperformance vs benchmark |
| Costi di transazione interni al fondo | Ricorrente | Rendiconto annuale del fondo o EMT (European MiFID Template) | 0,15% annuo stimato |
| Costi di strutturazione (prodotti strutturati) | Implicito | KID PRIIPs | Variabile, spesso 1-3% |
| Spread denaro-lettera (per ETF, certificati) | Implicito | Osservazione di mercato | 0,05-0,50% |
| Oneri fiscali interni al prodotto (es. imposta lussemburghese) | Ricorrente | Documentazione del fondo | Taxe d'abonnement 0,05% |

#### C. Incentivi (inducements) — art. 24(9) MiFID II

| Voce | Descrizione | Obbligo di comunicazione |
|------|-------------|-------------------------|
| Retrocessioni da case prodotto | Quota della commissione di gestione del fondo retrocessa all'intermediario distributore | Importo esatto in € e % |
| Commissioni di collocamento | Commissione pagata dal produttore all'intermediario per la distribuzione | Importo esatto |
| Soft commission | Servizi non monetari ricevuti dall'intermediario (ricerca, accesso a piattaforme) | Descrizione qualitativa + stima valore |

L'intermediario deve dimostrare che gli incentivi sono destinati ad accrescere la qualità del servizio al cliente (**quality enhancement test**). Esempi di quality enhancement accettati da ESMA:
- Accesso a gamma più ampia di prodotti
- Consulenza non indipendente di qualità superiore
- Report periodici aggiuntivi
- Strumenti di monitoraggio del portafoglio

#### D. Pagamenti da/verso terze parti

| Voce | Descrizione |
|------|-------------|
| Pagamenti a terzi | Commissioni pagate dall'intermediario a soggetti terzi (es. consulenti finanziari abilitati all'offerta fuori sede) |
| Pagamenti ricevuti da terzi | Retrocessioni, commissioni di distribuzione (da riportare anche nella sezione C) |

### Step 2: Aggregare i costi — formato tabellare obbligatorio

**Tabella ex-ante completa (formato ESMA):**

| Voce di costo | Una tantum (€) | Una tantum (%) | Ricorrente (€/anno) | Ricorrente (%/anno) |
|--------------|---------------|---------------|--------------------|--------------------|
| **A. Costi del servizio** | | | | |
| Commissione di consulenza | — | — | | |
| Commissione di sottoscrizione | | | — | — |
| Commissione di negoziazione | | | — | — |
| Costi di custodia | — | — | | |
| **Subtotale servizio** | | | | |
| **B. Costi del prodotto** | | | | |
| Commissione di gestione (TER) | — | — | | |
| Commissione di performance | — | — | | |
| Costi di transazione interni | — | — | | |
| **Subtotale prodotto** | | | | |
| **C. Incentivi** | | | | |
| Retrocessioni ricevute da terzi | — | — | | |
| **TOTALE COSTI** | | | | |
| **D. Impatto cumulato su rendimento** | | | | |

### Step 3: Calcolo dell'impatto cumulato sul rendimento

Mostrare come i costi riducono il rendimento nel tempo. Calcolo obbligatorio a più orizzonti:

**Metodologia:**
1. Ipotizzare un rendimento lordo (es. rendimento atteso del portafoglio o scenario neutrale)
2. Sottrarre tutti i costi anno per anno (compounding)
3. Mostrare la differenza tra rendimento lordo e rendimento netto

| Orizzonte | Capitale investito (€) | Rendimento lordo cumulato (€) | Costi cumulati (€) | Rendimento netto cumulato (€) | Impatto costi (%) |
|-----------|----------------------|-------------------------------|--------------------|-----------------------------|-------------------|
| 1 anno | | | | | |
| 3 anni | | | | | |
| 5 anni | | | | | |
| Orizzonte consigliato | | | | | |

**Esempio numerico:**

Per un investimento di €100.000 con rendimento lordo ipotizzato del 5% annuo:

| Anno | Valore lordo (€) | Costi annui (€) | Valore netto (€) | Differenza cumulata (€) |
|------|-----------------|-----------------|------------------|------------------------|
| 0 | 100.000 | 1.500 (ingresso) | 98.500 | −1.500 |
| 1 | 103.425 | 1.970 (1,50% gest. + 0,50% cons.) | 101.455 | −3.470 |
| 3 | 112.087 | — | 106.512 | −5.575 |
| 5 | 121.551 | — | 111.828 | −9.723 |
| 10 | 147.746 | — | 125.036 | −22.710 |

Rendimento effettivo annuo netto: 5,00% − 2,15% costi = **2,85% netto** (prima delle imposte).

### Step 4: Comunicazione al cliente

**Formato di presentazione (requisiti ESMA):**

1. **Tabella aggregata** — Step 2 (sempre)
2. **Illustrazione dell'impatto** — Step 3 (sempre)
3. **Dettaglio per singolo prodotto** — Se il portafoglio contiene più prodotti, mostrare anche il costo di ciascuno
4. **Lingua** — In italiano, chiara e non fuorviante
5. **Supporto** — Durevole (PDF, stampa, email). La comunicazione orale non è sufficiente
6. **Tempistica** — Prima della conclusione dell'operazione (in tempo utile per il cliente per prendere una decisione informata)

## Informativa ex-post (rendicontazione annuale)

### Step 1: Raccogliere i costi effettivi dell'anno

A differenza dell'ex-ante (che è una stima), l'ex-post riporta i costi **effettivamente sostenuti**:

| Voce | Ex-ante (stima, €) | Ex-post (effettivo, €) | Delta (€) | Note |
|------|-------------------|----------------------|----------|------|
| Costi del servizio | | | | |
| Costi del prodotto | | | | |
| Incentivi | | | | |
| **Totale** | | | | |

### Step 2: Impatto su rendimento effettivo

| Voce | Importo (€) | % su patrimonio medio |
|------|-------------|----------------------|
| Patrimonio medio nell'anno | | 100% |
| Rendimento lordo | | % |
| Costi totali effettivi | | % |
| **Rendimento netto (ante imposte)** | | % |
| Imposte | | % |
| **Rendimento netto (post imposte)** | | % |

### Step 3: Dettaglio per strumento

Per ciascuno strumento in portafoglio:

| Strumento | ISIN | Patrimonio medio (€) | Costo prodotto (€) | Costo prodotto (%) | Costo servizio allocato (€) | Incentivi (€) | Costo totale (%) |
|-----------|------|---------------------|--------------------|--------------------|----------------------------|--------------|-----------------|
| | | | | | | | |

### Step 4: Confronto pluriennale

Se disponibili dati storici, mostrare l'andamento dei costi nel tempo:

| Anno | Patrimonio medio (€) | Costi totali (€) | Costi totali (%) | Rendimento netto (%) |
|------|---------------------|------------------|------------------|---------------------|
| 2024 | | | | |
| 2025 | | | | |
| 2026 | | | | |

### Step 5: Comunicazione

| Requisito | Dettaglio |
|-----------|-----------|
| Frequenza | **Annuale** (almeno). Può essere inclusa nel rendiconto periodico |
| Tempistica | Entro i primi mesi dell'anno successivo (tipicamente entro marzo-aprile) |
| Formato | Supporto durevole (PDF, email, area riservata). Tabella aggregata + dettaglio |
| Lingua | Italiano, chiara e comprensibile |

## Casi particolari

### Consulenza indipendente (art. 24(7) MiFID II)

| Differenza | Consulenza non indipendente | Consulenza indipendente |
|------------|---------------------------|------------------------|
| Incentivi | Ammessi (con quality enhancement test e comunicazione al cliente) | **Vietati**. L'intermediario non può ricevere alcun incentivo monetario da terzi |
| Fee | Può essere inclusa nelle commissioni del prodotto (retrocessa) | Fee esplicita pagata dal cliente (% su AUM, fee fissa, fee per consulenza) |
| Comunicazione costi | Tutte le voci, inclusi incentivi | Tutte le voci. Gli incentivi devono essere restituiti al cliente |

### Gestione di portafogli (GPM/GPF)

| Requisito aggiuntivo | Dettaglio |
|---------------------|-----------|
| Frequenza reportistica | **Trimestrale** (art. 60(1) Reg. Delegato), non solo annuale |
| Contenuto aggiuntivo | Composizione del portafoglio, rendimento del periodo, benchmark, turnover |
| Costi di transazione | Devono essere riportati singolarmente (ogni eseguito) nella reportistica periodica |
| Soglia di perdita | Comunicazione immediata se il patrimonio scende del **10%** (e successivamente per ogni multiplo di 10%) rispetto al valore di inizio periodo |

### Prodotti assicurativi d'investimento (IBIP)

Per polizze unit-linked, multiramo e index-linked (regolate anche da IVASS):

| Voce aggiuntiva | Dettaglio |
|-----------------|-----------|
| Caricamenti | Costi di sottoscrizione specifici delle polizze |
| Costi di riscatto | Penali di uscita anticipata, spesso decrescenti nel tempo |
| Costi di gestione della polizza | Distinti dalla commissione di gestione del fondo sottostante |
| Costo di copertura caso morte | Se inclusa garanzia assicurativa, indicarne il costo |
| KID PRIIPs | Obbligatorio per IBIP distribuiti a clienti retail dal 01/01/2023 |

## Workflow completo

### Step 1: Input

Raccogliere:
- Profilo del cliente (retail, professionale, controparte qualificata)
- Tipo di servizio (consulenza non indipendente, consulenza indipendente, gestione, RTO, execution only)
- Strumenti finanziari coinvolti (con ISIN)
- Capitale investito o da investire
- KID/KIID di ciascun prodotto (per costi del prodotto)
- Condizioni economiche del servizio (contratto quadro, foglio informativo)
- EMT (European MiFID Template) dei prodotti, se disponibile

### Step 2: Costruzione informativa ex-ante

1. Estrarre costi del servizio dal contratto/foglio informativo
2. Estrarre costi del prodotto da KID/KIID o EMT
3. Identificare incentivi (retrocessioni) dal pricing sheet interno
4. Aggregare nella tabella dello Step 2 della sezione ex-ante
5. Calcolare impatto cumulato su rendimento (Step 3 della sezione ex-ante)
6. Formattare in PDF/supporto durevole

### Step 3: Costruzione rendicontazione ex-post

1. Estrarre costi effettivi dal sistema contabile dell'intermediario
2. Estrarre costi del prodotto dal rendiconto annuale del fondo/EMT aggiornato
3. Calcolare patrimonio medio dell'anno (media dei valori a fine mese o fine trimestre)
4. Confrontare ex-ante vs ex-post
5. Calcolare impatto su rendimento effettivo
6. Dettagliare per strumento
7. Formattare in PDF/supporto durevole

### Step 4: Output

Produrre:
1. **Informativa costi ex-ante** — Tabella aggregata + impatto cumulato (PDF)
2. **Rendicontazione costi ex-post** — Tabella aggregata + dettaglio per strumento + confronto con ex-ante (PDF)
3. **Scheda confronto pluriennale** — Se disponibili dati storici
4. **Alert** — Segnalare se i costi totali superano soglie di attenzione (es. >2,5% annuo per un portafoglio bilanciato retail)

## Note importanti

- L'obbligo di informativa costi si applica a **tutti** i clienti, inclusi i professionali (ESMA ha chiarito che l'opt-out è possibile solo per controparti qualificate e per costi del prodotto di clienti professionali, previa richiesta esplicita)
- I costi di transazione interni ai fondi sono spesso la voce più sottostimata: l'EMT è la fonte più affidabile
- La commissione di performance deve essere stimata ex-ante sulla base dei dati storici o di un modello ragionevole
- Se l'intermediario riceve incentivi non monetari (es. accesso a piattaforme di ricerca), deve darne comunicazione qualitativa
- CONSOB ha più volte sanzionato intermediari per informativa costi inadeguata — è un'area di attenzione ispettiva prioritaria
- Per i servizi di execution only su strumenti non complessi: l'obbligo di informativa costi è ridotto ma non eliminato (art. 50(1) Reg. Delegato si applica comunque)
- L'impatto cumulato deve essere calcolato con la metodologia del compounding (interesse composto), non con la semplice somma dei costi annui — la differenza è significativa su orizzonti lunghi
