"""Modulo per il calcolo del WACC (Weighted Average Cost of Capital).

WACC = (E/V) * Re + (D/V) * Rd * (1 - t)

Dove:
- E/V = peso dell'equity nella struttura del capitale (a valori di mercato)
- D/V = peso del debito nella struttura del capitale (a valori di mercato)
- Re  = costo dell'equity (calcolato con il CAPM)
- Rd  = costo del debito pre-tax
- t   = aliquota fiscale marginale

Fornisce sia il calcolo diretto del WACC sia funzioni di alto livello
che integrano automaticamente i dati da fonti esterne (Damodaran, API).
"""

from __future__ import annotations

import logging
from typing import Any

from valuation_analyst.config.constants import (
    DEFAULT_ERP,
    DEFAULT_RISK_FREE_RATE,
    DEFAULT_TAX_RATE,
)
from valuation_analyst.models.cost_of_capital import CostoCapitale
from valuation_analyst.utils.validators import (
    valida_non_negativo,
    valida_percentuale,
    valida_peso,
    valida_positivo,
    valida_tasso,
)

logger = logging.getLogger(__name__)

# Tolleranza per la verifica che i pesi sommino a 1.0
_TOLLERANZA_PESI: float = 0.01


# ---------------------------------------------------------------------------
# Calcolo base del WACC
# ---------------------------------------------------------------------------

def calcola_wacc(
    costo_equity: float,
    costo_debito_pre_tax: float,
    tax_rate: float,
    peso_equity: float,
    peso_debito: float,
) -> float:
    """Calcola il WACC (Weighted Average Cost of Capital).

    Formula:
        WACC = We * Re + Wd * Rd * (1 - t)

    Parametri
    ---------
    costo_equity : float
        Costo dell'equity (es. 0.10 per 10%).
    costo_debito_pre_tax : float
        Costo del debito al lordo delle imposte (es. 0.05 per 5%).
    tax_rate : float
        Aliquota fiscale marginale (es. 0.25 per 25%).
    peso_equity : float
        Peso dell'equity nella struttura del capitale (tra 0 e 1).
    peso_debito : float
        Peso del debito nella struttura del capitale (tra 0 e 1).

    Restituisce
    -----------
    float
        Il WACC come valore decimale.

    Solleva
    -------
    ValueError
        Se i pesi non sommano approssimativamente a 1.0 o se
        i parametri non superano la validazione.
    """
    # Validazione
    costo_equity = valida_tasso(costo_equity, "costo equity")
    costo_debito_pre_tax = valida_tasso(costo_debito_pre_tax, "costo debito pre-tax")
    tax_rate = valida_percentuale(tax_rate, "tax rate")
    peso_equity = valida_peso(peso_equity, "peso equity")
    peso_debito = valida_peso(peso_debito, "peso debito")

    # Verifica che i pesi sommino a ~1.0
    somma_pesi = peso_equity + peso_debito
    if abs(somma_pesi - 1.0) > _TOLLERANZA_PESI:
        raise ValueError(
            f"I pesi della struttura del capitale devono sommare a 1.0 "
            f"(tolleranza: {_TOLLERANZA_PESI}). "
            f"Somma attuale: {somma_pesi:.4f} "
            f"(equity: {peso_equity:.4f}, debito: {peso_debito:.4f})."
        )

    # WACC = We * Re + Wd * Rd * (1 - t)
    costo_debito_post_tax = costo_debito_pre_tax * (1.0 - tax_rate)
    wacc = peso_equity * costo_equity + peso_debito * costo_debito_post_tax

    logger.debug(
        "WACC calcolato: %.4f (Re=%.4f, Rd_pre=%.4f, Rd_post=%.4f, "
        "We=%.2f%%, Wd=%.2f%%, t=%.2f%%)",
        wacc, costo_equity, costo_debito_pre_tax, costo_debito_post_tax,
        peso_equity * 100, peso_debito * 100, tax_rate * 100,
    )

    return wacc


# ---------------------------------------------------------------------------
# Calcolo completo del WACC con restituzione di CostoCapitale
# ---------------------------------------------------------------------------

