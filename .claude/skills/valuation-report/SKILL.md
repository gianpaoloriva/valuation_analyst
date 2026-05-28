---
name: valuation-report
description: Genera un report di valutazione completo a 10 sezioni orchestrando tutti gli agenti specializzati
user_invocable: true
---

# Skill: Report di Valutazione Completo (Damodaran)

Orchestrazione end-to-end per produrre un report di valutazione professionale a 10 sezioni,
integrando DCF, valutazione relativa, sensitivity, scenari e Monte Carlo. L'output e'
un documento markdown (convertibile in PDF) con raccomandazione finale ponderata.

## Utilizzo

```
/valuation-report AAPL
/valuation-report ENEL.MI
/valuation-report AAPL --metodi "DCF,RELATIVE,OPTION"
```

---

## Vincoli Critici

1. **Il config deve esistere** — `configs/{TICKER}.json` e' prerequisito. Se non esiste, invocare prima `/new-analysis`
2. **MAI creare script .py ad-hoc** — usare SEMPRE `python scripts/run_analysis.py {TICKER}`
3. **Coerenza tra metodi** — il DCF e i multipli devono dare risultati nello stesso ordine di grandezza; divergenze > 30% richiedono spiegazione
4. **Ogni sezione ha un formato prescrittivo** — seguire la struttura sotto
5. **Raccomandazione con range di confidenza** — mai dare un prezzo target puntuale senza intervallo

---

## Processo di Orchestrazione

### Step 1: Verifica Prerequisiti

- Verificare che `configs/{TICKER}.json` esista e sia completo
- Controllare: ticker, paese, comparabili, sensitivity ranges, scenari
- Se manca qualcosa, segnalare e proporre di completare prima di procedere
- Se `paese == "IT"`: verificare parametri italiani (tax 27.9%, ERP 7%, BTP come Rf)

> **CHECKPOINT**: Confermare che il config e' completo e pronto per l'analisi.

### Step 2: Raccolta Dati

- Dati aziendali da Massive.com API (o fallback da config `fondamentali_fallback`)
- Parametri settore da dataset Damodaran (beta, ERP, multipli)
- Prezzo corrente di mercato per confronto

> **CHECKPOINT**: Mostrare dati raccolti e fonte (API o fallback). Confermare.

### Step 3: Esecuzione Analisi

Flusso di esecuzione — le skill vengono invocate in ordine:

```
1. cost-of-capital  ──→  WACC
                            │
2. dcf-valuation    ──→  Valore intrinseco DCF
                            │
3. comparable-analysis ──→ Range multipli
                            │
4. sensitivity-analysis ──→ Tabelle + Scenari + Monte Carlo
                            │
5. [opzionale] option-valuation ──→ Se azienda in distress
                            │
6. [opzionale] private-valuation ──→ Se societa' privata
```

Ogni skill produce la sua sezione del report con checkpoint intermedi.

### Step 4: Generazione Report

Eseguire:
```bash
python scripts/run_analysis.py {TICKER}
```

Output in `output/markdown/{TICKER}_{YYYY-MM-DD}_valuation.md`

### Step 5: Generazione PDF (opzionale)

```bash
python scripts/md_to_pdf.py {TICKER}
```

Output in `output/pdf/{TICKER}_{YYYY-MM-DD}_valuation.pdf`

> **CHECKPOINT FINALE**: Confermare che il report e' stato generato e mostrare il path.

---

## Le 10 Sezioni del Report

### Sezione 1: Executive Summary

| Elemento | Contenuto |
|---------|-----------|
| Ticker e nome azienda | {TICKER} — {Nome} |
| Prezzo corrente | €/$ X.XX |
| Valore intrinseco (DCF) | €/$ X.XX |
| Range valutazione relativa | €/$ X.XX - €/$ X.XX |
| Upside/Downside | +/-XX% |
| Raccomandazione | BUY/HOLD/SELL |
| Data analisi | YYYY-MM-DD |

### Sezione 2: Panoramica Aziendale

- Descrizione business (2-3 righe)
- Settore e mercato principale
- Dati finanziari chiave (ricavi, EBITDA, utile netto, debito netto)
- Margini operativi e trend

### Sezione 3: Costo del Capitale (WACC)

Tabella completa da skill `cost-of-capital`:
- Rf, Beta, ERP, CRP, Re
- Rating, spread, Rd pre/post-tax
- Pesi E/V e D/V
- **WACC finale**

