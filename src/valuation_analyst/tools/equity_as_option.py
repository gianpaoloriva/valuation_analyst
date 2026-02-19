"""Valutazione dell'equity come call option sugli asset aziendali.

Secondo Damodaran, l'equity puo' essere vista come una call option europea
dove:
- Sottostante (V) = Valore totale asset
- Strike (K) = Valore nominale debito
- Scadenza (T) = Maturity media ponderata debito
- Volatilita' (sigma) = Volatilita' del valore degli asset
"""

from __future__ import annotations

import math

from scipy.stats import norm

from valuation_analyst.models.option_inputs import InputBlackScholes
from valuation_analyst.models.valuation_result import ValuationResult
from valuation_analyst.tools.black_scholes import calcola_d1, calcola_d2, prezzo_call


def valuta_equity_come_opzione(
    valore_asset: float,
    debito_nominale: float,
    scadenza_debito: float,
    risk_free_rate: float,
    volatilita_asset: float,
    dividendo_yield: float = 0.0,
) -> dict[str, float]:
    """Valuta l'equity come call option sugli asset.

    Nel modello di Merton, l'equity di un'azienda e' una call europea
    sul valore delle attivita' aziendali, con strike pari al valore
    nominale del debito.

    Parametri
    ---------
    valore_asset : float
        Valore corrente delle attivita' aziendali (V).
    debito_nominale : float
        Valore nominale del debito (K, strike).
    scadenza_debito : float
        Scadenza media ponderata del debito in anni (T).
    risk_free_rate : float
        Tasso risk-free annuale (r).
    volatilita_asset : float
        Volatilita' annualizzata del valore degli asset (sigma).
    dividendo_yield : float, opzionale
        Dividend yield continuo (default 0.0).

    Restituisce
    -----------
    dict[str, float]
        Dizionario con:
        - valore_equity: valore stimato dell'equity
        - valore_debito: valore di mercato implicito del debito (V - E)
        - probabilita_default: probabilita' di default N(-d2)
        - d1, d2: valori intermedi della formula
        - N_d1, N_d2: probabilita' cumulate
        - yield_implicito_debito: rendimento implicito del debito
        - default_spread: spread di default rispetto al risk-free
    """
    # Calcolo d1 e d2
    d1 = calcola_d1(
        valore_asset, debito_nominale, risk_free_rate,
        volatilita_asset, scadenza_debito, dividendo_yield,
    )
    d2 = calcola_d2(d1, volatilita_asset, scadenza_debito)

    # Probabilita' cumulate
    n_d1 = float(norm.cdf(d1))
    n_d2 = float(norm.cdf(d2))

    # Valore dell'equity = call option
    valore_equity = prezzo_call(
        valore_asset, debito_nominale, risk_free_rate,
        volatilita_asset, scadenza_debito, dividendo_yield,
    )

    # Valore di mercato implicito del debito
    valore_debito = valore_asset - valore_equity

    # Probabilita' di default = N(-d2)
    probabilita_default = float(norm.cdf(-d2))

    # Yield implicito del debito: -ln(D/K) / T
    # D e' il valore di mercato del debito, K e' il nominale
    if valore_debito > 0 and debito_nominale > 0 and scadenza_debito > 0:
        yield_implicito = -math.log(valore_debito / debito_nominale) / scadenza_debito
    else:
        yield_implicito = float("inf")

    # Spread di default rispetto al risk-free
    default_spread = yield_implicito - risk_free_rate

    return {
        "valore_equity": valore_equity,
        "valore_debito": valore_debito,
        "probabilita_default": probabilita_default,
        "d1": d1,
        "d2": d2,
        "N_d1": n_d1,
        "N_d2": n_d2,
        "yield_implicito_debito": yield_implicito,
        "default_spread": default_spread,
    }


