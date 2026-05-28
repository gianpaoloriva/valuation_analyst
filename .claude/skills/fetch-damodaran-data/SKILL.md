---
name: fetch-damodaran-data
description: Scarica e aggiorna i dataset Damodaran (beta, ERP, WACC, multipli per settore e paese)
user_invocable: true
---

# Skill: Download Dataset Damodaran

Scarica i dataset di Aswath Damodaran dal sito NYU Stern e li salva nella cache locale
(`data/cache/`). Questi dataset forniscono parametri di settore e paese necessari per
le valutazioni: beta, ERP, WACC, multipli, margini, CapEx ratios.

## Utilizzo

```
/fetch-damodaran-data                    # Scarica tutti i dataset
/fetch-damodaran-data --dataset betas    # Solo beta di settore
/fetch-damodaran-data --forza            # Forza re-download anche se in cache
/fetch-damodaran-data --lista            # Lista dataset disponibili
```

---

## Vincoli Critici

1. **Dati aggiornati a gennaio** — Damodaran aggiorna i dataset a inizio anno; durante l'anno i dati sono dell'anno precedente
2. **I file sono Excel (.xlsx)** — il parsing richiede openpyxl o xlrd
3. **La cache ha validita' annuale** — re-scaricare solo se i dati in cache sono dell'anno precedente
4. **Mai modificare i file scaricati** — sono read-only; le elaborazioni vanno in memoria
5. **Connessione internet richiesta** — senza connessione, usare l'ultima cache disponibile
6. **I dataset US-centric** — per Italia/Europa applicare aggiustamenti (CRP, tax, dimensione)

---

## Dataset Disponibili

| ID | File Damodaran | Contenuto | Usato da |
|----|---------------|-----------|----------|
| `betas` | `betas.xlsx` | Beta unlevered/levered per settore | `cost-of-capital` |
| `erp` | `ctryprem.xlsx` | Equity Risk Premium per paese | `cost-of-capital` |
| `wacc` | `wacc.xlsx` | WACC e componenti per settore | `cost-of-capital`, `dcf-valuation` |
| `pe` | `pedata.xlsx` | P/E ratio per settore | `comparable-analysis` |
| `ev_ebitda` | `vebitda.xlsx` | EV/EBITDA per settore | `comparable-analysis` |
| `pb` | `pbvdata.xlsx` | P/B ratio per settore | `comparable-analysis` |
| `ps` | `psdata.xlsx` | Price/Sales per settore | `comparable-analysis` |
| `margins` | `margin.xlsx` | Margini operativi per settore | `dcf-valuation` |
| `capex` | `capex.xlsx` | CapEx e D&A per settore | `dcf-valuation` |
| `roe` | `roe.xlsx` | ROE per settore | `comparable-analysis` |
| `dividends` | `divfund.xlsx` | Payout e dividend yield | `dcf-valuation` |
| `country_risk` | `ctryprem.xlsx` | Risk premium per paese | `cost-of-capital` |

---

## Processo di Download

### Step 1: Verifica Cache

- Controllare se `data/cache/{dataset}.xlsx` esiste
- Se esiste: verificare data ultimo download (metadata o timestamp file)
- Se cache valida (stesso anno): usare cache, skip download
- Se cache scaduta o assente: procedere con download

### Step 2: Download

**Base URL**: `https://pages.stern.nyu.edu/~adamodar/`

**Percorsi:**
- Current datasets: `New_Home_Page/datafile/`
- Archived datasets: `New_Home_Page/dataarchived/`

Scaricare il file .xlsx e salvare in `data/cache/` con timestamp.

**Gestione errori:**
- Se il server non risponde: usare ultima cache disponibile, segnalare all'utente
- Se il file e' corrotto: ri-scaricare con retry (max 3 tentativi)
- Se il dataset non esiste: segnalare errore, listare dataset validi

### Step 3: Parsing e Validazione

