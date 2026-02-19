"""Modello Black-Scholes per la valutazione di opzioni.

Implementa la formula classica di Black-Scholes per opzioni europee,
con estensione per dividendi (Merton).
"""

from __future__ import annotations

import math

from scipy.stats import norm

from valuation_analyst.models.option_inputs import InputBlackScholes
from valuation_analyst.utils.validators import (
    valida_non_negativo,
    valida_positivo,
    valida_tasso,
)


def calcola_d1(
    V: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    q: float = 0.0,
) -> float:
    """Calcola d1 della formula Black-Scholes.

    d1 = [ln(V/K) + (r - q + sigma^2/2)*T] / (sigma*sqrt(T))

    Parametri
    ---------
    V : float
        Valore del sottostante (prezzo spot o valore asset).
    K : float
        Prezzo di esercizio (strike).
    r : float
        Tasso risk-free annuale.
    sigma : float
        Volatilita' annualizzata del sottostante.
    T : float
        Tempo alla scadenza in anni.
    q : float, opzionale
        Dividend yield continuo (default 0.0).

    Restituisce
    -----------
    float
        Valore di d1.
    """
    # Validazione parametri
    valida_positivo(V, "valore_sottostante")
    valida_positivo(K, "strike")
    valida_positivo(sigma, "volatilita")
    valida_positivo(T, "tempo_scadenza")
    valida_non_negativo(q, "dividend_yield")

    numeratore = math.log(V / K) + (r - q + sigma**2 / 2) * T
    denominatore = sigma * math.sqrt(T)
    return numeratore / denominatore


def calcola_d2(d1: float, sigma: float, T: float) -> float:
    """Calcola d2 = d1 - sigma*sqrt(T).

    Parametri
    ---------
    d1 : float
        Valore di d1 gia' calcolato.
    sigma : float
        Volatilita' annualizzata del sottostante.
    T : float
        Tempo alla scadenza in anni.

    Restituisce
    -----------
    float
        Valore di d2.
    """
    return d1 - sigma * math.sqrt(T)


def prezzo_call(
    V: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    q: float = 0.0,
) -> float:
    """Calcola il prezzo di una call europea con Black-Scholes.

    C = V*e^(-qT)*N(d1) - K*e^(-rT)*N(d2)

    Parametri
    ---------
    V : float
        Valore del sottostante.
    K : float
        Prezzo di esercizio.
    r : float
        Tasso risk-free annuale.
    sigma : float
        Volatilita' annualizzata.
    T : float
        Tempo alla scadenza in anni.
    q : float, opzionale
        Dividend yield continuo (default 0.0).

    Restituisce
    -----------
    float
        Prezzo della call europea.
    """
    d1 = calcola_d1(V, K, r, sigma, T, q)
    d2 = calcola_d2(d1, sigma, T)

    call = (
        V * math.exp(-q * T) * norm.cdf(d1)
        - K * math.exp(-r * T) * norm.cdf(d2)
    )
    return call


def prezzo_put(
    V: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    q: float = 0.0,
) -> float:
    """Calcola il prezzo di una put europea con Black-Scholes.

    P = K*e^(-rT)*N(-d2) - V*e^(-qT)*N(-d1)

    Parametri
    ---------
    V : float
        Valore del sottostante.
    K : float
        Prezzo di esercizio.
    r : float
        Tasso risk-free annuale.
    sigma : float
        Volatilita' annualizzata.
    T : float
        Tempo alla scadenza in anni.
    q : float, opzionale
        Dividend yield continuo (default 0.0).

    Restituisce
    -----------
    float
        Prezzo della put europea.
    """
    d1 = calcola_d1(V, K, r, sigma, T, q)
    d2 = calcola_d2(d1, sigma, T)

    put = (
        K * math.exp(-r * T) * norm.cdf(-d2)
        - V * math.exp(-q * T) * norm.cdf(-d1)
    )
    return put


def greche(
    V: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    q: float = 0.0,
) -> dict[str, float]:
    """Calcola le greche (delta, gamma, theta, vega, rho) per una call.

    Parametri
    ---------
    V : float
        Valore del sottostante.
    K : float
        Prezzo di esercizio.
    r : float
        Tasso risk-free annuale.
    sigma : float
        Volatilita' annualizzata.
    T : float
        Tempo alla scadenza in anni.
    q : float, opzionale
        Dividend yield continuo (default 0.0).

    Restituisce
    -----------
    dict[str, float]
        Dizionario con le greche: delta, gamma, theta, vega, rho.
    """
    d1 = calcola_d1(V, K, r, sigma, T, q)
    d2 = calcola_d2(d1, sigma, T)

    # Delta: sensibilita' al prezzo del sottostante
    delta = math.exp(-q * T) * norm.cdf(d1)

    # Gamma: sensibilita' del delta al prezzo del sottostante
    gamma = math.exp(-q * T) * norm.pdf(d1) / (V * sigma * math.sqrt(T))

    # Theta: decadimento temporale (per anno)
    theta = (
        -(V * sigma * math.exp(-q * T) * norm.pdf(d1)) / (2 * math.sqrt(T))
        - r * K * math.exp(-r * T) * norm.cdf(d2)
        + q * V * math.exp(-q * T) * norm.cdf(d1)
    )

    # Vega: sensibilita' alla volatilita'
    vega = V * math.exp(-q * T) * norm.pdf(d1) * math.sqrt(T)

    # Rho: sensibilita' al tasso risk-free
    rho = K * T * math.exp(-r * T) * norm.cdf(d2)

    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "rho": rho,
    }


def black_scholes_completo(inputs: InputBlackScholes) -> dict[str, float | dict[str, float]]:
    """Calcolo completo Black-Scholes da InputBlackScholes dataclass.

    Esegue il calcolo completo della call e della put, comprese le greche,
    le probabilita' e i valori intermedi d1 e d2.

    Parametri
    ---------
    inputs : InputBlackScholes
        Dataclass con tutti gli input del modello.

    Restituisce
    -----------
    dict
        Dizionario con:
        - prezzo_call: prezzo della call europea
        - prezzo_put: prezzo della put europea
        - d1: valore di d1
        - d2: valore di d2
        - greche: dizionario con delta, gamma, theta, vega, rho
        - N_d1: probabilita' cumulata N(d1)
        - N_d2: probabilita' cumulata N(d2)
        - prob_itm: probabilita' che l'opzione scada in-the-money (N(d2) per la call)
    """
    # Estrazione parametri dalla dataclass
    V = inputs.valore_attivita
    K = inputs.valore_nominale_debito
    r = inputs.risk_free_rate
    sigma = inputs.volatilita
    T = inputs.scadenza_debito
    q = inputs.dividendo_yield

    # Calcolo valori intermedi
    d1 = calcola_d1(V, K, r, sigma, T, q)
    d2 = calcola_d2(d1, sigma, T)

    # Probabilita' cumulate
    n_d1 = float(norm.cdf(d1))
    n_d2 = float(norm.cdf(d2))

    # Prezzi delle opzioni
    call = prezzo_call(V, K, r, sigma, T, q)
    put = prezzo_put(V, K, r, sigma, T, q)

    # Greche della call
    greche_call = greche(V, K, r, sigma, T, q)

    return {
        "prezzo_call": call,
        "prezzo_put": put,
        "d1": d1,
        "d2": d2,
        "greche": greche_call,
        "N_d1": n_d1,
        "N_d2": n_d2,
        "prob_itm": n_d2,
    }
