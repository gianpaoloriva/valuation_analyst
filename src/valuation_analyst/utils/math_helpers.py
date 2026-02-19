"""Funzioni di matematica finanziaria per la valutazione aziendale.

Fornisce utilita' di calcolo comunemente usate nell'analisi
finanziaria e nella valutazione d'impresa: NPV, IRR, PV, FV,
CAGR, Gordon Growth Model, WACC, beta levered/unlevered.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq


# ---------------------------------------------------------------------------
# Valore Attuale Netto (NPV)
# ---------------------------------------------------------------------------

def npv(tasso: float, cash_flows: list[float]) -> float:
    """Calcola il Valore Attuale Netto di una serie di flussi di cassa.

    Parametri
    ---------
    tasso : float
        Tasso di sconto per periodo (es. 0.10 per il 10 %).
    cash_flows : list[float]
        Lista di flussi di cassa. Il primo elemento e' il flusso al
        tempo 0 (tipicamente un investimento negativo).

    Restituisce
    -----------
    float
        Il valore attuale netto dei flussi di cassa.

    Solleva
    -------
    ValueError
        Se la lista dei flussi di cassa e' vuota o il tasso e' <= -1.
    """
    if not cash_flows:
        raise ValueError("La lista dei flussi di cassa non puo' essere vuota.")
    if tasso <= -1.0:
        raise ValueError(
            f"Il tasso di sconto deve essere maggiore di -1 (ricevuto: {tasso})."
        )

    risultato: float = float(
        np.npv(tasso, cash_flows)  # type: ignore[attr-defined]
        if hasattr(np, "npv")
        else sum(cf / (1.0 + tasso) ** t for t, cf in enumerate(cash_flows))
    )
    return risultato


# ---------------------------------------------------------------------------
# Tasso Interno di Rendimento (IRR) - metodo Brent (piu' robusto di Newton)
# ---------------------------------------------------------------------------

def irr(cash_flows: list[float], guess: float = 0.1) -> float:
    """Calcola il Tasso Interno di Rendimento (IRR) di una serie di flussi.

    Utilizza il metodo di Brent per trovare la radice dell'equazione
    NPV(r) = 0 nell'intervallo [-0.999, 10], garantendo maggiore
    stabilita' rispetto a Newton-Raphson puro.

    Parametri
    ---------
    cash_flows : list[float]
        Lista di flussi di cassa (almeno 2 elementi, con almeno
        un cambio di segno).
    guess : float, opzionale
        Stima iniziale (usata per definire l'intervallo di ricerca).

    Restituisce
    -----------
    float
        Il tasso interno di rendimento.

    Solleva
    -------
    ValueError
        Se i flussi di cassa non sono validi (lista vuota, meno di 2
        elementi, nessun cambio di segno) o se non e' possibile
        trovare una soluzione.
    """
    if len(cash_flows) < 2:
        raise ValueError(
            "Servono almeno due flussi di cassa per calcolare l'IRR."
        )

    # Verifica che ci sia almeno un cambio di segno
    segni = [cf > 0 for cf in cash_flows if cf != 0.0]
    if len(set(segni)) < 2:
        raise ValueError(
            "I flussi di cassa devono contenere almeno un cambio di segno "
            "per poter calcolare l'IRR."
        )

    def _npv_func(r: float) -> float:
        return sum(cf / (1.0 + r) ** t for t, cf in enumerate(cash_flows))

    # Intervallo di ricerca: da -99.9 % a +1000 %
    limite_inf = -0.999
    limite_sup = 10.0

    try:
        risultato: float = float(brentq(_npv_func, limite_inf, limite_sup))
    except ValueError as exc:
        raise ValueError(
            "Impossibile trovare l'IRR nell'intervallo "
            f"[{limite_inf}, {limite_sup}]. "
            "Verificare i flussi di cassa."
        ) from exc

    return risultato


# ---------------------------------------------------------------------------
# Valore Attuale (PV)
# ---------------------------------------------------------------------------

def pv(fv: float, tasso: float, periodi: int) -> float:
    """Calcola il Valore Attuale di un importo futuro.

    Parametri
    ---------
    fv : float
        Valore futuro.
    tasso : float
        Tasso di sconto per periodo.
    periodi : int
        Numero di periodi.

    Restituisce
    -----------
    float
        Il valore attuale.
    """
    if tasso <= -1.0:
        raise ValueError(
            f"Il tasso di sconto deve essere maggiore di -1 (ricevuto: {tasso})."
        )
    if periodi < 0:
        raise ValueError(
            f"Il numero di periodi non puo' essere negativo (ricevuto: {periodi})."
        )

    return fv / (1.0 + tasso) ** periodi


# ---------------------------------------------------------------------------
# Valore Futuro (FV)
# ---------------------------------------------------------------------------

def fv(pv_val: float, tasso: float, periodi: int) -> float:
    """Calcola il Valore Futuro di un importo presente.

    Parametri
    ---------
    pv_val : float
        Valore presente.
    tasso : float
        Tasso di capitalizzazione per periodo.
    periodi : int
        Numero di periodi.

    Restituisce
    -----------
    float
        Il valore futuro.
    """
    if tasso <= -1.0:
        raise ValueError(
            f"Il tasso deve essere maggiore di -1 (ricevuto: {tasso})."
        )
    if periodi < 0:
        raise ValueError(
            f"Il numero di periodi non puo' essere negativo (ricevuto: {periodi})."
        )

    return pv_val * (1.0 + tasso) ** periodi


# ---------------------------------------------------------------------------
# CAGR - Tasso di crescita annuale composto
# ---------------------------------------------------------------------------

def cagr(valore_iniziale: float, valore_finale: float, anni: int) -> float:
    """Calcola il Tasso di Crescita Annuale Composto (CAGR).

    Parametri
    ---------
    valore_iniziale : float
        Valore all'inizio del periodo (deve essere > 0).
    valore_finale : float
        Valore alla fine del periodo (deve essere > 0).
    anni : int
        Numero di anni (deve essere > 0).

    Restituisce
    -----------
    float
        Il tasso di crescita annuale composto.
    """
    if valore_iniziale <= 0:
        raise ValueError(
            f"Il valore iniziale deve essere positivo (ricevuto: {valore_iniziale})."
        )
    if valore_finale <= 0:
        raise ValueError(
            f"Il valore finale deve essere positivo (ricevuto: {valore_finale})."
        )
    if anni <= 0:
        raise ValueError(
            f"Il numero di anni deve essere positivo (ricevuto: {anni})."
        )

    return (valore_finale / valore_iniziale) ** (1.0 / anni) - 1.0


# ---------------------------------------------------------------------------
# Gordon Growth Model (valore terminale)
# ---------------------------------------------------------------------------

def gordon_growth(
    cash_flow: float,
    tasso_sconto: float,
    tasso_crescita: float,
) -> float:
    """Calcola il valore terminale con il modello di Gordon Growth.

    Formula: TV = CF * (1 + g) / (r - g)

    Parametri
    ---------
    cash_flow : float
        Flusso di cassa dell'ultimo periodo esplicito (deve essere > 0).
    tasso_sconto : float
        Tasso di sconto (r).
    tasso_crescita : float
        Tasso di crescita perpetua (g). Deve essere < tasso_sconto.

    Restituisce
    -----------
    float
        Il valore terminale.
    """
    if cash_flow <= 0:
        raise ValueError(
            f"Il flusso di cassa deve essere positivo (ricevuto: {cash_flow})."
        )
    if tasso_crescita >= tasso_sconto:
        raise ValueError(
            "Il tasso di crescita ({:.4f}) deve essere inferiore al "
            "tasso di sconto ({:.4f}).".format(tasso_crescita, tasso_sconto)
        )
    denominatore = tasso_sconto - tasso_crescita
    if abs(denominatore) < 1e-12:
        raise ValueError(
            "La differenza tra tasso di sconto e tasso di crescita e' troppo "
            "vicina a zero: il valore terminale sarebbe infinito."
        )

    return cash_flow * (1.0 + tasso_crescita) / denominatore


# ---------------------------------------------------------------------------
# WACC - Costo Medio Ponderato del Capitale
# ---------------------------------------------------------------------------

def wacc_formula(
    peso_equity: float,
    costo_equity: float,
    peso_debito: float,
    costo_debito: float,
    tax_rate: float,
) -> float:
    """Calcola il WACC (Weighted Average Cost of Capital).

    Formula: WACC = wE * rE + wD * rD * (1 - t)

    Parametri
    ---------
    peso_equity : float
        Peso dell'equity nella struttura del capitale (tra 0 e 1).
    costo_equity : float
        Costo dell'equity (es. 0.10 per 10 %).
    peso_debito : float
        Peso del debito nella struttura del capitale (tra 0 e 1).
    costo_debito : float
        Costo del debito pre-tax.
    tax_rate : float
        Aliquota fiscale (tra 0 e 1).

    Restituisce
    -----------
    float
        Il costo medio ponderato del capitale.
    """
    if not (0.0 <= peso_equity <= 1.0):
        raise ValueError(
            f"Il peso dell'equity deve essere tra 0 e 1 (ricevuto: {peso_equity})."
        )
    if not (0.0 <= peso_debito <= 1.0):
        raise ValueError(
            f"Il peso del debito deve essere tra 0 e 1 (ricevuto: {peso_debito})."
        )
    if not (0.0 <= tax_rate <= 1.0):
        raise ValueError(
            f"L'aliquota fiscale deve essere tra 0 e 1 (ricevuto: {tax_rate})."
        )
    # Tolleranza per arrotondamenti nei pesi
    somma_pesi = peso_equity + peso_debito
    if abs(somma_pesi - 1.0) > 0.01:
        raise ValueError(
            "La somma dei pesi (equity + debito) deve essere pari a 1 "
            f"(ricevuto: {somma_pesi:.4f})."
        )

    return peso_equity * costo_equity + peso_debito * costo_debito * (1.0 - tax_rate)


# ---------------------------------------------------------------------------
# Beta Levered / Unlevered (Hamada)
# ---------------------------------------------------------------------------

def levered_beta(
    beta_unlevered: float,
    tax_rate: float,
    debt_equity_ratio: float,
) -> float:
    """Calcola il beta levered partendo dal beta unlevered (formula di Hamada).

    Formula: beta_L = beta_U * [1 + (1 - t) * (D/E)]

    Parametri
    ---------
    beta_unlevered : float
        Beta unlevered (asset beta), deve essere > 0.
    tax_rate : float
        Aliquota fiscale (tra 0 e 1).
    debt_equity_ratio : float
        Rapporto debito/equity (D/E), deve essere >= 0.

    Restituisce
    -----------
    float
        Il beta levered.
    """
    if beta_unlevered <= 0:
        raise ValueError(
            f"Il beta unlevered deve essere positivo (ricevuto: {beta_unlevered})."
        )
    if not (0.0 <= tax_rate <= 1.0):
        raise ValueError(
            f"L'aliquota fiscale deve essere tra 0 e 1 (ricevuto: {tax_rate})."
        )
    if debt_equity_ratio < 0:
        raise ValueError(
            f"Il rapporto D/E non puo' essere negativo (ricevuto: {debt_equity_ratio})."
        )

    return beta_unlevered * (1.0 + (1.0 - tax_rate) * debt_equity_ratio)


def unlevered_beta(
    beta_levered: float,
    tax_rate: float,
    debt_equity_ratio: float,
) -> float:
    """Calcola il beta unlevered partendo dal beta levered (formula di Hamada).

    Formula: beta_U = beta_L / [1 + (1 - t) * (D/E)]

    Parametri
    ---------
    beta_levered : float
        Beta levered (equity beta), deve essere > 0.
    tax_rate : float
        Aliquota fiscale (tra 0 e 1).
    debt_equity_ratio : float
        Rapporto debito/equity (D/E), deve essere >= 0.

    Restituisce
    -----------
    float
        Il beta unlevered.
    """
    if beta_levered <= 0:
        raise ValueError(
            f"Il beta levered deve essere positivo (ricevuto: {beta_levered})."
        )
    if not (0.0 <= tax_rate <= 1.0):
        raise ValueError(
            f"L'aliquota fiscale deve essere tra 0 e 1 (ricevuto: {tax_rate})."
        )
    if debt_equity_ratio < 0:
        raise ValueError(
            f"Il rapporto D/E non puo' essere negativo (ricevuto: {debt_equity_ratio})."
        )

    denominatore = 1.0 + (1.0 - tax_rate) * debt_equity_ratio
    if abs(denominatore) < 1e-12:
        raise ValueError(
            "Il denominatore della formula di Hamada e' troppo vicino a zero."
        )

    return beta_levered / denominatore
