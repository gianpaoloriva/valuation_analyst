"""Helper per recuperare dati finanziari live da Massive.com.

Centralizza il fetch dei dati necessari per gli script di analisi,
convertendo i valori nelle unita' usate dagli script (milioni USD).

Endpoint utilizzati (API Massive.com):
- /v3/reference/tickers/{ticker}  -> profilo, market_cap, shares
- /v2/aggs/ticker/{ticker}/prev   -> prezzo di chiusura
- /fed/v1/treasury-yields          -> rendimento Treasury US 10Y
- /stocks/financials/v1/*          -> fondamentali (richiede piano superiore)
"""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

# Assicura che src/ sia nel path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

load_dotenv()

logger = logging.getLogger(__name__)

MASSIVE_API_KEY: str = os.getenv("MASSIVE_API_KEY", "")
MASSIVE_BASE_URL: str = "https://api.massive.com"


def _safe_float(valore: Any, default: float = 0.0) -> float:
    """Converte un valore in float con fallback al default."""
    if valore is None:
        return default
    try:
        val = float(valore)
        if val != val:  # NaN check
            return default
        return val
    except (ValueError, TypeError):
        return default


def _get(client: httpx.Client, endpoint: str, params: dict[str, Any] | None = None) -> Any:
    """Esegue una GET verso l'API Massive.com con gestione errori."""
    r = client.get(endpoint, params=params)
    if r.status_code == 403:
        return None  # Endpoint non disponibile con il piano corrente
    r.raise_for_status()
    return r.json()


def _fetch_ticker_overview(client: httpx.Client, ticker: str) -> dict[str, Any]:
    """Recupera il profilo aziendale da /v3/reference/tickers/{ticker}."""
    data = _get(client, f"/v3/reference/tickers/{ticker}")
    return data.get("results", {}) if data else {}


def _fetch_prezzo(client: httpx.Client, ticker: str) -> float:
    """Recupera il prezzo di chiusura da /v2/aggs/ticker/{ticker}/prev."""
    data = _get(client, f"/v2/aggs/ticker/{ticker}/prev")
    if data and data.get("results"):
        return _safe_float(data["results"][0].get("c"))
    return 0.0


def _fetch_risk_free_rate(client: httpx.Client) -> float:
    """Recupera il rendimento Treasury US 10Y da /fed/v1/treasury-yields."""
    data = _get(client, "/fed/v1/treasury-yields", params={"sort": "date.desc", "limit": 1})
    if data and data.get("results"):
        yield_10y = data["results"][0].get("yield_10_year")
        if yield_10y is not None:
            return float(yield_10y) / 100.0  # Da percentuale a decimale
    return 0.043  # Default


def _fetch_fondamentali(
    client: httpx.Client, ticker: str,
) -> dict[str, Any] | None:
    """Tenta di recuperare income statement, balance sheet e cash flow.

    Restituisce None se gli endpoint non sono accessibili (piano free).
    """
    base_params = {"tickers": ticker, "timeframe": "annual", "limit": 1, "sort": "period_end.desc"}

    income = _get(client, "/stocks/financials/v1/income-statements", params=base_params)
    balance = _get(client, "/stocks/financials/v1/balance-sheets", params=base_params)
    cashflow = _get(client, "/stocks/financials/v1/cash-flow-statements", params=base_params)

    # Se anche uno solo e' None (403), i fondamentali non sono disponibili
    if income is None or balance is None or cashflow is None:
        return None

    inc = income.get("results", [{}])[0] if income.get("results") else {}
    bal = balance.get("results", [{}])[0] if balance.get("results") else {}
    cf = cashflow.get("results", [{}])[0] if cashflow.get("results") else {}

    return {"income": inc, "balance": bal, "cashflow": cf}


def _carica_fallback(ticker: str) -> dict[str, Any] | None:
    """Carica i fondamentali di fallback da scripts/configs/{TICKER}.json.

    Restituisce None se il file non esiste o non contiene fondamentali_fallback.
    """
    config_path = ROOT / "scripts" / "configs" / f"{ticker.upper()}.json"
    if not config_path.exists():
        return None
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)
    return config.get("fondamentali_fallback")


