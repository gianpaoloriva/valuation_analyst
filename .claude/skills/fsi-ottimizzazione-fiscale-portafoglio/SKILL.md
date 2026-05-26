---
name: fsi-ottimizzazione-fiscale-portafoglio
description: >
  Ottimizzazione fiscale del portafoglio investimenti nel contesto italiano.
  Identifica minusvalenze da compensare, gestisce il plafond quadriennale,
  distingue redditi di capitale e redditi diversi, confronta i tre regimi
  fiscali (dichiarativo, amministrato, gestito).
  Triggers on "ottimizzazione fiscale", "compensazione minusvalenze",
  "tax loss", "harvest", "minusvalenze in scadenza", "zainetto fiscale",
  "regime fiscale portafoglio", "planning fiscale investimenti".
---

# Ottimizzazione Fiscale Portafoglio

Rewrite completo dello skill US `tax-loss-harvesting`. La wash sale rule non esiste in Italia; il sistema fiscale italiano opera su logiche completamente diverse (tre regimi, distinzione redditi di capitale/diversi, plafond quadriennale).

## Quadro Normativo di Riferimento

- **D.Lgs. 461/1997**: disciplina dei redditi diversi di natura finanziaria e i tre regimi
- **TUIR art. 44-48**: definizione redditi di capitale
- **TUIR art. 67-68**: definizione redditi diversi
- **L. 190/2014 art. 1 c. 999-1006**: aliquota unificata 26%
- **D.Lgs. 44/2014**: riforma tassazione OICR (redditi di capitale dal 1° luglio 2014)

## Concetti Fondamentali

### Distinzione Redditi di Capitale vs Redditi Diversi

Questa è la distinzione più critica dell'intero skill. Le minusvalenze possono compensare SOLO redditi diversi, MAI redditi di capitale.

| Categoria | Tipo | Aliquota | Compensabile con minusvalenze? |
|-----------|------|----------|-------------------------------|
| Capital gain da vendita azioni/ETF | Reddito diverso | 26% | ✅ SÌ |
| Capital gain da vendita obbligazioni corporate | Reddito diverso | 26% | ✅ SÌ |
| Capital gain da vendita titoli di stato (BTP, BOT, CCT) | Reddito diverso | 12,5% | ✅ SÌ (al 48,08%) |
| Proventi da OICR (fondi comuni, SICAV) — dal 01/07/2014 | **Reddito di capitale** | 26% | ❌ NO |
| Dividendi azionari | **Reddito di capitale** | 26% | ❌ NO |
| Cedole obbligazionarie | **Reddito di capitale** | 26% (12,5% gov) | ❌ NO |
| Proventi da certificates (senza capital protection) | Reddito diverso | 26% | ✅ SÌ |
| Proventi da certificates (con capital protection) | **Reddito di capitale** | 26% | ❌ NO |
| Proventi da polizze unit-linked (riscatto) | **Reddito di capitale** | 26% | ❌ NO |

**Coefficiente di equalizzazione titoli di stato**: le minusvalenze su titoli tassati al 12,5% sono compensabili solo per il 48,08% (= 12,5/26) del loro importo.

### I Tre Regimi Fiscali

| Aspetto | Dichiarativo | Amministrato | Gestito |
|---------|-------------|-------------|---------|
| Chi calcola le imposte | Investitore (in dichiarazione) | Intermediario (per singola operazione) | Intermediario (su risultato netto annuo) |
| Compensazione minusvalenze | Tra tutti gli intermediari, in dichiarazione | Solo all'interno dello stesso intermediario | Automatica, redditi di capitale e diversi compensati insieme |
| Plafond minusvalenze | Gestito dall'investitore | Gestito dall'intermediario ("zainetto fiscale") | Risultato negativo riportato al periodo successivo |
| Compensazione cross-intermediario | ✅ SÌ | ❌ NO (serve passaggio a dichiarativo) | ❌ NO |
| Dividendi/cedole compensabili | ❌ NO | ❌ NO | ✅ SÌ (regime gestito compensa tutto) |
| Adatto a | Investitori con più intermediari, vuole flessibilità | Retail, semplicità, singolo intermediario | Grandi patrimoni, gestioni patrimoniali |

### Regola del Plafond Quadriennale

Le minusvalenze realizzate in un anno possono essere utilizzate per compensare plusvalenze realizzate **entro i 4 anni successivi**:

