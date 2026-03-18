---
name: valuation-report
description: Genera un report di valutazione completo orchestrando tutti gli agenti specializzati
user_invocable: true
---

# Skill: Report di Valutazione Completo

Orchestra tutti gli agenti per produrre un report di valutazione professionale e completo.

## Utilizzo
```
/valuation-report AAPL
/valuation-report "Ferrari NV" --metodi "DCF,RELATIVE,OPTION"
/valuation-report AAPL --tipo privata --partecipazione maggioranza
```

## Workflow

### 1. Raccolta Dati
- Dati aziendali da Massive.com
- Parametri settore da dataset Damodaran

### 2. Orchestrazione Agenti
Segui il flusso definito nell'orchestrator:
1. cost-of-capital -> WACC
2. dcf-analyst -> Valore intrinseco (in parallelo con 3)
3. relative-analyst -> Range multipli
4. risk-analyst -> Sensitivity e Monte Carlo
5. (Se distress) option-pricing -> Equity come opzione
6. (Se privata) private-valuation -> Sconti/premi

### 3. Generazione Report
Esegui `python scripts/run_analysis.py {TICKER}`.
Il report viene salvato in `output/markdown/{TICKER}_{data}_valuation.md`.

**IMPORTANTE**: NON creare script .py ad-hoc. Usare SEMPRE run_analysis.py.
Il config deve esistere in `configs/{TICKER}.json` prima di lanciare l'analisi.

### 4. Generazione PDF
Esegui `python scripts/md_to_pdf.py {TICKER}`.
PDF salvato in `output/pdf/`.

### 5. Logging
Logga ogni fase in `data/logs/prompt_log.md`.
