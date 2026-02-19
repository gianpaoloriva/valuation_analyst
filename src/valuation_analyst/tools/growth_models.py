"""Modelli di crescita multi-fase per proiezioni DCF.

Implementa modelli a 2 e 3 fasi secondo Damodaran per generare
tassi di crescita variabili nel tempo, partendo da una fase di
alta crescita fino alla convergenza verso un tasso stabile.
"""

from __future__ import annotations

from valuation_analyst.utils.math_helpers import cagr


# ---------------------------------------------------------------------------
# Modello a 2 fasi
# ---------------------------------------------------------------------------

def crescita_2_fasi(
    tasso_alta: float,
    tasso_stabile: float,
    anni_alta: int = 5,
) -> list[float]:
    """Genera tassi di crescita per modello a 2 fasi.

    Nella prima fase (anni 1..anni_alta) si applica il tasso di alta
    crescita. Dal periodo successivo in poi si assume crescita stabile
    perpetua (usata per il terminal value).

    Parametri
    ---------
    tasso_alta : float
        Tasso di crescita annuale nella fase di alta crescita (es. 0.20).
    tasso_stabile : float
        Tasso di crescita perpetua nella fase stabile (es. 0.025).
    anni_alta : int
        Durata della fase di alta crescita in anni (default 5).

    Restituisce
    -----------
    list[float]
        Lista di tassi di crescita per anno 1..anni_alta.
        L'ultimo elemento della lista rappresenta il tasso usato
        nell'anno finale della proiezione esplicita; il tasso stabile
        sara' applicato dal terminal value in poi.
    """
    if anni_alta < 1:
        raise ValueError(
            f"anni_alta deve essere almeno 1 (ricevuto: {anni_alta})."
        )

    # Fase 1: alta crescita costante
    tassi: list[float] = [tasso_alta] * anni_alta
    return tassi


# ---------------------------------------------------------------------------
# Modello a 3 fasi
# ---------------------------------------------------------------------------

def crescita_3_fasi(
    tasso_alta: float,
    tasso_stabile: float,
    anni_alta: int = 5,
    anni_transizione: int = 5,
) -> list[float]:
    """Genera tassi di crescita per modello a 3 fasi.

    Fase 1: alta crescita costante (anni 1..anni_alta).
    Fase 2: convergenza lineare dal tasso di alta crescita al tasso
            stabile (anni anni_alta+1..anni_alta+anni_transizione).
    Fase 3: crescita stabile perpetua (terminal value, non inclusa
            nella lista restituita).

    Parametri
    ---------
    tasso_alta : float
        Tasso di crescita nella fase di alta crescita.
    tasso_stabile : float
        Tasso di crescita perpetua nella fase stabile.
    anni_alta : int
        Durata della fase di alta crescita (default 5).
    anni_transizione : int
        Durata della fase di transizione (default 5).

    Restituisce
    -----------
    list[float]
        Lista di tassi di crescita per anno 1..(anni_alta + anni_transizione).
        L'ultimo tasso sara' pari a tasso_stabile, segnando la fine
        della transizione.
    """
    if anni_alta < 1:
        raise ValueError(
            f"anni_alta deve essere almeno 1 (ricevuto: {anni_alta})."
        )
    if anni_transizione < 1:
        raise ValueError(
            f"anni_transizione deve essere almeno 1 (ricevuto: {anni_transizione})."
        )

    tassi: list[float] = []

    # Fase 1: alta crescita costante
    tassi.extend([tasso_alta] * anni_alta)

    # Fase 2: convergenza lineare da alta a stabile
    # In anni_transizione passi il tasso converge linearmente.
    # Al passo 1 della transizione il tasso inizia a scendere,
    # all'ultimo passo raggiunge esattamente tasso_stabile.
    for i in range(1, anni_transizione + 1):
        frazione = i / anni_transizione
        tasso_anno = tasso_alta + (tasso_stabile - tasso_alta) * frazione
        tassi.append(tasso_anno)

    return tassi


# ---------------------------------------------------------------------------
# Crescita da fondamentali (Damodaran)
# ---------------------------------------------------------------------------

def crescita_da_fondamentali(
    reinvestment_rate: float,
    roic: float,
) -> float:
    """Crescita fondamentale: g = RIR * ROIC (Damodaran).

    La crescita attesa e' pari al prodotto tra il tasso di
    reinvestimento e il ritorno sul capitale investito.

    Parametri
    ---------
    reinvestment_rate : float
        Tasso di reinvestimento (es. 0.50 per il 50 %).
    roic : float
        Return on Invested Capital (es. 0.15 per il 15 %).

    Restituisce
    -----------
    float
        Tasso di crescita fondamentale atteso.
    """
    return reinvestment_rate * roic


# ---------------------------------------------------------------------------
# Reinvestment rate
# ---------------------------------------------------------------------------

