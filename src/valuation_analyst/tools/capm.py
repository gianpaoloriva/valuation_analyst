"""Modulo per il calcolo del costo dell'equity tramite CAPM.

Formula: Re = Rf + Beta * ERP + CRP + SCP + CSP
Dove:
- Re  = Costo equity
- Rf  = Risk-free rate
- Beta = Sensibilita' al rischio sistematico
- ERP = Equity Risk Premium
- CRP = Country Risk Premium
- SCP = Small Cap Premium
- CSP = Company Specific Premium
"""

from __future__ import annotations

import logging
from typing import Any

from valuation_analyst.config.constants import (
    DEFAULT_ERP,
    DEFAULT_RISK_FREE_RATE,
)
from valuation_analyst.utils.validators import valida_non_negativo, valida_tasso

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Calcolo del costo dell'equity (CAPM esteso)
# ---------------------------------------------------------------------------

def calcola_costo_equity(
    risk_free_rate: float = DEFAULT_RISK_FREE_RATE,
    beta: float = 1.0,
    equity_risk_premium: float = DEFAULT_ERP,
    country_risk_premium: float = 0.0,
    small_cap_premium: float = 0.0,
    company_specific_premium: float = 0.0,
) -> float:
    """Calcola il costo dell'equity tramite il CAPM esteso.

    Formula:
        Re = Rf + Beta * ERP + CRP + SCP + CSP

    Parametri
    ---------
    risk_free_rate : float
        Tasso risk-free (es. rendimento Treasury 10Y). Default da costanti.
    beta : float
        Beta levered dell'azione (default: 1.0).
    equity_risk_premium : float
        Equity Risk Premium del mercato maturo. Default da costanti.
    country_risk_premium : float
        Premio aggiuntivo per il rischio paese (default: 0.0).
    small_cap_premium : float
        Premio per la piccola capitalizzazione (default: 0.0).
    company_specific_premium : float
        Premio per rischi specifici dell'azienda (default: 0.0).

    Restituisce
    -----------
    float
        Il costo dell'equity come valore decimale (es. 0.10 per 10%).

    Solleva
    -------
    ValueError
        Se uno degli input non supera la validazione.
    """
    # Validazione degli input
    risk_free_rate = valida_tasso(risk_free_rate, "risk-free rate")
    equity_risk_premium = valida_tasso(equity_risk_premium, "equity risk premium")
    country_risk_premium = valida_non_negativo(
        country_risk_premium, "country risk premium",
    )
    small_cap_premium = valida_non_negativo(
        small_cap_premium, "small cap premium",
    )
    company_specific_premium = valida_non_negativo(
        company_specific_premium, "company specific premium",
    )

    # Il beta puo' essere negativo (es. oro), ma non puo' essere estremo
    if not isinstance(beta, (int, float)):
        raise ValueError(
            f"Il beta deve essere un numero (ricevuto: {type(beta).__name__})."
        )
    beta = float(beta)
    if beta < -2.0 or beta > 5.0:
        raise ValueError(
            f"Il beta deve essere compreso tra -2 e 5. Ricevuto: {beta}."
        )

    # Re = Rf + Beta * ERP + CRP + SCP + CSP
    costo_equity = (
        risk_free_rate
        + beta * equity_risk_premium
        + country_risk_premium
        + small_cap_premium
        + company_specific_premium
    )

    logger.debug(
        "Costo equity calcolato: %.4f (Rf=%.4f, Beta=%.3f, ERP=%.4f, "
        "CRP=%.4f, SCP=%.4f, CSP=%.4f)",
        costo_equity, risk_free_rate, beta, equity_risk_premium,
        country_risk_premium, small_cap_premium, company_specific_premium,
    )

    return costo_equity


# ---------------------------------------------------------------------------
# Versione dettagliata con scomposizione dei componenti
# ---------------------------------------------------------------------------

def calcola_costo_equity_dettagliato(
    risk_free_rate: float = DEFAULT_RISK_FREE_RATE,
    beta: float = 1.0,
    equity_risk_premium: float = DEFAULT_ERP,
    country_risk_premium: float = 0.0,
    small_cap_premium: float = 0.0,
    company_specific_premium: float = 0.0,
) -> dict[str, Any]:
    """Versione dettagliata che restituisce tutti i componenti del CAPM.

    Identica a :func:`calcola_costo_equity` ma restituisce un dizionario
    con il costo totale e la scomposizione di ciascun componente, utile
    per la reportistica e l'analisi di sensitivita'.

    Parametri
    ---------
    risk_free_rate : float
        Tasso risk-free. Default da costanti.
    beta : float
        Beta levered (default: 1.0).
    equity_risk_premium : float
        Equity Risk Premium. Default da costanti.
    country_risk_premium : float
        Country Risk Premium (default: 0.0).
    small_cap_premium : float
        Small Cap Premium (default: 0.0).
    company_specific_premium : float
        Company Specific Premium (default: 0.0).

    Restituisce
    -----------
    dict[str, Any]
        Dizionario con le chiavi:
        - ``costo_equity`` : costo totale dell'equity
        - ``risk_free_rate`` : tasso risk-free utilizzato
        - ``beta`` : beta utilizzato
        - ``equity_risk_premium`` : ERP utilizzato
        - ``premio_rischio_sistematico`` : contributo Beta * ERP
        - ``country_risk_premium`` : CRP utilizzato
        - ``small_cap_premium`` : SCP utilizzato
        - ``company_specific_premium`` : CSP utilizzato
        - ``componenti`` : sotto-dizionario con la scomposizione additiva

    Solleva
    -------
    ValueError
        Se uno degli input non supera la validazione.
    """
    # Calcola il costo equity totale (include validazione)
    costo_equity = calcola_costo_equity(
        risk_free_rate=risk_free_rate,
        beta=beta,
        equity_risk_premium=equity_risk_premium,
        country_risk_premium=country_risk_premium,
        small_cap_premium=small_cap_premium,
        company_specific_premium=company_specific_premium,
    )

    # Scomposizione dei singoli contributi additivi
    premio_rischio_sistematico = beta * equity_risk_premium

    componenti = {
        "risk_free_rate": risk_free_rate,
        "premio_rischio_sistematico": premio_rischio_sistematico,
        "country_risk_premium": country_risk_premium,
        "small_cap_premium": small_cap_premium,
        "company_specific_premium": company_specific_premium,
    }

    return {
        "costo_equity": costo_equity,
        "risk_free_rate": risk_free_rate,
        "beta": beta,
        "equity_risk_premium": equity_risk_premium,
        "premio_rischio_sistematico": premio_rischio_sistematico,
        "country_risk_premium": country_risk_premium,
        "small_cap_premium": small_cap_premium,
        "company_specific_premium": company_specific_premium,
        "componenti": componenti,
    }