def stima_volatilita_asset(
    volatilita_equity: float,
    market_cap: float,
    debito_mercato: float,
) -> float:
    """Stima approssimata della volatilita' degli asset dalla volatilita' equity.

    Utilizza la relazione semplificata (senza effetto leva di Merton):
        sigma_V = sigma_E * E / (E + D)

    dove E e' la capitalizzazione di mercato e D e' il valore di mercato
    del debito.

    Parametri
    ---------
    volatilita_equity : float
        Volatilita' annualizzata dell'equity (sigma_E).
    market_cap : float
        Capitalizzazione di mercato (E).
    debito_mercato : float
        Valore di mercato del debito (D).

    Restituisce
    -----------
    float
        Stima della volatilita' degli asset (sigma_V).
    """
    if market_cap + debito_mercato <= 0:
        raise ValueError(
            "La somma di market cap e debito deve essere positiva."
        )

    return volatilita_equity * market_cap / (market_cap + debito_mercato)


def stima_volatilita_asset_iterativa(
    volatilita_equity: float,
    market_cap: float,
    debito_nominale: float,
    scadenza_debito: float,
    risk_free_rate: float,
    max_iter: int = 100,
    tolleranza: float = 1e-6,
) -> dict[str, float | int | bool]:
    """Stima iterativa della volatilita' asset (metodo Damodaran).

    Utilizza un procedimento iterativo a punto fisso basato sulla relazione:
        sigma_V = sigma_E * (E / V) / N(d1)

    dove E e' la capitalizzazione di mercato e V e' il valore degli asset
    (calcolato come E + D di mercato). La procedura converge perche' il
    valore dell'equity (E) e d1 dipendono a loro volta da sigma_V.

    Algoritmo:
    1. Stima iniziale di sigma_V con l'approssimazione lineare.
    2. Calcola il valore dell'equity E tramite Black-Scholes con sigma_V.
    3. Aggiorna sigma_V = sigma_E * (E / (E + D_mercato)) / N(d1).
    4. Ripeti fino a convergenza.

    Parametri
    ---------
    volatilita_equity : float
        Volatilita' annualizzata dell'equity osservata.
    market_cap : float
        Capitalizzazione di mercato attuale.
    debito_nominale : float
        Valore nominale del debito (strike dell'opzione).
    scadenza_debito : float
        Scadenza media ponderata del debito in anni.
    risk_free_rate : float
        Tasso risk-free annuale.
    max_iter : int, opzionale
        Numero massimo di iterazioni (default 100).
    tolleranza : float, opzionale
        Tolleranza per la convergenza (default 1e-6).

    Restituisce
    -----------
    dict
        Dizionario con:
        - sigma_asset: volatilita' stimata degli asset
        - sigma_equity: volatilita' equity di input (per riferimento)
        - iterazioni: numero di iterazioni effettuate
        - convergenza: True se l'algoritmo e' convergente
    """
    # Stima iniziale: approssimazione lineare
    # V_0 = E + D (approssimazione grezza)
    valore_asset_stima = market_cap + debito_nominale
    sigma_v = volatilita_equity * market_cap / valore_asset_stima

    convergenza = False
    iterazioni = 0

    for i in range(max_iter):
        iterazioni = i + 1

        # Calcola d1 con la sigma_V corrente
        d1 = calcola_d1(
            valore_asset_stima, debito_nominale, risk_free_rate,
            sigma_v, scadenza_debito,
        )

        # N(d1)
        n_d1 = float(norm.cdf(d1))

        # Calcola il valore dell'equity con la sigma_V corrente
        equity_bs = prezzo_call(
            valore_asset_stima, debito_nominale, risk_free_rate,
            sigma_v, scadenza_debito,
        )

        # Aggiorna il valore degli asset: V = E + D_mercato
        # Usiamo il valore di E calcolato da BS per stimare V
        # Il valore di mercato del debito implicito e': D_mkt = V - E
        # Ma V e' anche E_mercato + D_mercato, quindi usiamo
        # V = market_cap + (V_old - equity_bs) come aggiornamento,
        # oppure piu' semplicemente: V = market_cap + D_mercato_implicito
        # Per il metodo di Damodaran, manteniamo V costante come
        # market_cap + debito_nominale_attualizzato.
        # Approccio: V = market_cap + valore_debito_implicito
        valore_debito_implicito = valore_asset_stima - equity_bs
        if valore_debito_implicito > 0:
            valore_asset_stima = market_cap + valore_debito_implicito
        else:
            # Se il debito implicito e' negativo, usiamo il nominale attualizzato
            valore_asset_stima = market_cap + debito_nominale * math.exp(
                -risk_free_rate * scadenza_debito
            )

        # Aggiorna sigma_V
        if n_d1 > 0 and valore_asset_stima > 0:
            sigma_v_nuovo = volatilita_equity * (market_cap / valore_asset_stima) / n_d1
        else:
            # Protezione contro divisione per zero
            sigma_v_nuovo = sigma_v

        # Verifica convergenza
        if abs(sigma_v_nuovo - sigma_v) < tolleranza:
            sigma_v = sigma_v_nuovo
            convergenza = True
            break

        sigma_v = sigma_v_nuovo

    return {
        "sigma_asset": sigma_v,
        "sigma_equity": volatilita_equity,
        "iterazioni": iterazioni,
        "convergenza": convergenza,
    }