- Minusvalenza realizzata nel 2024 → utilizzabile fino al 31/12/2028
- **FIFO**: le minusvalenze più vecchie vengono utilizzate per prime
- **Scadenza**: le minusvalenze non utilizzate entro il 4° anno vengono perse definitivamente
- Nel regime amministrato: l'intermediario gestisce automaticamente il plafond ("zainetto fiscale")
- Nel regime dichiarativo: l'investitore deve tracciare e riportare in dichiarazione (quadro RT)

## Workflow

### Step 1: Mappatura Regime Fiscale e Posizioni

Raccogliere tutte le informazioni sulla situazione fiscale del cliente:

**1a — Regime e intermediari:**

| Intermediario | Regime | Deposito Titoli | Note |
|--------------|--------|----------------|------|
| | Dichiarativo / Amministrato / Gestito | | |

**1b — Posizioni con plusvalenze/minusvalenze latenti:**

| Titolo | ISIN | Tipo strumento | Classe fiscale | Quantità | PMC (€) | Prezzo attuale (€) | P/L latente (€) | P/L % | Intermediario |
|--------|------|---------------|---------------|----------|---------|-------------------|-----------------|-------|---------------|
| | | Azione/ETF/Obbligazione/Fondo/Certificate | Rd.Diverso / Rd.Capitale | | | | | | |

- **PMC** = Prezzo Medio di Carico (costo fiscalmente riconosciuto, può differire dal prezzo di acquisto per corporate action, raggruppamenti, ecc.)
- **Classe fiscale**: determinare se il provento sarà reddito diverso o reddito di capitale — questo è il dato più importante

**1c — Zainetto fiscale attuale (regime amministrato) o plafond minusvalenze (dichiarativo):**

| Anno di realizzo | Minusvalenza residua (€) | Scadenza | Mesi alla scadenza | Urgenza |
|-----------------|-------------------------|----------|-------------------|---------|
| 2022 | | 31/12/2026 | | 🔴 ALTA |
| 2023 | | 31/12/2027 | | 🟡 MEDIA |
| 2024 | | 31/12/2028 | | 🟢 BASSA |
| 2025 | | 31/12/2029 | | 🟢 BASSA |
| **Totale plafond** | | | | |

### Step 2: Analisi Urgenze — Minusvalenze in Scadenza

Calcolare le minusvalenze che rischiano di andare perse:

**Priorità 1 — Minusvalenze in scadenza entro l'anno corrente:**
- Importo in scadenza: €___
- Mesi residui: ___
- Azione richiesta: realizzare plusvalenze su redditi diversi entro il 31/12

**Priorità 2 — Minusvalenze in scadenza l'anno prossimo:**
- Importo in scadenza: €___
- Pianificazione anticipata consigliata

**Stima capacità di assorbimento del portafoglio:**
- Plusvalenze latenti su strumenti che generano redditi diversi: €___
- Di cui realizzabili senza alterare l'asset allocation: €___
- Gap rispetto alle minusvalenze in scadenza: €___

### Step 3: Identificazione Opportunità di Compensazione

Tre strategie distinte, in ordine di priorità:

**Strategia A — Realizzo plusvalenze per assorbire minusvalenze in scadenza:**

Se il cliente ha minusvalenze nel plafond in scadenza, cercare posizioni con plusvalenze latenti su strumenti che generano REDDITI DIVERSI:

| Titolo in gain | P/L latente (€) | Tipo reddito | Minusvalenza compensata | Risparmio fiscale (€) | Azione |
|---------------|-----------------|-------------|------------------------|----------------------|--------|
| | | Rd. Diverso ✅ | | × 26% = | Vendere e riacquistare |
| | | Rd. Capitale ❌ | Non compensabile | 0 | Non utile |

**⚠️ ATTENZIONE — NESSUNA WASH SALE IN ITALIA**: a differenza degli USA, in Italia non esiste la wash sale rule. Il cliente può vendere un titolo per realizzare la plusvalenza e riacquistarlo immediatamente. Questo è perfettamente legale e una delle strategie di ottimizzazione più efficaci.

**Strategia B — Realizzo minusvalenze per creare plafond futuro:**

Se il cliente ha posizioni in perdita e prevede plusvalenze future, valutare il realizzo anticipato delle minusvalenze:

| Titolo in loss | P/L latente (€) | Tipo reddito | Scadenza se realizzata oggi | Azione |
|---------------|-----------------|-------------|---------------------------|--------|
| | | Rd. Diverso | 31/12/(anno+4) | Vendere e riacquistare |

