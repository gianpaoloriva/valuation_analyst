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

### Moduli Implementati
- [x] Fondamenta (config, models, utils)
- [x] Costo del Capitale (CAPM, WACC, beta)
- [ ] DCF Valuation (FCFF, FCFE)
- ...

### Test
- Totale: XX test
- Passati: XX
- Falliti: XX
- Coverage: XX%

### Ultimo Prompt
(Ultima entry da prompt_log.md)
```
