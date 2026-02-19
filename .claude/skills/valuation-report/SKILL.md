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
Usa il template in `templates/report_template.md` per generare il report.
Salva in `report/{ticker}_{data}_valuation.md`.

### 4. Logging
Logga ogni fase in prompt_log.md.