# ---------------------------------------------------------------------------
# Stima del costo equity da dati di settore Damodaran
# ---------------------------------------------------------------------------

def stima_costo_equity_da_settore(
    settore: str,
    paese: str = "US",
    risk_free_rate: float | None = None,
) -> dict[str, Any]:
    """Stima il costo dell'equity usando i dati di settore di Damodaran.

    Carica il beta unlevered di settore dal dataset Damodaran e l'ERP
    dal dataset per paese. Se il risk-free rate non e' fornito,
    utilizza il valore di default.

    Parametri
    ---------
    settore : str
        Nome del settore/industria (es. ``"Technology"``,
        ``"Consumer Electronics"``). La ricerca e' fuzzy.
    paese : str, opzionale
        Paese per cui calcolare il CRP (default: ``"US"``).
        Per gli USA il CRP e' 0.
    risk_free_rate : float | None, opzionale
        Tasso risk-free da utilizzare. Se ``None``, viene usato
        il valore di default.

    Restituisce
    -----------
    dict[str, Any]
        Dizionario con le chiavi:
        - ``costo_equity`` : costo totale dell'equity stimato
        - ``risk_free_rate`` : tasso risk-free utilizzato
        - ``beta_levered`` : beta levered del settore
        - ``beta_unlevered`` : beta unlevered del settore
        - ``equity_risk_premium`` : ERP totale del paese
        - ``country_risk_premium`` : CRP del paese
        - ``settore`` : nome del settore trovato
        - ``fonte`` : fonte dei dati (``"Damodaran"`` o ``"default"``)

    Solleva
    -------
    ValueError
        Se il settore non e' trovato nel dataset.
    """
    # Importazione ritardata per evitare dipendenze circolari
    from valuation_analyst.tools.damodaran_data import (
        get_beta_settore,
        get_erp_paese,
    )

    # Determina il risk-free rate
    if risk_free_rate is None:
        risk_free_rate = DEFAULT_RISK_FREE_RATE

    risk_free_rate = valida_tasso(risk_free_rate, "risk-free rate")

    # Recupera il beta di settore da Damodaran
    fonte = "Damodaran"
    try:
        dati_beta = get_beta_settore(settore)
        beta_unlevered = float(dati_beta.get("unlevered_beta", 1.0))
        beta_levered = float(dati_beta.get("levered_beta", 1.0))
    except (ValueError, KeyError, ConnectionError, RuntimeError) as e:
        logger.warning(
            "Impossibile recuperare il beta di settore per '%s' da Damodaran: %s. "
            "Utilizzo beta di default (1.0).",
            settore, e,
        )
        beta_unlevered = 1.0
        beta_levered = 1.0
        fonte = "default"

    # Recupera l'ERP e il CRP per il paese
    erp_base = DEFAULT_ERP
    crp = 0.0
    try:
        dati_erp = get_erp_paese(paese)
        erp_totale = dati_erp.get("equity_risk_premium")
        crp_val = dati_erp.get("country_risk_premium")
        if erp_totale is not None:
            erp_base = float(erp_totale)
            # L'ERP base maturo e' l'ERP totale meno il CRP
            if crp_val is not None:
                crp = float(crp_val)
                erp_base = erp_base - crp
        elif crp_val is not None:
            crp = float(crp_val)
    except (ValueError, KeyError, ConnectionError, RuntimeError) as e:
        logger.warning(
            "Impossibile recuperare l'ERP per il paese '%s' da Damodaran: %s. "
            "Utilizzo valori di default.",
            paese, e,
        )
        erp_base = DEFAULT_ERP
        crp = 0.0
        if fonte == "Damodaran":
            fonte = "Damodaran/default"
        else:
            fonte = "default"

    # Calcola il costo equity usando il beta levered del settore
    costo_equity = calcola_costo_equity(
        risk_free_rate=risk_free_rate,
        beta=beta_levered,
        equity_risk_premium=erp_base,
        country_risk_premium=crp,
    )

    logger.info(
        "Costo equity stimato per settore '%s' (paese '%s'): %.4f "
        "(Rf=%.4f, Beta_L=%.3f, ERP=%.4f, CRP=%.4f) - Fonte: %s",
        settore, paese, costo_equity, risk_free_rate,
        beta_levered, erp_base, crp, fonte,
    )

    return {
        "costo_equity": costo_equity,
        "risk_free_rate": risk_free_rate,
        "beta_levered": beta_levered,
        "beta_unlevered": beta_unlevered,
        "equity_risk_premium": erp_base,
        "country_risk_premium": crp,
        "settore": settore,
        "fonte": fonte,
    }
