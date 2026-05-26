---
name: fsi-merger-model-italy
description: >
  Modello merger (accretion/dilution) per operazioni M&A in Italia: UPA pro forma,
  purchase price allocation IFRS 3, goodwill IAS 36 (impairment, no ammortamento),
  fiscalità IRES+IRAP ~27,9%, affrancamento art. 176 TUIR, deducibilità interessi
  art. 96 TUIR (30% ROL), sinergie, sensitivity. Valuta EUR.
  Triggers on "merger model", "modello merger", "accretion dilution",
  "M&A model", "UPA pro forma", "merger consequences", "impatto acquisizione".
---

# Merger Model — Contesto Italiano

Adapt dello skill US `merger-model`. La meccanica accretion/dilution è universale. Adattati: principi contabili, fiscalità, finanziamento, trattamento goodwill.

**Per il workflow completo** (Step 1-7, sensitivity tables, output): riferirsi allo skill US `merger-model`. Qui si documentano gli adattamenti.

## Adattamenti al Contesto Italiano

### 1. Input — Parametri Italiani

**Acquirente:**
- UPA (Utile Per Azione), non EPS — LTM e NTM, IFRS
- Costo del debito pre-tax su base **Euribor** (non SOFR/Treasury)
- Aliquota fiscale: **~27,9%** (IRES 24% + IRAP ~3,9%)
- Bilancio IFRS: Utile netto, PFN (Posizione Finanziaria Netta)

**Target:**
- Stessi dati in IFRS
- Se non quotato: Valore d'impresa (Enterprise Value) da perizia o negoziazione

**Deal Terms:**
- Consideration: cash, azioni, misto, earnout, vendor loan
- Finanziamento debito: Euribor + spread (tipico 250-450 bps)
- Valuta: **EUR** per tutti gli importi

### 2. Sources & Uses — EUR

| Sources | €M | Uses | €M |
|---------|-----|------|-----|
| Nuovo debito | | Prezzo equity | |
| Cassa disponibile | | Rifinanziamento debito target | |
| Nuove azioni emesse | | Costi di transazione | |
| Vendor loan | | Costi di finanziamento | |
| | | Imposta di registro (se asset deal) | |
| **Totale** | | **Totale** | |

Nota: se asset deal, includere nelle Uses l'imposta di registro (3% avviamento, 2% immobili, fissa per altri beni).

### 3. Pro Forma UPA — IFRS

| | Standalone | Pro Forma | Accretion/(Dilution) |
|---|-----------|-----------|---------------------|
| Utile netto acquirente | | | |
| Utile netto target | | | |
| Sinergie (al netto imposte) | | | |
| Mancati proventi finanziari su cassa (al netto imposte) | | | |
| Nuovi interessi passivi (al netto imposte) | | | |
| Ammortamento intangibili identificati (al netto imposte) | | | |
| **Goodwill: NO ammortamento** (solo impairment test IAS 36) | — | — | — |
| Utile netto pro forma | | | |
| Azioni pro forma | | | |
| **UPA pro forma** | | | |
| **Accretion / (Dilution) %** | | | |

### 4. Goodwill e PPA — IFRS 3

Differenza critica rispetto al modello US:

**IFRS 3 (Business Combinations):**
- Il goodwill **non viene ammortizzato** — sottoposto a impairment test annuale (IAS 36)
- Impatto sul merger model: il goodwill NON genera un costo annuo nell'accretion/dilution (a differenza di vecchi principi contabili)
- Gli intangibili identificati con vita utile definita (customer relationships, tecnologia, brand) vengono ammortizzati — questo SÌ impatta l'UPA pro forma

**Purchase Price Allocation (PPA):**

| Voce | Valore (€M) | Vita utile | Ammortamento annuo |
|------|------------|-----------|-------------------|
| Customer relationships | | X anni | |
| Tecnologia / brevetti | | X anni | |
| Brand / marchio | | Indefinita / X anni | |
| Contratti / backlog | | X anni | |
| Goodwill (residuo) | | Indefinita (no ammort.) | |
| **Totale intangibili** | | | |

Tax benefit dell'ammortamento intangibili: deducibile ai fini IRES (24%), generalmente NON deducibile ai fini IRAP.

### 5. Fiscalità — Differenze Chiave

**Aliquota su sinergie e adjustments:**
- IRES: 24% su sinergie di costo e ricavo
- IRAP: ~3,9% — ma attenzione: IRAP non deduce interessi passivi né costo del lavoro dipendente
- Per sinergie di costo da riduzione personale: il risparmio IRAP è MINORE perché il costo del lavoro non era deducibile in partenza

