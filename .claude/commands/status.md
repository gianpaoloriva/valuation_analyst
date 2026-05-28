---
name: status
description: Mostra lo stato corrente del progetto Valuation Analyst
user_invocable: true
---

# Comando: /status

Mostra lo stato corrente del progetto Valuation Analyst.

## Azioni
1. Leggi `checklist.md` dalla root del progetto
2. Conta i task completati vs totali
3. Verifica che i test passino con `pytest tests/ -q`
4. Mostra un riepilogo dello stato

## Formato Output

```
## Stato Progetto Valuation Analyst

### Avanzamento
- Fase corrente: X di 9
- Task completati: XX/YY (ZZ%)

### Modalita' Damodaran (Python, report markdown/PDF)
- [x] Fondamenta (config, models, utils)
- [x] Costo del Capitale (CAPM, WACC, beta)
- [x] DCF Valuation (FCFF, FCFE)
- [x] Valutazione Relativa (Multipli)
- [x] Sensitivity e Monte Carlo
- [x] Report completo (10 sezioni)

### Modalita' FSI Italy (Excel con formule vive)
- [x] 58 skill FSI Italy integrate (prefisso fsi-)
- [x] 10 agenti FSI Italy (model-builder, pitch-agent, etc.)
- [x] Costanti italiane (IRES+IRAP, BTP, ERP italiano)
- [x] Template config italiano (_template_italia.json)
- [x] Skill /fsi-valuation come entry point
- [x] 6 verticali: Financial Analysis, Equity Research, Investment Banking,
      Private Equity, Wealth Management, Operations
- [x] Compliance: CONSOB, AGCM, MiFID II, Golden Power, KYC/AML, SFDR, DORA

### Test
- Totale: XX test
- Passati: XX
- Falliti: XX
- Coverage: XX%

### Ultimo Prompt
(Ultima entry da prompt_log.md)
```
