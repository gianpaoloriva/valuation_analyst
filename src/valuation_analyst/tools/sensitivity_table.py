"""Modulo per la generazione di tabelle di sensitivita' bidimensionali.

Varia due parametri chiave (es. WACC e terminal growth) per creare
una matrice di valori risultanti.
"""
from __future__ import annotations

import numpy as np
from typing import Callable

from valuation_analyst.models.scenario import RisultatoSensitivity
from valuation_analyst.utils.formatting import formatta_valuta, tabella_markdown


def crea_tabella_sensitivity(
    funzione_valutazione: Callable[[float, float], float],
    parametro_riga: str,
    valori_riga: list[float],
    parametro_colonna: str,
    valori_colonna: list[float],
) -> RisultatoSensitivity:
    """Crea una tabella di sensitivita' 2D.

    Itera su tutte le combinazioni dei due parametri e calcola il
    valore risultante tramite la funzione di valutazione fornita.

    Args:
        funzione_valutazione: f(param_riga, param_colonna) -> valore
        parametro_riga: nome del parametro sulle righe (es. "WACC")
        valori_riga: valori da testare per le righe
        parametro_colonna: nome del parametro sulle colonne (es. "Terminal Growth")
        valori_colonna: valori da testare per le colonne

    Returns:
        RisultatoSensitivity con la matrice completa dei risultati.
    """
    matrice: list[list[float]] = []
    for r in valori_riga:
        riga: list[float] = []
        for c in valori_colonna:
            try:
                val = funzione_valutazione(r, c)
            except (ValueError, ZeroDivisionError):
                val = float("nan")
            riga.append(val)
        matrice.append(riga)

    return RisultatoSensitivity(
        parametro_riga=parametro_riga,
        parametro_colonna=parametro_colonna,
        valori_riga=valori_riga,
        valori_colonna=valori_colonna,
        matrice_risultati=matrice,
    )


def sensitivity_wacc_growth(
    fcff_base: float,
    debito_netto: float,
    shares_outstanding: float,
    wacc_range: list[float] | None = None,
    growth_range: list[float] | None = None,
    anni_proiezione: int = 10,
    crescita_alta: float = 0.10,
) -> RisultatoSensitivity:
    """Crea tabella sensitivity WACC vs Terminal Growth Rate.

    Per ogni combinazione di WACC e tasso di crescita terminale esegue
    un DCF semplificato: proietta i flussi di cassa con crescita che
    converge linearmente dalla crescita alta al tasso terminale, poi
    calcola il terminal value con il modello di Gordon.

    Range predefiniti: WACC 7-11 %, Growth 1.5-3.5 %.

    Args:
        fcff_base: flusso di cassa libero per l'impresa al tempo 0.
        debito_netto: debito netto da sottrarre all'enterprise value.
        shares_outstanding: numero di azioni in circolazione.
        wacc_range: lista di valori WACC da testare.
        growth_range: lista di tassi di crescita terminale da testare.
        anni_proiezione: numero di anni di proiezione esplicita.
        crescita_alta: tasso di crescita iniziale (primo anno).

    Returns:
        RisultatoSensitivity con valore per azione per ogni combinazione.
    """
    if wacc_range is None:
        wacc_range = [0.07, 0.08, 0.085, 0.09, 0.095, 0.10, 0.11]
    if growth_range is None:
        growth_range = [0.015, 0.020, 0.025, 0.030, 0.035]

    def valuta(wacc: float, g: float) -> float:
        """DCF semplificato per una coppia (wacc, g)."""
        if wacc <= g:
            return float("nan")
        fcff = fcff_base
        valore = 0.0
        for anno in range(1, anni_proiezione + 1):
            # Convergenza lineare dalla crescita alta al tasso terminale
            t_crescita = crescita_alta - (crescita_alta - g) * (anno / anni_proiezione)
            fcff = fcff * (1 + t_crescita)
            valore += fcff / (1 + wacc) ** anno
        # Terminal value (modello di Gordon)
        tv = fcff * (1 + g) / (wacc - g)
        valore += tv / (1 + wacc) ** anni_proiezione
        # Da enterprise value a equity per azione
        equity = valore - debito_netto
        return equity / shares_outstanding if shares_outstanding > 0 else 0.0

    return crea_tabella_sensitivity(
        valuta, "WACC", wacc_range, "Terminal Growth", growth_range
    )


