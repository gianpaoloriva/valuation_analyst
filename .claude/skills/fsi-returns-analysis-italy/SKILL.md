---
name: fsi-returns-analysis-italy
description: >
  Analisi rendimenti per deal PE nel contesto italiano: sensitivity IRR/MOIC,
  fiscalità cessione partecipazioni (PEX) vs cessione azienda, IRES+IRAP,
  deducibilità interessi (art. 96 TUIR), carried interest (art. 60 D.L. 50/2017),
  financing su Euribor.
  Triggers on "returns analysis", "analisi rendimenti", "IRR sensitivity",
  "MOIC", "rendimento deal", "back of the envelope", "modello rendimenti PE".
---

# Returns Analysis — Contesto Italiano

Rewrite dello skill US `returns-analysis`. Formule IRR/MOIC e sensitivity tables sono universali. Riscritta la sezione fiscale (cessione partecipazioni vs azienda, PEX, IRES+IRAP, carried interest) e il financing (Euribor, leva 3-4x).

## Workflow

### Step 1: Raccolta Input del Deal

Raccogliere o estrarre da analisi precedenti:

**Entry:**
- EBITDA di ingresso (LTM o NTM)
- Multiplo di ingresso (EV / EBITDA)
- Enterprise Value
- PFN (Posizione Finanziaria Netta) al closing
- Equity check
- Costi di transazione (vedi sezione dedicata sotto)

**Finanziamento:**

| Tranche | Multiplo (x EBITDA) | Tasso | Ammortamento | Note |
|---------|-------------------|-------|-------------|------|
| Senior secured (Term Loan A) | | Euribor + spread bps | Ammortizing | |
| Senior secured (Term Loan B) | | Euribor + spread bps | Bullet | |
| Mezzanino / Subordinato | | Fisso o Euribor + spread | PIK o cash | |
| **Leva totale** | | | | |
| Equity | | | | |

**Range tipici mercato italiano mid-market:**
- Leva totale: 3,0-4,5x EBITDA (vs 4,0-6,0x US)
- Senior: 2,0-3,5x EBITDA
- Mezzanino: 0,5-1,5x EBITDA (se presente)
- Costo senior: Euribor 3M/6M + 250-450 bps
- Costo mezzanino: 8-12% (cash + PIK)
- **NON usare SOFR, LIBOR, o Treasury come base rate**

**Ipotesi operative:**
- Crescita ricavi (CAGR)
- Traiettoria margine EBITDA
- Capex come % dei ricavi
- Variazioni NWC (capitale circolante netto)
- Piano di rimborso debito

**Uscita:**
- Holding period (anni) — tipicamente 4-6 anni
- Multiplo di uscita (EV / EBITDA)
- EBITDA all'uscita (calcolato da ipotesi di crescita)

### Step 2: Rendimenti Caso Base

Calcolare:

| Metrica | Valore (€) |
|---------|-----------|
| EV di ingresso | |
| Equity investito | |
| EBITDA all'uscita | |
| EV all'uscita | |
| PFN all'uscita | |
| Equity value all'uscita (lordo) | |
| Costi di uscita (advisory, break fee) | |
| **Equity value all'uscita (netto costi)** | |
| **MOIC lordo** | |
| **IRR lordo** | |
| Cash-on-cash | |

**Returns waterfall — Scomposizione del rendimento:**
- Crescita EBITDA: (Exit EBITDA − Entry EBITDA) × Exit Multiple / Equity
- Espansione/contrazione multiplo: (Exit Multiple − Entry Multiple) × Entry EBITDA / Equity
- Deleveraging: debito rimborsato nel periodo / Equity
- Drag costi di transazione

### Step 3: Sensitivity Tables

Matrici di sensitività a 2 variabili:

**Multiplo di ingresso vs Multiplo di uscita:**

| IRR / MOIC | Uscita 5x | Uscita 6x | Uscita 7x | Uscita 8x | Uscita 9x |
|------------|----------|----------|----------|----------|----------|
| Ingresso 5x | | | | | |
| Ingresso 6x | | | | | |
| Ingresso 7x | | | | | |
| Ingresso 8x | | | | | |

**Crescita EBITDA vs Multiplo di uscita** (a multiplo di ingresso fisso)

**Leva vs Multiplo di uscita** (a ingresso e crescita fissi)

**Holding period vs Multiplo di uscita**

Mostrare sia IRR che MOIC in ogni cella (formato IRR / MOIC).

**Range multipli mercato italiano:**
- Mid-market (EV €30-200M): 5-8x EBITDA
- Large cap: 8-12x EBITDA
- Settori premium (tech, healthcare, lusso): 10-15x
- Settori ciclici/tradizionali: 4-7x

### Step 4: Analisi Scenari

