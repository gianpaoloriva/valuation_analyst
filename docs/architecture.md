# Architettura - Valuation Analyst

## Panoramica

Il sistema Valuation Analyst e' un toolkit multi-agente per equity valuation
costruito su Claude Code. L'architettura e' composta da 4 livelli principali.

## Livelli Architetturali

```
┌─────────────────────────────────────────────────┐
│                  LIVELLO AGENTI                  │
│  orchestrator | dcf-analyst | relative-analyst   │
│  cost-of-capital | option-pricing | risk-analyst │
│  private-valuation | ma-analyst                  │
├─────────────────────────────────────────────────┤
│                  LIVELLO SKILLS                  │
│  /dcf-valuation | /comparable-analysis           │
│  /cost-of-capital | /option-valuation             │
│  /sensitivity-analysis | /valuation-report        │
├─────────────────────────────────────────────────┤
│               LIVELLO STRUMENTI                  │
│  tools/ (DCF, WACC, multipli, Black-Scholes...)  │
│  prompts/ (template per interazione)             │
├─────────────────────────────────────────────────┤
│               LIVELLO FONDAMENTA                 │
│  models/ (dataclass) | config/ (impostazioni)    │
│  utils/ (math, formatting, logging, parsing)     │
│  data/ (cache, samples, reports)                 │
└─────────────────────────────────────────────────┘
```

## Flusso Dati

```
                    ┌──────────┐
                    │  Utente  │
                    └────┬─────┘
                         │
                    ┌────▼─────┐
                    │Orchestrator│
                    └────┬─────┘
              ┌──────────┼──────────┐
              │          │          │
        ┌─────▼──┐ ┌────▼───┐ ┌───▼────┐
        │  Cost   │ │  DCF   │ │Relative│
        │Capital  │ │Analyst │ │Analyst │
        └────┬────┘ └───┬────┘ └───┬────┘
             │          │          │
        ┌────▼──────────▼──────────▼────┐
        │         TOOLS (Python)         │
        │  capm | wacc | dcf_fcff | ...  │
        └────────────┬──────────────────┘
                     │
        ┌────────────▼──────────────────┐
        │          DATA SOURCES          │
        │  Massive.com | Damodaran | Cache│
        └───────────────────────────────┘
```

## Componenti Principali

### Agenti (.claude/agents/)
8 agenti specializzati, ciascuno con un system prompt che definisce:
- Ruolo e competenze
- Strumenti Python disponibili
- Workflow standard passo-passo
- Formato output atteso
- Regole e vincoli

### Skills (.claude/skills/)
9 skill invocabili dall'utente con `/nome-skill`, ciascuna con:
- SKILL.md: workflow e istruzioni
- reference.md: riferimento metodologico Damodaran

### Strumenti Python (src/valuation_analyst/tools/)
Moduli di calcolo puri, senza side-effect:
- Input: parametri numerici
- Output: risultati strutturati (dataclass o dict)
- Testabili indipendentemente

### Modelli Dati (src/valuation_analyst/models/)
Dataclass Python per tipizzazione forte:
- Company, ValuationResult, CashFlowProjection
- CostoCapitale, Comparabile, InputBlackScholes
- Scenario, RisultatoSensitivity

## Principi di Design

1. **Separazione responsabilita'**: Ogni modulo ha un compito specifico
2. **Composabilita'**: I moduli si compongono tramite l'orchestrator
3. **Testabilita'**: Funzioni pure con input/output ben definiti
4. **Trasparenza**: Ogni calcolo documenta le assunzioni usate
5. **Logging**: Ogni interazione e' tracciata in prompt_log.md

## Dipendenze Tra Moduli

```
cost-of-capital ──────┐
                      ├──▶ dcf-analyst ──┐
damodaran_data  ──────┘                  │
                                         ├──▶ risk-analyst
relative-analyst ────────────────────────┤
                                         │
option-pricing  ─────────────────────────┘

private-valuation ──▶ usa output di dcf/relative
ma-analyst        ──▶ usa output di dcf/relative + sinergie
```
