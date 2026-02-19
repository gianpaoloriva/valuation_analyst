# Valuation Analyst - Istruzioni per Claude Code

## Panoramica Progetto
Toolkit multi-agente per equity valuation basato sulle metodologie di Aswath Damodaran (NYU Stern).
Doppio scopo: (1) strumento di lavoro per analisti finanziari, (2) demo per mostrare Claude Code.

## Convenzioni
- **Lingua**: Tutto in italiano (commenti, docstring, README, docs, skill descriptions)
- **Python**: 3.11+, type hints ovunque, dataclass per modelli dati
- **Stile**: ruff per formatting, mypy per type checking
- **Test**: pytest, coverage >80%

## Data Provider
- **Massive.com** (https://massive.com) per dati aziendali reali
- **Damodaran datasets** (https://pages.stern.nyu.edu/~adamodar/) per parametri di settore
- API key in `.env` (mai committare)

## Struttura
- `src/valuation_analyst/` - Codice sorgente principale
  - `config/` - Impostazioni, costanti, URL Damodaran
  - `models/` - Dataclass (Company, ValuationResult, CashFlow, etc.)
  - `tools/` - Moduli di calcolo (DCF, WACC, multipli, Black-Scholes, etc.)
  - `prompts/` - Template prompt per ogni tipo di analisi
  - `utils/` - Utilita' (math, formatting, logging, validazione)
- `.claude/agents/` - 8 agenti specializzati
- `.claude/skills/` - 9 skill di valutazione
- `.claude/commands/` - Comandi slash (/status, /demo, /checklist)
- `tests/` - Unit e integration test
- `demos/` - Script demo numerati 01-08
- `docs/` - Documentazione completa

## Agenti Disponibili
1. **orchestrator** - Coordina tutti gli agenti
2. **dcf-analyst** - Valutazione DCF (FCFF/FCFE)
3. **relative-analyst** - Multipli e comparabili
4. **cost-of-capital** - WACC/CAPM/Beta
5. **option-pricing** - Black-Scholes, equity come opzione
6. **private-valuation** - Societa' private, sconti illiquidita'
7. **ma-analyst** - M&A e sinergie
8. **risk-analyst** - Sensitivity e Monte Carlo

## Logging Prompt
Ogni interazione significativa va loggata in `prompt_log.md` usando `utils/logging_utils.py`.
Formato: data, skill/agent usato, input, summary del risultato.

## Formule Chiave (Damodaran)
- **FCFF** = EBIT(1-t) - (CapEx - Depr) - DeltaWC
- **CAPM**: Re = Rf + Beta * ERP + CRP
- **WACC**: WACC = (E/V)*Re + (D/V)*Rd*(1-t)
- **Terminal Value**: TV = FCF*(1+g)/(r-g)
- **Black-Scholes**: Equity = V*N(d1) - K*e^(-rT)*N(d2)

## Comandi Utili
```bash
pip install -e ".[dev]"     # Installazione
pytest tests/ --cov          # Test con coverage
python demos/01_cost_of_capital.py  # Demo
```