| | Bull | Base | Bear |
|---|------|------|------|
| CAGR ricavi | | | |
| Margine EBITDA all'uscita | | | |
| Multiplo di uscita | | | |
| EBITDA all'uscita | | | |
| MOIC lordo | | | |
| IRR lordo | | | |

### Step 5: Analisi Fiscale — Rendimenti Netti

Questa è la sezione più diversa dal modello US. In Italia non esiste il 338(h)(10) election. Le strutture fiscali rilevanti sono:

#### 5a — Cessione di Partecipazioni (Share Deal)

La struttura più comune per deal PE in Italia.

**Venditore = società (es. fondo PE):**

| Regime | Condizione | Tassazione plusvalenza |
|--------|-----------|----------------------|
| **PEX — Participation Exemption** (art. 87 TUIR) | (i) detenzione ≥12 mesi, (ii) classificazione in immobilizzazioni finanziarie dal 1° bilancio, (iii) società partecipata non in Paese black-list, (iv) società partecipata esercita impresa commerciale | **95% esente** → aliquota effettiva ~1,2% (= 5% imponibile × 24% IRES) |
| Regime ordinario | Se PEX non applicabile | Plusvalenza tassata 100% a IRES 24% + eventuale IRAP |

**Venditore = persona fisica:**

| Regime | Tassazione |
|--------|-----------|
| Partecipazione qualificata o non qualificata | Imposta sostitutiva **26%** sulla plusvalenza |

**Impatto su IRR netto:**
```
Se PEX applicabile (caso tipico per fondo PE):
  Tax on gain ≈ 1,2% della plusvalenza
  IRR netto ≈ IRR lordo − impatto marginale

Se PEX non applicabile:
  Tax on gain = 24% IRES (+ eventuale IRAP ~3,9%)
  IRR netto significativamente inferiore
```

**Verificare sempre i requisiti PEX** — il mancato rispetto di una delle 4 condizioni (soprattutto la classificazione in immobilizzazioni finanziarie dal primo bilancio) fa perdere l'esenzione.

#### 5b — Cessione di Azienda (Asset Deal)

Meno comune nel PE, ma rilevante per carve-out o acquisizioni di rami d'azienda.

| Voce | Trattamento fiscale |
|------|-------------------|
| Plusvalenza | Tassata IRES 24% + IRAP ~3,9% = ~27,9%. Rateizzabile in max 5 esercizi se azienda detenuta >3 anni (art. 86 c. 4 TUIR) |
| Avviamento | Deducibile in 18 anni (1/18 per anno) per l'acquirente |
| Imposta di registro | Proporzionale: 3% su avviamento, 2% su immobili, 1% su altri beni. NON recuperabile |
| IVA | Esclusa (art. 2 c. 3 lett. b DPR 633/72) — cessione d'azienda fuori campo IVA |

**Step-up fiscale (affrancamento):**
L'acquirente può affrancare il maggior valore dei beni acquisiti (incluso avviamento) pagando un'imposta sostitutiva (art. 176 c. 2-ter TUIR):
- 12% fino a €5M
- 14% da €5M a €10M
- 16% oltre €10M

L'affrancamento accelera la deducibilità dell'avviamento e dei maggiori valori, migliorando il cash flow fiscale post-acquisizione.

#### 5c — Deducibilità Interessi (art. 96 TUIR)

Critico per i rendimenti di un LBO:

```
Interessi passivi deducibili nel limite del 30% del ROL
ROL = Valore della produzione − Costi della produzione + Ammortamenti + Canoni leasing

Eccedenza: riportabile senza limiti di tempo ai periodi d'imposta successivi
ROL capiente non utilizzato: riportabile per 5 anni
```

**Impatto sul modello:**
- Con ROL elevato: tutti gli interessi deducibili → tax shield pieno
- Con ROL basso (es. azienda capital-light): parte degli interessi non deducibili → tax shield ridotto → IRR netto inferiore
- Nella sensitivity: modellare l'impatto della limitazione art. 96 sul cash flow effettivo

#### 5d — IRAP sulla Società Target

L'IRAP (aliquota base 3,9%, variabile per regione e settore) ha una base imponibile diversa dall'IRES:
- Interessi passivi: **non deducibili** ai fini IRAP
- Costo del lavoro dipendente: **non deducibile** ai fini IRAP (salvo deduzioni forfettarie)

In un LBO con alta leva, l'IRAP amplifica il carico fiscale effettivo perché gli interessi che riducono l'imponibile IRES non riducono l'imponibile IRAP.

#### 5e — Carried Interest (art. 60 D.L. 50/2017)

Il carried interest percepito dai gestori del fondo PE può essere tassato come reddito di capitale al 26% (anziché come reddito di lavoro, fino al 43%+) se:

