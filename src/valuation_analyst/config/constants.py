"""Costanti finanziarie e parametri di default per le valutazioni.

I valori di default sono basati sui dati di Aswath Damodaran
e sulle convenzioni di mercato comunemente utilizzate nella
valutazione d'azienda.
"""

from dataclasses import dataclass, field


# --- Tassi di default (basati su Damodaran) ---

DEFAULT_RISK_FREE_RATE: float = 0.042
"""Tasso risk-free di default (US 10Y Treasury yield)."""

DEFAULT_MARKET_RETURN: float = 0.10
"""Rendimento atteso del mercato azionario (media storica S&P 500)."""

DEFAULT_ERP: float = 0.055
"""Equity Risk Premium maturo (premio per il rischio azionario)."""

DEFAULT_TAX_RATE: float = 0.25
"""Aliquota fiscale marginale di default."""

DEFAULT_TERMINAL_GROWTH: float = 0.025
"""Tasso di crescita nel valore terminale (crescita perpetua)."""

DEFAULT_STABLE_GROWTH: float = 0.025
"""Tasso di crescita nella fase stabile."""

DEFAULT_HIGH_GROWTH_YEARS: int = 5
"""Numero di anni nella fase di alta crescita."""

DEFAULT_TRANSITION_YEARS: int = 5
"""Numero di anni nella fase di transizione verso la crescita stabile."""

DEFAULT_COST_OF_DEBT_SPREAD: float = 0.015
"""Spread di default sul costo del debito rispetto al risk-free rate."""

DEFAULT_DIVIDEND_PAYOUT_RATIO: float = 0.30
"""Payout ratio di default per i dividendi."""


# --- Soglie di capitalizzazione di mercato (in milioni di USD) ---

MARKET_CAP_THRESHOLDS: dict[str, tuple[float, float]] = {
    "micro": (0.0, 300.0),
    "small": (300.0, 2_000.0),
    "mid": (2_000.0, 10_000.0),
    "large": (10_000.0, 200_000.0),
    "mega": (200_000.0, float("inf")),
}
"""Classificazione per capitalizzazione di mercato (in milioni USD).

Chiave: categoria, Valore: (limite_inferiore, limite_superiore).
- micro:  < 300 milioni
- small:  300 milioni - 2 miliardi
- mid:    2 - 10 miliardi
- large:  10 - 200 miliardi
- mega:   > 200 miliardi
"""


# --- Mappatura nomi settori (inglese -> italiano) ---

SECTOR_NAMES: dict[str, str] = {
    "Technology": "Tecnologia",
    "Healthcare": "Sanita'",
    "Financial Services": "Servizi Finanziari",
    "Consumer Cyclical": "Beni di Consumo Ciclici",
    "Consumer Defensive": "Beni di Consumo Difensivi",
    "Industrials": "Industriali",
    "Energy": "Energia",
    "Utilities": "Servizi Pubblici",
    "Real Estate": "Immobiliare",
    "Communication Services": "Servizi di Comunicazione",
    "Basic Materials": "Materiali di Base",
}
"""Mappatura dei nomi dei settori da inglese a italiano."""


# --- Mappatura nomi multipli ---

MULTIPLE_NAMES: dict[str, str] = {
    "pe_ratio": "P/E (Prezzo/Utili)",
    "ev_ebitda": "EV/EBITDA",
    "pb_ratio": "P/BV (Prezzo/Valore Contabile)",
    "ev_sales": "EV/Ricavi",
    "ps_ratio": "P/S (Prezzo/Ricavi)",
    "ev_ebit": "EV/EBIT",
    "dividend_yield": "Rendimento Dividendo",
}
"""Nomi descrittivi dei multipli di mercato in italiano."""


# --- Metodi di valutazione supportati ---

METODI_VALUTAZIONE: list[str] = [
    "DCF_FCFF",
    "DCF_FCFE",
    "DDM",
    "RELATIVE_PE",
    "RELATIVE_EV_EBITDA",
    "RELATIVE_PB",
    "RELATIVE_EV_SALES",
    "OPTION_EQUITY",
    "OPTION_PATENT",
    "APV",
    "EVA",
]
"""Lista dei metodi di valutazione supportati dal sistema."""


@dataclass(frozen=True)
class ParametriDCF:
    """Parametri di default per il modello DCF.

    Raccoglie tutti i parametri necessari per un'analisi
    Discounted Cash Flow con valori sensati di default.
    """

    anni_proiezione: int = DEFAULT_HIGH_GROWTH_YEARS + DEFAULT_TRANSITION_YEARS
    """Numero totale di anni di proiezione esplicita."""

    anni_alta_crescita: int = DEFAULT_HIGH_GROWTH_YEARS
    """Anni nella fase di alta crescita."""

    anni_transizione: int = DEFAULT_TRANSITION_YEARS
    """Anni nella fase di transizione."""

    tasso_crescita_terminale: float = DEFAULT_TERMINAL_GROWTH
    """Tasso di crescita perpetua per il valore terminale."""

    risk_free_rate: float = DEFAULT_RISK_FREE_RATE
    """Tasso risk-free di partenza."""

    erp: float = DEFAULT_ERP
    """Equity Risk Premium."""

    aliquota_fiscale: float = DEFAULT_TAX_RATE
    """Aliquota fiscale marginale."""


@dataclass(frozen=True)
class ParametriRelativa:
    """Parametri di default per la valutazione relativa.

    Definisce le soglie e i criteri per la selezione
    e l'analisi dei comparabili.
    """

    min_comparabili: int = 5
    """Numero minimo di aziende comparabili richieste."""

    max_comparabili: int = 20
    """Numero massimo di aziende comparabili da considerare."""

    scarti_deviazione_standard: float = 2.0
    """Soglia per escludere outlier (numero di deviazioni standard)."""

    multipli_default: list[str] = field(
        default_factory=lambda: ["pe_ratio", "ev_ebitda", "pb_ratio", "ev_sales"]
    )
    """Lista dei multipli da calcolare di default."""