**Deducibilità interessi — Art. 96 TUIR:**
- Interessi passivi netti deducibili fino al **30% del ROL** (pro forma combinato)
- Se il nuovo debito di acquisizione genera interessi superiori al 30% del ROL → parte del tax shield si perde
- Modellare separatamente:
  1. Interessi passivi netti pro forma
  2. ROL pro forma (acquirente + target + sinergie)
  3. Interessi deducibili = MIN(Interessi netti, 30% ROL)
  4. Tax shield = Interessi deducibili × 24% (solo IRES)

**Affrancamento (art. 176 c. 2-ter TUIR):**
- Opzione di step-up fiscale degli intangibili tramite imposta sostitutiva (12-16%)
- Se esercitato: genera ammortamento fiscalmente deducibile su intangibili rivalutati
- Valutare costo imposta sostitutiva vs beneficio deduzioni future (analisi NPV)
- NON esiste l'equivalente del 338(h)(10) election US

**Share deal vs Asset deal:**
- Share deal: no step-up automatico (salvo affrancamento). Plusvalenza del venditore: PEX ~1,2% se requisiti art. 87 TUIR
- Asset deal: step-up naturale degli asset, ma imposta di registro proporzionale e plusvalenza tassata ordinariamente (~27,9%)

### 6. Sensitivity Tables — Adattamenti

Stessa meccanica dello skill US. Adattare:

**Accretion/Dilution vs Sinergie e Premio:**

| | €0M sin. | €10M sin. | €20M sin. | €30M sin. | €40M sin. |
|---|---------|----------|----------|----------|----------|
| 15% premio | | | | | |
| 20% premio | | | | | |
| 25% premio | | | | | |
| 30% premio | | | | | |

Range sinergie calibrato su deal italiani/europei (tipicamente inferiori a quelli US in valore assoluto).

**Sensitivity aggiuntiva per contesto italiano:**

Accretion/Dilution vs Mix cash/azioni e Deducibilità interessi:

| | 30% ROL binding | 30% ROL non binding |
|---|----------------|-------------------|
| 100% cash | | |
| 50/50 | | |
| 100% azioni | | |

Questa sensitivity mostra l'impatto del vincolo art. 96 TUIR sui deal cash-heavy.

### 7. Breakeven Synergies

Stessa logica dello skill US: sinergie minime per UPA-neutral al Year 1. Nota: il breakeven è diverso da quello US per via di:
- Aliquota più alta (~27,9% vs ~21%)
- Vincolo deducibilità interessi (meno tax shield → servono più sinergie per compensare)
- No ammortamento goodwill (favorisce l'accretion rispetto a US GAAP pre-2001)

### 8. Aspetti Regolamentari nel Modello

Includere una sezione con impatto sulle tempistiche e rischio di esecuzione:

| Approvazione | Tempistica | Rischio |
|-------------|-----------|---------|
| AGCM (se soglie superate) | 30-75 giorni | Remedies possibili |
| EUMR (se soglie UE) | 25 gg lavorativi Fase I | Raro per mid-market |
| Golden Power (se settore strategico) | 45 giorni | Prescrizioni, veto |
| Regolatore settoriale | Variabile | Dipende dal settore |

## Errori Comuni da Evitare

### ❌ Ammortizzare il goodwill
Sotto IFRS 3, il goodwill NON si ammortizza. Si sottopone a impairment test annuale (IAS 36). Inserire ammortamento goodwill nel merger model sovrastima la dilution.

### ❌ Applicare aliquota US 21%
L'aliquota italiana è ~27,9%. Inoltre, IRES e IRAP hanno basi imponibili diverse — non è un'unica aliquota applicata uniformemente.

### ❌ Ignorare art. 96 TUIR
Per deal cash-heavy con leva significativa, il limite di deducibilità interessi (30% ROL) può ridurre materialmente il tax shield. Il modello deve calcolare esplicitamente se il vincolo è binding.

### ❌ Includere 338(h)(10) election
Non esiste in Italia. L'opzione più vicina è l'affrancamento ex art. 176 c. 2-ter TUIR, che ha meccanica e costi completamente diversi.

### ❌ Non distinguere share deal da asset deal
L'impatto fiscale sull'acquirente (step-up, deduzioni, imposta di registro) e sul venditore (PEX vs tassazione ordinaria) è radicalmente diverso. Il merger model deve specificare la struttura.
