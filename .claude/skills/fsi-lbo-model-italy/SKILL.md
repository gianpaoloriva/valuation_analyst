---
name: fsi-lbo-model-italy
description: >
  Modello LBO per operazioni di private equity in Italia: template Excel con
  formule, debt schedule su Euribor, fiscalità IRES+IRAP (~27,9%), leva 3-4x,
  PEX per exit, art. 96 TUIR su deducibilità interessi, PFN, valuta EUR.
  Triggers on "LBO model", "modello LBO", "leveraged buyout", "LBO Italia",
  "modello acquisizione con leva", "LBO template".
---

# Modello LBO — Contesto Italiano

Adapt dello skill US `lbo-model`. La meccanica Excel (formule, formattazione, Office JS/openpyxl, verifica) è universale. Qui si documentano gli adattamenti per deal PE in mercato italiano.

**Per template, istruzioni Excel, color conventions, verification checklist**: riferirsi allo skill US `lbo-model`. Tutte le istruzioni su Office JS, openpyxl, formula color conventions (blue/black/purple/green), fill palette, section-by-section workflow restano invariate.

## Adattamenti al Contesto Italiano

### 1. Formattazione Numeri — EUR

Sostituire tutti i formati valuta US con formati EUR:

| Tipo | US | Italia |
|------|-----|--------|
| Valuta | `$#,##0;($#,##0);"-"` | `€#.##0;(€#.##0);"-"` |
| Valuta decimale | `$#,##0.0` | `€#.##0,0` |
| Percentuali | `0.0%` | `0,0%` |
| Multipli | `0.0"x"` | `0,0"x"` |
| MOIC | `0.00"x"` | `0,00"x"` |

Nota: Excel italiano usa `;` come separatore decimale e `.` come migliaia. Verificare le impostazioni regionali del file.

### 2. Sources & Uses — Parametri Italiani

**Leva tipica mercato italiano:**
- Senior secured: 2,0-3,0x EBITDA (vs 3,0-4,0x US)
- Totale debito: 3,0-4,5x EBITDA (vs 4,0-6,0x US)
- Equity: 40-55% delle sources (vs 30-45% US)

**Costo del debito:**
- Base rate: **Euribor 3M o 6M** (NON SOFR/Treasury)
- Senior secured: Euribor + 300-450 bps
- Mezzanino: Euribor + 600-900 bps (o tasso fisso 8-12%)
- Unitranche: Euribor + 500-700 bps

**Costi di transazione tipici:**
- Commissione di arrangement: 1,5-2,5% del debito
- Advisory fee: 1,0-2,0% dell'enterprise value
- Due diligence (contabile, fiscale, legale, ambientale): €200K-€1M+ a seconda della dimensione
- Notaio e imposta di registro (se asset deal): variabile

**PFN (Posizione Finanziaria Netta):**
Nella sezione Uses, il debito netto del target va espresso come PFN — metrica standard nel mercato italiano:
```
PFN = Debiti finanziari (breve + lungo termine) + TFR (se > 5% EV)
      − Disponibilità liquide − Titoli a breve
```
Il TFR va considerato come passività quasi-finanziaria se materiale rispetto all'enterprise value.

### 3. Operating Model — Fiscalità Italiana

**Aliquota fiscale:**
- **IRES**: 24% (imposta sul reddito delle società)
- **IRAP**: ~3,9% (varia per regione, base imponibile diversa — no deduzione costo del lavoro pieno)
- **Aliquota combinata**: ~27,9%

**Calcolo IRAP (semplificato):**
L'IRAP si calcola su una base imponibile diversa dall'IRES: non deduce interessi passivi né costo del lavoro dipendente (con eccezioni). Nel modello LBO:
```
IRAP ≈ (EBIT + Costo del lavoro non deducibile) × 3,9%
```
Per semplicità, molti modelli usano ~27,9% su EBIT. Se il deal ha forte componente labour-intensive, modellare IRAP separatamente.

**Deducibilità interessi — Art. 96 TUIR:**
- Interessi passivi deducibili fino al **30% del ROL** (Risultato Operativo Lordo ≈ EBITDA fiscale)
- Eccedenza non dedotta: riportabile in avanti **senza limiti di tempo**
- ROL eccedente non utilizzato: riportabile in avanti per **5 anni**
- Nel debt schedule, modellare separatamente:
  1. Interessi passivi lordi
  2. Limite 30% ROL
  3. Interessi deducibili = MIN(Interessi, 30% ROL + ROL riportato)
  4. Tax shield effettivo = Interessi deducibili × 24% (solo IRES, non IRAP)

Questa è una differenza critica rispetto al modello US dove gli interessi sono generalmente deducibili per intero.

**ACE / Super ACE (se applicabile):**
- Agevolazione sul capitale proprio incrementale (Aiuto alla Crescita Economica)
- Verificare normativa in vigore (soggetta a modifiche con Legge di Bilancio annuale)