def calcola_wacc_completo(
    risk_free_rate: float,
    beta: float,
    equity_risk_premium: float,
    costo_debito_pre_tax: float,
    tax_rate: float,
    market_cap: float,
    total_debt: float,
    country_risk_premium: float = 0.0,
    small_cap_premium: float = 0.0,
    company_specific_premium: float = 0.0,
) -> CostoCapitale:
    """Calcola il WACC completo e restituisce un oggetto CostoCapitale.

    Integra il calcolo del costo dell'equity (CAPM), il costo del debito
    post-tax e i pesi della struttura del capitale, restituendo un
    oggetto ``CostoCapitale`` completamente popolato.

    Parametri
    ---------
    risk_free_rate : float
        Tasso risk-free.
    beta : float
        Beta levered dell'azione.
    equity_risk_premium : float
        Equity Risk Premium del mercato maturo.
    costo_debito_pre_tax : float
        Costo del debito al lordo delle imposte.
    tax_rate : float
        Aliquota fiscale marginale.
    market_cap : float
        Capitalizzazione di mercato (valore dell'equity a mercato).
    total_debt : float
        Debito totale a valore di mercato (o contabile come proxy).
    country_risk_premium : float, opzionale
        Country Risk Premium (default: 0.0).
    small_cap_premium : float, opzionale
        Small Cap Premium (default: 0.0).
    company_specific_premium : float, opzionale
        Company Specific Premium (default: 0.0).

    Restituisce
    -----------
    CostoCapitale
        Oggetto con tutti i componenti del costo del capitale.

    Solleva
    -------
    ValueError
        Se i parametri non superano la validazione.
    """
    # Validazione degli input
    risk_free_rate = valida_tasso(risk_free_rate, "risk-free rate")
    equity_risk_premium = valida_tasso(equity_risk_premium, "equity risk premium")
    costo_debito_pre_tax = valida_tasso(costo_debito_pre_tax, "costo debito pre-tax")
    tax_rate = valida_percentuale(tax_rate, "tax rate")
    market_cap = valida_positivo(market_cap, "market cap")
    total_debt = valida_non_negativo(total_debt, "total debt")
    country_risk_premium = valida_non_negativo(
        country_risk_premium, "country risk premium",
    )
    small_cap_premium = valida_non_negativo(
        small_cap_premium, "small cap premium",
    )
    company_specific_premium = valida_non_negativo(
        company_specific_premium, "company specific premium",
    )

    # Calcola i pesi della struttura del capitale
    valore_totale = market_cap + total_debt
    peso_equity = market_cap / valore_totale
    peso_debito = total_debt / valore_totale

    # Calcola il rapporto D/E
    rapporto_de = total_debt / market_cap

    # Calcola il beta unlevered
    beta_unlevered_val = CostoCapitale.beta_unlevered_da_levered(
        beta_levered=beta,
        rapporto_de=rapporto_de,
        tax_rate=tax_rate,
    )

    # Calcola il costo dell'equity via CAPM
    from valuation_analyst.tools.capm import calcola_costo_equity

    costo_equity = calcola_costo_equity(
        risk_free_rate=risk_free_rate,
        beta=beta,
        equity_risk_premium=equity_risk_premium,
        country_risk_premium=country_risk_premium,
        small_cap_premium=small_cap_premium,
        company_specific_premium=company_specific_premium,
    )

    # Calcola il costo del debito post-tax
    costo_debito_post_tax = costo_debito_pre_tax * (1.0 - tax_rate)

    # Calcola il WACC
    wacc = peso_equity * costo_equity + peso_debito * costo_debito_post_tax

    # Costruisci l'oggetto CostoCapitale
    risultato = CostoCapitale(
        risk_free_rate=risk_free_rate,
        beta_levered=beta,
        beta_unlevered=beta_unlevered_val,
        equity_risk_premium=equity_risk_premium,
        country_risk_premium=country_risk_premium,
        costo_equity=costo_equity,
        costo_debito_pre_tax=costo_debito_pre_tax,
        costo_debito_post_tax=costo_debito_post_tax,
        tax_rate=tax_rate,
        peso_equity=peso_equity,
        peso_debito=peso_debito,
        wacc=wacc,
        small_cap_premium=small_cap_premium,
        company_specific_premium=company_specific_premium,
    )

    logger.info(
        "WACC completo calcolato: %s", risultato,
    )

    return risultato


