"""Modulo per il calcolo del premio di controllo.

Il premio di controllo rappresenta il valore aggiuntivo per il controllo
delle decisioni aziendali (management, dividendi, strategia).
"""

from __future__ import annotations

from valuation_analyst.tools.illiquidity_discount import calcola_sconto_illiquidita
from valuation_analyst.utils.validators import valida_non_negativo, valida_positivo


# ---------------------------------------------------------------------------
# Tabella benchmark premi settoriali (dati storici Mergerstat / Bloomberg)
# ---------------------------------------------------------------------------

_PREMI_SETTORE: dict[str, dict] = {
    "Technology": {"medio": 0.30, "mediano": 0.27, "range": (0.15, 0.50)},
    "Healthcare": {"medio": 0.35, "mediano": 0.30, "range": (0.20, 0.55)},
    "Financial": {"medio": 0.22, "mediano": 0.20, "range": (0.10, 0.35)},
    "Consumer": {"medio": 0.28, "mediano": 0.25, "range": (0.15, 0.45)},
    "Industrial": {"medio": 0.25, "mediano": 0.22, "range": (0.12, 0.40)},
    "Energy": {"medio": 0.20, "mediano": 0.18, "range": (0.10, 0.35)},
    "default": {"medio": 0.27, "mediano": 0.25, "range": (0.15, 0.45)},
}

# Benchmark del premio per qualita' management e tipo di controllo
_BENCHMARK_PREMIO: dict[str, dict[str, tuple[float, float]]] = {
    "maggioranza": {
        "scarso": (0.25, 0.40),
        "media": (0.15, 0.25),
        "buono": (0.05, 0.15),
    },
    "minoranza": {
        "scarso": (0.0, 0.0),
        "media": (0.0, 0.0),
        "buono": (0.0, 0.0),
    },
}


# ---------------------------------------------------------------------------
# Premio di controllo
# ---------------------------------------------------------------------------

def calcola_premio_controllo(
    valore_status_quo: float,
    valore_ottimale: float | None = None,
    tipo_controllo: str = "maggioranza",
    settore: str | None = None,
    qualita_management: str = "media",
) -> dict:
    """Calcola il premio di controllo secondo Damodaran.

    Se valore_ottimale fornito:
        Premio = (V_ottimale - V_status_quo) / V_status_quo

    Altrimenti, usa benchmark:
    - Maggioranza, management scarso: 25-40%
    - Maggioranza, management medio: 15-25%
    - Maggioranza, management buono: 5-15%
    - Minoranza: 0% (no premio)

    Parametri
    ---------
    valore_status_quo : float
        Valore dell'azienda nella gestione attuale (deve essere > 0).
    valore_ottimale : float | None, opzionale
        Valore dell'azienda con gestione ottimale. Se fornito, il premio
        viene calcolato analiticamente.
    tipo_controllo : str, opzionale
        Tipo di partecipazione: "maggioranza" o "minoranza".
    settore : str | None, opzionale
        Settore dell'azienda, per affinare il benchmark.
    qualita_management : str, opzionale
        Qualita' del management attuale: "scarso", "media" o "buono".

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - premio: float (percentuale, es. 0.20 per 20%)
        - tipo_controllo: str
        - valore_status_quo: float
        - valore_ottimale: float | None
        - note: list[str]
    """
    valida_positivo(valore_status_quo, "valore_status_quo")

    note: list[str] = []

    # Se il tipo e' minoranza non si applica alcun premio
    if tipo_controllo == "minoranza":
        note.append(
            "Partecipazione di minoranza: il premio di controllo non si applica"
        )
        return {
            "premio": 0.0,
            "tipo_controllo": tipo_controllo,
            "valore_status_quo": valore_status_quo,
            "valore_ottimale": valore_ottimale,
            "note": note,
        }

    # Se il valore ottimale e' fornito, calcolo analitico
    if valore_ottimale is not None:
        valida_positivo(valore_ottimale, "valore_ottimale")
        if valore_ottimale < valore_status_quo:
            note.append(
                "Il valore ottimale e' inferiore allo status quo: "
                "il premio e' negativo (il management attuale e' gia' efficiente)"
            )
        premio = (valore_ottimale - valore_status_quo) / valore_status_quo
        premio = max(0.0, premio)  # Il premio non puo' essere negativo
        note.append(
            f"Premio calcolato analiticamente: "
            f"({valore_ottimale:,.0f} - {valore_status_quo:,.0f}) / "
            f"{valore_status_quo:,.0f} = {premio:.2%}"
        )
        return {
            "premio": premio,
            "tipo_controllo": tipo_controllo,
            "valore_status_quo": valore_status_quo,
            "valore_ottimale": valore_ottimale,
            "note": note,
        }

    # Calcolo da benchmark
    qualita_management = qualita_management.lower()
    if qualita_management not in ("scarso", "media", "buono"):
        qualita_management = "media"
        note.append(
            "Qualita' management non riconosciuta, usato valore 'media'"
        )

    range_premio = _BENCHMARK_PREMIO.get(tipo_controllo, {}).get(
        qualita_management, (0.15, 0.25)
    )
    # Punto medio del range di benchmark
    premio = (range_premio[0] + range_premio[1]) / 2.0

    # Aggiustamento settoriale se disponibile
    if settore and settore in _PREMI_SETTORE:
        dati_settore = _PREMI_SETTORE[settore]
        # Media ponderata tra benchmark base e dato settoriale
        premio = 0.6 * premio + 0.4 * dati_settore["mediano"]
        note.append(
            f"Premio aggiustato con dato settoriale ({settore}): "
            f"mediano transazioni = {dati_settore['mediano']:.1%}"
        )

    note.append(
        f"Premio da benchmark: management {qualita_management}, "
        f"range {range_premio[0]:.0%} - {range_premio[1]:.0%}"
    )

    return {
        "premio": premio,
        "tipo_controllo": tipo_controllo,
        "valore_status_quo": valore_status_quo,
        "valore_ottimale": valore_ottimale,
        "note": note,
    }