### 4. Debt Schedule — Struttura Italiana

**Tipologie di debito:**
| Tranche | Tasso | Ammortamento | Priorità |
|---------|-------|-------------|----------|
| Revolving Credit Facility | Euribor + 250-350 bps | Bullet | 1 (draw/repay) |
| Term Loan A | Euribor + 300-400 bps | Ammortamento 5-10% annuo | 2 |
| Term Loan B | Euribor + 350-450 bps | Bullet (5-7 anni) | 3 |
| Mezzanino | 8-12% fisso o Euribor + 600-900 | PIK o bullet | 4 |
| Vendor Loan | 3-5% fisso | Bullet (2-3 anni) | 5 |

**Cash sweep:**
- Tipico: 50-75% dell'Excess Cash Flow
- Excess Cash Flow = EBITDA − Interessi cash − Tasse − CapEx − ΔWC − Ammortamento debito obbligatorio
- Step-down: riduzione % sweep al raggiungimento di target di leva (es. 75% sopra 3,0x → 50% sotto 3,0x)

**Covenant finanziari (per verifica nel modello):**
- Leverage ratio: PFN/EBITDA ≤ soglia (tipico 4,0-5,0x, decrescente)
- Interest cover: EBITDA/Interessi ≥ soglia (tipico 2,0-3,0x)
- DSCR (Debt Service Coverage Ratio): ≥ 1,1-1,2x

### 5. Returns Analysis — Regime Fiscale Exit

**Scenario PEX (Participation Exemption — art. 87 TUIR):**
Se il veicolo di acquisizione è una società italiana e soddisfa i 4 requisiti:
1. Holding period ≥ 12 mesi
2. Iscrizione in bilancio come immobilizzazione finanziaria dal primo esercizio
3. Residenza fiscale della partecipata in paese non black-list
4. La partecipata esercita un'impresa commerciale

→ **95% della plusvalenza esente** da IRES → aliquota effettiva ~1,2%

**Scenario regime ordinario:**
Se PEX non applicabile → plusvalenza tassata IRES 24% + eventuale IRAP

**Nel modello, mostrare sempre entrambi gli scenari:**
```
Exit Equity Value
− Invested Equity
= Capital Gain
× Aliquota (PEX 1,2% vs Ordinario 24%)
= Tasse su exit
= Net Proceeds

IRR (PEX)      | IRR (Ordinario)
MOIC (PEX)     | MOIC (Ordinario)
```

**Carried interest:**
Per GP con carried interest strutturato come reddito di capitale (art. 60 D.L. 50/2017), aliquota 26% — modellare separatamente se richiesto.

### 6. Sensitivity Tables — Assi Italiani

Le sensitivity tables seguono la stessa meccanica US (dimensioni dispari, centro = base case, highlight centro). Adattare le variabili agli assi rilevanti per il mercato italiano:

**Assi tipici:**
- Entry multiple (EV/EBITDA) vs Exit multiple
- Entry multiple vs Crescita EBITDA
- Leva (PFN/EBITDA) vs Exit multiple
- Spread Euribor vs Crescita EBITDA

**Formati:**
- IRR in `0,0%`
- MOIC in `0,00x`
- Importi in `€#.##0`

### 7. Errori Comuni — Specifici Italia

### ❌ Usare SOFR o Treasury come base rate
Il debito in Italia è prezzato su **Euribor**. Usare sempre Euribor 3M o 6M + spread.

### ❌ Applicare aliquota US 21%
L'aliquota italiana è ~27,9% (IRES 24% + IRAP ~3,9%). Sottostimare le tasse gonfia i rendimenti.

### ❌ Ignorare il limite art. 96 TUIR
In Italia gli interessi NON sono deducibili per intero. Il limite è 30% del ROL. Per deal con alta leva, il tax shield effettivo può essere significativamente inferiore a quanto modellato senza questo vincolo.

### ❌ Non mostrare scenario PEX vs Ordinario
La differenza fiscale sull'exit è enorme (~1,2% vs ~24%). Il modello deve sempre presentare entrambi gli scenari nei returns.

### ❌ Assumere leva US (5-6x)
Il mercato italiano supporta leva inferiore (3-4,5x EBITDA). Assumere leva US produce modelli irrealistici per deal italiani.

### ❌ Dimenticare il TFR nella PFN
Il TFR è una passività specifica italiana. Se materiale, va incluso nella PFN come passività quasi-finanziaria. Omettere il TFR sottostima il debito effettivo del target.

### ❌ Non modellare IRAP separatamente per deal labour-intensive
L'IRAP ha base imponibile diversa dall'IRES (non deduce costo del lavoro). Per aziende con alto costo del personale, l'aliquota effettiva complessiva può superare il 28%. Modellare separatamente.