# ---------------------------------------------------------------------------
# Calcolo WACC a partire da un ticker
# ---------------------------------------------------------------------------

def calcola_wacc_da_ticker(ticker: str) -> CostoCapitale:
    """Calcola il WACC partendo dal ticker di un'azienda quotata.

    Procedura:
    1. Recupera i dati fondamentali dell'azienda (market cap, debito,
       beta, tax rate) tramite i moduli ``market_data`` e ``fundamentals``
    2. Stima il beta bottom-up usando i dati di settore Damodaran
    3. Ottiene il risk premium per il paese dell'azienda
    4. Calcola il WACC completo

    Parametri
    ---------
    ticker : str
        Simbolo azionario (es. ``"AAPL"``, ``"MSFT"``).

    Restituisce
    -----------
    CostoCapitale
        Oggetto con tutti i componenti del costo del capitale.

    Solleva
    -------
    ValueError
        Se non e' possibile recuperare dati sufficienti per il calcolo.
    """
    # Importazioni ritardate per evitare dipendenze circolari
    from valuation_analyst.tools.fundamentals import get_company_completa
    from valuation_analyst.tools.market_data import get_risk_free_rate
    from valuation_analyst.tools.risk_premium import (
        costo_debito_sintetico,
        get_equity_risk_premium,
    )
    from valuation_analyst.utils.validators import valida_ticker

    ticker = valida_ticker(ticker)

    # Passo 1: recupera i dati fondamentali dell'azienda
    company = get_company_completa(ticker)

    # Verifica disponibilita' dei dati minimi
    if company.market_cap is None or company.market_cap <= 0:
        raise ValueError(
            f"Market cap non disponibile per '{ticker}'. "
            "Impossibile calcolare il WACC."
        )

    market_cap = company.market_cap
    total_debt = company.total_debt if company.total_debt is not None else 0.0
    cash = company.cash if company.cash is not None else 0.0

    # Determina il tax rate
    tax_rate = company.tax_rate if company.tax_rate is not None else DEFAULT_TAX_RATE
    # Limita il tax rate a un range ragionevole
    tax_rate = max(0.0, min(tax_rate, 0.50))

    # Passo 2: recupera il risk-free rate
    rf = get_risk_free_rate()

    # Passo 3: determina il beta
    beta_val = company.beta
    if beta_val is None or beta_val <= 0:
        # Tenta la stima bottom-up dal settore
        try:
            from valuation_analyst.tools.beta_estimation import stima_beta_bottom_up

            rapporto_de = total_debt / market_cap if market_cap > 0 else 0.0
            cash_pct = cash / (market_cap + total_debt) if (market_cap + total_debt) > 0 else 0.0
            dati_beta = stima_beta_bottom_up(
                settore=company.industria or company.settore,
                debt_equity_ratio=rapporto_de,
                tax_rate=tax_rate,
                cash_as_pct_firm_value=cash_pct,
            )
            beta_val = dati_beta["beta_levered"]
            logger.info(
                "Beta bottom-up stimato per %s: %.3f (settore: %s)",
                ticker, beta_val, company.industria or company.settore,
            )
        except (ValueError, KeyError, ConnectionError, RuntimeError) as e:
            logger.warning(
                "Impossibile stimare il beta bottom-up per %s: %s. "
                "Utilizzo beta di default (1.0).",
                ticker, e,
            )
            beta_val = 1.0

    # Passo 4: determina l'ERP e il CRP
    paese = company.paese if company.paese else "US"
    dati_erp = get_equity_risk_premium(paese)
    erp_base = dati_erp["erp_base"]
    crp = dati_erp["country_risk_premium"]

    # Passo 5: stima il costo del debito
    if company.ebit is not None and total_debt > 0:
        # Stima gli interessi passivi dal conto economico se disponibili
        # Approssimazione: se non abbiamo gli interessi, usiamo un costo
        # sintetico basato sull'interest coverage
        try:
            from valuation_analyst.tools.fundamentals import get_conto_economico

            ce = get_conto_economico(ticker, anni=1)
            interessi = abs(ce["interessi_passivi"].iloc[0]) if "interessi_passivi" in ce.columns else 0.0

            if interessi > 0 and company.ebit is not None:
                coverage = company.ebit / interessi
                dati_kd = costo_debito_sintetico(coverage, rf)
                kd_pre_tax = dati_kd["costo_debito"]
                logger.info(
                    "Costo debito sintetico per %s: %.4f (coverage=%.2f, "
                    "rating=%s)",
                    ticker, kd_pre_tax, coverage, dati_kd["rating_implicito"],
                )
            else:
                # Fallback: risk-free + spread di default
                kd_pre_tax = rf + DEFAULT_COST_OF_DEBT_SPREAD_FALLBACK
        except (ValueError, KeyError, IndexError) as e:
            logger.warning(
                "Impossibile stimare il costo del debito per %s: %s. "
                "Utilizzo risk-free + spread di default.",
                ticker, e,
            )
            kd_pre_tax = rf + DEFAULT_COST_OF_DEBT_SPREAD_FALLBACK
    elif total_debt > 0:
        # Nessun EBIT disponibile: usa un costo generico
        kd_pre_tax = rf + DEFAULT_COST_OF_DEBT_SPREAD_FALLBACK
    else:
        # Azienda senza debito
        kd_pre_tax = 0.0

    # Passo 6: calcola il WACC completo
    risultato = calcola_wacc_completo(
        risk_free_rate=rf,
        beta=beta_val,
        equity_risk_premium=erp_base,
        costo_debito_pre_tax=kd_pre_tax,
        tax_rate=tax_rate,
        market_cap=market_cap,
        total_debt=total_debt,
        country_risk_premium=crp,
    )

    logger.info(
        "WACC calcolato per %s (%s): %s",
        ticker, company.nome, risultato,
    )

    return risultato