| Condizione | Requisito |
|-----------|----------|
| Investimento minimo del gestore | ≥1% del commitment totale del fondo |
| Maturazione | Diritto matura solo dopo restituzione ai LPs del capitale investito + rendimento minimo (hurdle) |
| Detenzione | Strumenti detenuti per l'intera durata dell'investimento |
| Rischio | Partecipazione effettiva al rischio di perdita |

Se le condizioni non sono soddisfatte → il carried è tassato come reddito di lavoro (IRPEF progressiva fino al 43% + addizionali).

### Step 6: Costi di Transazione — Contesto Italiano

| Voce | Stima | Note |
|------|-------|------|
| Advisory M&A (sell-side) | 1,5-3,0% dell'EV | Percentuale decrescente per deal più grandi |
| Advisory M&A (buy-side) | 1,0-2,0% dell'EV | |
| Due diligence (financial, tax, legal) | €150.000 - €500.000 | Per deal mid-market |
| Spese legali | €100.000 - €300.000 | Incluso strutturazione, contratti, regulatory |
| Notaio | €5.000 - €50.000 | Obbligatorio per cessione quote SRL, atti societari |
| Imposta di registro | Proporzionale (se asset deal) o €200 fissa (se share deal con atto registrato) | |
| Financing fees | 1,0-2,5% del debito | Arrangement + commitment fees |
| **Totale tipico** | **3-6% dell'EV** | |

### Step 7: Output

- **Workbook Excel** con:
  - Tab Ipotesi (entry, financing, operative, exit)
  - Tab Calcolo rendimenti (waterfall, MOIC, IRR)
  - Tab Sensitivity (matrici con formattazione condizionale)
  - Tab Scenari (Bull/Base/Bear)
  - Tab Fiscale (confronto share deal PEX vs ordinario vs asset deal, impatto art. 96)
  - Tab Costi di transazione
- **Riepilogo 1 pagina** per deck IC — in EUR, con IRR lordo e netto

## Formule Chiave

```
MOIC = Equity Value all'uscita / Equity Investito

IRR = risolvere per r: Σ CF_t / (1+r)^t = 0
  (dove CF_0 = −Equity investito, CF_n = Exit equity + eventuali distribuzioni intermedie)

Scomposizione rendimenti:
  Crescita = (Exit EBITDA − Entry EBITDA) × Exit Multiple / Equity
  Multiplo = (Exit Multiple − Entry Multiple) × Entry EBITDA / Equity
  Leva     = Debito rimborsato nel periodo / Equity

Tax shield annuo (se interessi deducibili):
  = min(Interessi passivi, 30% ROL) × Aliquota IRES (24%)

PEX — Imposta effettiva su plusvalenza:
  = Plusvalenza × 5% × 24% = Plusvalenza × 1,2%
```

## Errori Comuni da Evitare

### ❌ Applicare il 338(h)(10) election
Non esiste in Italia. Le strutture fiscali rilevanti per deal PE sono: cessione partecipazioni (share deal, regime PEX) e cessione d'azienda (asset deal, con affrancamento opzionale).

### ❌ Usare SOFR o Treasury per il costo del debito
Il mercato italiano/europeo prezza il debito su Euribor (3M o 6M) + spread. Usare sempre Euribor come base rate.

### ❌ Assumere leva US-level
Il mercato italiano mid-market supporta tipicamente 3,0-4,5x EBITDA di leva totale (vs 4,0-6,0x negli US). Banche italiane ed europee sono più conservative. Leva >5x richiede giustificazione forte.

### ❌ Ignorare la limitazione art. 96 TUIR sugli interessi
In un LBO con alta leva, parte degli interessi può non essere deducibile se eccede il 30% del ROL. Questo riduce il tax shield effettivo e peggiora l'IRR netto. Modellare sempre l'impatto.

### ❌ Dare per scontata la PEX
La PEX richiede 4 condizioni cumulative (art. 87 TUIR). Se anche una sola non è soddisfatta — in particolare la classificazione in immobilizzazioni finanziarie dal primo bilancio — l'esenzione non si applica e la plusvalenza è tassata al 100%.

### ❌ Dimenticare l'IRAP sul target
L'IRAP ha una base imponibile che non deduce interessi passivi né costo del lavoro. In un LBO, l'IRAP effettiva è significativamente più alta dell'aliquota nominale 3,9% rapportata all'utile pre-tax. Includerla sempre nel modello.

### ❌ Non considerare l'imposta di registro su asset deal
In una cessione d'azienda, l'imposta di registro proporzionale (3% avviamento, 2% immobili, 1% altri beni) è un costo di transazione significativo e non recuperabile. Includerla nei costi di chiusura.
