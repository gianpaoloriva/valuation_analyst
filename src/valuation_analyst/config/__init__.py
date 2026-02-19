"""Pacchetto di configurazione per valuation_analyst.

Esporta le impostazioni globali, le costanti finanziarie
e gli URL dei dataset di Damodaran.
"""

from valuation_analyst.config.settings import (
    ROOT_DIR,
    DATA_DIR,
    CACHE_DIR,
    REPORTS_DIR,
    LOGS_DIR,
    SAMPLES_DIR,
    MASSIVE_API_KEY,
    MASSIVE_BASE_URL,
    DAMODARAN_BASE_URL,
    PROMPT_LOG_PATH,
    CACHE_EXPIRY_HOURS,
    LOG_LEVEL,
    assicura_directory,
)
from valuation_analyst.config.constants import (
    DEFAULT_RISK_FREE_RATE,
    DEFAULT_MARKET_RETURN,
    DEFAULT_ERP,
    DEFAULT_TAX_RATE,
    DEFAULT_TERMINAL_GROWTH,
    DEFAULT_STABLE_GROWTH,
    DEFAULT_HIGH_GROWTH_YEARS,
    DEFAULT_TRANSITION_YEARS,
    MARKET_CAP_THRESHOLDS,
    SECTOR_NAMES,
    MULTIPLE_NAMES,
    METODI_VALUTAZIONE,
    ParametriDCF,
    ParametriRelativa,
)
from valuation_analyst.config.damodaran_urls import (
    DamodaranDataset,
    DAMODARAN_DATASETS,
    ottieni_url_html,
    ottieni_url_excel,
    lista_dataset_disponibili,
)

__all__ = [
    # Percorsi
    "ROOT_DIR",
    "DATA_DIR",
    "CACHE_DIR",
    "REPORTS_DIR",
    "LOGS_DIR",
    "SAMPLES_DIR",
    "PROMPT_LOG_PATH",
    # API
    "MASSIVE_API_KEY",
    "MASSIVE_BASE_URL",
    "DAMODARAN_BASE_URL",
    # Impostazioni
    "CACHE_EXPIRY_HOURS",
    "LOG_LEVEL",
    "assicura_directory",
    # Costanti finanziarie
    "DEFAULT_RISK_FREE_RATE",
    "DEFAULT_MARKET_RETURN",
    "DEFAULT_ERP",
    "DEFAULT_TAX_RATE",
    "DEFAULT_TERMINAL_GROWTH",
    "DEFAULT_STABLE_GROWTH",
    "DEFAULT_HIGH_GROWTH_YEARS",
    "DEFAULT_TRANSITION_YEARS",
    "MARKET_CAP_THRESHOLDS",
    "SECTOR_NAMES",
    "MULTIPLE_NAMES",
    "METODI_VALUTAZIONE",
    "ParametriDCF",
    "ParametriRelativa",
    # Damodaran
    "DamodaranDataset",
    "DAMODARAN_DATASETS",
    "ottieni_url_html",
    "ottieni_url_excel",
    "lista_dataset_disponibili",
]