### Sezione 4: Valutazione DCF (FCFF)

Da skill `dcf-valuation`:
- FCFF base e componenti
- Tabella proiezione cash flow multi-stage
- Terminal Value e metodo
- Ponte EV → Equity → Per Azione
- Confronto con prezzo mercato

### Sezione 5: Valutazione Relativa (Multipli)

Da skill `comparable-analysis`:
- Tabella comparabili con multipli
- Statistiche (media, mediana, Q1, Q3)
- Valutazione implicita per multiplo
- Range di valutazione

### Sezione 6: Analisi di Sensitivita'

Da skill `sensitivity-analysis` (workflow 1):
- Tabella WACC vs Terminal Growth
- Tabella Crescita vs Margine
- Range di valori plausibili

### Sezione 7: Analisi per Scenari

Da skill `sensitivity-analysis` (workflow 2):
- Tabella scenari (best/base/worst) con probabilita'
- Valore atteso ponderato
- Descrizione narrativa di ogni scenario

### Sezione 8: Simulazione Monte Carlo

Da skill `sensitivity-analysis` (workflow 3):
- Distribuzioni assunte per ogni parametro
- Statistiche (media, mediana, std, percentili)
- Intervalli di confidenza (IC 50%, IC 90%)
- Probabilita' sopra prezzo mercato

### Sezione 9: Sintesi e Raccomandazione

**Pesi multi-metodo per la sintesi:**

| Metodo | Peso Default |
|--------|-------------|
| DCF (FCFF) | 40% |
| Valutazione Relativa | 25% |
| Scenario Analysis | 15% |
| Monte Carlo | 20% |

```
Valore Composito = 40% * V_DCF + 25% * V_Relativa + 15% * V_Scenario + 20% * V_MonteCarlo
```

**Scala raccomandazione:**

| Upside/Downside | Raccomandazione |
|-----------------|-----------------|
| > +25% | STRONG BUY |
| +15% a +25% | BUY |
| +5% a +15% | MODERATE BUY |
| -5% a +5% | HOLD |
| -15% a -5% | MODERATE SELL |
| -25% a -15% | SELL |
| < -25% | STRONG SELL |

**Range di confidenza:**
- Range stretto: IC 50% del Monte Carlo
- Range largo: IC 90% del Monte Carlo

### Sezione 10: Rischi e Disclaimer

- Rischi al rialzo (da `config.rischi_rialzo`)
- Rischi al ribasso (da `config.rischi_ribasso`)
- Disclaimer standard (analisi a scopo informativo, non consulenza finanziaria)

---

## Errori Comuni

| Errore | Perche' e' grave | Come evitarlo |
|--------|-----------------|---------------|
| Non validare coerenza tra metodi | DCF e multipli divergono senza spiegazione | Se divergono > 30%, indagare |
| Raccomandazione senza range | Falsa precisione | Sempre IC 50% e IC 90% |
| Report senza data e fonte dati | Non riproducibile | Specificare data analisi e fonti |
| Saltare sezioni | Report incompleto | Tutte le 10 sezioni sono obbligatorie |
| Usare solo DCF | Bias da singolo metodo | Multi-metodo con pesi espliciti |
| Non specificare la valuta | Ambiguita' | EUR per Italia, USD per US, sempre esplicita |
| Creare script ad-hoc | Bypassare il flow standard | SEMPRE `run_analysis.py` |

---

## Parametri per Paese

| Parametro | US | Italia |
|-----------|-----|--------|
| Valuta report | USD ($) | EUR (€) |
| Formato numeri | 1,234.56 | 1.234,56 |
| Tax reference | IRC §xxx | IRES/IRAP |
| Risk-free label | US 10Y Treasury | BTP 10Y |
| Indice mercato | S&P 500 | FTSE MIB |
| Disclaimer | SEC safe harbor | CONSOB compliance |

---

## Note Operative

- **Naming convention output**: `{TICKER}_{YYYY-MM-DD}_valuation.md`
- Se il ticker ha suffisso `.MI`: azienda italiana, usare parametri IT
- Il report e' la skill di orchestrazione — invoca tutte le altre skill in sequenza
- Loggare ogni fase in `data/logs/prompt_log.md` tramite `utils/logging_utils.py`