def valutazione_equity_opzione(
    ticker: str,
    valore_asset: float,
    debito_nominale: float,
    scadenza_debito: float,
    risk_free_rate: float,
    volatilita_asset: float,
    shares_outstanding: float,
    prezzo_corrente: float | None = None,
    dividendo_yield: float = 0.0,
) -> ValuationResult:
    """Valutazione completa dell'equity come opzione.

    Applica il modello di Merton per ottenere il valore dell'equity
    e lo converte in valore per azione. Genera un ValuationResult
    completo con parametri, dettagli e note.

    Parametri
    ---------
    ticker : str
        Simbolo di borsa dell'azienda.
    valore_asset : float
        Valore corrente delle attivita' aziendali (in milioni).
    debito_nominale : float
        Valore nominale del debito (in milioni).
    scadenza_debito : float
        Scadenza media ponderata del debito in anni.
    risk_free_rate : float
        Tasso risk-free annuale.
    volatilita_asset : float
        Volatilita' annualizzata degli asset.
    shares_outstanding : float
        Numero di azioni in circolazione (in milioni).
    prezzo_corrente : float | None, opzionale
        Prezzo corrente per azione per il confronto (default None).
    dividendo_yield : float, opzionale
        Dividend yield continuo (default 0.0).

    Restituisce
    -----------
    ValuationResult
        Risultato completo della valutazione.
    """
    # Esegui la valutazione dell'equity come opzione
    risultato_opzione = valuta_equity_come_opzione(
        valore_asset=valore_asset,
        debito_nominale=debito_nominale,
        scadenza_debito=scadenza_debito,
        risk_free_rate=risk_free_rate,
        volatilita_asset=volatilita_asset,
        dividendo_yield=dividendo_yield,
    )

    valore_equity = risultato_opzione["valore_equity"]

    # Valore per azione
    if shares_outstanding > 0:
        valore_per_azione = valore_equity / shares_outstanding
    else:
        raise ValueError(
            "Il numero di azioni in circolazione deve essere positivo."
        )

    # Costruisci i parametri
    parametri: dict[str, float | str | int | bool] = {
        "valore_asset": valore_asset,
        "debito_nominale": debito_nominale,
        "scadenza_debito": scadenza_debito,
        "risk_free_rate": risk_free_rate,
        "volatilita_asset": volatilita_asset,
        "dividendo_yield": dividendo_yield,
        "shares_outstanding": shares_outstanding,
    }
    if prezzo_corrente is not None:
        parametri["prezzo_corrente"] = prezzo_corrente

    # Costruisci i dettagli
    dettagli: dict[str, float | str | list[float]] = {
        "valore_equity": valore_equity,
        "valore_debito": risultato_opzione["valore_debito"],
        "d1": risultato_opzione["d1"],
        "d2": risultato_opzione["d2"],
        "N_d1": risultato_opzione["N_d1"],
        "N_d2": risultato_opzione["N_d2"],
        "probabilita_default": risultato_opzione["probabilita_default"],
        "yield_implicito_debito": risultato_opzione["yield_implicito_debito"],
        "default_spread": risultato_opzione["default_spread"],
    }

    # Note interpretative
    note: list[str] = []

    prob_default = risultato_opzione["probabilita_default"]
    if prob_default > 0.20:
        note.append(
            f"Attenzione: probabilita' di default elevata ({prob_default:.1%}). "
            "Il modello suggerisce un significativo rischio di insolvenza."
        )
    elif prob_default > 0.05:
        note.append(
            f"Probabilita' di default moderata ({prob_default:.1%}). "
            "Monitorare la situazione finanziaria."
        )
    else:
        note.append(
            f"Probabilita' di default contenuta ({prob_default:.1%})."
        )

    # Verifica se l'azienda e' in distress
    if valore_asset < debito_nominale:
        note.append(
            "L'azienda appare in distress: il valore degli asset e' inferiore "
            "al debito nominale. L'equity ha comunque valore positivo grazie "
            "al valore temporale dell'opzione."
        )

    # Nota sullo spread
    spread = risultato_opzione["default_spread"]
    if spread > 0.05:
        note.append(
            f"Lo spread di default implicito e' molto elevato ({spread:.2%}), "
            "indicativo di alto rischio creditizio."
        )

    return ValuationResult(
        ticker=ticker,
        metodo="OPTION_EQUITY",
        valore_equity=valore_equity,
        valore_per_azione=valore_per_azione,
        parametri=parametri,
        dettagli=dettagli,
        note=note,
    )


