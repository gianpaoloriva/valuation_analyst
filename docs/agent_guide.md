# Guida agli Agenti - Valuation Analyst

## Panoramica

Il sistema usa 8 agenti Claude Code specializzati che collaborano
per produrre valutazioni complete e affidabili.

## Come Funzionano gli Agenti

Ogni agente e' definito da un file `.md` in `.claude/agents/` con:
- **Frontmatter YAML**: nome, descrizione, strumenti disponibili
- **System prompt**: ruolo, competenze, workflow, regole

Gli agenti vengono invocati dall'orchestrator o direttamente dall'utente.

## Agenti Disponibili

### 1. Orchestrator (`orchestrator.md`)
- **Ruolo**: Coordinatore principale
- **Quando usarlo**: Per valutazioni complete che richiedono piu' metodi
- **Invocazione**: Automatica via `/valuation-report`

### 2. Cost of Capital (`cost-of-capital.md`)
- **Ruolo**: WACC, CAPM, beta, risk premium
- **Quando usarlo**: Sempre come primo passo di qualsiasi valutazione
- **Invocazione**: `/cost-of-capital TICKER`
- **Output**: Oggetto `CostoCapitale` con tutti i componenti

### 3. DCF Analyst (`dcf-analyst.md`)
- **Ruolo**: Valutazione DCF (FCFF e FCFE)
- **Dipendenze**: Richiede WACC da cost-of-capital
- **Invocazione**: `/dcf-valuation TICKER`
- **Output**: `ValuationResult` con proiezione cash flow

### 4. Relative Analyst (`relative-analyst.md`)
- **Ruolo**: Multipli e comparabili
- **Quando usarlo**: Come complemento al DCF per cross-check
- **Invocazione**: `/comparable-analysis TICKER`
- **Output**: `ValuationResult` con range da multipli

### 5. Option Pricing (`option-pricing.md`)
- **Ruolo**: Black-Scholes, equity come opzione
- **Quando usarlo**: Aziende in distress, alto leverage, utili negativi
- **Invocazione**: `/option-valuation TICKER`
- **Output**: Valore equity, probabilita' default

### 6. Private Valuation (`private-valuation.md`)
- **Ruolo**: Sconti illiquidita', premio controllo
- **Quando usarlo**: Societa' non quotate
- **Invocazione**: `/private-valuation --ricavi X --ebitda Y`

### 7. M&A Analyst (`ma-analyst.md`)
- **Ruolo**: Sinergie e valore acquisizione
- **Quando usarlo**: Analisi di acquisizioni
- **Invocazione**: `/ma-valuation --acquirente X --target Y`

### 8. Risk Analyst (`risk-analyst.md`)
- **Ruolo**: Sensitivity, scenari, Monte Carlo
- **Quando usarlo**: Dopo DCF per quantificare incertezza
- **Invocazione**: `/sensitivity-analysis TICKER`

## Flusso di Collaborazione

### Valutazione Standard
```
Utente ──▶ Orchestrator
              │
              ├──1──▶ Cost of Capital (WACC)
              │
              ├──2──▶ DCF Analyst (usa WACC)
              │       Relative Analyst (in parallelo)
              │
              ├──3──▶ Risk Analyst (sensitivity su DCF)
              │
              └──4──▶ Sintesi report finale
```

### Valutazione Distress
```
Orchestrator ──▶ Cost of Capital
             ──▶ DCF Analyst (se possibile)
             ──▶ Option Pricing (parallelo)
             ──▶ Risk Analyst (scenari recovery)
```

### Valutazione M&A
```
Orchestrator ──▶ Valutazione standalone (x2)
             ──▶ M&A Analyst (sinergie)
             ──▶ Risk Analyst (sensitivity)
```

## Creare un Nuovo Agente

Per aggiungere un agente specializzato:

1. Crea `.claude/agents/nome-agente.md`
2. Definisci frontmatter con nome e tools
3. Scrivi system prompt con ruolo, workflow, regole
4. Aggiungi riferimento in `orchestrator.md`
5. (Opzionale) Crea skill corrispondente in `.claude/skills/`
