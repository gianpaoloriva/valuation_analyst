"""Template prompt per analisi di rischio e sensitivita'."""

PROMPT_SENSITIVITY = """Esegui analisi di sensitivita' per {ticker}.

## Parametri Base
- Valore per azione: {valore_base}
- WACC: {wacc:.2%}
- Terminal Growth: {g_stabile:.2%}

## Richiesta
1. Crea tabella sensitivity WACC vs Terminal Growth
2. Crea tabella sensitivity Crescita Ricavi vs Margine Operativo
3. Identifica i parametri con maggior impatto
"""

PROMPT_SCENARI = """Analisi per scenari per {ticker}:

| Scenario | Probabilita' | Crescita | Margine | WACC | Valore |
|---------|-------------|----------|---------|------|--------|
| Best | {p_best:.0%} | {g_best:.1%} | {m_best:.1%} | {w_best:.1%} | {v_best} |
| Base | {p_base:.0%} | {g_base:.1%} | {m_base:.1%} | {w_base:.1%} | {v_base} |
| Worst | {p_worst:.0%} | {g_worst:.1%} | {m_worst:.1%} | {w_worst:.1%} | {v_worst} |
| **Valore Atteso** | | | | | **{v_atteso}** |
"""

PROMPT_MONTE_CARLO = """Risultati simulazione Monte Carlo per {ticker}:

- Simulazioni: {num_sim:,}
- Media: {media}
- Mediana: {mediana}
- IC 90%: {ic90_min} - {ic90_max}
- IC 50%: {ic50_min} - {ic50_max}
- Prob. valore < prezzo corrente: {prob_sotto:.1%}
"""
