"""Template prompt per il report di valutazione completo."""

PROMPT_REPORT_INIZIO = """Genera un report di valutazione completo per {ticker} ({nome}).

## Informazioni Azienda
- Settore: {settore}
- Paese: {paese}
- Market Cap: {market_cap}
- Prezzo Corrente: {prezzo_corrente}

## Metodi da Applicare
1. Costo del Capitale (WACC/CAPM)
2. DCF (FCFF e FCFE)
3. Valutazione Relativa (multipli e comparabili)
4. Analisi di Sensitivita' (WACC vs Growth)
5. Simulazione Monte Carlo

## Formato Output
Genera il report seguendo il template in:
.claude/skills/valuation-report/templates/report_template.md
"""

PROMPT_REPORT_SINTESI = """## Sintesi Valutazione {ticker}

### Range di Valutazione

| Metodo | Valore/Azione | Range |
|--------|--------------|-------|
| DCF FCFF | {dcf_fcff} | {dcf_fcff_range} |
| DCF FCFE | {dcf_fcfe} | {dcf_fcfe_range} |
| Multipli | {multipli} | {multipli_range} |
| Monte Carlo | {mc_mediana} | {mc_range} |

### Valore Consigliato: {valore_min} - {valore_max}
### Prezzo Corrente: {prezzo}
### Upside/Downside: {upside}

### Note
{note}
"""

PROMPT_LOG_ENTRY = """### {timestamp}
**Skill:** {skill}
**Input:** {input_text}
**Agent:** {agent}
**Summary:** {summary}
---
"""