- Aprire il file .xlsx con openpyxl
- Verificare che contenga dati (non vuoto, non solo headers)
- Estrarre numero settori/paesi presenti
- Salvare metadata (data download, fonte, dimensione, righe)

### Step 4: Conferma

**Output:**

| Dataset | File | Dimensione | Settori/Paesi | Data Download |
|---------|------|-----------|---------------|---------------|
| betas | betas.xlsx | XXX KB | XXX settori | YYYY-MM-DD |
| erp | ctryprem.xlsx | XXX KB | XXX paesi | YYYY-MM-DD |
| ... | | | | |

> **CHECKPOINT**: Mostrare tabella riepilogativa dei dataset scaricati/aggiornati.

---

## Uso dei Dataset nelle Altre Skill

### Beta di Settore (`betas.xlsx`)

Contenuto: Beta unlevered, beta levered, D/E ratio, tax rate per ~95 settori.
Usato dalla skill `cost-of-capital` per il metodo bottom-up:
```
1. Trova il settore dell'azienda
2. Leggi Beta_Unlevered del settore
3. Relever: Beta_L = Beta_U * (1 + (1-t) * D/E_target)
```

### Country Risk Premium (`ctryprem.xlsx`)

Contenuto: ERP, default spread, CRP per ~150 paesi.
Usato dalla skill `cost-of-capital`:
```
1. Trova il paese dell'azienda
2. Leggi ERP e CRP
3. Re = Rf + Beta * ERP + CRP
```

### Multipli per Settore (`pedata.xlsx`, `vebitda.xlsx`, etc.)

Contenuto: Mediana e media dei multipli per ~95 settori.
Usato dalla skill `comparable-analysis` come benchmark settoriale:
```
1. Trova il settore
2. Confronta multipli dei peer con la mediana settoriale
3. Identifica se il target e' sopra/sotto la mediana
```

---

## Errori Comuni

| Errore | Perche' e' grave | Come evitarlo |
|--------|-----------------|---------------|
| Usare dati dell'anno scorso senza segnalare | Parametri obsoleti (beta, ERP cambiano) | Verificare timestamp, segnalare eta' dati |
| Non trovare il settore giusto | Damodaran usa classificazione propria (~95 settori) | Cercare con fuzzy matching |
| Usare il beta US per azienda IT | I beta sono calcolati su aziende US | Applicare aggiustamento per dimensione/liquidita' |
| Scaricare durante l'analisi (rallenta) | Il download puo' fallire mid-analysis | Pre-scaricare prima dell'analisi |
| Ignorare la data di aggiornamento | I dati sono annuali, non real-time | Specificare "dati Damodaran aggiornati a gennaio YYYY" |

---

## Parametri per Paese

| Aspetto | US | Italia |
|---------|-----|--------|
| Rappresentativita' dataset | Alta (dati su aziende US) | Bassa (poche aziende IT nel sample) |
| Aggiustamento necessario | Nessuno | CRP, dimensione, liquidita' |
| Settori disponibili | Tutti i 95 | Verificare copertura (alcuni settori IT non mappano) |
| Fonte alternativa | - | AIDA/Bureau van Dijk per dati specifici IT |

**Nota Italia**: I dataset Damodaran sono calcolati prevalentemente su aziende US.
Per aziende italiane:
- Il beta unlevered e' un buon proxy per il rischio operativo (global)
- ERP e CRP vanno presi dalla tabella per paese (`ctryprem.xlsx`)
- I multipli settoriali possono differire (P/E IT tipicamente inferiore a P/E US)
- Considerare AIDA come fonte alternativa per multipli specifici al mercato italiano

---

## Note Operative

- Cache in `data/cache/` — non committare nel repository (in `.gitignore`)
- Fonte unica: https://pages.stern.nyu.edu/~adamodar/
- Aggiornamento tipicamente a gennaio
- Se la connessione fallisce, l'analisi puo' procedere con dati in cache
- Loggare download in `data/logs/prompt_log.md`
- Per forzare re-download: eliminare il file dalla cache o usare `--forza`