def analisi_distress(
    valore_asset: float,
    debito_nominale: float,
    scadenza_debito: float,
    risk_free_rate: float,
    volatilita_asset: float,
) -> dict[str, float | bool]:
    """Analisi di distress: confronta valore asset vs debito.

    Valuta la situazione finanziaria dell'azienda utilizzando il modello
    di Merton per determinare la probabilita' di default e il valore
    residuo dell'equity anche in condizioni di distress.

    Parametri
    ---------
    valore_asset : float
        Valore corrente delle attivita' aziendali.
    debito_nominale : float
        Valore nominale del debito.
    scadenza_debito : float
        Scadenza media ponderata del debito in anni.
    risk_free_rate : float
        Tasso risk-free annuale.
    volatilita_asset : float
        Volatilita' annualizzata degli asset.

    Restituisce
    -----------
    dict
        Dizionario con:
        - in_distress: True se il valore degli asset e' inferiore al debito
        - rapporto_copertura: V / K (valori > 1 indicano copertura adeguata)
        - probabilita_default: N(-d2)
        - valore_equity_residuo: valore dell'equity anche se V < K
        - recovery_rate_implicito: D_mercato / K (tasso di recupero per i creditori)
    """
    # Calcolo della call option (equity)
    risultato = valuta_equity_come_opzione(
        valore_asset=valore_asset,
        debito_nominale=debito_nominale,
        scadenza_debito=scadenza_debito,
        risk_free_rate=risk_free_rate,
        volatilita_asset=volatilita_asset,
    )

    # Indicatori di distress
    in_distress = valore_asset < debito_nominale
    rapporto_copertura = valore_asset / debito_nominale

    # Valore di mercato del debito e recovery rate
    valore_debito_mercato = risultato["valore_debito"]
    recovery_rate = valore_debito_mercato / debito_nominale if debito_nominale > 0 else 0.0

    return {
        "in_distress": in_distress,
        "rapporto_copertura": rapporto_copertura,
        "probabilita_default": risultato["probabilita_default"],
        "valore_equity_residuo": risultato["valore_equity"],
        "recovery_rate_implicito": recovery_rate,
    }
