"""Modulo per il calcolo dell'Equity Risk Premium e Country Risk Premium.

Segue la metodologia Damodaran per la stima dei premi per il rischio:
- ERP base del mercato maturo (tipicamente USA)
- Country Risk Premium basato su rating sovrano e default spread
- Costo del debito sintetico da interest coverage ratio

Riferimento: Aswath Damodaran, "Equity Risk Premiums (ERP):
Determinants, Estimation, and Implications".
"""

from __future__ import annotations

import logging
from typing import Any

from valuation_analyst.config.constants import DEFAULT_ERP, DEFAULT_RISK_FREE_RATE
from valuation_analyst.utils.validators import valida_non_negativo, valida_tasso

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Tabella dei default spread per rating creditizio
# ---------------------------------------------------------------------------

RATING_DEFAULT_SPREADS: dict[str, float] = {
    "AAA": 0.0075,
    "AA+": 0.0085,
    "AA": 0.010,
    "AA-": 0.011,
    "A+": 0.0115,
    "A": 0.0125,
    "A-": 0.0140,
    "BBB+": 0.0165,
    "BBB": 0.020,
    "BBB-": 0.025,
    "BB+": 0.0275,
    "BB": 0.030,
    "BB-": 0.035,
    "B+": 0.0375,
    "B": 0.040,
    "B-": 0.050,
    "CCC+": 0.060,
    "CCC": 0.080,
    "CCC-": 0.090,
    "CC": 0.100,
    "C": 0.120,
    "D": 0.150,
}
"""Tabella dei default spread associati a ciascun rating creditizio.

I valori sono espressi come decimali (es. 0.02 = 200 basis points)
e sono basati sulle stime medie di Damodaran per i corporate bonds.
"""


# ---------------------------------------------------------------------------
# Tabella interest coverage -> rating implicito
# ---------------------------------------------------------------------------

_COVERAGE_TO_RATING: list[tuple[float, str]] = [
    # (soglia minima coverage, rating implicito)
    (8.50, "AAA"),
    (6.50, "AA"),
    (5.50, "A+"),
    (4.25, "A"),
    (3.00, "A-"),
    (2.50, "BBB"),
    (2.25, "BB+"),
    (2.00, "BB"),
    (1.75, "BB-"),
    (1.50, "B+"),
    (1.25, "B"),
    (0.80, "B-"),
    (0.65, "CCC"),
    (0.20, "CC"),
    (0.00, "C"),
]
"""Tabella di conversione interest coverage ratio -> rating implicito.

Basata sulla mappatura di Damodaran per grandi imprese. Per le piccole
imprese i range sono leggermente diversi (piu' restrittivi), ma questa
tabella fornisce una buona approssimazione generale.
"""


# ---------------------------------------------------------------------------
# Equity Risk Premium per paese
# ---------------------------------------------------------------------------

def get_equity_risk_premium(paese: str = "US") -> dict[str, Any]:
    """Ottiene l'Equity Risk Premium per un dato paese.

    Per gli USA restituisce l'ERP base del mercato maturo.
    Per gli altri paesi aggiunge il Country Risk Premium.

    Tenta di caricare i dati dal dataset Damodaran; in caso di
    errore, ricade sui valori di default.

    Parametri
    ---------
    paese : str, opzionale
        Nome o codice del paese (default: ``"US"``).
        Accetta sia codici ISO (``"US"``, ``"IT"``) sia nomi
        completi (``"United States"``, ``"Italy"``).

    Restituisce
    -----------
    dict[str, Any]
        Dizionario con le chiavi:
        - ``erp_base`` : ERP del mercato maturo (senza CRP)
        - ``country_risk_premium`` : premio per il rischio paese
        - ``erp_totale`` : ERP base + CRP
        - ``default_spread`` : default spread del debito sovrano
        - ``fonte`` : origine dei dati (``"Damodaran"`` o ``"default"``)

    Note
    ----
    Per i paesi USA, ``country_risk_premium`` e ``default_spread``
    sono sempre 0.
    """
    # Importazione ritardata per evitare dipendenze circolari
    from valuation_analyst.tools.damodaran_data import get_erp_paese

    # Normalizza il codice paese a nome completo per il lookup
    paese_normalizzato = _normalizza_paese(paese)

    # Caso USA: ERP base senza CRP
    if paese_normalizzato.upper() in ("US", "USA", "UNITED STATES"):
        # Prova comunque a ottenere l'ERP da Damodaran
        try:
            dati = get_erp_paese("United States")
            erp_totale = dati.get("equity_risk_premium")
            if erp_totale is not None:
                return {
                    "erp_base": float(erp_totale),
                    "country_risk_premium": 0.0,
                    "erp_totale": float(erp_totale),
                    "default_spread": 0.0,
                    "fonte": "Damodaran",
                }
        except (ValueError, KeyError, ConnectionError, RuntimeError) as e:
            logger.warning(
                "Impossibile recuperare l'ERP USA da Damodaran: %s. "
                "Utilizzo valore di default.",
                e,
            )

        # Fallback su default
        return {
            "erp_base": DEFAULT_ERP,
            "country_risk_premium": 0.0,
            "erp_totale": DEFAULT_ERP,
            "default_spread": 0.0,
            "fonte": "default",
        }

    # Caso altri paesi: carica da Damodaran
    try:
        dati = get_erp_paese(paese_normalizzato)
        erp_totale = dati.get("equity_risk_premium")
        crp = dati.get("country_risk_premium", 0.0) or 0.0
        default_spread = dati.get("default_spread", 0.0) or 0.0

        if erp_totale is not None:
            erp_base = float(erp_totale) - float(crp)
        else:
            erp_base = DEFAULT_ERP

        return {
            "erp_base": erp_base,
            "country_risk_premium": float(crp),
            "erp_totale": erp_base + float(crp),
            "default_spread": float(default_spread),
            "fonte": "Damodaran",
        }

    except (ValueError, KeyError, ConnectionError, RuntimeError) as e:
        logger.warning(
            "Impossibile recuperare l'ERP per il paese '%s' da Damodaran: %s. "
            "Utilizzo valori di default.",
            paese, e,
        )

        return {
            "erp_base": DEFAULT_ERP,
            "country_risk_premium": 0.0,
            "erp_totale": DEFAULT_ERP,
            "default_spread": 0.0,
            "fonte": "default",
        }