# ---------------------------------------------------------------------------
# Premio medio da transazioni M&A
# ---------------------------------------------------------------------------

def premio_da_transazioni(settore: str | None = None) -> dict:
    """Premio medio pagato nelle transazioni M&A per settore.

    Basato su dati storici (Mergerstat, Bloomberg).

    Parametri
    ---------
    settore : str | None, opzionale
        Settore dell'azienda. Se None o non trovato, usa il default.

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - premio_medio: float
        - premio_mediano: float
        - range: tuple[float, float]
        - settore_utilizzato: str
    """
    chiave = settore if settore and settore in _PREMI_SETTORE else "default"
    dati = _PREMI_SETTORE[chiave]

    return {
        "premio_medio": dati["medio"],
        "premio_mediano": dati["mediano"],
        "range": dati["range"],
        "settore_utilizzato": chiave,
    }


# ---------------------------------------------------------------------------
# Sconto di minoranza
# ---------------------------------------------------------------------------

def sconto_minoranza(premio_controllo: float) -> float:
    """Calcola sconto di minoranza dal premio di controllo.

    Formula: Sconto = 1 - 1 / (1 + Premio)

    Esempio: se il premio di controllo e' 25%, lo sconto di minoranza
    e' 1 - 1/1.25 = 20%.

    Parametri
    ---------
    premio_controllo : float
        Premio di controllo espresso come decimale (es. 0.25 per 25%).

    Restituisce
    -----------
    float
        Sconto di minoranza (es. 0.20 per 20%).
    """
    valida_non_negativo(premio_controllo, "premio_controllo")

    if premio_controllo == 0.0:
        return 0.0

    return 1.0 - 1.0 / (1.0 + premio_controllo)


# ---------------------------------------------------------------------------
# Applicazione premio di controllo
# ---------------------------------------------------------------------------

def applica_premio_controllo(
    valore_base: float,
    premio: float,
) -> dict:
    """Applica premio di controllo al valore base.

    Parametri
    ---------
    valore_base : float
        Valore dell'azienda prima del premio (deve essere > 0).
    premio : float
        Premio di controllo da applicare (es. 0.20 per 20%).

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - valore_base: float
        - premio_applicato: float (importo assoluto del premio)
        - valore_con_premio: float
        - premio_percentuale: float
    """
    valida_positivo(valore_base, "valore_base")
    valida_non_negativo(premio, "premio")

    premio_applicato = valore_base * premio
    valore_con_premio = valore_base + premio_applicato

    return {
        "valore_base": valore_base,
        "premio_applicato": premio_applicato,
        "valore_con_premio": valore_con_premio,
        "premio_percentuale": premio,
    }


# ---------------------------------------------------------------------------
# Valutazione privata completa
# ---------------------------------------------------------------------------

def valutazione_privata_completa(
    valore_quotata: float,
    ricavi: float,
    margine_ebitda: float,
    tipo_partecipazione: str = "maggioranza",
    qualita_management: str = "media",
) -> dict:
    """Valutazione privata completa: parte dal valore 'come se quotata',
    applica premio controllo (se maggioranza), poi sconto illiquidita'.

    Flusso logico:
    1. Valore come se quotata
    2. + Premio di controllo (solo per maggioranza)
    3. - Sconto di illiquidita' (sempre, per societa' private)
    = Valore finale partecipazione privata

    Parametri
    ---------
    valore_quotata : float
        Valore dell'azienda stimato come se fosse quotata (deve essere > 0).
    ricavi : float
        Ricavi totali dell'azienda in euro.
    margine_ebitda : float
        Margine EBITDA espresso come decimale (es. 0.15 per 15%).
    tipo_partecipazione : str, opzionale
        "maggioranza" o "minoranza".
    qualita_management : str, opzionale
        Qualita' del management: "scarso", "media" o "buono".

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - valore_quotata: float
        - premio_controllo_pct: float
        - sconto_illiquidita_pct: float
        - valore_dopo_controllo: float
        - valore_finale: float
        - dettagli: dict (risultati intermedi completi)
    """
    valida_positivo(valore_quotata, "valore_quotata")

    # Passo 1: Calcolo premio di controllo
    risultato_premio = calcola_premio_controllo(
        valore_status_quo=valore_quotata,
        tipo_controllo=tipo_partecipazione,
        qualita_management=qualita_management,
    )
    premio_pct = risultato_premio["premio"]

    # Passo 2: Applicazione premio di controllo
    valore_dopo_controllo = valore_quotata * (1.0 + premio_pct)

    # Passo 3: Calcolo sconto di illiquidita'
    risultato_sconto = calcola_sconto_illiquidita(
        ricavi=ricavi,
        margine_ebitda=margine_ebitda,
    )
    sconto_pct = risultato_sconto["sconto"]

    # Passo 4: Applicazione sconto di illiquidita' al valore post-premio
    valore_finale = valore_dopo_controllo * (1.0 - sconto_pct)

    return {
        "valore_quotata": valore_quotata,
        "premio_controllo_pct": premio_pct,
        "sconto_illiquidita_pct": sconto_pct,
        "valore_dopo_controllo": valore_dopo_controllo,
        "valore_finale": valore_finale,
        "dettagli": {
            "premio_controllo": risultato_premio,
            "sconto_illiquidita": risultato_sconto,
        },
    }
