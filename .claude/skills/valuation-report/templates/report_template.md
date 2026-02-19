# Report di Valutazione: {AZIENDA} ({TICKER})

**Data:** {DATA}
**Analista:** Valuation Analyst (Claude Code Multi-Agent System)
**Valuta:** {VALUTA}

---

## 1. Executive Summary

| Metrica | Valore |
|---------|--------|
| **Valore Consigliato** | **{VALORE_RANGE}** |
| Prezzo Corrente | {PREZZO_CORRENTE} |
| Upside/Downside | {UPSIDE_DOWNSIDE} |
| Rating Implicito | {RATING} |

## 2. Profilo Aziendale

- **Settore:** {SETTORE}
- **Industria:** {INDUSTRIA}
- **Paese:** {PAESE}
- **Market Cap:** {MARKET_CAP}
- **Enterprise Value:** {ENTERPRISE_VALUE}

## 3. Costo del Capitale

| Componente | Valore |
|-----------|--------|
| Risk-Free Rate | {RF}% |
| Beta Levered | {BETA} |
| ERP | {ERP}% |
| Country Risk Premium | {CRP}% |
| Costo Equity | {RE}% |
| Costo Debito (post-tax) | {RD}% |
| Peso Equity | {WE}% |
| Peso Debito | {WD}% |
| **WACC** | **{WACC}%** |

## 4. Valutazione DCF

### 4.1 Assunzioni di Crescita

| Fase | Anni | Crescita | ROIC |
|------|------|----------|------|
| Alta | {ANNI_ALTA} | {G_ALTA}% | {ROIC_ALTA}% |
| Transizione | {ANNI_TRANS} | {G_TRANS}% | {ROIC_TRANS}% |
| Stabile | Perpetuita' | {G_STABILE}% | {ROIC_STABILE}% |

### 4.2 Proiezione Cash Flow

{TABELLA_CASH_FLOW}

### 4.3 Risultato DCF

| Metodo | Valore Firm | Valore Equity | Per Azione |
|--------|------------|---------------|------------|
| FCFF | {VFIRM_FCFF} | {VEQUITY_FCFF} | {VPA_FCFF} |
| FCFE | {VFIRM_FCFE} | {VEQUITY_FCFE} | {VPA_FCFE} |

## 5. Valutazione Relativa

### 5.1 Societa' Comparabili

{TABELLA_COMPARABILI}

### 5.2 Statistiche Multipli

{TABELLA_STATISTICHE_MULTIPLI}

### 5.3 Valore Implicito per Multiplo

| Multiplo | Mediana Comp. | Metrica Target | Valore/Azione |
|----------|--------------|----------------|---------------|
| P/E | {PE_MED}x | EPS {EPS} | {VPA_PE} |
| EV/EBITDA | {EVEBITDA_MED}x | EBITDA {EBITDA} | {VPA_EVEBITDA} |
| P/B | {PB_MED}x | BV {BV} | {VPA_PB} |

## 6. Analisi di Sensitivita'

### 6.1 Sensitivity WACC vs Terminal Growth

{TABELLA_SENSITIVITY}

### 6.2 Analisi Scenari

| Scenario | Probabilita' | Valore/Azione |
|---------|-------------|---------------|
| Best Case | {P_BEST}% | {V_BEST} |
| Base Case | {P_BASE}% | {V_BASE} |
| Worst Case | {P_WORST}% | {V_WORST} |
| **Valore Atteso** | | **{V_ATTESO}** |

## 7. Sintesi - Football Field

```
{FOOTBALL_FIELD}
```

| Metodo | Min | Valore | Max |
|--------|-----|--------|-----|
| DCF FCFF | {DCF_MIN} | {DCF_VAL} | {DCF_MAX} |
| DCF FCFE | {FCFE_MIN} | {FCFE_VAL} | {FCFE_MAX} |
| Multipli | {MULT_MIN} | {MULT_VAL} | {MULT_MAX} |
| Monte Carlo P5-P95 | {MC_P5} | {MC_MED} | {MC_P95} |

## 8. Note e Avvertenze

{NOTE}

---

*Report generato automaticamente dal sistema Valuation Analyst.*
*Metodologia: Aswath Damodaran (NYU Stern).*
*Fonti dati: Massive.com, Dataset Damodaran.*