**Strategia C — Switch strumenti per efficienza fiscale:**

Sostituire strumenti che generano redditi di capitale con strumenti equivalenti che generano redditi diversi:

| Strumento attuale | Tipo reddito | Sostituto proposto | Tipo reddito sostituto | Esposizione equivalente? | Note |
|------------------|-------------|-------------------|----------------------|------------------------|------|
| Fondo comune azionario | Rd. Capitale ❌ | ETF equivalente | Rd. Diverso ✅ | Sì | Il gain da vendita ETF è compensabile |
| SICAV | Rd. Capitale ❌ | ETF stesso indice | Rd. Diverso ✅ | Sì | |
| Polizza unit-linked | Rd. Capitale ❌ | Certificates (no capital protection) | Rd. Diverso ✅ | Valutare | Rischio emittente su certificates |

### Step 4: Simulazione Impatto Fiscale

Calcolare il risparmio netto di ogni operazione proposta:

**Per ciascuna operazione:**

```
Plusvalenza / Minusvalenza realizzata:      € ___
Minusvalenza compensata dal plafond:        € ___ (FIFO)
Imponibile netto:                           € ___
Imposta (26% o 12,5%):                      € ___
Risparmio vs. non-operare:                  € ___
Costi di transazione (commissioni + spread): € ___
Risparmio netto:                            € ___
```

**Riepilogo complessivo:**

| Metrica | Importo (€) |
|---------|-------------|
| Minusvalenze in scadenza recuperate | |
| Plusvalenze realizzate (per assorbire plafond) | |
| Imposta risparmiata (plafond che sarebbe scaduto × 26%) | |
| Nuove minusvalenze create (plafond futuro) | |
| Valore fiscale del nuovo plafond (× 26%) | |
| Costi di transazione totali | |
| **Beneficio fiscale netto** | |

**Verifica regime amministrato multi-intermediario:**
Se il cliente ha conti presso più intermediari in regime amministrato, le minusvalenze di un intermediario NON possono compensare plusvalenze di un altro. In questo caso valutare:
1. Concentrare le operazioni sullo stesso intermediario dove risiede il plafond
2. Passaggio temporaneo a regime dichiarativo per compensazione cross-intermediario
3. Trasferimento titoli (con mantenimento del PMC) verso l'intermediario con il plafond

### Step 5: Considerazioni per Regime Specifico

**Se regime AMMINISTRATO (più comune):**
- La compensazione è automatica all'interno dello stesso intermediario
- Lo "zainetto fiscale" è visibile sull'estratto conto o posizione titoli
- Attenzione al timing: operazioni entro il 31/12 per utilizzare plafond in scadenza
- Verificare che l'intermediario applichi correttamente il FIFO sulle minusvalenze
- Se il cliente ha più intermediari: il plafond è isolato per ciascuno

**Se regime DICHIARATIVO:**
- Il cliente ha piena flessibilità: può compensare tra intermediari diversi
- Richiede compilazione quadro RT del Modello Redditi PF
- Le minusvalenze vanno riportate anno per anno
- Più complesso ma più flessibile per ottimizzazione
- Consigliato per clienti con patrimoni su più intermediari

**Se regime GESTITO (GPM):**
- Il gestore compensa automaticamente plusvalenze e minusvalenze
- Vantaggio unico: anche i redditi di capitale sono compensabili nel risultato netto di gestione
- Il risultato negativo di gestione si riporta ai periodi successivi
- Se il cliente esce dal regime gestito: il risultato negativo non è trasferibile al regime amministrato/dichiarativo (si perde)
- "Affrancamento" a fine anno: possibilità di cristallizzare il risultato positivo

### Step 6: Titoli di Stato — Trattamento Speciale

I titoli di stato italiani (BTP, BOT, CCT, CTZ) e equivalenti white-list hanno tassazione agevolata al 12,5%. Questo impatta la compensazione:

**Coefficiente 48,08% (= 12,5 / 26):**
- Se si realizza una minusvalenza di €1.000 su un BTP → il plafond aumenta solo di €480,80
- Se si vuole compensare una plusvalenza di €1.000 su un'azione → servono €2.080 di plusvalenza su BTP per consumare lo stesso plafond
- Viceversa: una minusvalenza di €1.000 su azioni genera plafond pieno di €1.000

**Implicazione strategica:** è più efficiente generare minusvalenze su strumenti tassati al 26% e plusvalenze su titoli di stato, piuttosto che il contrario.