# ---------------------------------------------------------------------------
# Country Risk Premium
# ---------------------------------------------------------------------------

def calcola_country_risk_premium(
    rating_sovrano: str | None = None,
    default_spread: float | None = None,
    moltiplicatore_equity: float = 1.5,
) -> float:
    """Calcola il Country Risk Premium da rating sovrano o default spread.

    Il CRP viene calcolato come:
        CRP = Default Spread * Moltiplicatore Equity

    Il moltiplicatore equity (tipicamente 1.5) riflette il fatto che
    i mercati azionari sono piu' volatili dei mercati obbligazionari.

    Almeno uno tra ``rating_sovrano`` e ``default_spread`` deve essere
    fornito.

    Parametri
    ---------
    rating_sovrano : str | None, opzionale
        Rating creditizio sovrano (es. ``"BBB"``, ``"A+"``, ``"BB-"``).
        Se fornito, il default spread viene ricavato dalla tabella.
    default_spread : float | None, opzionale
        Default spread del debito sovrano. Se fornito insieme al
        rating, prevale sul valore ricavato dalla tabella.
    moltiplicatore_equity : float, opzionale
        Moltiplicatore per convertire il default spread obbligazionario
        in premio per il rischio equity (default: 1.5).

    Restituisce
    -----------
    float
        Country Risk Premium come valore decimale.

    Solleva
    -------
    ValueError
        Se ne' ``rating_sovrano`` ne' ``default_spread`` sono forniti,
        oppure se il rating non e' riconosciuto.
    """
    if rating_sovrano is None and default_spread is None:
        raise ValueError(
            "Specificare almeno uno tra 'rating_sovrano' e 'default_spread' "
            "per calcolare il Country Risk Premium."
        )

    if moltiplicatore_equity <= 0:
        raise ValueError(
            f"Il moltiplicatore equity deve essere positivo. "
            f"Ricevuto: {moltiplicatore_equity}."
        )

    # Determina il default spread
    if default_spread is not None:
        ds = valida_non_negativo(default_spread, "default_spread")
    elif rating_sovrano is not None:
        ds = spread_da_rating(rating_sovrano)
    else:
        # Non dovrebbe mai arrivarci dato il check iniziale
        ds = 0.0

    crp = ds * moltiplicatore_equity

    logger.debug(
        "CRP calcolato: %.4f (default_spread=%.4f, moltiplicatore=%.2f, "
        "rating=%s)",
        crp, ds, moltiplicatore_equity,
        rating_sovrano if rating_sovrano else "N/D",
    )

    return crp


# ---------------------------------------------------------------------------
# Spread da rating creditizio
# ---------------------------------------------------------------------------

def spread_da_rating(rating: str) -> float:
    """Restituisce il default spread associato a un rating creditizio.

    Esegue il lookup nella tabella ``RATING_DEFAULT_SPREADS``.
    La ricerca e' case-insensitive.

    Parametri
    ---------
    rating : str
        Rating creditizio (es. ``"BBB"``, ``"A+"``, ``"BB-"``).

    Restituisce
    -----------
    float
        Default spread come valore decimale (es. 0.02 per 200 bps).

    Solleva
    -------
    ValueError
        Se il rating non e' riconosciuto nella tabella.
    """
    if not isinstance(rating, str) or not rating.strip():
        raise ValueError(
            "Il rating deve essere una stringa non vuota."
        )

    rating_normalizzato = rating.strip().upper()

    # Lookup diretto
    if rating_normalizzato in RATING_DEFAULT_SPREADS:
        return RATING_DEFAULT_SPREADS[rating_normalizzato]

    # Tentativo di match parziale: prova senza segno + o -
    rating_base = rating_normalizzato.rstrip("+-")
    if rating_base in RATING_DEFAULT_SPREADS:
        logger.info(
            "Rating '%s' non trovato esattamente; utilizzo il valore "
            "del rating base '%s'.",
            rating_normalizzato, rating_base,
        )
        return RATING_DEFAULT_SPREADS[rating_base]

    # Rating non trovato
    rating_disponibili = ", ".join(sorted(RATING_DEFAULT_SPREADS.keys()))
    raise ValueError(
        f"Rating '{rating}' non riconosciuto. "
        f"Rating disponibili: {rating_disponibili}."
    )


