---
name: fsi-portfolio-rebalance-italy
description: >
  Analisi drift di portafoglio e raccomandazioni di ribilanciamento per clienti
  italiani. Considera i tre regimi fiscali (amministrato/dichiarativo/gestito),
  compensazione minusvalenze con plafond quadriennale, asset location tra
  deposito titoli, fondo pensione, GPM e PIR, coerenza MiFID II.
  Triggers on "ribilanciamento", "rebalance", "drift portafoglio", "portafoglio
  sbilanciato", "asset allocation check", "ribilanciare", "riequilibrare portafoglio".
---

# Ribilanciamento Portafoglio — Contesto Italiano

Adapt dello skill US `portfolio-rebalance`. L'algoritmo di drift detection e trade generation è universale. Riscritta la tassonomia conti, la logica fiscale (no wash sale, compensazione minusvalenze, 3 regimi), e l'asset location.

## Workflow

### Step 1: Stato Attuale

Per ciascun contenitore del cliente, raccogliere:

| Contenitore | Intermediario | Regime fiscale | Valore (€) | Note |
|------------|---------------|---------------|-----------|------|
| Deposito titoli | | Amministrato / Dichiarativo | | Plafond minusvalenze: € |
| Fondo pensione (negoziale/aperto/PIP) | | — (regime proprio) | | Linea: |
| GPM (Gestione Patrimoniale) | | Gestito | | Risultato netto YTD: € |
| PIR | | Amministrato/Dichiarativo | | Holding period rispettato? |
| Polizza Unit-linked | | — (regime assicurativo) | | Ramo I / III / Multiramo |
| Conto corrente / Depositi | | | | |

Per il deposito titoli, catturare per ogni posizione:

| Titolo | ISIN | Asset class | Tipo strumento | Quantità | PMC (€) | Valore (€) | P/L latente (€) | Classe fiscale |
|--------|------|-----------|---------------|----------|---------|-----------|-----------------|---------------|
| | | | Azione/ETF/Fondo/Bond/Certificate | | | | | Rd.Diverso / Rd.Capitale |

### Step 2: Analisi Drift

Confrontare l'allocazione corrente con i target dell'IPS (Investment Policy Statement) o del profilo MiFID II:

| Asset Class | Target % | Attuale % | Drift | € Sovra/Sotto |
|------------|----------|-----------|-------|---------------|
| Azionario Europa (FTSE MIB, EURO STOXX) | | | | |
| Azionario USA | | | | |
| Azionario Paesi Emergenti | | | | |
| Azionario Globale ex-Europa | | | | |
| Obbligazionario Governativo EUR | | | | |
| Obbligazionario Corporate EUR | | | | |
| Obbligazionario High Yield | | | | |
| Obbligazionario Inflation-Linked | | | | |
| Alternativi (Immobiliare/Commodities) | | | | |
| Liquidità | | | | |

Segnalare le posizioni che superano la banda di ribilanciamento (tipicamente ±3-5%).

**Verifica coerenza MiFID II**: il portafoglio ribilanciato deve restare coerente con il profilo di adeguatezza del cliente (conoscenza, esperienza, situazione finanziaria, obiettivi, tolleranza al rischio, preferenze ESG). Se il drift ha portato il portafoglio fuori dal profilo, il ribilanciamento è prioritario.

### Step 3: Raccomandazioni di Trade

#### 3a — Regole di Ribilanciamento Tax-Aware

**In Italia NON esiste la wash sale rule**: si può vendere e ricomprare lo stesso titolo immediatamente. Questo semplifica enormemente il ribilanciamento rispetto al modello US.

La logica fiscale del ribilanciamento italiano si basa su:

**Priorità 1 — Ribilanciare nel fondo pensione (se possibile):**
- Cambiare linea di investimento (es. da bilanciata ad azionaria) non genera eventi fiscali
- Nessun impatto su plafond minusvalenze
- Limiti: si può solo scegliere tra le linee offerte dal fondo, non singoli titoli

**Priorità 2 — Ribilanciare nella GPM:**
- Il regime gestito compensa automaticamente tutti i redditi (capitale + diversi)
- Nessun impatto su plafond esterno alla GPM
- Il gestore può operare nei limiti del mandato

**Priorità 3 — Ribilanciare nel deposito titoli con logica fiscale:**

| Situazione | Azione consigliata |
|-----------|-------------------|
| Plafond minusvalenze in scadenza | Vendere posizioni in GAIN su strumenti che generano redditi diversi per assorbire il plafond |
| Posizione in loss da ridurre | Vendere per creare plafond minusvalenze (utilizzabile entro 4 anni) e riacquistare subito |
| Posizione in gain ST da ridurre | Vendere — l'aliquota è 26% flat (non penalizzazione per short-term come in US) |
| Posizione in gain LT da ridurre | Vendere — stessa aliquota 26% (nessuna distinzione ST/LT in Italia) |
| Sottopeso da colmare | Acquistare — nessun impatto fiscale |
| Fondo comune in gain da ridurre | Attenzione: il provento è reddito di capitale (NON compensabile con minusvalenze) |

**Nessuna distinzione short-term / long-term in Italia**: l'aliquota sul capital gain è 26% flat indipendentemente dalla durata di detenzione. Questo elimina la penalizzazione fiscale per vendite a breve termine.

**Priorità 4 — Dirigere i nuovi flussi:**
- PAC (Piano di Accumulo) sulle classi sottopeso
- Nuovi contributi al fondo pensione se sotto il massimo deducibile
- Nuova liquidità diretta agli strumenti in sottopeso

#### 3b — Lista Trade

