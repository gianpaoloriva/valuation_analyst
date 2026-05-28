# Architettura - Valuation Analyst

## Panoramica

Il sistema Valuation Analyst e' un toolkit multi-agente per equity valuation
costruito su Claude Code. L'architettura e' composta da 4 livelli principali.

## Livelli Architetturali

```text
+-------------------------------------------------+
|                  LIVELLO AGENTI                  |
|  orchestrator | dcf-analyst | relative-analyst   |
|  cost-of-capital | option-pricing | risk-analyst |
|  private-valuation | ma-analyst                  |
+-------------------------------------------------+
|                  LIVELLO SKILLS                  |
|  /new-analysis | /valuation-report               |
|  /dcf-valuation | /comparable-analysis           |
|  /cost-of-capital | /option-valuation             |
|  /sensitivity-analysis | /fetch-damodaran-data    |
+-------------------------------------------------+
|               LIVELLO STRUMENTI                  |
|  tools/ (DCF, WACC, multipli, Black-Scholes,     |
|          fetch_dati, sensitivity, Monte Carlo)    |
+-------------------------------------------------+
|               LIVELLO FONDAMENTA                 |
|  models/ (dataclass) | config/ (impostazioni)    |
|  utils/ (math, formatting, logging, validazione) |
|  configs/ (parametri analista per ticker)         |
|  data/ (cache Damodaran, logs)                   |
+-------------------------------------------------+
```

## Flusso Dati

```text
                    +----------+
                    |  Utente  |
                    +----+-----+
                         |
                    +----v-----+
                    |Orchestrator|
                    +----+-----+
              +----------+----------+
              |          |          |
        +-----v--+ +----v---+ +---v----+
        |  Cost   | |  DCF   | |Relative|
        |Capital  | |Analyst | |Analyst |
        +----+----+ +---+----+ +---+----+
             |          |          |
        +----v----------v----------v----+
        |         TOOLS (Python)         |
        |  capm | wacc | dcf_fcff | ... |
        +------------+------------------+
                     |
        +------------v------------------+
        |          DATA SOURCES          |
        |  Massive.com | Damodaran |Cache|
        +--------------------------------+
```

## Componenti Principali

### Agenti (.claude/agents/)

8 agenti specializzati, ciascuno con un file `.md` che definisce:

- Ruolo e competenze
- Strumenti Python disponibili
- Workflow standard passo-passo
- Formato output atteso

### Skills (.claude/skills/)

10 skill invocabili dall'utente con `/nome-skill`, ciascuna con SKILL.md
che definisce workflow e istruzioni. La skill `/new-analysis` guida il
setup del config per un nuovo ticker.

### Strumenti Python (src/valuation_analyst/tools/)

Moduli di calcolo puri, senza side-effect:

- Input: parametri numerici
- Output: risultati strutturati (dataclass o dict)
- Testabili indipendentemente
- `fetch_dati.py`: recupero dati live da Massive.com con fallback su config JSON

### Modelli Dati (src/valuation_analyst/models/)

Dataclass Python per tipizzazione forte:

- Company, ValuationResult, CashFlowProjection
- CostoCapitale, Comparabile, InputBlackScholes
- Scenario, RisultatoSensitivity

### Configurazione (configs/)

File JSON per ogni ticker con i parametri dell'analista:

- Crescita, rating, comparabili, scenari, rischi
- Fondamentali di fallback per quando l'API non fornisce i dati
- Template `_template.json` per nuove analisi

### Script (scripts/)

Due script generici che coprono tutto il flow:

- `run_analysis.py`: legge config, fetch dati, calcola, genera report .md
- `md_to_pdf.py`: converte report .md in .pdf con layout professionale

**Non devono essere creati script ad-hoc per singole analisi.**

## Principi di Design

1. **Separazione responsabilita'**: ogni modulo ha un compito specifico
2. **Composabilita'**: i moduli si compongono tramite l'orchestrator
3. **Testabilita'**: funzioni pure con input/output ben definiti (165 test)
4. **Trasparenza**: ogni calcolo documenta le assunzioni usate
5. **Robustezza**: gestione automatica di aziende in perdita (EBIT/EPS negativi)
6. **Un solo flow**: `run_analysis.py` gestisce tutti i casi, niente script ad-hoc

## Dipendenze Tra Moduli

```text
cost-of-capital ------+
                      +---> dcf-analyst ---+
damodaran_data  ------+                    |
                                           +---> risk-analyst
relative-analyst  -------------------------+
                                           |
option-pricing  ---------------------------+

private-valuation --> usa output di dcf/relative
ma-analyst        --> usa output di dcf/relative + sinergie
```
