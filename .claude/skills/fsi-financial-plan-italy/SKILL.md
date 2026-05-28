---
name: fsi-financial-plan-italy
description: >
  Piano finanziario personalizzato per clienti italiani: proiezioni pensionistiche
  (INPS + previdenza complementare D.Lgs. 252), cash flow con IRPEF progressiva,
  pianificazione successoria (imposta successione italiana), obiettivi di risparmio.
  Triggers on "piano finanziario", "financial plan", "pianificazione finanziaria",
  "posso andare in pensione", "pensione", "piano previdenziale", "successione",
  "cash flow personale", "piano risparmi".
---

# Piano Finanziario — Contesto Italiano

Rewrite dello skill US `financial-plan`. Il framework metodologico (accumulo/distribuzione/scenari) si riusa, ma ogni componente è riscritto per il sistema previdenziale, fiscale e successorio italiano.

## Quadro Normativo di Riferimento

- **INPS / Pensione pubblica**: L. 335/1995 (Dini), L. 214/2011 (Fornero), D.L. 4/2019 (Quota 100/102/103)
- **Previdenza complementare**: D.Lgs. 252/2005
- **Fiscalità investimenti**: D.Lgs. 461/1997, TUIR (DPR 917/1986)
- **IRPEF**: TUIR art. 11-14, scaglioni aggiornati alla Legge di Bilancio vigente
- **Successione e donazione**: D.Lgs. 346/1990 (TUS)
- **TFR**: art. 2120 c.c., L. 296/2006 (conferimento a fondo pensione)

## Workflow

### Step 1: Profilo Cliente

Raccogliere o confermare:

**1a — Anagrafica e lavoro:**
- Età, età coniuge/partner, figli a carico (con età)
- Stato lavorativo: dipendente privato / dipendente pubblico / autonomo / libero professionista / imprenditore
- RAL (Retribuzione Annua Lorda) o reddito professionale lordo
- Anzianità contributiva INPS attuale (anni e mesi)
- Cassa previdenziale di appartenenza (se professionista: Cassa Forense, ENPAM, Inarcassa, CNPADC, ecc.)
- Aspettativa di crescita retributiva reale

**1b — Patrimonio finanziario:**

| Voce | Valore (€) | Intermediario | Regime fiscale | Note |
|------|-----------|---------------|---------------|------|
| Deposito titoli (azioni, ETF, obbligazioni) | | | Amm./Dich./Gestito | |
| Conti correnti e depositi | | | | |
| Fondo pensione negoziale | | | | Contributo datore + TFR |
| Fondo pensione aperto / PIP | | | | |
| TFR lasciato in azienda | | | | Solo se azienda >50 dip. = Fondo INPS |
| PIR (Piani Individuali di Risparmio) | | | | Holding period e composizione |
| Polizze vita / Unit-linked | | | | Ramo I / III / multiramo |
| Immobili (esclusa prima casa) | | | | Rendita catastale, IMU, cedolare secca |
| Partecipazioni societarie | | | | Qualificate / non qualificate |
| **Totale patrimonio** | | | | |

**1c — Redditi e fonti:**

| Fonte | Lordo annuo (€) | Netto stimato (€) | Durata prevista |
|-------|-----------------|-------------------|----------------|
| Stipendio / Reddito professionale | | | Fino a pensionamento |
| Redditi da locazione | | | |
| Dividendi / cedole | | | |
| Altro (assegni, rendite) | | | |

**1d — Passività:**

| Debito | Saldo residuo (€) | Rata mensile (€) | Tasso | Scadenza |
|--------|-------------------|------------------|-------|----------|
| Mutuo prima casa | | | Fisso/Variabile | |
| Mutuo altri immobili | | | | |
| Prestiti personali | | | | |
| Altro | | | | |

**1e — Protezione e assicurazioni:**

| Copertura | Presente? | Importo/Dettaglio | Adeguatezza |
|-----------|----------|------------------|-------------|
| TCM (Temporanea Caso Morte) | | Capitale assicurato € | |
| Invalidità permanente | | | |
| Long-Term Care (LTC) | | | |
| RC professionale | | | Obbligatoria per professionisti |
| Polizza sanitaria integrativa | | | Fondo sanitario aziendale? |