def fetch_dati_azienda(ticker: str) -> dict[str, Any]:
    """Recupera dati finanziari live da Massive.com per un dato ticker.

    Usa gli endpoint REST corretti dell'API Massive.com. I dati di mercato
    (prezzo, market cap, shares, risk-free rate) vengono sempre recuperati
    live. I dati fondamentali (income statement, balance sheet, cash flow)
    vengono recuperati live se il piano API lo consente, altrimenti si usano
    i valori di fallback piu' recenti.

    Parametri
    ---------
    ticker : str
        Simbolo azionario (es. ``"GOOGL"``, ``"MSFT"``).

    Restituisce
    -----------
    dict[str, Any]
        Dizionario con tutti i valori necessari per l'analisi.
        Valori monetari in milioni, prezzo per azione in dollari.
    """
    if not MASSIVE_API_KEY:
        raise ValueError(
            "API key Massive.com non configurata. "
            "Imposta MASSIVE_API_KEY nel file .env nella radice del progetto."
        )

    print(f"Recupero dati live da Massive.com per {ticker}...")

    M = 1e6

    with httpx.Client(
        base_url=MASSIVE_BASE_URL,
        headers={
            "Authorization": f"Bearer {MASSIVE_API_KEY}",
            "Accept": "application/json",
        },
        timeout=30.0,
    ) as client:
        # --- Dati sempre disponibili (piano free) ---
        overview = _fetch_ticker_overview(client, ticker)
        prezzo = _fetch_prezzo(client, ticker)
        risk_free = _fetch_risk_free_rate(client)

        # --- Fondamentali (richiedono piano superiore) ---
        fondamentali = _fetch_fondamentali(client, ticker)

    # Profilo aziendale
    nome = overview.get("name", ticker)
    settore = overview.get("sic_description", "")
    paese = "US" if overview.get("locale") == "us" else overview.get("locale", "US")
    valuta = (overview.get("currency_name") or "usd").upper()

    # Market data live
    market_cap_abs = _safe_float(overview.get("market_cap"))
    # weighted_shares_outstanding include tutte le classi di azioni
    shares_abs = _safe_float(overview.get("weighted_shares_outstanding"))
    if shares_abs == 0:
        shares_abs = _safe_float(overview.get("share_class_shares_outstanding"))

    shares_outstanding = shares_abs / M
    market_cap = market_cap_abs / M

    if fondamentali is not None:
        # --- Dati fondamentali LIVE dall'API ---
        print("  Fondamentali: LIVE da API")
        inc = fondamentali["income"]
        bal = fondamentali["balance"]
        cf = fondamentali["cashflow"]

        ricavi = _safe_float(inc.get("revenue")) / M
        ebit = _safe_float(inc.get("operating_income")) / M
        ebitda = _safe_float(inc.get("ebitda")) / M
        utile_netto = _safe_float(inc.get("consolidated_net_income_loss")) / M

        # Tax rate
        utile_ante = _safe_float(inc.get("income_before_income_taxes"))
        imposte = _safe_float(inc.get("income_taxes"))
        if utile_ante > 0 and imposte > 0:
            tax_rate = max(0.0, min(imposte / utile_ante, 0.50))
        else:
            tax_rate = 0.21

        # Balance sheet (i campi Massive sono snake_case)
        debt_current = _safe_float(bal.get("debt_current"))
        debt_lt = _safe_float(bal.get("long_term_debt_and_capital_lease_obligations"))
        total_debt = (debt_current + debt_lt) / M
        cash = _safe_float(bal.get("cash_and_equivalents")) / M
        book_value_equity = _safe_float(bal.get("total_equity")) / M

        # Cash flow
        capex = abs(_safe_float(cf.get("purchase_of_property_plant_and_equipment"))) / M
        deprezzamento = _safe_float(cf.get("depreciation_depletion_and_amortization")) / M
        delta_wc_raw = _safe_float(cf.get("change_in_other_operating_assets_and_liabilities_net"))
        delta_wc = -delta_wc_raw / M

        beta_levered = 1.0  # Non disponibile nei fondamentali, da sovrascrivere nello script

    else:
        # --- Fallback: dati fondamentali da config JSON ---
        fb = _carica_fallback(ticker)
        if fb is None:
            raise ValueError(
                f"Fondamentali non disponibili dall'API per '{ticker}' "
                f"e nessun dato di fallback configurato. "
                f"Per usare questo ticker, aggiungi 'fondamentali_fallback' "
                f"in scripts/configs/{ticker.upper()}.json "
                f"o aggiorna il piano API Massive.com."
            )
        print(f"  Fondamentali: FALLBACK (piano API non include /stocks/financials/*)")

        ricavi = fb["ricavi"]
        ebit = fb["ebit"]
        ebitda = fb["ebitda"]
        utile_netto = fb["utile_netto"]
        total_debt = fb["total_debt"]
        cash = fb["cash"]
        book_value_equity = fb["book_value_equity"]
        capex = fb["capex"]
        deprezzamento = fb["deprezzamento"]
        delta_wc = fb["delta_wc"]
        tax_rate = fb["tax_rate"]
        beta_levered = fb["beta_levered"]

    # Valori derivati
    debito_netto = total_debt - cash
    enterprise_value = market_cap + debito_netto
    eps = utile_netto / shares_outstanding if shares_outstanding > 0 else 0.0
    bvps = book_value_equity / shares_outstanding if shares_outstanding > 0 else 0.0

    dati: dict[str, Any] = {
        # Info aziendali
        "nome": nome,
        "settore": settore,
        "paese": paese,
        "valuta": valuta,
        # Mercato (prezzo in USD, il resto in milioni)
        "prezzo_corrente": prezzo,
        "shares_outstanding": shares_outstanding,
        "market_cap": market_cap,
        # Conto economico (milioni)
        "ricavi": ricavi,
        "ebit": ebit,
        "ebitda": ebitda,
        "utile_netto": utile_netto,
        # Bilancio (milioni)
        "total_debt": total_debt,
        "cash": cash,
        "book_value_equity": book_value_equity,
        # Cash flow (milioni)
        "capex": capex,
        "deprezzamento": deprezzamento,
        "delta_wc": delta_wc,
        # Parametri
        "tax_rate": tax_rate,
        "beta_levered": beta_levered,
        "risk_free_rate": risk_free,
        # Derivati
        "debito_netto": debito_netto,
        "enterprise_value": enterprise_value,
        "eps": eps,
        "book_value_per_share": bvps,
    }

    print(f"  Prezzo: ${prezzo:.2f}")
    print(f"  Market Cap: {market_cap:,.0f}M")
    print(f"  Shares Outstanding: {shares_outstanding:,.0f}M")
    print(f"  Ricavi: {ricavi:,.0f}M")
    print(f"  EBIT: {ebit:,.0f}M")
    print(f"  Beta: {beta_levered:.2f}")
    print(f"  Tax Rate: {tax_rate:.2%}")
    print(f"  Risk-Free: {risk_free:.4f}")
    print()

    return dati
