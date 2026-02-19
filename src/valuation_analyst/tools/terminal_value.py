"""Calcolo del Terminal Value (valore terminale).

Due metodi principali: Gordon Growth Model e Exit Multiple.
Include anche la variante con reinvestment rate esplicito
secondo l'approccio di Damodaran, e una funzione di verifica
della ragionevolezza del peso del terminal value sul valore totale.
"""

from __future__ import annotations

from valuation_analyst.utils.math_helpers import gordon_growth


# ---------------------------------------------------------------------------
# Terminal Value - Gordon Growth Model
# ---------------------------------------------------------------------------

def terminal_value_gordon(
    cash_flow_ultimo: float,
    tasso_crescita_stabile: float,
    tasso_sconto: float,
) -> float:
    """Terminal Value con Gordon Growth Model.

    Formula: TV = FCF * (1 + g) / (r - g)

    Parametri
    ---------
    cash_flow_ultimo : float
        Flusso di cassa dell'ultimo anno del periodo di proiezione
        esplicita (deve essere > 0).
    tasso_crescita_stabile : float
        Tasso di crescita perpetua (g). Deve essere inferiore al
        tasso di sconto.
    tasso_sconto : float
        Tasso di sconto (WACC per FCFF, Ke per FCFE).

    Restituisce
    -----------
    float
        Il valore terminale (non scontato).

    Solleva
    -------
    ValueError
        Se g >= r o se il flusso di cassa non e' positivo.
    """
    if tasso_crescita_stabile >= tasso_sconto:
        raise ValueError(
            f"Il tasso di crescita stabile ({tasso_crescita_stabile:.4f}) "
            f"deve essere inferiore al tasso di sconto ({tasso_sconto:.4f})."
        )

    # Delega a gordon_growth di math_helpers che contiene gia' le validazioni
    return gordon_growth(
        cash_flow=cash_flow_ultimo,
        tasso_sconto=tasso_sconto,
        tasso_crescita=tasso_crescita_stabile,
    )


# ---------------------------------------------------------------------------
# Terminal Value - Exit Multiple
# ---------------------------------------------------------------------------

def terminal_value_exit_multiple(
    metrica_ultimo_anno: float,
    multiplo_uscita: float,
) -> float:
    """Terminal Value con metodo Exit Multiple.

    Formula: TV = Metrica * Multiplo
    Esempio tipico: TV = EBITDA_ultimo_anno * EV/EBITDA_settore

    Parametri
    ---------
    metrica_ultimo_anno : float
        Valore della metrica finanziaria nell'ultimo anno proiettato
        (es. EBITDA, EBIT, Ricavi). Deve essere > 0.
    multiplo_uscita : float
        Multiplo di uscita applicato (es. 8x EV/EBITDA). Deve essere > 0.

    Restituisce
    -----------
    float
        Il valore terminale (non scontato).

    Solleva
    -------
    ValueError
        Se la metrica o il multiplo non sono positivi.
    """
    if metrica_ultimo_anno <= 0:
        raise ValueError(
            f"La metrica dell'ultimo anno deve essere positiva "
            f"(ricevuto: {metrica_ultimo_anno})."
        )
    if multiplo_uscita <= 0:
        raise ValueError(
            f"Il multiplo di uscita deve essere positivo "
            f"(ricevuto: {multiplo_uscita})."
        )

    return metrica_ultimo_anno * multiplo_uscita


# ---------------------------------------------------------------------------
# Terminal Value con reinvestimento esplicito (Damodaran)
# ---------------------------------------------------------------------------

