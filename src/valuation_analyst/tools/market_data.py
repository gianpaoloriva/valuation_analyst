"""Funzioni di alto livello per i dati di mercato.

Fornisce un'interfaccia semplificata per ottenere dati di mercato
correnti utilizzando il client Massive.com come fonte dati.
Le funzioni restituiscono valori scalari o dizionari strutturati,
gestendo internamente la creazione e chiusura del client.
"""

from __future__ import annotations

import logging
from typing import Any

from valuation_analyst.config.constants import DEFAULT_RISK_FREE_RATE
from valuation_analyst.tools.massive_client import MassiveClient, MassiveClientError

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Funzioni di accesso ai dati di mercato
# ---------------------------------------------------------------------------

def get_prezzo_corrente(ticker: str) -> float:
    """Recupera il prezzo corrente di un'azione.

    Parametri
    ---------
    ticker : str
        Simbolo azionario (es. ``"AAPL"``).

    Restituisce
    -----------
    float
        Prezzo corrente dell'azione.

    Solleva
    -------
    ValueError
        Se il prezzo non e' disponibile per il ticker specificato.
    """
    with MassiveClient() as client:
        quote = client.get_quote(ticker)

    prezzo = quote.get("price")
    if prezzo is None:
        raise ValueError(
            f"Prezzo non disponibile per il ticker '{ticker}'. "
            "Verifica che il simbolo sia corretto."
        )

    return float(prezzo)


def get_market_cap(ticker: str) -> float:
    """Recupera la capitalizzazione di mercato corrente.

    Parametri
    ---------
    ticker : str
        Simbolo azionario.

    Restituisce
    -----------
    float
        Capitalizzazione di mercato in valuta base.

    Solleva
    -------
    ValueError
        Se la market cap non e' disponibile.
    """
    with MassiveClient() as client:
        valore = client.get_market_cap(ticker)

    if valore is None:
        raise ValueError(
            f"Capitalizzazione di mercato non disponibile per '{ticker}'."
        )

    return valore


def get_shares_outstanding(ticker: str) -> float:
    """Recupera il numero di azioni in circolazione.

    Parametri
    ---------
    ticker : str
        Simbolo azionario.

    Restituisce
    -----------
    float
        Numero di azioni in circolazione.

    Solleva
    -------
    ValueError
        Se il dato non e' disponibile.
    """
    with MassiveClient() as client:
        valore = client.get_shares_outstanding(ticker)

    if valore is None:
        raise ValueError(
            f"Azioni in circolazione non disponibili per '{ticker}'."
        )

    return valore


def get_enterprise_value(ticker: str) -> float:
    """Calcola l'Enterprise Value corrente.

    Formula: EV = Market Cap + Debito Totale - Disponibilita' Liquide

    I dati di debito e cassa sono recuperati dall'ultimo stato
    patrimoniale disponibile.

    Parametri
    ---------
    ticker : str
        Simbolo azionario.

    Restituisce
    -----------
    float
        Enterprise Value in valuta base.

    Solleva
    -------
    ValueError
        Se i dati necessari non sono disponibili.
    """
    with MassiveClient() as client:
        # Recupera market cap dalla quotazione
        mcap = client.get_market_cap(ticker)
        if mcap is None:
            raise ValueError(
                f"Market cap non disponibile per '{ticker}'. "
                "Impossibile calcolare l'Enterprise Value."
            )

        # Recupera debito e cassa dall'ultimo stato patrimoniale
        bilanci = client.get_balance_sheet(ticker, period="annual", limit=1)

    if not bilanci:
        raise ValueError(
            f"Stato patrimoniale non disponibile per '{ticker}'. "
            "Impossibile calcolare l'Enterprise Value."
        )

    ultimo_bilancio = bilanci[0]
    debito_totale = float(ultimo_bilancio.get("totalDebt", 0) or 0)
    cassa = float(ultimo_bilancio.get("cashAndCashEquivalents", 0) or 0)

    ev = mcap + debito_totale - cassa
    logger.info(
        "Enterprise Value per %s: %.0f (MCap=%.0f, Debito=%.0f, Cassa=%.0f)",
        ticker, ev, mcap, debito_totale, cassa,
    )

    return ev


def get_beta(ticker: str) -> float:
    """Recupera il beta del titolo rispetto al mercato.

    Cerca il beta nelle metriche chiave dell'azienda. Se non
    disponibile, usa il beta dal profilo aziendale.

    Parametri
    ---------
    ticker : str
        Simbolo azionario.

    Restituisce
    -----------
    float
        Beta levered del titolo.

    Solleva
    -------
    ValueError
        Se il beta non e' disponibile.
    """
    with MassiveClient() as client:
        # Tenta prima dalle metriche chiave
        try:
            metriche = client.get_key_metrics(ticker, limit=1)
            if metriche:
                beta_val = metriche[0].get("beta")
                if beta_val is not None:
                    return float(beta_val)
        except MassiveClientError:
            logger.debug("Key metrics non disponibili per %s, provo con il profilo.", ticker)

        # Fallback: profilo aziendale
        try:
            profilo = client.get_company_profile(ticker)
            beta_val = profilo.get("beta")
            if beta_val is not None:
                return float(beta_val)
        except MassiveClientError:
            pass

    raise ValueError(
        f"Beta non disponibile per il ticker '{ticker}'. "
        "Verifica che il simbolo sia corretto o usa un valore manuale."
    )


