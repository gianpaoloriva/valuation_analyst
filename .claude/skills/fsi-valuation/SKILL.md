---
name: fsi-valuation
description: Genera un modello Excel di valutazione di qualita' istituzionale per societa' italiane/europee utilizzando gli skill FSI Italy (DCF, LBO, 3-statement, comps). Produce workbook con formule vive, parametri IFRS, WACC italiano (BTP, Euribor, IRES+IRAP), compliance CONSOB/AGCM/Golden Power.
user_invocable: true
---

# Skill: Valutazione FSI Excel (Societa' Italiane/Europee)

Crea modelli Excel di valutazione con formule vive per societa' italiane/europee,
seguendo gli standard di investment banking istituzionale.

## Utilizzo
```
/fsi-valuation ENEL.MI
/fsi-valuation ENEL.MI --tipo dcf
/fsi-valuation ENEL.MI --tipo lbo
/fsi-valuation ENEL.MI --tipo comps
/fsi-valuation ENEL.MI --tipo pitch
```

## Differenza dalla modalita' Damodaran

| Aspetto | /valuation-report (Damodaran) | /fsi-valuation (FSI Excel) |
|---------|-------------------------------|---------------------------|
| Output | Report Markdown/PDF | Workbook Excel con formule vive |
| Calcolo | Python (automatizzato) | Claude guida la costruzione Excel |
| Interazione | Batch (config -> report) | Step-by-step con review utente |
| Parametri | Damodaran datasets | IFRS, BTP, Euribor, IRES+IRAP |
| Compliance | No | CONSOB, AGCM, Golden Power, MiFID II |

## Workflow

### 1. Identificazione Azienda e Tipo Modello

Chiedi all'utente:
- **Ticker/ISIN** della societa' target (es. ENEL.MI, ISP.MI, UCG.MI)
- **Tipo di modello** richiesto:
  - **DCF** -> usa agente `fsi-model-builder-italy` con skill `fsi-dcf-model-italy`
  - **LBO** -> usa agente `fsi-model-builder-italy` con skill `fsi-lbo-model-italy`
  - **3-Statement** -> usa agente `fsi-model-builder-italy` con skill `fsi-3-statement-model-italy`
  - **Comps** -> usa agente `fsi-model-builder-italy` con skill `fsi-comps-analysis-italy`
  - **Pitch completo** -> usa agente `fsi-pitch-agent-italy` (include tutti i modelli + deck)

### 2. Raccolta Dati

Fonti in ordine di priorita':
1. **MCP servers** (CapIQ, Daloopa, Refinitiv) se configurati
2. **Dati forniti dall'utente** (bilanci, stime)
3. **Ricerca web** come fallback (solo per dati pubblici)

Per societa' italiane: bilancio consolidato IFRS (CONSOB/Borsa Italiana), non SEC EDGAR.

### 3. Delegazione all'Agente FSI

Delega all'agente specializzato appropriato. L'agente:
- Costruisce il modello Excel cella per cella con formule vive
- Verifica con l'utente a ogni step (input -> proiezioni -> WACC -> DCF -> sensitivity)
- Esegue audit del modello (`fsi-audit-xls-italy`)
- Produce il workbook finale in EUR

### 4. Check Regolamentari (se applicabile)

Per operazioni M&A o pitch:
- **AGCM**: verifica soglie concentrazione (fatturato aggregato >532M EUR, target >32M EUR)
- **Golden Power**: verifica settori strategici (D.L. 21/2012)
- **CONSOB**: comunicazioni obbligatorie per target quotate

### 5. Consegna

Output: file .xlsx con formule vive, pronto per review e modifica dall'utente.

## Parametri Italiani di Riferimento

| Parametro | Valore | Fonte |
|-----------|--------|-------|
| Risk-free rate | BTP 10Y (~4%) | Banca d'Italia |
| ERP | 6-8% | Damodaran + CRP Italia |
| Costo debito base | Euribor 3M/6M + spread | BCE |
| IRES | 24% | D.P.R. 917/1986 |
| IRAP | ~3.9% (base) | D.Lgs. 446/1997 |
| Tax rate combinata | ~27.9% | IRES + IRAP |
| Terminal growth | 1-2% | PIL nominale Eurozona |
| Leverage tipico (LBO) | 3-4.5x EBITDA | Mercato italiano |
| DSO/DPO | 60-90 giorni | Prassi italiana |
