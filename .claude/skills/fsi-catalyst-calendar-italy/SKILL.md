---
name: fsi-catalyst-calendar-italy
description: >
  Calendario catalizzatori per universo di copertura su Borsa Italiana:
  date risultati, assemblee, stacchi dividendo, conferenze, decisioni
  regolatori italiani/europei, eventi macro BCE/ISTAT.
  Triggers on "calendario catalizzatori", "catalyst calendar", "prossimi eventi",
  "earnings calendar", "cosa succede questa settimana", "event calendar".
---

# Calendario Catalizzatori — Contesto Italiano

Adapt dello skill US `catalyst-calendar`. Struttura identica. Adattati eventi e riferimenti al mercato italiano.

## Workflow

### Step 1: Definire Universo di Copertura

- Lista società da monitorare (ticker Borsa Italiana)
- Settore / industria di focus
- Includere eventi macro? (BCE, ISTAT, aste BTP, rating sovrano)
- Orizzonte temporale (prossime 2 settimane, mese, trimestre)

### Step 2: Raccolta Catalizzatori

Per ciascuna società:

**Risultati e Eventi Finanziari**
- Data pubblicazione risultati (semestrale e annuale obbligatori; trimestrali opzionali)
- Assemblea ordinaria azionisti (tipicamente aprile-giugno)
- Stacco dividendo e pagamento (ex-date, record date, payment date)
- Investor day / Capital markets day
- Scadenze debito / rifinanziamenti

**Eventi Corporate**
- Lanci prodotto, acquisizioni, cessioni
- Decisioni regolatori settoriali (ARERA, AGCM, CONSOB, Banca d'Italia)
- Milestone PNRR (per società infrastrutturali / industriali)
- Scadenze Golden Power / autorizzazioni
- Cambi management, rinnovo CdA
- Finestre di trading per insider (blackout period prima dei risultati)

**Eventi di Settore**
- Conferenze (Italian Equity Conference di Borsa Italiana, Mediobanca CEO Conference, ecc.)
- Dati di settore (immatricolazioni auto, produzione industriale, vendite retail)
- Decisioni regolatori di settore (periodi regolatori ARERA, aste spettro AGCOM)

**Eventi Macro Italia / Eurozona**
- Riunioni BCE (date FOMC → date Governing Council BCE)
- Aste BTP / BOT (calendario MEF)
- Dati ISTAT: PIL, inflazione (CPI/HICP), produzione industriale, disoccupazione
- Dati Eurostat: PIL Eurozona, inflazione, PMI
- Revisioni rating sovrano Italia (Moody's, S&P, Fitch, DBRS) — date note
- Legge di Bilancio (autunno) e DEF (aprile) — impatto fiscale e settoriale

### Step 3: Vista Calendario

| Data | Evento | Società/Settore | Tipo | Impatto (A/M/B) | Posizionamento | Note |
|------|--------|----------------|------|------------------|---------------|------|
| | | | Risultati/Corporate/Settore/Macro | | Long/Short/Neutro | |

### Step 4: Preview Settimanale

**Eventi Chiave Questa Settimana:**
1. [Giorno]: [Società] risultati H1 — consensus EBITDA €XM, nostra stima €XM, focus: [metrica]
2. [Giorno]: [Evento] — perché conta per [titoli]
3. [Giorno]: [Dato macro / decisione BCE] — attese e posizionamento

**Preview Prossima Settimana:**
- Heads-up su eventi importanti in arrivo

**Implicazioni per le Posizioni:**
- Eventi che possono muovere titoli specifici
- Pre-posizionamento consigliato
- Risk management prima di eventi binari

**Calendario dividendi** (particolarmente rilevante in Italia — molte società hanno dividend yield >3-4%):

| Società | DPS (€) | Yield | Ex-date | Payment date |
|---------|---------|-------|---------|-------------|
| | | | | |

### Step 5: Output

- Workbook Excel con vista calendario e colonne ordinabili
- Preview settimanale (markdown) per distribuzione email
- Template ricorrente per dati mensili (immatricolazioni, PMI, produzione industriale)

## Errori Comuni da Evitare

### ❌ Usare date FOMC come catalizzatore primario
Il catalizzatore primario per il mercato italiano è la BCE (Governing Council), non il FOMC. Le riunioni FOMC sono contesto, non driver diretto.

### ❌ Dimenticare le aste BTP
Le aste di titoli di stato italiani (calendario MEF) possono muovere lo spread BTP-Bund e di conseguenza l'intero mercato. Includere sempre nel calendario macro.

### ❌ Trascurare i dividendi
Il mercato italiano ha un dividend yield medio superiore a quello US. Lo stacco dividendo (ex-date) causa aggiustamenti di prezzo e va tracciato per tutte le posizioni.