def sensitivity_crescita_margine(
    ricavi_base: float,
    debito_netto: float,
    shares_outstanding: float,
    wacc: float,
    tax_rate: float,
    capex_pct_ricavi: float = 0.05,
    depr_pct_ricavi: float = 0.04,
    crescita_range: list[float] | None = None,
    margine_range: list[float] | None = None,
) -> RisultatoSensitivity:
    """Sensitivity su crescita ricavi vs margine operativo.

    Per ogni combinazione proietta 10 anni di flussi di cassa a partire
    dai ricavi base, applicando crescita costante e margine operativo
    costante. Il terminal value e' calcolato con crescita al 2.5 %.

    Args:
        ricavi_base: ricavi dell'ultimo anno (anno 0).
        debito_netto: debito netto da sottrarre all'enterprise value.
        shares_outstanding: numero di azioni in circolazione.
        wacc: costo medio ponderato del capitale.
        tax_rate: aliquota fiscale (es. 0.25 per 25 %).
        capex_pct_ricavi: capex come percentuale dei ricavi.
        depr_pct_ricavi: ammortamenti come percentuale dei ricavi.
        crescita_range: lista di tassi di crescita da testare.
        margine_range: lista di margini operativi da testare.

    Returns:
        RisultatoSensitivity con valore per azione per ogni combinazione.
    """
    if crescita_range is None:
        crescita_range = [0.03, 0.05, 0.08, 0.10, 0.15]
    if margine_range is None:
        margine_range = [0.15, 0.20, 0.25, 0.30, 0.35]

    def valuta(crescita: float, margine: float) -> float:
        """DCF basato su ricavi, crescita e margine operativo."""
        valore = 0.0
        ricavi = ricavi_base
        for anno in range(1, 11):
            ricavi *= 1 + crescita
            ebit = ricavi * margine
            # FCFF = EBIT*(1-t) - investimenti netti
            fcff = ebit * (1 - tax_rate) - ricavi * (capex_pct_ricavi - depr_pct_ricavi)
            valore += fcff / (1 + wacc) ** anno
        # Terminal value con crescita stabile al 2.5 %
        g = 0.025
        fcff_terminal = (
            ricavi * (1 + g) * margine * (1 - tax_rate) * (1 - g / wacc)
        )
        tv = fcff_terminal / (wacc - g)
        valore += tv / (1 + wacc) ** 10
        # Da enterprise value a equity per azione
        equity = valore - debito_netto
        return equity / shares_outstanding if shares_outstanding > 0 else 0.0

    return crea_tabella_sensitivity(
        valuta, "Crescita Ricavi", crescita_range, "Margine Operativo", margine_range
    )


def formatta_sensitivity(risultato: RisultatoSensitivity, valuta: str = "USD") -> str:
    """Formatta la tabella sensitivity in markdown leggibile.

    Ogni cella della matrice viene formattata come valore monetario.
    Le intestazioni di riga e colonna vengono espresse in percentuale
    se il valore assoluto e' inferiore a 1, altrimenti come decimale.

    Args:
        risultato: oggetto RisultatoSensitivity da formattare.
        valuta: codice ISO della valuta per la formattazione.

    Returns:
        Stringa markdown con la tabella formattata.
    """
    # Intestazioni: prima cella = "ParamRiga \ ParamColonna"
    headers: list[str] = [
        risultato.parametro_riga + " \\ " + risultato.parametro_colonna
    ]
    for c in risultato.valori_colonna:
        if abs(c) < 1:
            headers.append(f"{c:.1%}")
        else:
            headers.append(f"{c:.1f}")

    # Righe della matrice
    rows: list[list[str]] = []
    for i, r in enumerate(risultato.valori_riga):
        if abs(r) < 1:
            row: list[str] = [f"{r:.1%}"]
        else:
            row = [f"{r:.1f}"]
        for val in risultato.matrice_risultati[i]:
            if np.isnan(val):
                row.append("N/A")
            else:
                row.append(formatta_valuta(val, valuta))
        rows.append(row)

    return tabella_markdown(headers, rows)