def get_risk_free_rate() -> float:
    """Recupera il tasso risk-free corrente (rendimento Treasury US 10Y).

    Se il dato non e' disponibile dall'API, restituisce il valore
    di default definito nelle costanti del progetto.

    Restituisce
    -----------
    float
        Tasso risk-free annuo come decimale (es. 0.042 per 4.2%).
    """
    try:
        with MassiveClient() as client:
            rendimento = client.get_treasury_yield(maturity="10Y")

        if rendimento is not None:
            logger.info("Tasso risk-free corrente (US 10Y): %.4f", rendimento)
            return rendimento
    except (MassiveClientError, ValueError) as e:
        logger.warning(
            "Impossibile recuperare il tasso risk-free dall'API: %s. "
            "Utilizzo il valore di default (%.4f).",
            e, DEFAULT_RISK_FREE_RATE,
        )

    logger.info(
        "Utilizzo tasso risk-free di default: %.4f", DEFAULT_RISK_FREE_RATE,
    )
    return DEFAULT_RISK_FREE_RATE


def get_snapshot_mercato(ticker: str) -> dict[str, Any]:
    """Recupera uno snapshot completo dei dati di mercato per un ticker.

    Combina in un'unica chiamata tutte le informazioni di mercato
    principali: prezzo, market cap, shares outstanding, enterprise
    value, beta, volume e range di prezzo.

    Parametri
    ---------
    ticker : str
        Simbolo azionario.

    Restituisce
    -----------
    dict[str, Any]
        Dizionario con le seguenti chiavi:
        - ``ticker``: Simbolo azionario
        - ``prezzo``: Prezzo corrente
        - ``variazione_percentuale``: Variazione percentuale giornaliera
        - ``market_cap``: Capitalizzazione di mercato
        - ``shares_outstanding``: Azioni in circolazione
        - ``enterprise_value``: Enterprise Value
        - ``beta``: Beta del titolo
        - ``volume``: Volume di scambi
        - ``volume_medio``: Volume medio
        - ``minimo_52_settimane``: Minimo a 52 settimane
        - ``massimo_52_settimane``: Massimo a 52 settimane
        - ``pe``: Rapporto prezzo/utili
        - ``eps``: Utile per azione
        - ``risk_free_rate``: Tasso risk-free corrente

    Solleva
    -------
    ValueError
        Se i dati di base (quotazione) non sono disponibili.
    """
    with MassiveClient() as client:
        # Recupera la quotazione corrente
        quote = client.get_quote(ticker)

        prezzo = quote.get("price")
        if prezzo is None:
            raise ValueError(
                f"Quotazione non disponibile per '{ticker}'. "
                "Verifica che il simbolo sia corretto."
            )

        mcap = float(quote.get("marketCap", 0) or 0)
        shares = float(quote.get("sharesOutstanding", 0) or 0)

        # Calcola Enterprise Value dal bilancio
        ev: float | None = None
        try:
            bilanci = client.get_balance_sheet(ticker, period="annual", limit=1)
            if bilanci:
                debito = float(bilanci[0].get("totalDebt", 0) or 0)
                cassa = float(bilanci[0].get("cashAndCashEquivalents", 0) or 0)
                ev = mcap + debito - cassa
        except MassiveClientError as e:
            logger.warning("Impossibile calcolare l'EV per %s: %s", ticker, e)

        # Recupera il beta
        beta_val: float | None = None
        try:
            metriche = client.get_key_metrics(ticker, limit=1)
            if metriche:
                beta_val = metriche[0].get("beta")
                if beta_val is not None:
                    beta_val = float(beta_val)
        except MassiveClientError:
            try:
                profilo = client.get_company_profile(ticker)
                b = profilo.get("beta")
                if b is not None:
                    beta_val = float(b)
            except MassiveClientError:
                pass

        # Recupera il tasso risk-free
        rf: float | None = None
        try:
            rf = client.get_treasury_yield(maturity="10Y")
        except MassiveClientError:
            pass

    snapshot: dict[str, Any] = {
        "ticker": ticker.upper(),
        "prezzo": float(prezzo),
        "variazione_percentuale": float(quote.get("changesPercentage", 0) or 0),
        "market_cap": mcap,
        "shares_outstanding": shares,
        "enterprise_value": ev,
        "beta": beta_val,
        "volume": float(quote.get("volume", 0) or 0),
        "volume_medio": float(quote.get("avgVolume", 0) or 0),
        "minimo_52_settimane": float(quote.get("yearLow", 0) or 0),
        "massimo_52_settimane": float(quote.get("yearHigh", 0) or 0),
        "pe": float(quote.get("pe", 0) or 0) or None,
        "eps": float(quote.get("eps", 0) or 0) or None,
        "risk_free_rate": rf if rf is not None else DEFAULT_RISK_FREE_RATE,
    }

    logger.info(
        "Snapshot mercato per %s: prezzo=%.2f, MCap=%.0f, EV=%s",
        ticker, snapshot["prezzo"], snapshot["market_cap"],
        f"{snapshot['enterprise_value']:.0f}" if snapshot["enterprise_value"] else "N/D",
    )

    return snapshot
