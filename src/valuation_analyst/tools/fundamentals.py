"""Funzioni di alto livello per i dati fondamentali delle aziende.

Fornisce un'interfaccia semplificata per costruire DataFrame pandas
con i dati di bilancio, conto economico, cash flow e ratios finanziari
utilizzando il client Massive.com come fonte dati. Include anche
funzioni per il calcolo storico dei flussi di cassa (FCFF e FCFE)
secondo le metodologie di Damodaran.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd

from valuation_analyst.models.company import Company
from valuation_analyst.tools.massive_client import MassiveClient, MassiveClientError

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Recupero dati finanziari come DataFrame
# ---------------------------------------------------------------------------

def get_dati_bilancio(ticker: str, anni: int = 5) -> pd.DataFrame:
    """Recupera lo stato patrimoniale e lo restituisce come DataFrame.

    Ogni riga rappresenta un esercizio, con le colonne:
    data, attivo_totale, attivo_corrente, cassa, debito_totale,
    debito_lungo_termine, debito_breve_termine, patrimonio_netto,
    passivita_totali.

    Parametri
    ---------
    ticker : str
        Simbolo azionario (es. ``"AAPL"``).
    anni : int, opzionale
        Numero di esercizi da recuperare (default: 5).

    Restituisce
    -----------
    pd.DataFrame
        DataFrame indicizzato per data con i dati patrimoniali.

    Solleva
    -------
    ValueError
        Se non ci sono dati disponibili per il ticker specificato.
    """
    with MassiveClient() as client:
        dati_raw = client.get_balance_sheet(ticker, period="annual", limit=anni)

    if not dati_raw:
        raise ValueError(
            f"Stato patrimoniale non disponibile per '{ticker}'."
        )

    righe: list[dict[str, Any]] = []
    for record in dati_raw:
        righe.append({
            "data": record.get("date", ""),
            "attivo_totale": _num(record.get("totalAssets")),
            "attivo_corrente": _num(record.get("totalCurrentAssets")),
            "cassa": _num(record.get("cashAndCashEquivalents")),
            "debito_totale": _num(record.get("totalDebt")),
            "debito_lungo_termine": _num(record.get("longTermDebt")),
            "debito_breve_termine": _num(record.get("shortTermDebt")),
            "patrimonio_netto": _num(record.get("totalStockholdersEquity")),
            "passivita_totali": _num(record.get("totalLiabilities")),
        })

    df = pd.DataFrame(righe)
    if "data" in df.columns:
        df = df.set_index("data")
        df.index.name = "data"

    logger.info("Recuperati %d esercizi di bilancio per %s.", len(df), ticker)
    return df


def get_conto_economico(ticker: str, anni: int = 5) -> pd.DataFrame:
    """Recupera il conto economico e lo restituisce come DataFrame.

    Ogni riga rappresenta un esercizio, con le colonne:
    data, ricavi, costo_venduto, utile_lordo, spese_operative,
    ebit, ebitda, utile_netto, eps, eps_diluito.

    Parametri
    ---------
    ticker : str
        Simbolo azionario.
    anni : int, opzionale
        Numero di esercizi (default: 5).

    Restituisce
    -----------
    pd.DataFrame
        DataFrame indicizzato per data con i dati del conto economico.

    Solleva
    -------
    ValueError
        Se non ci sono dati disponibili.
    """
    with MassiveClient() as client:
        dati_raw = client.get_income_statement(ticker, period="annual", limit=anni)

    if not dati_raw:
        raise ValueError(
            f"Conto economico non disponibile per '{ticker}'."
        )

    righe: list[dict[str, Any]] = []
    for record in dati_raw:
        righe.append({
            "data": record.get("date", ""),
            "ricavi": _num(record.get("revenue")),
            "costo_venduto": _num(record.get("costOfRevenue")),
            "utile_lordo": _num(record.get("grossProfit")),
            "spese_operative": _num(record.get("operatingExpenses")),
            "ebit": _num(record.get("operatingIncome")),
            "ebitda": _num(record.get("ebitda")),
            "utile_netto": _num(record.get("netIncome")),
            "eps": _num(record.get("eps")),
            "eps_diluito": _num(record.get("epsDiluted")),
            "interessi_passivi": _num(record.get("interestExpense")),
            "imposte": _num(record.get("incomeTaxExpense")),
        })

    df = pd.DataFrame(righe)
    if "data" in df.columns:
        df = df.set_index("data")
        df.index.name = "data"

    logger.info("Recuperati %d esercizi di conto economico per %s.", len(df), ticker)
    return df


def get_cash_flow(ticker: str, anni: int = 5) -> pd.DataFrame:
    """Recupera il rendiconto finanziario e lo restituisce come DataFrame.

    Ogni riga rappresenta un esercizio, con le colonne:
    data, flusso_operativo, capex, free_cash_flow, ammortamenti,
    variazione_wc, dividendi_pagati, flusso_finanziamento.

    Parametri
    ---------
    ticker : str
        Simbolo azionario.
    anni : int, opzionale
        Numero di esercizi (default: 5).

    Restituisce
    -----------
    pd.DataFrame
        DataFrame indicizzato per data con i dati del rendiconto finanziario.

    Solleva
    -------
    ValueError
        Se non ci sono dati disponibili.
    """
    with MassiveClient() as client:
        dati_raw = client.get_cash_flow_statement(ticker, period="annual", limit=anni)

    if not dati_raw:
        raise ValueError(
            f"Rendiconto finanziario non disponibile per '{ticker}'."
        )

    righe: list[dict[str, Any]] = []
    for record in dati_raw:
        righe.append({
            "data": record.get("date", ""),
            "flusso_operativo": _num(record.get("operatingCashFlow")),
            "capex": _num(record.get("capitalExpenditure")),
            "free_cash_flow": _num(record.get("freeCashFlow")),
            "ammortamenti": _num(record.get("depreciationAndAmortization")),
            "variazione_wc": _num(record.get("changeInWorkingCapital")),
            "dividendi_pagati": _num(record.get("dividendsPaid")),
            "flusso_finanziamento": _num(record.get("netCashFromFinancing")),
        })

    df = pd.DataFrame(righe)
    if "data" in df.columns:
        df = df.set_index("data")
        df.index.name = "data"

    logger.info("Recuperati %d esercizi di cash flow per %s.", len(df), ticker)
    return df


def get_ratios(ticker: str, anni: int = 5) -> pd.DataFrame:
    """Recupera gli indici finanziari e li restituisce come DataFrame.

    Ogni riga rappresenta un esercizio, con le colonne:
    data, margine_lordo, margine_operativo, margine_netto, roe, roa,
    rapporto_corrente, de_ratio, pe, pb, ev_ebitda.

    Parametri
    ---------
    ticker : str
        Simbolo azionario.
    anni : int, opzionale
        Numero di esercizi (default: 5).

    Restituisce
    -----------
    pd.DataFrame
        DataFrame indicizzato per data con gli indici finanziari.

    Solleva
    -------
    ValueError
        Se non ci sono dati disponibili.
    """
    with MassiveClient() as client:
        dati_raw = client.get_financial_ratios(ticker, period="annual", limit=anni)

    if not dati_raw:
        raise ValueError(
            f"Indici finanziari non disponibili per '{ticker}'."
        )

    righe: list[dict[str, Any]] = []
    for record in dati_raw:
        righe.append({
            "data": record.get("date", ""),
            "margine_lordo": _num(record.get("grossProfitMargin")),
            "margine_operativo": _num(record.get("operatingProfitMargin")),
            "margine_netto": _num(record.get("netProfitMargin")),
            "roe": _num(record.get("returnOnEquity")),
            "roa": _num(record.get("returnOnAssets")),
            "rapporto_corrente": _num(record.get("currentRatio")),
            "de_ratio": _num(record.get("debtEquityRatio")),
            "pe": _num(record.get("priceEarningsRatio")),
            "pb": _num(record.get("priceToBookRatio")),
            "ev_ebitda": _num(record.get("enterpriseValueOverEBITDA")),
        })

    df = pd.DataFrame(righe)
    if "data" in df.columns:
        df = df.set_index("data")
        df.index.name = "data"

    logger.info("Recuperati %d esercizi di ratios per %s.", len(df), ticker)
    return df


# ---------------------------------------------------------------------------
# Costruzione oggetto Company completo
# ---------------------------------------------------------------------------

def get_company_completa(ticker: str) -> Company:
    """Costruisce un oggetto Company con tutti i dati disponibili.

    Recupera profilo, quotazione, bilancio, conto economico,
    cash flow e metriche chiave per popolare una dataclass Company
    pronta per le analisi di valutazione.

    Parametri
    ---------
    ticker : str
        Simbolo azionario.

    Restituisce
    -----------
    Company
        Oggetto Company completamente popolato con i dati disponibili.

    Solleva
    -------
    ValueError
        Se il profilo aziendale non e' disponibile.
    """
    with MassiveClient() as client:
        # Recupera il profilo aziendale
        try:
            profilo = client.get_company_profile(ticker)
        except MassiveClientError as e:
            raise ValueError(
                f"Impossibile recuperare il profilo di '{ticker}': {e}"
            ) from e

        # Recupera la quotazione corrente
        quote: dict[str, Any] = {}
        try:
            quote = client.get_quote(ticker)
        except MassiveClientError as e:
            logger.warning("Quotazione non disponibile per %s: %s", ticker, e)

        # Recupera gli ultimi bilanci
        bilanci: list[dict[str, Any]] = []
        try:
            bilanci = client.get_balance_sheet(ticker, period="annual", limit=1)
        except MassiveClientError as e:
            logger.warning("Bilancio non disponibile per %s: %s", ticker, e)

        # Recupera il conto economico
        conti: list[dict[str, Any]] = []
        try:
            conti = client.get_income_statement(ticker, period="annual", limit=1)
        except MassiveClientError as e:
            logger.warning("Conto economico non disponibile per %s: %s", ticker, e)

        # Recupera il cash flow
        cash_flows: list[dict[str, Any]] = []
        try:
            cash_flows = client.get_cash_flow_statement(ticker, period="annual", limit=1)
        except MassiveClientError as e:
            logger.warning("Cash flow non disponibile per %s: %s", ticker, e)

        # Recupera le metriche chiave (per beta e altri dati)
        metriche: list[dict[str, Any]] = []
        try:
            metriche = client.get_key_metrics(ticker, limit=1)
        except MassiveClientError as e:
            logger.warning("Metriche chiave non disponibili per %s: %s", ticker, e)

    # Estrai il profilo. L'endpoint profilo puo' restituire una lista
    if isinstance(profilo, list) and len(profilo) > 0:
        profilo = profilo[0]

    # Costruisci l'oggetto Company
    mcap = _num(quote.get("marketCap"))
    debito_totale = _num(bilanci[0].get("totalDebt")) if bilanci else None
    cassa = _num(bilanci[0].get("cashAndCashEquivalents")) if bilanci else None

    # Calcola Enterprise Value
    ev: float | None = None
    if mcap and debito_totale is not None and cassa is not None:
        ev = mcap + debito_totale - cassa

    # Calcola tax rate approssimato dal conto economico
    tax_rate: float | None = None
    if conti:
        utile_ante_imposte = _num(conti[0].get("incomeBeforeTax"))
        imposte = _num(conti[0].get("incomeTaxExpense"))
        if utile_ante_imposte and utile_ante_imposte > 0 and imposte is not None:
            tax_rate = imposte / utile_ante_imposte

    # Beta
    beta_val: float | None = None
    if metriche:
        beta_val = _safe_float(metriche[0].get("beta"))
    if beta_val is None:
        beta_val = _safe_float(profilo.get("beta"))

    company = Company(
        ticker=ticker.upper(),
        nome=profilo.get("companyName", ""),
        settore=profilo.get("sector", ""),
        industria=profilo.get("industry", ""),
        paese=profilo.get("country", ""),
        valuta=profilo.get("currency", "USD"),
        market_cap=mcap,
        enterprise_value=ev,
        shares_outstanding=_num(quote.get("sharesOutstanding")),
        prezzo_corrente=_num(quote.get("price")),
        ricavi=_num(conti[0].get("revenue")) if conti else None,
        ebit=_num(conti[0].get("operatingIncome")) if conti else None,
        ebitda=_num(conti[0].get("ebitda")) if conti else None,
        utile_netto=_num(conti[0].get("netIncome")) if conti else None,
        total_debt=debito_totale,
        cash=cassa,
        capex=abs(_num(cash_flows[0].get("capitalExpenditure")) or 0) if cash_flows else None,
        deprezzamento=_num(
            cash_flows[0].get("depreciationAndAmortization")
        ) if cash_flows else None,
        delta_working_capital=_num(
            cash_flows[0].get("changeInWorkingCapital")
        ) if cash_flows else None,
        tax_rate=tax_rate,
        beta=beta_val,
        dividendo_per_azione=_num(quote.get("dividend")),
    )

    logger.info("Costruito oggetto Company per %s (%s).", company.ticker, company.nome)
    return company


# ---------------------------------------------------------------------------
# Calcolo FCFF e FCFE storici
# ---------------------------------------------------------------------------

def calcola_fcff_storico(ticker: str, anni: int = 5) -> pd.DataFrame:
    """Calcola il Free Cash Flow to Firm (FCFF) storico.

    Formula Damodaran: FCFF = EBIT * (1 - t) + Ammortamenti - CapEx - Delta WC

    Recupera i dati necessari da conto economico, bilancio e
    rendiconto finanziario e calcola il FCFF per ogni esercizio.

    Parametri
    ---------
    ticker : str
        Simbolo azionario.
    anni : int, opzionale
        Numero di esercizi (default: 5).

    Restituisce
    -----------
    pd.DataFrame
        DataFrame con colonne: ``data``, ``ebit``, ``tax_rate``,
        ``nopat``, ``ammortamenti``, ``capex``, ``delta_wc``, ``fcff``.

    Solleva
    -------
    ValueError
        Se i dati necessari non sono disponibili.
    """
    with MassiveClient() as client:
        conti = client.get_income_statement(ticker, period="annual", limit=anni)
        cash_flows = client.get_cash_flow_statement(ticker, period="annual", limit=anni)

    if not conti:
        raise ValueError(
            f"Conto economico non disponibile per '{ticker}'. "
            "Impossibile calcolare il FCFF."
        )
    if not cash_flows:
        raise ValueError(
            f"Rendiconto finanziario non disponibile per '{ticker}'. "
            "Impossibile calcolare il FCFF."
        )

    # Costruisci il dizionario dei cash flow indicizzato per data
    cf_per_data: dict[str, dict[str, Any]] = {
        cf.get("date", ""): cf for cf in cash_flows
    }

    righe: list[dict[str, Any]] = []
    for conto in conti:
        data = conto.get("date", "")
        ebit = _num(conto.get("operatingIncome"))

        # Calcola l'aliquota fiscale effettiva
        utile_ante_imposte = _num(conto.get("incomeBeforeTax"))
        imposte = _num(conto.get("incomeTaxExpense"))
        if utile_ante_imposte and utile_ante_imposte > 0 and imposte is not None:
            tax_rate = imposte / utile_ante_imposte
        else:
            tax_rate = 0.25  # Aliquota di default

        # Limita l'aliquota fiscale a range ragionevoli
        tax_rate = max(0.0, min(tax_rate, 0.50))

        nopat = ebit * (1.0 - tax_rate) if ebit else 0.0

        # Dati dal rendiconto finanziario
        cf = cf_per_data.get(data, {})
        ammortamenti = _num(cf.get("depreciationAndAmortization"))
        capex = abs(_num(cf.get("capitalExpenditure")) or 0)
        delta_wc = _num(cf.get("changeInWorkingCapital"))

        # FCFF = NOPAT + D&A - CapEx - Delta WC
        fcff = nopat + (ammortamenti or 0) - capex - (delta_wc or 0)

        righe.append({
            "data": data,
            "ebit": ebit,
            "tax_rate": tax_rate,
            "nopat": nopat,
            "ammortamenti": ammortamenti or 0,
            "capex": capex,
            "delta_wc": delta_wc or 0,
            "fcff": fcff,
        })

    df = pd.DataFrame(righe)
    if "data" in df.columns:
        df = df.set_index("data")
        df.index.name = "data"

    logger.info("Calcolato FCFF storico per %s (%d esercizi).", ticker, len(df))
    return df


def calcola_fcfe_storico(ticker: str, anni: int = 5) -> pd.DataFrame:
    """Calcola il Free Cash Flow to Equity (FCFE) storico.

    Formula Damodaran: FCFE = Utile Netto + Ammortamenti - CapEx
                              - Delta WC + Nuovi Debiti - Rimborsi Debiti

    Dove la variazione netta del debito e' approssimata dalla
    differenza tra debito totale di due periodi consecutivi.

    Parametri
    ---------
    ticker : str
        Simbolo azionario.
    anni : int, opzionale
        Numero di esercizi (default: 5).

    Restituisce
    -----------
    pd.DataFrame
        DataFrame con colonne: ``data``, ``utile_netto``,
        ``ammortamenti``, ``capex``, ``delta_wc``,
        ``variazione_debito``, ``fcfe``.

    Solleva
    -------
    ValueError
        Se i dati necessari non sono disponibili.
    """
    with MassiveClient() as client:
        conti = client.get_income_statement(ticker, period="annual", limit=anni)
        cash_flows = client.get_cash_flow_statement(ticker, period="annual", limit=anni)
        bilanci = client.get_balance_sheet(ticker, period="annual", limit=anni + 1)

    if not conti:
        raise ValueError(
            f"Conto economico non disponibile per '{ticker}'. "
            "Impossibile calcolare il FCFE."
        )
    if not cash_flows:
        raise ValueError(
            f"Rendiconto finanziario non disponibile per '{ticker}'. "
            "Impossibile calcolare il FCFE."
        )

    # Dizionario dei cash flow indicizzato per data
    cf_per_data: dict[str, dict[str, Any]] = {
        cf.get("date", ""): cf for cf in cash_flows
    }

    # Dizionario debito per data (per calcolare la variazione del debito)
    debito_per_data: dict[str, float] = {}
    for b in bilanci:
        data_b = b.get("date", "")
        debito_per_data[data_b] = _num(b.get("totalDebt")) or 0

    # Ordina le date del bilancio per calcolare le variazioni
    date_bilancio = sorted(debito_per_data.keys())

    righe: list[dict[str, Any]] = []
    for conto in conti:
        data = conto.get("date", "")
        utile_netto = _num(conto.get("netIncome"))

        cf = cf_per_data.get(data, {})
        ammortamenti = _num(cf.get("depreciationAndAmortization"))
        capex = abs(_num(cf.get("capitalExpenditure")) or 0)
        delta_wc = _num(cf.get("changeInWorkingCapital"))

        # Calcola la variazione del debito netto
        variazione_debito = 0.0
        debito_corrente = debito_per_data.get(data)
        if debito_corrente is not None:
            # Trova la data precedente nel bilancio
            idx = date_bilancio.index(data) if data in date_bilancio else -1
            if idx > 0:
                data_precedente = date_bilancio[idx - 1]
                debito_precedente = debito_per_data.get(data_precedente, 0)
                variazione_debito = debito_corrente - debito_precedente

        # FCFE = Utile Netto + D&A - CapEx - Delta WC + Variazione Debito
        fcfe = (
            (utile_netto or 0)
            + (ammortamenti or 0)
            - capex
            - (delta_wc or 0)
            + variazione_debito
        )

        righe.append({
            "data": data,
            "utile_netto": utile_netto or 0,
            "ammortamenti": ammortamenti or 0,
            "capex": capex,
            "delta_wc": delta_wc or 0,
            "variazione_debito": variazione_debito,
            "fcfe": fcfe,
        })

    df = pd.DataFrame(righe)
    if "data" in df.columns:
        df = df.set_index("data")
        df.index.name = "data"

    logger.info("Calcolato FCFE storico per %s (%d esercizi).", ticker, len(df))
    return df


# ---------------------------------------------------------------------------
# Utilita' interne
# ---------------------------------------------------------------------------

def _num(valore: Any) -> float | None:
    """Converte un valore in float, restituendo None se non valido.

    Gestisce valori None, stringhe vuote e tipi non numerici.

    Parametri
    ---------
    valore : Any
        Il valore da convertire.

    Restituisce
    -----------
    float | None
        Il valore numerico o None.
    """
    if valore is None:
        return None
    try:
        risultato = float(valore)
        if risultato != risultato:  # NaN check
            return None
        return risultato
    except (ValueError, TypeError):
        return None


def _safe_float(valore: Any) -> float | None:
    """Alias per _num, per chiarezza semantica nei contesti di parsing."""
    return _num(valore)