def terminal_value_con_reinvestimento(
    ebit_after_tax_ultimo: float,
    tasso_crescita_stabile: float,
    roic_stabile: float,
    tasso_sconto: float,
) -> dict:
    """Terminal Value con reinvestment rate esplicito (Damodaran).

    Questo approccio rende esplicito il legame tra crescita e
    reinvestimento: un'azienda puo' crescere del g% solo se
    reinveste g/ROIC dei propri utili operativi after-tax.

    Formule:
        RIR = g / ROIC
        FCFF_terminal = EBIT(1-t)_ultimo * (1+g) * (1 - g/ROIC)
        TV = FCFF_terminal / (r - g)

    Parametri
    ---------
    ebit_after_tax_ultimo : float
        EBIT * (1 - t) dell'ultimo anno proiettato. Deve essere > 0.
    tasso_crescita_stabile : float
        Tasso di crescita perpetua (g).
    roic_stabile : float
        ROIC atteso nella fase stabile. Deve essere > 0.
    tasso_sconto : float
        Tasso di sconto (WACC).

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - tv: Terminal Value.
        - fcff_terminal: FCFF del primo anno della fase terminale.
        - reinvestment_rate: Tasso di reinvestimento stabile (g/ROIC).
        - check: Stringa di verifica che confronta ROIC e WACC.
    """
    if ebit_after_tax_ultimo <= 0:
        raise ValueError(
            f"L'EBIT after-tax deve essere positivo (ricevuto: {ebit_after_tax_ultimo})."
        )
    if roic_stabile <= 0:
        raise ValueError(
            f"Il ROIC stabile deve essere positivo (ricevuto: {roic_stabile})."
        )
    if tasso_crescita_stabile >= tasso_sconto:
        raise ValueError(
            f"Il tasso di crescita stabile ({tasso_crescita_stabile:.4f}) "
            f"deve essere inferiore al tasso di sconto ({tasso_sconto:.4f})."
        )

    # Reinvestment rate stabile
    rir = tasso_crescita_stabile / roic_stabile

    # FCFF del primo anno della fase terminale
    ebit_at_terminale = ebit_after_tax_ultimo * (1.0 + tasso_crescita_stabile)
    fcff_terminal = ebit_at_terminale * (1.0 - rir)

    # Terminal value con Gordon
    denominatore = tasso_sconto - tasso_crescita_stabile
    tv = fcff_terminal / denominatore

    # Verifica ROIC vs WACC: se ROIC < WACC, la crescita distrugge valore
    if roic_stabile > tasso_sconto:
        check = (
            f"ROIC ({roic_stabile:.2%}) > WACC ({tasso_sconto:.2%}): "
            f"la crescita crea valore."
        )
    elif roic_stabile < tasso_sconto:
        check = (
            f"ATTENZIONE: ROIC ({roic_stabile:.2%}) < WACC ({tasso_sconto:.2%}): "
            f"la crescita distrugge valore."
        )
    else:
        check = (
            f"ROIC ({roic_stabile:.2%}) = WACC ({tasso_sconto:.2%}): "
            f"la crescita e' neutrale sul valore."
        )

    return {
        "tv": tv,
        "fcff_terminal": fcff_terminal,
        "reinvestment_rate": rir,
        "check": check,
    }


# ---------------------------------------------------------------------------
# Verifica ragionevolezza del Terminal Value
# ---------------------------------------------------------------------------

def verifica_terminal_value(
    tv: float,
    valore_totale: float,
    soglia_max: float = 0.80,
) -> dict:
    """Verifica che il TV non sia una percentuale eccessiva del valore totale.

    Un terminal value che rappresenta piu' dell'80 % (o della soglia
    specificata) del valore totale e' un segnale di attenzione: le
    ipotesi sulla crescita perpetua hanno un peso dominante e la
    valutazione potrebbe essere fragile.

    Parametri
    ---------
    tv : float
        Valore terminale scontato (valore attuale del terminal value).
    valore_totale : float
        Valore totale dell'impresa (flussi scontati + TV scontato).
    soglia_max : float
        Soglia massima accettabile come percentuale (default 0.80 = 80 %).

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - percentuale: peso del TV sul valore totale (es. 0.72 = 72 %).
        - accettabile: True se la percentuale e' <= soglia_max.
        - messaggio: Stringa descrittiva con il giudizio.
    """
    if valore_totale == 0:
        return {
            "percentuale": 0.0,
            "accettabile": False,
            "messaggio": "Il valore totale e' zero: impossibile calcolare il peso del TV.",
        }

    percentuale = tv / valore_totale
    accettabile = percentuale <= soglia_max

    if accettabile:
        messaggio = (
            f"Il terminal value rappresenta il {percentuale:.1%} del valore totale. "
            f"Entro la soglia del {soglia_max:.0%}: risultato ragionevole."
        )
    else:
        messaggio = (
            f"ATTENZIONE: il terminal value rappresenta il {percentuale:.1%} "
            f"del valore totale, superando la soglia del {soglia_max:.0%}. "
            f"Le ipotesi sulla crescita perpetua dominano la valutazione. "
            f"Verificare le assunzioni del terminal value."
        )

    return {
        "percentuale": percentuale,
        "accettabile": accettabile,
        "messaggio": messaggio,
    }