def reinvestment_rate(
    capex: float,
    deprezzamento: float,
    delta_wc: float,
    ebit_after_tax: float,
) -> float:
    """Calcola il reinvestment rate.

    RIR = (CapEx - Deprezzamento + Delta WC) / EBIT(1-t)

    Rappresenta la frazione di utile operativo dopo le tasse
    che l'azienda reinveste in immobilizzazioni e capitale
    circolante.

    Parametri
    ---------
    capex : float
        Spese in conto capitale (valore positivo).
    deprezzamento : float
        Ammortamenti e deprezzamento (valore positivo).
    delta_wc : float
        Variazione del capitale circolante netto (positivo = assorbimento).
    ebit_after_tax : float
        EBIT al netto delle imposte, cioe' EBIT * (1 - t).

    Restituisce
    -----------
    float
        Il tasso di reinvestimento.

    Solleva
    -------
    ValueError
        Se ebit_after_tax e' zero o negativo.
    """
    if ebit_after_tax <= 0:
        raise ValueError(
            "L'EBIT after-tax deve essere positivo per calcolare il "
            f"reinvestment rate (ricevuto: {ebit_after_tax})."
        )

    reinvestimento_netto = capex - deprezzamento + delta_wc
    return reinvestimento_netto / ebit_after_tax


# ---------------------------------------------------------------------------
# Reinvestment rate stabile (coerente con la crescita terminale)
# ---------------------------------------------------------------------------

def reinvestment_rate_stabile(
    tasso_crescita_stabile: float,
    roic_stabile: float,
) -> float:
    """Reinvestment rate coerente con la crescita stabile.

    RIR_stabile = g / ROIC

    Nella fase terminale il reinvestment rate deve essere consistente
    con il tasso di crescita stabile: se l'azienda vuole crescere del
    g% e il suo ROIC e' del ROIC%, deve reinvestire g/ROIC dei suoi
    utili operativi.

    Parametri
    ---------
    tasso_crescita_stabile : float
        Tasso di crescita perpetua (es. 0.025).
    roic_stabile : float
        ROIC atteso nella fase stabile (es. 0.10).

    Restituisce
    -----------
    float
        Il reinvestment rate stabile.

    Solleva
    -------
    ValueError
        Se roic_stabile e' zero o negativo.
    """
    if roic_stabile <= 0:
        raise ValueError(
            "Il ROIC stabile deve essere positivo per calcolare il "
            f"reinvestment rate stabile (ricevuto: {roic_stabile})."
        )

    return tasso_crescita_stabile / roic_stabile


# ---------------------------------------------------------------------------
# Stima crescita multi-metodo
# ---------------------------------------------------------------------------

def stima_crescita(
    ricavi_storici: list[float],
    utili_storici: list[float] | None = None,
    reinvestment_rate_val: float | None = None,
    roic: float | None = None,
) -> dict:
    """Stima la crescita utilizzando multipli metodi.

    Combina la crescita storica (CAGR dei ricavi e degli utili),
    la crescita fondamentale (RIR * ROIC) e produce una stima
    consigliata come media pesata dei metodi disponibili.

    Parametri
    ---------
    ricavi_storici : list[float]
        Serie storica dei ricavi (almeno 2 valori, ordinata
        dal piu' vecchio al piu' recente).
    utili_storici : list[float] | None
        Serie storica degli utili netti (facoltativo).
    reinvestment_rate_val : float | None
        Tasso di reinvestimento (facoltativo, per la crescita fondamentale).
    roic : float | None
        Return on Invested Capital (facoltativo, per la crescita fondamentale).

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - cagr_ricavi: CAGR calcolato sui ricavi storici (o None).
        - cagr_utili: CAGR calcolato sugli utili storici (o None).
        - crescita_fondamentale: g = RIR * ROIC (o None).
        - crescita_consigliata: media pesata dei metodi disponibili.
    """
    risultati: dict = {
        "cagr_ricavi": None,
        "cagr_utili": None,
        "crescita_fondamentale": None,
        "crescita_consigliata": None,
    }

    stime: list[float] = []

    # CAGR dei ricavi
    if len(ricavi_storici) >= 2 and ricavi_storici[0] > 0 and ricavi_storici[-1] > 0:
        cagr_ric = cagr(
            valore_iniziale=ricavi_storici[0],
            valore_finale=ricavi_storici[-1],
            anni=len(ricavi_storici) - 1,
        )
        risultati["cagr_ricavi"] = cagr_ric
        stime.append(cagr_ric)

    # CAGR degli utili
    if (
        utili_storici is not None
        and len(utili_storici) >= 2
        and utili_storici[0] > 0
        and utili_storici[-1] > 0
    ):
        cagr_ut = cagr(
            valore_iniziale=utili_storici[0],
            valore_finale=utili_storici[-1],
            anni=len(utili_storici) - 1,
        )
        risultati["cagr_utili"] = cagr_ut
        stime.append(cagr_ut)

    # Crescita fondamentale
    if reinvestment_rate_val is not None and roic is not None:
        g_fond = crescita_da_fondamentali(reinvestment_rate_val, roic)
        risultati["crescita_fondamentale"] = g_fond
        stime.append(g_fond)

    # Crescita consigliata: media semplice dei metodi disponibili
    if stime:
        risultati["crescita_consigliata"] = sum(stime) / len(stime)

    return risultati