| Operazione | Impatto su plafond | Efficienza |
|-----------|-------------------|------------|
| Minusvalenza su azione (26%) | 100% dell'importo | ✅ Ottimale |
| Minusvalenza su BTP (12,5%) | 48,08% dell'importo | ⚠️ Meno efficiente |
| Plusvalenza su azione compensata da plafond | Assorbe 100% | ✅ Ottimale |
| Plusvalenza su BTP compensata da plafond | Assorbe 48,08% | ✅ Consuma meno plafond |

### Step 7: Piano di Esecuzione

| # | Data | Intermediario | Azione | Titolo | ISIN | Quantità | Prezzo stimato (€) | P/L stimato (€) | Tipo reddito | Impatto plafond (€) | Riacquisto? |
|---|------|--------------|--------|--------|------|----------|-------------------|-----------------|-------------|--------------------|----|
| | | | Vendita | | | | | | | | |
| | | | Acquisto | | | | | | | | |

**Timing:**
- Per minusvalenze in scadenza: eseguire entro il 31/12 dell'anno corrente
- Settlement T+2: per operazioni di fine anno, ultimo giorno utile di trading ~ 28-29 dicembre
- Stacco cedola/dividendo: vendere PRIMA dello stacco se si vuole evitare il reddito di capitale non compensabile
- Operatività in strumenti illiquidi: considerare impatto bid-ask spread

**Riepilogo esecuzione:**

| Metrica | Valore |
|---------|--------|
| Minusvalenze plafond in scadenza salvate | € |
| Nuove minusvalenze create (plafond futuro) | € |
| Plusvalenze realizzate (assorbite da plafond) | € |
| Risparmio fiscale totale stimato | € |
| Costi di transazione stimati | € |
| Beneficio netto | € |
| Impatto su asset allocation | Minimo / Da ribilanciare |

### Step 8: Output

Produrre i seguenti deliverable:

1. **Mappa fiscale del portafoglio** (Excel) — ogni posizione con classe fiscale, PMC, P/L latente, intermediario
2. **Scadenziario minusvalenze** — plafond per anno con date di scadenza e urgenze
3. **Piano operazioni** — lista trade con timing, importi, e impatto fiscale
4. **Simulazione risparmio** — confronto scenario "non fare nulla" vs "ottimizzazione"
5. **Note per il consulente** — punti di attenzione specifici per il regime fiscale del cliente

## Errori Comuni da Evitare

### ❌ Compensare minusvalenze con redditi di capitale
Le minusvalenze (redditi diversi negativi) NON possono MAI compensare dividendi, cedole, o proventi da fondi/SICAV. Solo i proventi da vendita di azioni, ETF, obbligazioni, e certificates senza capital protection sono compensabili.

### ❌ Confondere ETF e fondi comuni ai fini fiscali
Dal 1° luglio 2014: il gain da vendita di un ETF è reddito diverso (compensabile ✅), mentre il provento da riscatto/vendita di un fondo comune/SICAV è reddito di capitale (non compensabile ❌). Questa distinzione è cruciale per la scelta degli strumenti sostitutivi.

### ❌ Ignorare la scadenza del plafond
Le minusvalenze scadono dopo 4 anni. Una minusvalenza di €50.000 che scade il 31/12 vale potenzialmente €13.000 di risparmio fiscale (50.000 × 26%). Non monitorare le scadenze equivale a perdere denaro.

### ❌ Dimenticare il coefficiente 48,08% su titoli di stato
Una minusvalenza di €10.000 su BTP non genera €10.000 di plafond, ma solo €4.808. Errore frequente nei calcoli di ottimizzazione.

### ❌ Pensare che il plafond sia cross-intermediario in regime amministrato
In regime amministrato, lo zainetto fiscale è ISOLATO per intermediario. Minusvalenze presso Banca A non compensano plusvalenze presso Banca B. Serve il regime dichiarativo per la compensazione cross-intermediario.

### ❌ Uscire dal regime gestito con risultato negativo
Se il cliente chiude una gestione patrimoniale con risultato negativo, quel saldo negativo viene PERSO — non è trasferibile ad altri regimi. Valutare sempre prima di uscire.

### ❌ Applicare la logica della wash sale rule US
In Italia NON esiste la wash sale rule. È perfettamente legale vendere un titolo e riacquistarlo immediatamente per realizzare una plusvalenza o minusvalenza. Non inserire vincoli temporali inesistenti.
