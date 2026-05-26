---
name: fsi-client-review-italy
description: >
  Preparazione incontri di revisione periodica con clienti italiani: performance
  portafoglio, allocazione, talking points, azioni raccomandate. Contenitori
  italiani, benchmark FTSE MIB, opportunità fiscali (minusvalenze, fondo pensione),
  verifica adeguatezza MiFID II.
  Triggers on "client review", "revisione cliente", "prep meeting cliente",
  "incontro trimestrale", "revisione portafoglio", "meeting prep [cliente]".
---

# Preparazione Revisione Cliente — Contesto Italiano

Adapt dello skill US `client-review`. Struttura meeting identica. Adattati account types, asset classes, raccomandazioni proattive al contesto italiano.

## Workflow

### Step 1: Contesto Cliente

Raccogliere o verificare:
- **Nome cliente** e nucleo familiare
- **Contenitori**: deposito titoli (regime fiscale), fondo pensione, GPM, PIR, polizze
- **AUM totale** across contenitori
- **Profilo MiFID II**: target allocation, tolleranza al rischio, preferenze ESG, orizzonte temporale
- **Fase di vita**: accumulo, pre-pensionamento, pensionamento, trasmissione patrimoniale
- **Data ultimo incontro** e azioni in sospeso
- **Plafond minusvalenze**: importo e scadenze

### Step 2: Performance Portafoglio

Per ciascun contenitore e aggregato:

| Metrica | Trim. | YTD | 1 Anno | 3 Anni | Dall'inizio |
|---------|-------|-----|--------|--------|-------------|
| Rendimento portafoglio | | | | | |
| Rendimento benchmark | | | | | |
| Alpha | | | | | |

**Attribuzione performance:**
- Quali asset class / posizioni hanno guidato i rendimenti?
- Top 3 contributor e top 3 detractor
- Impatto di singole posizioni sovradimensionate?

### Step 3: Revisione Allocazione

| Asset Class | Target % | Attuale % | Drift | Azione |
|------------|----------|-----------|-------|--------|
| Azionario Europa | | | | |
| Azionario USA | | | | |
| Azionario Emergenti | | | | |
| Obbligazionario Gov. EUR | | | | |
| Obbligazionario Corporate | | | | |
| Alternativi | | | | |
| Liquidità | | | | |

Segnalare drift che supera la soglia di ribilanciamento IPS (tipicamente ±3-5%).

### Step 4: Talking Points

Agenda meeting:

1. **Contesto di mercato** (2-3 min): mercato italiano/europeo, BCE, spread BTP-Bund, outlook
2. **Performance portafoglio** (5 min): come è andato? Perché?
3. **Revisione allocazione** (5 min): serve ribilanciamento? → vedi skill `portfolio-rebalance-italy`
4. **Aggiornamenti di pianificazione** (5-10 min):
   - Cambiamenti di vita? (lavoro, salute, famiglia, casa, figli)
   - Necessità di reddito cambiate?
   - Aggiornamenti situazione fiscale (cambio regime, nuova CU)
   - Situazione previdenziale (estratto conto INPS, contributo fondo pensione)
   - Pianificazione successoria (testamento, beneficiari polizze)
5. **Azioni** (5 min): cosa facciamo prima del prossimo incontro?

### Step 5: Raccomandazioni Proattive

Basate sulla revisione, suggerire:
- **Ribilanciamento** se drift supera soglia → skill `portfolio-rebalance-italy`
- **Compensazione minusvalenze** in scadenza → skill `ottimizzazione-fiscale-portafoglio`
- **Contributo fondo pensione**: il cliente sta massimizzando la deducibilità (€5.164,57/anno)?
- **Conferimento TFR**: se ancora in azienda, valutare conferimento a fondo pensione
- **Switch strumenti**: fondi comuni (redditi di capitale) → ETF (redditi diversi) se il cliente ha minusvalenze
- **PIR**: se il cliente ha spazio, valutare apertura/incremento per esenzione fiscale
- **Verifica adeguatezza MiFID II**: il profilo è ancora attuale? Aggiornare se necessario
- **Protezione**: revisione TCM, LTC, polizza sanitaria integrativa
- **Successione**: verifica beneficiari polizze vita, regime patrimoniale coniugale

### Step 6: Output

- Sintesi revisione 1 pagina (Word o PDF)
- Tabella performance con benchmark
- Grafico allocazione (attuale vs target)
- Azioni raccomandate con priorità
- Agenda meeting
- Nota scadenze (minusvalenze, rinnovo adeguatezza, contributi fondo pensione entro 31/12)

## Errori Comuni da Evitare

### ❌ Suggerire Roth conversion o tax-loss harvesting con logica US
Non esistono Roth conversion in Italia. Il tax-loss harvesting italiano non ha wash sale rule e opera su logiche diverse (plafond quadriennale, redditi di capitale vs diversi). Usare gli skill italiani specifici.

### ❌ Non verificare l'adeguatezza MiFID II
Ad ogni incontro verificare se il profilo MiFID II del cliente è ancora attuale. Cambiamenti di vita (pensionamento, eredità, perdita lavoro) possono modificare il profilo e rendere il portafoglio non adeguato.

### ❌ Dimenticare le scadenze fiscali
Il meeting è l'occasione per ricordare: minusvalenze in scadenza 31/12, contributi fondo pensione deducibili entro 31/12, compilazione 730/Redditi PF (giugno-settembre).