# Spread di fallback per il costo del debito quando non si riesce
# a stimare l'interest coverage (tipicamente BBB- ~250 bps)
DEFAULT_COST_OF_DEBT_SPREAD_FALLBACK: float = 0.025


# ---------------------------------------------------------------------------
# WACC settoriale da dataset Damodaran
# ---------------------------------------------------------------------------

def wacc_settoriale(settore: str) -> dict[str, Any]:
    """Restituisce il WACC medio di settore dal dataset Damodaran.

    Scarica (se necessario) il dataset del WACC settoriale e restituisce
    tutti i componenti per il settore richiesto.

    Parametri
    ---------
    settore : str
        Nome del settore/industria (es. ``"Technology"``).
        La ricerca e' fuzzy.

    Restituisce
    -----------
    dict[str, Any]
        Dizionario con le chiavi:
        - ``wacc`` : WACC medio del settore
        - ``cost_of_equity`` : costo dell'equity medio
        - ``cost_of_debt`` : costo del debito medio
        - ``d_e_ratio`` : rapporto D/E medio del settore
        - ``settore`` : nome del settore trovato
        - ``fonte`` : origine dei dati

    Solleva
    -------
    ValueError
        Se il settore non e' trovato nel dataset.
    """
    # Importazione ritardata per evitare dipendenze circolari
    from valuation_analyst.tools.damodaran_data import get_wacc_settore

    dati = get_wacc_settore(settore)

    risultato = {
        "wacc": dati.get("wacc"),
        "cost_of_equity": dati.get("cost_of_equity"),
        "cost_of_debt": dati.get("cost_of_debt"),
        "d_e_ratio": dati.get("d_e_ratio"),
        "settore": settore,
        "fonte": "Damodaran",
    }

    logger.info(
        "WACC settoriale per '%s': wacc=%s, ke=%s, kd=%s, D/E=%s",
        settore,
        f"{risultato['wacc']:.4f}" if risultato["wacc"] else "N/D",
        f"{risultato['cost_of_equity']:.4f}" if risultato["cost_of_equity"] else "N/D",
        f"{risultato['cost_of_debt']:.4f}" if risultato["cost_of_debt"] else "N/D",
        f"{risultato['d_e_ratio']:.4f}" if risultato["d_e_ratio"] else "N/D",
    )

    return risultato