# ---------------------------------------------------------------------------
# Costo del debito sintetico da interest coverage
# ---------------------------------------------------------------------------

def costo_debito_sintetico(
    interest_coverage: float,
    risk_free_rate: float,
) -> dict[str, Any]:
    """Stima il costo del debito sintetico basato sull'interest coverage ratio.

    Mappa l'interest coverage ratio a un rating implicito tramite la
    tabella di Damodaran, quindi somma il default spread al tasso
    risk-free per ottenere il costo del debito pre-tax.

    Parametri
    ---------
    interest_coverage : float
        Rapporto di copertura degli interessi (EBIT / Interessi Passivi).
        Puo' essere negativo se l'azienda ha un EBIT negativo.
    risk_free_rate : float
        Tasso risk-free da utilizzare come base (es. 0.042).

    Restituisce
    -----------
    dict[str, Any]
        Dizionario con le chiavi:
        - ``rating_implicito`` : rating creditizio stimato
        - ``default_spread`` : spread associato al rating
        - ``costo_debito`` : costo del debito pre-tax (Rf + spread)
        - ``interest_coverage`` : valore di input

    Solleva
    -------
    ValueError
        Se il risk-free rate non supera la validazione.
    """
    risk_free_rate = valida_tasso(risk_free_rate, "risk-free rate")

    if not isinstance(interest_coverage, (int, float)):
        raise ValueError(
            "L'interest coverage deve essere un numero "
            f"(ricevuto: {type(interest_coverage).__name__})."
        )
    interest_coverage = float(interest_coverage)

    # Mappa l'interest coverage al rating implicito
    rating_implicito = "D"  # default per coverage molto basso o negativo
    for soglia, rating in _COVERAGE_TO_RATING:
        if interest_coverage >= soglia:
            rating_implicito = rating
            break

    # Caso speciale: coverage negativo -> rating D
    if interest_coverage < 0:
        rating_implicito = "D"

    # Ottieni il default spread per il rating implicito
    ds = RATING_DEFAULT_SPREADS.get(rating_implicito, 0.15)

    # Costo del debito pre-tax = Rf + default spread
    costo_debito = risk_free_rate + ds

    logger.info(
        "Costo debito sintetico: rating=%s, spread=%.4f, "
        "Kd=%.4f (coverage=%.2f, Rf=%.4f)",
        rating_implicito, ds, costo_debito,
        interest_coverage, risk_free_rate,
    )

    return {
        "rating_implicito": rating_implicito,
        "default_spread": ds,
        "costo_debito": costo_debito,
        "interest_coverage": interest_coverage,
    }


# ---------------------------------------------------------------------------
# Utilita' interne
# ---------------------------------------------------------------------------

# Mappatura codici ISO comuni -> nomi completi per il lookup Damodaran
_PAESE_ISO_MAP: dict[str, str] = {
    "US": "United States",
    "USA": "United States",
    "IT": "Italy",
    "DE": "Germany",
    "FR": "France",
    "GB": "United Kingdom",
    "UK": "United Kingdom",
    "ES": "Spain",
    "JP": "Japan",
    "CN": "China",
    "BR": "Brazil",
    "IN": "India",
    "RU": "Russia",
    "CA": "Canada",
    "AU": "Australia",
    "CH": "Switzerland",
    "KR": "South Korea",
    "MX": "Mexico",
    "NL": "Netherlands",
    "SE": "Sweden",
    "BE": "Belgium",
    "AT": "Austria",
    "PT": "Portugal",
    "GR": "Greece",
    "TR": "Turkey",
    "PL": "Poland",
    "NO": "Norway",
    "DK": "Denmark",
    "FI": "Finland",
    "IE": "Ireland",
    "SG": "Singapore",
    "HK": "Hong Kong",
    "ZA": "South Africa",
    "AR": "Argentina",
    "CL": "Chile",
    "CO": "Colombia",
    "PE": "Peru",
    "IL": "Israel",
    "AE": "United Arab Emirates",
    "SA": "Saudi Arabia",
}


def _normalizza_paese(paese: str) -> str:
    """Normalizza un codice/nome paese al nome completo per Damodaran.

    Se il codice ISO viene riconosciuto, restituisce il nome completo;
    altrimenti restituisce la stringa originale con la prima lettera
    maiuscola.

    Parametri
    ---------
    paese : str
        Codice ISO o nome del paese.

    Restituisce
    -----------
    str
        Nome del paese normalizzato.
    """
    paese_upper = paese.strip().upper()
    if paese_upper in _PAESE_ISO_MAP:
        return _PAESE_ISO_MAP[paese_upper]
    # Se e' gia' un nome completo, restituiscilo con capitalizzazione corretta
    return paese.strip().title()