**1f — Situazione successoria:**
- Testamento redatto? (olografo / pubblico / assente)
- Regime patrimoniale coniugale: comunione / separazione dei beni
- Donazioni effettuate (rilevano ai fini della franchigia successoria)
- Beneficiari designati su polizze vita e fondi pensione

### Step 2: Analisi Cash Flow

Proiezione annuale del cash flow:

| Anno | Età | Reddito lordo (€) | IRPEF + addiz. (€) | Contributi INPS (€) | Spese correnti (€) | Rate debiti (€) | Risparmio netto (€) |
|------|-----|-------------------|-------------------|---------------------|--------------------|-----------------|--------------------|
| | | | | | | | |

**Parametri chiave:**
- **Inflazione**: obiettivo BCE 2%, usare 2,0-2,5% per proiezioni
- **IRPEF**: scaglioni vigenti (2024-2026: 23% fino a €28.000, 35% €28.001-€50.000, 43% oltre €50.000) + addizionali regionali (0,9-3,33%) + comunali (0-0,9%)
- **Contributi previdenziali**: dipendenti ~9,19% a carico lavoratore; autonomi/professionisti variabile per cassa
- **Detrazioni**: lavoro dipendente/autonomo, carichi di famiglia, interessi mutuo prima casa (19% fino a €4.000), spese sanitarie (19% oltre franchigia €129,11)
- **Deduzioni**: contributi previdenza complementare (fino a €5.164,57/anno), contributi obbligatori

### Step 3: Proiezioni Pensionistiche

Questa è la sezione più critica e diversa dal modello US.

**3a — Pensione pubblica INPS:**

| Parametro | Valore |
|-----------|--------|
| Sistema di calcolo | Contributivo / Misto / Retributivo |
| Montante contributivo attuale | € (da Estratto Conto INPS) |
| Aliquota di computo | 33% (dipendenti) / 24-25% (autonomi) |
| Tasso di capitalizzazione | Media quinquennale PIL nominale |
| Coefficiente di trasformazione | Basato sull'età al pensionamento (tabelle INPS, aggiornate ogni 2 anni) |

**Requisiti di accesso alla pensione (verificare aggiornamenti normativi):**

| Tipologia | Età | Contributi | Note |
|-----------|-----|-----------|------|
| Vecchiaia ordinaria | 67 anni | 20 anni | Adeguamento aspettativa di vita |
| Anticipata (uomini) | Qualsiasi | 42 anni e 10 mesi | |
| Anticipata (donne) | Qualsiasi | 41 anni e 10 mesi | |
| Opzione Donna | 61 anni | 35 anni | Con penalizzazione, requisiti restrittivi |
| APE Sociale | 63 anni e 5 mesi | 30-36 anni | Categorie specifiche (gravosi, disoccupati, caregiver, invalidi) |
| Quota 103 | 62 anni | 41 anni | Verificare se ancora in vigore — misura temporanea |

**Stima pensione pubblica:**
```
Pensione annua lorda = Montante contributivo × Coefficiente di trasformazione

Esempio (età 67):
- Montante: €400.000
- Coefficiente: 5,723% (tabelle 2023)
- Pensione lorda: €22.892/anno → ~€1.750/mese netti
```

**Tasso di sostituzione**: rapporto pensione netta / ultimo stipendio netto
- Dipendente RAL €40.000: ~60-65% (contributivo puro)
- Dipendente RAL €80.000: ~50-55%
- Autonomo: ~40-50%
- Il gap rispetto al 100% è il "gap previdenziale" da colmare con previdenza complementare

**3b — Previdenza complementare (D.Lgs. 252/2005):**

