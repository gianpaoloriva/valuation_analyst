"""Moduli di accesso ai dati e strumenti di analisi finanziaria.

Questo pacchetto contiene i client API, le funzioni di recupero dati
e gli strumenti di calcolo utilizzati dal sistema di valutazione.

Esportazioni principali
-----------------------
- **MassiveClient**: Client wrapper per l'API Massive.com
- **Dati di mercato**: get_prezzo_corrente, get_market_cap, get_enterprise_value, ecc.
- **Fondamentali**: get_conto_economico, get_dati_bilancio, calcola_fcff_storico, ecc.
- **Damodaran**: get_beta_settore, get_erp_paese, get_wacc_settore, ecc.
- **Cache**: salva_cache, leggi_cache, pulisci_cache, ecc.
- **CAPM**: calcola_costo_equity, stima_costo_equity_da_settore, ecc.
- **Beta**: beta_levered, beta_unlevered, stima_beta_bottom_up, ecc.
- **Risk Premium**: get_equity_risk_premium, calcola_country_risk_premium, ecc.
- **WACC**: calcola_wacc, calcola_wacc_completo, calcola_wacc_da_ticker, ecc.
"""

# --- Client API ---
from valuation_analyst.tools.massive_client import (
    MassiveClient,
    MassiveClientError,
)

# --- Dati di mercato ---
from valuation_analyst.tools.market_data import (
    get_beta,
    get_enterprise_value,
    get_market_cap,
    get_prezzo_corrente,
    get_risk_free_rate,
    get_shares_outstanding,
    get_snapshot_mercato,
)

# --- Dati fondamentali ---
from valuation_analyst.tools.fundamentals import (
    calcola_fcfe_storico,
    calcola_fcff_storico,
    get_cash_flow,
    get_company_completa,
    get_conto_economico,
    get_dati_bilancio,
    get_ratios,
)

# --- Dati Damodaran ---
from valuation_analyst.tools.damodaran_data import (
    get_beta_settore,
    get_erp_paese,
    get_multipli_settore,
    get_wacc_settore,
    lista_paesi,
    lista_settori,
    scarica_dataset,
)

# --- Gestione cache ---
from valuation_analyst.tools.data_cache import (
    dimensione_cache,
    is_cached,
    leggi_cache,
    pulisci_cache,
    salva_cache,
)

# --- CAPM ---
from valuation_analyst.tools.capm import (
    calcola_costo_equity,
    calcola_costo_equity_dettagliato,
    stima_costo_equity_da_settore,
)

# --- Stima Beta ---
from valuation_analyst.tools.beta_estimation import (
    beta_da_regressione,
    beta_levered,
    beta_unlevered,
    stima_beta_bottom_up,
    total_beta,
)

# --- Risk Premium ---
from valuation_analyst.tools.risk_premium import (
    RATING_DEFAULT_SPREADS,
    calcola_country_risk_premium,
    costo_debito_sintetico,
    get_equity_risk_premium,
    spread_da_rating,
)

# --- WACC ---
from valuation_analyst.tools.wacc import (
    calcola_wacc,
    calcola_wacc_completo,
    calcola_wacc_da_ticker,
    wacc_settoriale,
)

__all__ = [
    # Client
    "MassiveClient",
    "MassiveClientError",
    # Dati di mercato
    "get_prezzo_corrente",
    "get_market_cap",
    "get_shares_outstanding",
    "get_enterprise_value",
    "get_beta",
    "get_risk_free_rate",
    "get_snapshot_mercato",
    # Fondamentali
    "get_dati_bilancio",
    "get_conto_economico",
    "get_cash_flow",
    "get_ratios",
    "get_company_completa",
    "calcola_fcff_storico",
    "calcola_fcfe_storico",
    # Damodaran
    "scarica_dataset",
    "get_beta_settore",
    "get_erp_paese",
    "get_wacc_settore",
    "get_multipli_settore",
    "lista_settori",
    "lista_paesi",
    # Cache
    "salva_cache",
    "leggi_cache",
    "is_cached",
    "pulisci_cache",
    "dimensione_cache",
    # CAPM
    "calcola_costo_equity",
    "calcola_costo_equity_dettagliato",
    "stima_costo_equity_da_settore",
    # Beta
    "beta_levered",
    "beta_unlevered",
    "stima_beta_bottom_up",
    "beta_da_regressione",
    "total_beta",
    # Risk Premium
    "get_equity_risk_premium",
    "calcola_country_risk_premium",
    "spread_da_rating",
    "RATING_DEFAULT_SPREADS",
    "costo_debito_sintetico",
    # WACC
    "calcola_wacc",
    "calcola_wacc_completo",
    "calcola_wacc_da_ticker",
    "wacc_settoriale",
]
