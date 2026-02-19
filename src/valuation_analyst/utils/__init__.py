"""Pacchetto di utilita' per valuation_analyst.

Esporta le funzioni principali dei moduli di utilita' per un
accesso comodo tramite ``from valuation_analyst.utils import ...``.
"""

from __future__ import annotations

# --- Funzioni di matematica finanziaria ---
from valuation_analyst.utils.math_helpers import (
    cagr,
    fv,
    gordon_growth,
    irr,
    levered_beta,
    npv,
    pv,
    unlevered_beta,
    wacc_formula,
)

# --- Funzioni di formattazione ---
from valuation_analyst.utils.formatting import (
    formatta_miliardi,
    formatta_milioni,
    formatta_multiplo,
    formatta_numero,
    formatta_percentuale,
    formatta_valuta,
    tabella_markdown,
)

# --- Funzioni di validazione ---
from valuation_analyst.utils.validators import (
    valida_anni,
    valida_non_negativo,
    valida_percentuale,
    valida_peso,
    valida_positivo,
    valida_tasso,
    valida_ticker,
)

# --- Logging dei prompt ---
from valuation_analyst.utils.logging_utils import (
    leggi_log,
    log_prompt,
)

# --- Parser Excel Damodaran ---
from valuation_analyst.utils.excel_parser import (
    cerca_settore,
    estrai_beta_settore,
    estrai_erp_paese,
    parse_damodaran_excel,
)

__all__ = [
    # math_helpers
    "npv",
    "irr",
    "pv",
    "fv",
    "cagr",
    "gordon_growth",
    "wacc_formula",
    "levered_beta",
    "unlevered_beta",
    # formatting
    "formatta_valuta",
    "formatta_percentuale",
    "formatta_numero",
    "formatta_milioni",
    "formatta_miliardi",
    "formatta_multiplo",
    "tabella_markdown",
    # validators
    "valida_ticker",
    "valida_tasso",
    "valida_positivo",
    "valida_non_negativo",
    "valida_percentuale",
    "valida_anni",
    "valida_peso",
    # logging_utils
    "log_prompt",
    "leggi_log",
    # excel_parser
    "parse_damodaran_excel",
    "cerca_settore",
    "estrai_beta_settore",
    "estrai_erp_paese",
]
