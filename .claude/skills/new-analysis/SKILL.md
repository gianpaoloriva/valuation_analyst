---
name: new-analysis
description: Crea la configurazione per una nuova analisi copiando dal template e guidando l'utente nella compilazione
user_invocable: true
---

# Skill: Setup Nuova Analisi

Prepara il file di configurazione JSON per analizzare un nuovo ticker.

## Utilizzo

```
/new-analysis NVDA
/new-analysis TSLA
```

## Workflow

### 1. Rileva il contesto geografico e crea il config JSON

Rileva automaticamente se il ticker e' italiano/europeo:
- Suffisso `.MI` (Milano), `.BIT` (Borsa Italiana) -> societa' italiana
- Ticker come `ENEL`, `ISP`, `UCG`, `ENI`, `STM` senza suffisso -> chiedi conferma

**Se societa' italiana/europea (`paese: "IT"`):**
- Copia `configs/_template_italia.json` in `configs/{TICKER}.json`
- Defaults: ERP 7%, crescita stabile 1.5%, tax rate 27.9% (IRES+IRAP), BTP 10Y
- Proponi anche la modalita' FSI Excel: `/fsi-valuation {TICKER}` per modelli Excel

**Se societa' US/internazionale:**
- Copia `configs/_template.json` in `configs/{TICKER}.json`
- Defaults standard Damodaran

Imposta il campo `ticker` con il valore corretto.

### 2. Chiedi all'utente i parametri chiave

Chiedi all'utente (o ricerca autonomamente) i seguenti parametri:

**Obbligatori:**
- Rating credito (es. "AA+", "BBB", "BB")
- Tasso di crescita alta (fase 1 del DCF)
- Tasso di crescita stabile (fase terminale, tipicamente 2-3% US, 1-2% Italia)
- Lista di 5-7 societa' comparabili con i loro multipli

**Opzionali (hanno default ragionevoli):**
- ERP (default 5.5% per US, 7% per Italia)
- Anni alta crescita (default 5)
- Anni transizione (default 5)
- Range sensitivity, scenari, Monte Carlo

### 3. Popola i fondamentali di fallback

Se i dati fondamentali non sono disponibili via API, chiedi all'utente:
- Ricavi, EBIT, EBITDA, Utile Netto
- Debito totale, Cassa, Book Value Equity
- CapEx, Deprezzamento, Delta WC
- Tax rate, Beta levered

### 4. Popola rischi e scenari

Chiedi o suggerisci:
- 3-5 rischi al rialzo
- 3-5 rischi al ribasso
- Descrizioni scenari best/base/worst

### 5. Verifica e lancia

- Mostra il riepilogo del config all'utente
- Dopo conferma, lancia `python scripts/run_analysis.py {TICKER}`
- Output in `output/markdown/{TICKER}_{data}_valuation.md`

## Note

- **MAI creare script .py ad-hoc** per l'analisi. Usare SEMPRE run_analysis.py
- Il config e' lo **step zero** prima di qualsiasi analisi
- Due template disponibili: `configs/_template.json` (US/internazionale) e `configs/_template_italia.json` (Italia/Europa)
- Per modelli Excel interattivi con compliance normativa italiana, usare `/fsi-valuation`