| Parametro | Valore |
|-----------|--------|
| Tipo fondo | Negoziale / Aperto / PIP |
| Posizione accumulata | € |
| Contributo lavoratore | % della RAL |
| Contributo datore di lavoro | % della RAL (solo negoziale) |
| Conferimento TFR | 100% / Quota / Nessuno |
| Linea di investimento | Garantita / Obbligazionaria / Bilanciata / Azionaria |
| Anni mancanti al pensionamento | |
| Rendimento atteso netto (per linea) | 1-4% reale |

**Proiezione rendita complementare:**
```
Montante a scadenza = Posizione attuale × (1 + r)^n + Contribuzione annua × [(1 + r)^n - 1] / r

Prestazione:
- Rendita (100%) — tassazione agevolata 15% (ridotta di 0,30% per ogni anno oltre il 15° di partecipazione, minimo 9%)
- Capitale (max 50%) + Rendita (min 50%) — se montante > limite COVIP
- Capitale 100% — solo se rendita < 50% assegno sociale
```

**Vantaggi fiscali previdenza complementare:**
- Deducibilità contributi fino a €5.164,57/anno (riduce IRPEF all'aliquota marginale)
- Rendimenti tassati al 20% (vs 26% regime ordinario)
- Prestazione finale: 15% → 9% (vs IRPEF ordinaria, risparmio molto significativo)
- TFR in fondo pensione rivalutato a rendimenti di mercato (vs 1,5% + 75% inflazione se lasciato in azienda)

**3c — Riepilogo pensionistico:**

| Voce | Importo lordo annuo (€) | Importo netto mensile stimato (€) |
|------|------------------------|----------------------------------|
| Pensione INPS | | |
| Rendita fondo pensione | | |
| Eventuali altre rendite (affitti, capitale) | | |
| **Totale entrate in pensione** | | |
| Spese stimate in pensione | | |
| **Gap annuo** | | |

### Step 4: Analisi per Obiettivo

#### 4a — Istruzione figli

In Italia non esiste un equivalente del 529 plan US. L'istruzione universitaria pubblica è relativamente accessibile:

| Voce | Costo annuo stimato (€) | Note |
|------|------------------------|------|
| Università pubblica (tasse) | 500 - 4.000 | In base a ISEE |
| Università privata (Bocconi, LUISS, Cattolica) | 8.000 - 15.000 | |
| Master post-laurea | 5.000 - 30.000 | MBA internazionali molto di più |
| Alloggio fuori sede | 5.000 - 10.000/anno | Città variabile (Milano > Bologna > Napoli) |
| Erasmus / studio all'estero | 3.000 - 8.000/semestre | Borsa UE parziale |

**Piano di accumulo per istruzione:**
- Orizzonte: anni alla prima iscrizione del figlio
- Importo target totale per figlio
- Risparmio mensile necessario (con rendimento atteso)
- Strumenti: PAC in ETF azionari (lungo termine), BTP o fondi obbligazionari (medio termine)
- Nessun vantaggio fiscale specifico per accumulo istruzione (a differenza del 529 US)

#### 4b — Pianificazione Successoria

Il sistema successorio italiano è radicalmente diverso da quello US.

**Imposta di successione (D.Lgs. 346/1990):**

| Grado di parentela | Aliquota | Franchigia per beneficiario |
|--------------------|----------|---------------------------|
| Coniuge e parenti in linea retta (figli, genitori) | 4% | €1.000.000 |
| Fratelli e sorelle | 6% | €100.000 |
| Altri parenti fino al 4° grado, affini in linea retta, affini in linea collaterale fino al 3° grado | 6% | Nessuna |
| Tutti gli altri soggetti | 8% | Nessuna |
| Portatori di handicap (L. 104) | Come sopra | €1.500.000 |

**Differenze chiave vs US:**
- In US: estate tax 40% sopra ~$13M → in Italia: max 8%, franchigie per beneficiario (non per patrimonio totale)
- L'imposta italiana è molto più leggera; la pianificazione successoria è meno urgente fiscalmente ma resta importante civilisticamente
- **Legittima**: quote riservate inderogabili a coniuge e figli (art. 536-564 c.c.) — non si può diseredare
- **Donazioni in vita**: le donazioni riducono la franchigia successoria (coacervo)

**Strumenti di pianificazione successoria italiana:**

| Strumento | Uso | Vantaggio |
|-----------|-----|----------|
| Testamento | Disposizione della quota disponibile | Flessibilità, basso costo |
| Donazione | Trasferimento in vita | Anticipo successione, gestione patrimonio |
| Polizza vita | Designazione beneficiario | Esente da imposta di successione (art. 12 TUS), impignorabile e insequestrabile |
| Trust | Segregazione patrimonio | Protezione, pianificazione generazionale (complesso) |
| Patto di famiglia (art. 768-bis c.c.) | Trasferimento azienda/partecipazioni | Evita conflitti successori, efficienza fiscale |
| Fondo patrimoniale | Protezione beni familiari | Destinazione a bisogni della famiglia |

**Polizza vita — Vantaggio successorio:**
Le somme corrisposte ai beneficiari di polizze vita per causa di morte sono esenti dall'imposta di successione (art. 12 c. 2 D.Lgs. 346/1990). Questo le rende uno strumento potente per la trasmissione del patrimonio.

#### 4c — Gestione del Rischio

| Rischio | Copertura italiana | Note |
|---------|-------------------|------|
| Morte prematura | TCM (Temporanea Caso Morte) | Calcolo capitale: reddito da proteggere × anni, meno patrimonio disponibile |
| Invalidità | INPS riconosce assegno ordinario di invalidità e pensione di inabilità; gap da coprire con polizza privata | L'assegno INPS è spesso insufficiente |
| Non autosufficienza (LTC) | Polizze LTC private; INPS eroga indennità di accompagnamento (~€530/mese nel 2024) | Costo RSA: €2.000-4.000/mese — gap enorme |
| Salute | SSN copre il base; integrare con polizza sanitaria o fondo sanitario aziendale (es. FASI, Metasalute) | Tempi SSN lunghi per visite specialistiche |
| RC professionale | Obbligatoria per professionisti (L. 148/2011) | |
| RC auto/casa | Polizza auto obbligatoria; casa consigliata | |

### Step 5: Scenari

Modellare gli scenari chiave:

| Scenario | Patrimonio a 67 anni (€) | Rendita totale netta (€/mese) | Gap vs spese (€/mese) | Probabilità di sostenibilità |
|----------|--------------------------|-------------------------------|----------------------|----------------------------|
| Caso base | | | | |
| Pensionamento anticipato (−2 anni) | | | | Coefficiente trasformazione inferiore |
| Crollo mercati −20% anno 1 | | | | |
| Spese +20% | | | | |
| Longevità: un coniuge vive fino a 95 | | | | |
| Evento LTC (5 anni di non autosufficienza) | | | | Costo €3.000/mese × 60 mesi |
| Aumento contributo fondo pensione al massimo deducibile | | | | Effetto fiscale + accumulo |

**Scenari specifici italiani da testare:**
- Cambio normativo pensioni (innalzamento età, riduzione coefficienti)
- Variazione addizionali regionali (trasferimento residenza)
- Passaggio da cedolare secca a IRPEF su immobili (o viceversa)
- Liquidazione TFR in azienda vs conferimento a fondo pensione

### Step 6: Raccomandazioni

Azioni prioritizzate:

**Previdenza e risparmio:**
1. Ottimizzare contribuzione al fondo pensione (massimizzare deducibilità €5.164,57)
2. Conferire il TFR al fondo pensione (se non già fatto)
3. Valutare linea di investimento del fondo pensione in base all'orizzonte temporale
4. Adeguare il tasso di risparmio per colmare il gap previdenziale

**Fiscalità:**
5. Ottimizzazione regime fiscale investimenti (dichiarativo vs amministrato) — vedi skill `ottimizzazione-fiscale-portafoglio`
6. Valutare detrazioni/deduzioni non utilizzate (interessi mutuo, spese mediche, erogazioni liberali)
7. Cedolare secca vs IRPEF ordinaria su immobili locati

**Protezione:**
8. Adeguare copertura TCM al fabbisogno calcolato
9. Valutare polizza LTC (prima si sottoscrive, più basso il premio)
10. Verificare adeguatezza polizza sanitaria integrativa

**Successione:**
11. Redigere o aggiornare testamento
12. Valutare designazione beneficiari su polizze vita per vantaggio successorio (esenzione art. 12 TUS)
13. Verificare regime patrimoniale coniugale (comunione/separazione) in coerenza con obiettivi
14. Se patrimonio elevato: valutare donazioni in vita (con coacervo franchigia)

**Investimenti:**
15. Asset allocation coerente con orizzonte temporale e profilo MiFID II — vedi skill `mifid-ii-adeguatezza`
16. Valutare PIR per efficienza fiscale su investimenti in PMI italiane — vedi skill `pir-pianificazione`
17. Ribilanciamento periodico del portafoglio

### Step 7: Output

Produrre i seguenti deliverable:

1. **Piano finanziario** (Word/PDF, 20-30 pagine) con:
   - Sintesi situazione attuale
   - Analisi previdenziale completa (gap pensionistico)
   - Cash flow proiettato (pre e post pensionamento)
   - Analisi per obiettivo (istruzione, successione, protezione)
   - Scenari e stress test
   - Raccomandazioni prioritizzate con timeline
2. **Foglio di calcolo proiezioni** (Excel):
   - Cash flow annuale proiettato
   - Montante INPS e fondo pensione
   - Evoluzione patrimonio per scenario
3. **Scheda pensionistica** — riepilogo 1 pagina: età pensionamento, pensione INPS stimata, rendita complementare, gap, azioni
4. **Checklist azioni** — lista prioritizzata con responsabile (cliente / consulente / commercialista / notaio) e scadenza

## Errori Comuni da Evitare

### ❌ Usare la Social Security per stimare la pensione italiana
Il sistema INPS è contributivo (dal 1996 per i nuovi assunti, misto per chi aveva anzianità pre-1996). I coefficienti di trasformazione, il montante, e le regole di accesso sono completamente diversi dalla Social Security US.

### ❌ Riferirsi a 401k, IRA, o Roth IRA
In Italia: fondi pensione negoziali (per categoria contrattuale), fondi aperti, PIP. La deducibilità è €5.164,57/anno (non $23.500). Non esiste la distinzione pre-tax/Roth. La tassazione agevolata è sulla prestazione finale (15%→9%), non sui contributi.

### ❌ Usare RMD (Required Minimum Distributions)
Le RMD non esistono in Italia. La prestazione dal fondo pensione è erogabile al pensionamento in rendita e/o capitale (max 50% in capitale, salvo eccezioni). Non c'è obbligo di distribuzione minima.

### ❌ Sottovalutare il vantaggio fiscale del fondo pensione
Il triplo vantaggio (deduzione contributi + tassazione agevolata rendimenti 20% + tassazione agevolata prestazione 15-9%) rende il fondo pensione lo strumento più efficiente in Italia per il risparmio previdenziale. Molti clienti non massimizzano la deducibilità.

### ❌ Applicare l'estate tax US alla successione italiana
L'imposta di successione italiana è molto più leggera (4-8% con franchigie) rispetto alla US (40% sopra ~$13M). La pianificazione successoria italiana è più focalizzata sulla legittima (quote riservate) che sull'ottimizzazione fiscale.

### ❌ Ignorare il TFR come componente del piano
Il TFR è un asset significativo (circa 1 mensilità/anno di lavoro). La scelta tra lasciarlo in azienda (rivalutazione 1,5% + 75% CPI) e conferirlo al fondo pensione (rendimenti di mercato + vantaggio fiscale) ha un impatto rilevante sul patrimonio finale.

### ❌ Non considerare le addizionali regionali e comunali IRPEF
Le addizionali possono aggiungere fino al 4% all'aliquota marginale. Ignorarle porta a sottostimare il carico fiscale e sovrastimare il cash flow netto. Il cambio di residenza regionale può avere impatto fiscale significativo.