| # | Contenitore | Azione | Titolo | ISIN | Quantità/€ | Motivo | Impatto fiscale | Impatto plafond |
|---|------------|--------|--------|------|-----------|--------|----------------|----------------|
| | Dep. Titoli | Vendita | | | | Ribilanciamento / Compensazione | Gain €X (26%) / Loss €X | +/− € plafond |
| | Dep. Titoli | Acquisto | | | | Ribilanciamento | Nessuno | Nessuno |
| | Fondo Pensione | Switch linea | | | | Ribilanciamento | Nessuno | Nessuno |

### Step 4: Asset Location — Ottimizzazione per Contenitore

La logica di asset location italiana è strutturalmente diversa da quella US perché i contenitori hanno regimi fiscali diversi.

| Contenitore | Strumenti ideali | Motivazione |
|------------|-----------------|-------------|
| **Fondo pensione** | Linea con più alta componente azionaria se orizzonte lungo | Rendimenti tassati 20% (vs 26%); linea più aggressiva massimizza il vantaggio fiscale differito |
| **PIR** | Azioni/ETF italiani ed europei (PMI) | Esente da capital gain se holding 5 anni e composizione rispettata; mettere qui asset ad alta crescita attesa |
| **GPM (Gestione Patrimoniale)** | Fondi comuni, OICR, obbligazioni con cedole elevate | Il regime gestito compensa redditi di capitale con minusvalenze — vantaggio unico; collocare qui strumenti che generano redditi di capitale non compensabili altrove |
| **Deposito titoli** | ETF, azioni, certificates (redditi diversi) | Preferire strumenti che generano redditi diversi — compensabili con minusvalenze; evitare fondi comuni (redditi di capitale) se si hanno minusvalenze da assorbire |
| **Polizza Unit-linked** | Asset a lungo termine, componente successoria | Vantaggio successorio (esenzione art. 12 TUS), impignorabilità; non prioritario per ribilanciamento tattico |

**Regola chiave**: se il cliente ha minusvalenze nel plafond, concentrare le vendite in gain su strumenti che generano redditi diversi (azioni, ETF) nel deposito titoli. NON vendere fondi comuni in gain per ribilanciare — quel gain è reddito di capitale e non assorbe il plafond.

### Step 5: Verifica PIR

Se il cliente ha un PIR, verificare che il ribilanciamento non violi i vincoli di composizione:

| Vincolo PIR | Requisito | Rispettato? |
|------------|----------|-------------|
| ≥70% in strumenti finanziari emessi da imprese residenti in Italia o UE/SEE con stabile organizzazione in Italia | | |
| Di cui ≥30% del 70% (= 21% del totale) in strumenti non FTSE MIB / equivalente | | |
| ≤10% concentrazione su singolo emittente | | |
| Holding period 5 anni per esenzione fiscale | | |

Se il ribilanciamento proposto viola un vincolo PIR → segnalare e proporre alternative che rispettino la composizione.

### Step 6: Implementazione

| Metrica | Valore |
|---------|--------|
| Totale trade per contenitore | Dep. titoli: X, Fondo pensione: X, GPM: X |
| Costi di transazione stimati (commissioni + spread) | € |
| Imposta su plusvalenze realizzate (26%) | € |
| Minusvalenze realizzate (nuovo plafond) | € |
| Minusvalenze in scadenza assorbite | € |
| Risparmio fiscale da compensazione | € |
| Drift residuo dopo ribilanciamento | |

### Step 7: Output

1. **Tabella drift** — prima e dopo il ribilanciamento, con target
2. **Lista trade** (Excel) — per contenitore, con impatto fiscale per trade
3. **Riepilogo fiscale** — plusvalenze tassate, minusvalenze create/assorbite, impatto su plafond
4. **Confronto allocazione** — grafico before/after
5. **Nota MiFID II** — conferma coerenza con profilo di adeguatezza

## Errori Comuni da Evitare

### ❌ Applicare la wash sale rule
Non esiste in Italia. Si può vendere e ricomprare lo stesso titolo immediatamente per realizzare un gain o un loss. Non inserire vincoli temporali di 30 giorni.

### ❌ Distinguere short-term e long-term gain
In Italia l'aliquota capital gain è 26% flat indipendentemente dalla durata. Non c'è penalizzazione per vendite a breve termine (a differenza degli US dove ST gain è tassato come reddito ordinario).

### ❌ Vendere fondi comuni per assorbire minusvalenze
Il provento da vendita/riscatto di fondi comuni e SICAV è reddito di capitale dal 2014. NON è compensabile con minusvalenze nel plafond. Se il cliente ha minusvalenze da assorbire, vendere ETF o azioni in gain.

### ❌ Ribilanciare nel deposito titoli senza considerare il plafond
Ogni operazione di vendita nel deposito titoli ha impatto sul plafond minusvalenze. Il ribilanciamento è un'occasione per ottimizzare: vendere in gain per assorbire minusvalenze in scadenza, o vendere in loss per creare plafond futuro.

### ❌ Ignorare i vincoli PIR
Vendere titoli nel PIR può far perdere il beneficio fiscale (esenzione capital gain) se si viola la composizione o si interrompe il holding period. Verificare sempre prima di operare.

### ❌ Considerare il fondo pensione come un conto libero
Nel fondo pensione non si scelgono i singoli titoli — si può solo cambiare linea di investimento. Includere il fondo nella visione complessiva dell'asset allocation, ma le operazioni possibili sono limitate allo switch di linea.

### ❌ Non considerare i flussi in arrivo
Prima di generare trade, verificare: prossime cedole/dividendi, contributi fondo pensione in arrivo, PAC attivi, scadenze obbligazionarie. Questi flussi possono correggere il drift senza necessità di operazioni aggiuntive.
