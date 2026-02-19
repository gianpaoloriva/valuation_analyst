"""Modulo per la stima del beta (levered e unlevered).

Implementa il metodo bottom-up di Damodaran per la stima del beta:
1. Trova il beta unlevered medio di settore
2. Aggiusta per la componente di cash (operating beta)
3. Rileva il beta per il rapporto D/E target dell'azienda

Fornisce anche il calcolo del beta tramite regressione OLS e
del total beta per investitori non diversificati.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

from valuation_analyst.utils.validators import (
    valida_non_negativo,
    valida_percentuale,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Formula di Hamada: conversione beta levered <-> unlevered
# ---------------------------------------------------------------------------

def beta_levered(
    beta_unlevered: float,
    tax_rate: float,
    debt_equity_ratio: float,
) -> float:
    """Calcola il beta levered dal beta unlevered (formula di Hamada).

    Formula:
        Beta_L = Beta_U * (1 + (1 - t) * D/E)

    Parametri
    ---------
    beta_unlevered : float
        Beta dell'attivo (senza effetto leva finanziaria).
    tax_rate : float
        Aliquota fiscale marginale (es. 0.25 per 25%).
    debt_equity_ratio : float
        Rapporto Debito/Equity a valori di mercato.

    Restituisce
    -----------
    float
        Beta levered (con effetto della leva finanziaria).

    Solleva
    -------
    ValueError
        Se i parametri non superano la validazione.
    """
    _valida_beta(beta_unlevered, "beta_unlevered")
    tax_rate = valida_percentuale(tax_rate, "tax_rate")
    debt_equity_ratio = valida_non_negativo(debt_equity_ratio, "debt_equity_ratio")

    return beta_unlevered * (1.0 + (1.0 - tax_rate) * debt_equity_ratio)


def beta_unlevered(
    beta_levered_val: float,
    tax_rate: float,
    debt_equity_ratio: float,
) -> float:
    """Calcola il beta unlevered dal beta levered (formula di Hamada inversa).

    Formula:
        Beta_U = Beta_L / (1 + (1 - t) * D/E)

    Parametri
    ---------
    beta_levered_val : float
        Beta con effetto leva finanziaria.
    tax_rate : float
        Aliquota fiscale marginale (es. 0.25 per 25%).
    debt_equity_ratio : float
        Rapporto Debito/Equity a valori di mercato.

    Restituisce
    -----------
    float
        Beta unlevered (dell'attivo).

    Solleva
    -------
    ValueError
        Se i parametri non superano la validazione.
    """
    _valida_beta(beta_levered_val, "beta_levered")
    tax_rate = valida_percentuale(tax_rate, "tax_rate")
    debt_equity_ratio = valida_non_negativo(debt_equity_ratio, "debt_equity_ratio")

    denominatore = 1.0 + (1.0 - tax_rate) * debt_equity_ratio
    # Il denominatore e' sempre >= 1.0 dato che (1-t)*D/E >= 0
    return beta_levered_val / denominatore


# ---------------------------------------------------------------------------
# Stima bottom-up del beta (metodo Damodaran)
# ---------------------------------------------------------------------------

def stima_beta_bottom_up(
    settore: str,
    debt_equity_ratio: float,
    tax_rate: float,
    cash_as_pct_firm_value: float = 0.0,
) -> dict[str, Any]:
    """Stima bottom-up del beta secondo il metodo Damodaran.

    Procedura:
    1. Ottieni il beta unlevered medio del settore dal dataset Damodaran
    2. Aggiusta per la componente di cassa (operating beta):
       Beta_operativo = Beta_unlevered_settore / (1 - Cash/FirmValue)
    3. Rileva il beta per il rapporto D/E target dell'azienda
       usando la formula di Hamada

    Parametri
    ---------
    settore : str
        Nome del settore/industria (es. ``"Technology"``).
    debt_equity_ratio : float
        Rapporto Debito/Equity target dell'azienda.
    tax_rate : float
        Aliquota fiscale marginale dell'azienda (es. 0.25).
    cash_as_pct_firm_value : float, opzionale
        Peso della cassa sul valore totale dell'azienda
        (default: 0.0, nessun aggiustamento).

    Restituisce
    -----------
    dict[str, Any]
        Dizionario con le chiavi:
        - ``beta_unlevered_settore`` : beta unlevered medio del settore
        - ``beta_unlevered_operativo`` : beta aggiustato per cassa
        - ``beta_levered`` : beta finale relevered
        - ``debt_equity_ratio`` : rapporto D/E utilizzato
        - ``tax_rate`` : aliquota fiscale utilizzata
        - ``cash_as_pct_firm_value`` : peso della cassa utilizzato
        - ``settore`` : nome del settore

    Solleva
    -------
    ValueError
        Se il settore non e' trovato o i parametri non sono validi.
    """
    # Importazione ritardata per evitare dipendenze circolari
    from valuation_analyst.tools.damodaran_data import get_beta_settore

    # Validazione
    debt_equity_ratio = valida_non_negativo(debt_equity_ratio, "debt_equity_ratio")
    tax_rate = valida_percentuale(tax_rate, "tax_rate")
    cash_as_pct_firm_value = valida_non_negativo(
        cash_as_pct_firm_value, "cash_as_pct_firm_value",
    )
    if cash_as_pct_firm_value >= 1.0:
        raise ValueError(
            "La percentuale di cassa sul valore dell'azienda deve essere "
            f"inferiore a 1.0 (ricevuto: {cash_as_pct_firm_value})."
        )

    # Passo 1: recupera il beta unlevered di settore da Damodaran
    dati_settore = get_beta_settore(settore)
    beta_unlevered_settore = float(dati_settore.get("unlevered_beta", 1.0))

    # Passo 2: aggiusta per la componente di cassa (operating beta)
    # La cassa ha beta ~0, quindi il beta dell'attivo operativo e' piu' alto
    # Beta_operativo = Beta_unlevered / (1 - Cash/FirmValue)
    if cash_as_pct_firm_value > 0.0:
        beta_unlevered_operativo = (
            beta_unlevered_settore / (1.0 - cash_as_pct_firm_value)
        )
    else:
        beta_unlevered_operativo = beta_unlevered_settore

    # Passo 3: rileva il beta per il D/E target dell'azienda
    beta_levered_val = beta_levered(
        beta_unlevered=beta_unlevered_operativo,
        tax_rate=tax_rate,
        debt_equity_ratio=debt_equity_ratio,
    )

    logger.info(
        "Beta bottom-up per settore '%s': "
        "Bu_settore=%.3f, Bu_operativo=%.3f, Bl=%.3f (D/E=%.3f, t=%.2f%%)",
        settore, beta_unlevered_settore, beta_unlevered_operativo,
        beta_levered_val, debt_equity_ratio, tax_rate * 100,
    )

    return {
        "beta_unlevered_settore": beta_unlevered_settore,
        "beta_unlevered_operativo": beta_unlevered_operativo,
        "beta_levered": beta_levered_val,
        "debt_equity_ratio": debt_equity_ratio,
        "tax_rate": tax_rate,
        "cash_as_pct_firm_value": cash_as_pct_firm_value,
        "settore": settore,
    }


# ---------------------------------------------------------------------------
# Beta da regressione OLS
# ---------------------------------------------------------------------------

def beta_da_regressione(
    rendimenti_titolo: list[float] | np.ndarray,
    rendimenti_mercato: list[float] | np.ndarray,
) -> dict[str, float]:
    """Calcola il beta tramite regressione OLS (metodo dei minimi quadrati).

    Esegue la regressione R_i = alpha + beta * R_m + epsilon
    e restituisce beta, alpha, R-quadro, errore standard e t-statistic.

    Parametri
    ---------
    rendimenti_titolo : list[float] | np.ndarray
        Serie dei rendimenti periodici del titolo.
    rendimenti_mercato : list[float] | np.ndarray
        Serie dei rendimenti periodici dell'indice di mercato.
        Deve avere la stessa lunghezza di ``rendimenti_titolo``.

    Restituisce
    -----------
    dict[str, float]
        Dizionario con le chiavi:
        - ``beta`` : coefficiente angolare della regressione
        - ``alpha`` : intercetta (rendimento in eccesso)
        - ``r_squared`` : coefficiente di determinazione R^2
        - ``std_error`` : errore standard del beta
        - ``t_stat`` : t-statistic del beta

    Solleva
    -------
    ValueError
        Se le serie hanno lunghezze diverse o hanno meno di 3 osservazioni.
    """
    # Converti in array numpy
    y = np.asarray(rendimenti_titolo, dtype=np.float64)
    x = np.asarray(rendimenti_mercato, dtype=np.float64)

    # Validazione
    if y.ndim != 1 or x.ndim != 1:
        raise ValueError(
            "I rendimenti devono essere array monodimensionali."
        )
    if len(y) != len(x):
        raise ValueError(
            f"Le serie dei rendimenti devono avere la stessa lunghezza. "
            f"Titolo: {len(y)}, Mercato: {len(x)}."
        )
    if len(y) < 3:
        raise ValueError(
            f"Servono almeno 3 osservazioni per la regressione. "
            f"Ricevute: {len(y)}."
        )

    # Rimuovi eventuali coppie con NaN
    maschera_valida = ~(np.isnan(y) | np.isnan(x))
    y = y[maschera_valida]
    x = x[maschera_valida]

    if len(y) < 3:
        raise ValueError(
            "Dopo la rimozione dei valori mancanti rimangono meno di 3 "
            "osservazioni valide."
        )

    n = len(y)

    # Calcolo della regressione OLS: y = alpha + beta * x
    x_media = np.mean(x)
    y_media = np.mean(y)

    # Covarianza e varianza
    cov_xy = np.sum((x - x_media) * (y - y_media))
    var_x = np.sum((x - x_media) ** 2)

    if var_x == 0.0:
        raise ValueError(
            "La varianza dei rendimenti di mercato e' zero: impossibile "
            "calcolare il beta."
        )

    beta_val = cov_xy / var_x
    alpha_val = y_media - beta_val * x_media

    # Residui e R-quadro
    y_stimato = alpha_val + beta_val * x
    residui = y - y_stimato
    ss_res = np.sum(residui ** 2)
    ss_tot = np.sum((y - y_media) ** 2)

    if ss_tot == 0.0:
        r_squared = 0.0
    else:
        r_squared = 1.0 - ss_res / ss_tot

    # Errore standard del beta e t-statistic
    # Gradi di liberta': n - 2 (alpha e beta stimati)
    gradi_liberta = n - 2
    if gradi_liberta > 0 and var_x > 0:
        varianza_residui = ss_res / gradi_liberta
        std_error = float(np.sqrt(varianza_residui / var_x))
    else:
        std_error = float("inf")

    if std_error > 0 and std_error != float("inf"):
        t_stat = beta_val / std_error
    else:
        t_stat = 0.0

    risultato = {
        "beta": float(beta_val),
        "alpha": float(alpha_val),
        "r_squared": float(r_squared),
        "std_error": float(std_error),
        "t_stat": float(t_stat),
    }

    logger.info(
        "Regressione OLS: beta=%.4f, alpha=%.6f, R2=%.4f, "
        "SE=%.4f, t=%.2f (n=%d)",
        risultato["beta"], risultato["alpha"], risultato["r_squared"],
        risultato["std_error"], risultato["t_stat"], n,
    )

    return risultato


# ---------------------------------------------------------------------------
# Total beta per investitori non diversificati
# ---------------------------------------------------------------------------

def total_beta(beta_mercato: float, correlazione_mercato: float) -> float:
    """Calcola il total beta per investitori non diversificati.

    Il total beta cattura il rischio totale (sistematico + specifico)
    ed e' rilevante per aziende private i cui proprietari non sono
    adeguatamente diversificati.

    Formula:
        Total_Beta = Beta / Correlazione_con_il_mercato

    Parametri
    ---------
    beta_mercato : float
        Beta standard calcolato dalla regressione rispetto al mercato.
    correlazione_mercato : float
        Correlazione tra i rendimenti del titolo e quelli del mercato.
        Deve essere compresa tra -1 e 1 (escluso 0).

    Restituisce
    -----------
    float
        Total beta dell'investimento.

    Solleva
    -------
    ValueError
        Se la correlazione e' zero o fuori dall'intervallo ammesso.
    """
    _valida_beta(beta_mercato, "beta_mercato")

    if not isinstance(correlazione_mercato, (int, float)):
        raise ValueError(
            "La correlazione deve essere un numero "
            f"(ricevuto: {type(correlazione_mercato).__name__})."
        )
    correlazione_mercato = float(correlazione_mercato)

    if correlazione_mercato < -1.0 or correlazione_mercato > 1.0:
        raise ValueError(
            f"La correlazione deve essere compresa tra -1 e 1. "
            f"Ricevuto: {correlazione_mercato}."
        )
    if correlazione_mercato == 0.0:
        raise ValueError(
            "La correlazione con il mercato non puo' essere zero "
            "(il total beta non e' definito)."
        )

    risultato = beta_mercato / correlazione_mercato

    logger.debug(
        "Total beta: %.4f (beta=%.4f, correlazione=%.4f)",
        risultato, beta_mercato, correlazione_mercato,
    )

    return risultato


# ---------------------------------------------------------------------------
# Utilita' interne
# ---------------------------------------------------------------------------

def _valida_beta(valore: float, nome: str = "beta") -> float:
    """Valida un valore di beta.

    L'intervallo ammesso e' da -5 a 10. Valori estremi indicano
    probabilmente un errore nei dati di input.

    Parametri
    ---------
    valore : float
        Il beta da validare.
    nome : str, opzionale
        Nome del parametro per il messaggio di errore.

    Restituisce
    -----------
    float
        Il beta validato.

    Solleva
    -------
    ValueError
        Se il beta e' fuori dall'intervallo ammesso.
    """
    if not isinstance(valore, (int, float)):
        raise ValueError(
            f"Il parametro '{nome}' deve essere un numero "
            f"(ricevuto: {type(valore).__name__})."
        )
    valore = float(valore)

    if valore < -5.0 or valore > 10.0:
        raise ValueError(
            f"Il parametro '{nome}' deve essere compreso tra -5 e 10. "
            f"Ricevuto: {valore}."
        )

    return valore
