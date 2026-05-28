---
name: fsi-model-update-italy
description: >
  Aggiornamento modelli finanziari con nuovi dati per società italiane/europee:
  risultati trimestrali/semestrali IFRS, guidance management, variazioni macro,
  ipotesi riviste. Ricalcola stime e valutazione con WACC italiano.
  Triggers on "aggiorna modello", "update model", "plug earnings", "nuova guidance",
  "revisione stime", "aggiorna numeri per [società]".
---

# Aggiornamento Modello — Contesto Italiano

Adapt dello skill US `model-update`. Il workflow è quasi interamente universale. Adattamenti puntuali su fonti, contabilità e parametri di valutazione.

## Workflow

### Step 1: Identificare Cosa è Cambiato

Determinare il trigger dell'aggiornamento:
- **Risultati pubblicati**: nuovi dati consuntivi da relazione semestrale / bilancio consolidato IFRS
- **Cambio guidance**: la società ha aggiornato l'outlook (spesso qualitativo per società italiane)
- **Revisione stime**: l'analista cambia ipotesi su nuovi dati
- **Aggiornamento macro**: tassi BCE, spread BTP-Bund, EUR/USD, prezzi commodity
- **Evento**: M&A, ristrutturazione, nuovo prodotto, cambio management, decisione regolatore (ARERA, AGCM, Banca d'Italia)

### Step 2: Inserire Nuovi Dati

#### Dopo Pubblicazione Risultati

| Voce | Stima precedente | Consuntivo | Delta | Note |
|------|-----------------|------------|-------|------|
| Ricavi | | | | |
| EBITDA | | | | |
| EBITDA Adjusted (MAP) | | | | Verificare riconciliazione IFRS |
| EBIT | | | | |
| Utile netto | | | | |
| EPS (€) | | | | |
| [Metrica chiave settoriale] | | | | |

**Dettaglio per segmento** (IFRS 8, se applicabile):
- Aggiornare ricavi e margini per segmento
- Verificare cambio di perimetro o mix

**Stato patrimoniale / Cash flow:**
- PFN (Posizione Finanziaria Netta) aggiornata
- Share count (buyback, diluizione, aumenti di capitale)
- CapEx consuntivo vs stima
- NWC (DSO, DPO — tipicamente più lunghi in Italia: DSO 60-90 gg)
- Fondo TFR e altri fondi (IAS 19, IAS 37) — variazioni attuariali

### Step 3: Revisione Stime Forward

| | Vecchia stima FY | Nuova stima FY | Δ | Vecchia stima FY+1 | Nuova stima FY+1 | Δ |
|---|-----------------|---------------|---|--------------------|--------------------|---|
| Ricavi | | | | | | |
| EBITDA | | | | | | |
| EPS (€) | | | | | | |

**Ipotesi chiave modificate:**
- Crescita ricavi: vecchia → nuova (motivazione)
- Margine: vecchio → nuovo (motivazione)
- Aliquota fiscale effettiva (~27,9% IRES+IRAP, verificare variazioni IRAP regionale)
- Eventuali nuove voci (svalutazione avviamento IAS 36, oneri ristrutturazione, impatti IFRS 16)

### Step 4: Impatto su Valutazione

Ricalcolare la valutazione con stime aggiornate:

| Metodo | Precedente (€) | Aggiornato (€) | Δ |
|--------|---------------|----------------|---|
| DCF (WACC italiano: BTP 10Y + beta × ERP) | | | |
| P/E (EPS NTM × multiplo target) | | | |
| EV/EBITDA (EBITDA NTM × multiplo target) | | | |
| **Prezzo Target** | | | |

Multipli di riferimento vs peer europei (non S&P 500).

### Step 5: Sintesi e Azione

**Riepilogo variazione stime:**
- Un paragrafo: cosa è cambiato, perché, cosa implica per il titolo
- Evento che cambia la tesi o rumore di fondo?

**Rating / Prezzo Target:**
- Mantenere o cambiare rating (COMPRARE / MANTENERE / VENDERE)?
- Nuovo prezzo target in € (se modificato) con metodologia
- Upside/downside vs prezzo corrente

### Step 6: Output

- Modello Excel aggiornato (se l'utente fornisce il modello esistente)
- Nota di revisione stime (markdown o Word)
- Derivazione aggiornata del prezzo target

## Errori Comuni da Evitare

### ❌ Usare stime "GAAP vs Non-GAAP"
In IFRS non esiste questa distinzione. Usare: voci IFRS e "misure alternative di performance" (MAP). La società deve riconciliare le MAP alle voci IFRS (ESMA Guidelines).

### ❌ Confrontare con consensus US-centric
Usare Refinitiv IBES o Bloomberg con filtro analisti europei. Per small cap italiane, il consensus può avere 1-3 analisti — notare la numerosità.

### ❌ Dimenticare l'IRAP nelle stime fiscali
L'aliquota IRES 24% da sola sottostima il carico fiscale. Includere sempre l'IRAP (~3,9%) che ha base imponibile diversa (non deduce interessi e costo del lavoro).
