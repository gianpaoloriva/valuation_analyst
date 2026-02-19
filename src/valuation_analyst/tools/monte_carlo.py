"""Modulo per simulazioni Monte Carlo applicate alla valutazione.

Genera distribuzioni di valori per quantificare l'incertezza
nella stima del valore aziendale.
"""
from __future__ import annotations

from typing import Any, Callable

import numpy as np

from valuation_analyst.utils.formatting import formatta_valuta, formatta_percentuale


# ---------------------------------------------------------------------------
# Definizione distribuzioni
# ---------------------------------------------------------------------------

def definisci_distribuzione(
    tipo: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """Definisce una distribuzione per un parametro.

    Tipi supportati e parametri richiesti:
    - ``normale``: media, deviazione_standard
    - ``triangolare``: minimo, moda, massimo
    - ``uniforme``: minimo, massimo
    - ``lognormale``: media_log, sigma_log

    Args:
        tipo: tipo di distribuzione (normale, triangolare, uniforme, lognormale).
        **kwargs: parametri specifici della distribuzione.

    Returns:
        Dizionario con chiavi ``tipo``, ``parametri`` e ``descrizione``.

    Raises:
        ValueError: se il tipo non e' supportato o mancano parametri.
    """
    tipi_validi = {"normale", "triangolare", "uniforme", "lognormale"}
    tipo_lower = tipo.lower().strip()

    if tipo_lower not in tipi_validi:
        raise ValueError(
            f"Tipo distribuzione '{tipo}' non supportato. "
            f"Tipi validi: {sorted(tipi_validi)}"
        )

    # Validazione parametri per ogni tipo
    parametri_richiesti: dict[str, list[str]] = {
        "normale": ["media", "deviazione_standard"],
        "triangolare": ["minimo", "moda", "massimo"],
        "uniforme": ["minimo", "massimo"],
        "lognormale": ["media_log", "sigma_log"],
    }

    mancanti = [p for p in parametri_richiesti[tipo_lower] if p not in kwargs]
    if mancanti:
        raise ValueError(
            f"Parametri mancanti per distribuzione '{tipo_lower}': {mancanti}"
        )

    # Validazione specifica
    if tipo_lower == "triangolare":
        if not (kwargs["minimo"] <= kwargs["moda"] <= kwargs["massimo"]):
            raise ValueError(
                "Per la distribuzione triangolare deve valere: minimo <= moda <= massimo"
            )
    if tipo_lower == "uniforme":
        if kwargs["minimo"] >= kwargs["massimo"]:
            raise ValueError(
                "Per la distribuzione uniforme deve valere: minimo < massimo"
            )
    if tipo_lower == "normale" and kwargs["deviazione_standard"] <= 0:
        raise ValueError("La deviazione standard deve essere positiva.")
    if tipo_lower == "lognormale" and kwargs["sigma_log"] <= 0:
        raise ValueError("Il parametro sigma_log deve essere positivo.")

    # Costruzione descrizione leggibile
    descrizioni: dict[str, str] = {
        "normale": (
            f"Normale(media={kwargs.get('media')}, "
            f"std={kwargs.get('deviazione_standard')})"
        ),
        "triangolare": (
            f"Triangolare(min={kwargs.get('minimo')}, "
            f"moda={kwargs.get('moda')}, max={kwargs.get('massimo')})"
        ),
        "uniforme": (
            f"Uniforme(min={kwargs.get('minimo')}, max={kwargs.get('massimo')})"
        ),
        "lognormale": (
            f"LogNormale(mu={kwargs.get('media_log')}, "
            f"sigma={kwargs.get('sigma_log')})"
        ),
    }

    risultato: dict[str, Any] = {"tipo": tipo_lower}
    # Aggiungi tutti i parametri forniti
    for chiave, valore in kwargs.items():
        risultato[chiave] = valore
    risultato["descrizione"] = descrizioni[tipo_lower]

    return risultato


# ---------------------------------------------------------------------------
# Generazione campioni con correlazione
# ---------------------------------------------------------------------------

def _genera_campioni_correlati(
    campioni: dict[str, np.ndarray],
    correlazioni: dict[tuple[str, str], float],
) -> dict[str, np.ndarray]:
    """Applica correlazioni ai campioni tramite decomposizione di Cholesky.

    Trasforma campioni indipendenti in campioni correlati mantenendo
    le distribuzioni marginali (approssimazione basata su ranghi).

    Args:
        campioni: dizionario {nome_parametro: array_campioni}.
        correlazioni: dizionario {(param1, param2): coefficiente_rho}.

    Returns:
        Dizionario con campioni trasformati per riflettere le correlazioni.
    """
    nomi = list(campioni.keys())
    n_params = len(nomi)
    n_sim = len(next(iter(campioni.values())))

    # Costruisci la matrice di correlazione
    matrice_corr = np.eye(n_params)
    indice = {nome: i for i, nome in enumerate(nomi)}

    for (p1, p2), rho in correlazioni.items():
        if p1 in indice and p2 in indice:
            i, j = indice[p1], indice[p2]
            matrice_corr[i, j] = rho
            matrice_corr[j, i] = rho

    # Decomposizione di Cholesky
    try:
        L = np.linalg.cholesky(matrice_corr)
    except np.linalg.LinAlgError:
        # Se la matrice non e' definita positiva, restituisci campioni invariati
        return campioni

    # Converti i campioni in ranghi normalizzati
    from scipy import stats  # type: ignore[import-untyped]

    Z = np.zeros((n_params, n_sim))
    ranghi_originali: dict[str, np.ndarray] = {}

    for i, nome in enumerate(nomi):
        # Salva l'ordinamento originale per ricostruire
        ranghi_originali[nome] = np.argsort(np.argsort(campioni[nome]))
        # Converti in variabile normale standard tramite ranghi
        ranghi_norm = (ranghi_originali[nome] + 0.5) / n_sim
        Z[i] = stats.norm.ppf(ranghi_norm)

    # Applica correlazione
    Z_correlato = L @ Z

    # Ricostruisci i campioni correlati mantenendo la distribuzione originale
    risultato: dict[str, np.ndarray] = {}
    for i, nome in enumerate(nomi):
        # Ordina i campioni originali
        ordinati = np.sort(campioni[nome])
        # Ricava i nuovi ranghi dai campioni correlati
        nuovi_ranghi = np.argsort(np.argsort(Z_correlato[i]))
        risultato[nome] = ordinati[nuovi_ranghi]

    return risultato


# ---------------------------------------------------------------------------
# Simulazione Monte Carlo
# ---------------------------------------------------------------------------

def simulazione_monte_carlo(
    funzione_valutazione: Callable[..., float],
    distribuzioni: dict[str, dict[str, Any]],
    num_simulazioni: int = 10_000,
    seed: int | None = 42,
    correlazioni: dict[tuple[str, str], float] | None = None,
) -> dict[str, Any]:
    """Esegue simulazione Monte Carlo.

    Genera campioni casuali per ogni parametro secondo la distribuzione
    specificata, applica eventuali correlazioni e calcola il valore
    per ogni iterazione tramite la funzione di valutazione.

    Args:
        funzione_valutazione: f(**params) -> valore per azione.
        distribuzioni: {nome_param: {tipo, ...kwargs distribuzione}}.
        num_simulazioni: numero iterazioni (default 10.000).
        seed: seed per riproducibilita' (None per casuale).
        correlazioni: {(param1, param2): rho} per correlazioni tra parametri.

    Returns:
        Dizionario con:
        - valori: np.ndarray di tutti i risultati validi
        - media, mediana, deviazione_standard: statistiche descrittive
        - percentili: dict con chiavi 5, 10, 25, 50, 75, 90, 95
        - minimo, massimo: estremi della distribuzione
        - intervallo_confidenza_90: tupla (P5, P95)
        - intervallo_confidenza_50: tupla (P25, P75)
        - probabilita_negativo: P(valore < 0)
        - num_simulazioni: numero di simulazioni valide
        - num_errori: numero di simulazioni fallite
        - distribuzioni_usate: dizionario delle distribuzioni
    """
    rng = np.random.default_rng(seed)

    # Generazione campioni per ogni parametro
    campioni: dict[str, np.ndarray] = {}
    for nome, dist in distribuzioni.items():
        tipo = dist["tipo"]
        if tipo == "normale":
            campioni[nome] = rng.normal(
                dist["media"], dist["deviazione_standard"], num_simulazioni
            )
        elif tipo == "triangolare":
            campioni[nome] = rng.triangular(
                dist["minimo"], dist["moda"], dist["massimo"], num_simulazioni
            )
        elif tipo == "uniforme":
            campioni[nome] = rng.uniform(
                dist["minimo"], dist["massimo"], num_simulazioni
            )
        elif tipo == "lognormale":
            campioni[nome] = rng.lognormal(
                dist["media_log"], dist["sigma_log"], num_simulazioni
            )
        else:
            raise ValueError(f"Tipo distribuzione non supportato: {tipo}")

    # Applicazione correlazioni (se specificate)
    if correlazioni:
        campioni = _genera_campioni_correlati(campioni, correlazioni)

    # Esecuzione simulazioni
    valori = np.zeros(num_simulazioni)
    errori = 0
    for i in range(num_simulazioni):
        params = {nome: float(campioni[nome][i]) for nome in distribuzioni}
        try:
            valori[i] = funzione_valutazione(**params)
        except (ValueError, ZeroDivisionError, TypeError):
            valori[i] = float("nan")
            errori += 1

    # Rimozione valori non validi (NaN e infiniti)
    valori_validi = valori[np.isfinite(valori)]

    if len(valori_validi) == 0:
        # Nessuna simulazione valida
        return {
            "valori": valori_validi,
            "media": float("nan"),
            "mediana": float("nan"),
            "deviazione_standard": float("nan"),
            "percentili": {p: float("nan") for p in [5, 10, 25, 50, 75, 90, 95]},
            "minimo": float("nan"),
            "massimo": float("nan"),
            "intervallo_confidenza_90": (float("nan"), float("nan")),
            "intervallo_confidenza_50": (float("nan"), float("nan")),
            "probabilita_negativo": float("nan"),
            "num_simulazioni": 0,
            "num_errori": errori,
            "distribuzioni_usate": distribuzioni,
        }

    # Calcolo statistiche
    percentili = {
        p: float(np.percentile(valori_validi, p))
        for p in [5, 10, 25, 50, 75, 90, 95]
    }

    return {
        "valori": valori_validi,
        "media": float(np.mean(valori_validi)),
        "mediana": float(np.median(valori_validi)),
        "deviazione_standard": float(np.std(valori_validi)),
        "percentili": percentili,
        "minimo": float(np.min(valori_validi)),
        "massimo": float(np.max(valori_validi)),
        "intervallo_confidenza_90": (percentili[5], percentili[95]),
        "intervallo_confidenza_50": (percentili[25], percentili[75]),
        "probabilita_negativo": float(np.mean(valori_validi < 0)),
        "num_simulazioni": len(valori_validi),
        "num_errori": errori,
        "distribuzioni_usate": distribuzioni,
    }


# ---------------------------------------------------------------------------
# Monte Carlo specifico per DCF
# ---------------------------------------------------------------------------

def monte_carlo_dcf(
    fcff_base: float,
    debito_netto: float,
    shares_outstanding: float,
    distribuzioni: dict[str, dict[str, Any]] | None = None,
    num_simulazioni: int = 10_000,
    seed: int | None = 42,
) -> dict[str, Any]:
    """Monte Carlo specifico per valutazione DCF.

    Se le distribuzioni non sono fornite, usa i seguenti default:
    - wacc: Normale(media=0.09, std=0.01)
    - crescita_alta: Normale(media=0.10, std=0.03)
    - crescita_stabile: Triangolare(min=0.015, moda=0.025, max=0.035)

    Il modello proietta 10 anni di flussi di cassa con crescita che
    converge dalla fase alta alla fase stabile, poi calcola il terminal
    value con Gordon Growth Model.

    Args:
        fcff_base: flusso di cassa libero per l'impresa al tempo 0.
        debito_netto: debito netto da sottrarre all'enterprise value.
        shares_outstanding: numero di azioni in circolazione.
        distribuzioni: distribuzioni personalizzate per i parametri.
        num_simulazioni: numero di iterazioni (default 10.000).
        seed: seed per riproducibilita'.

    Returns:
        Dizionario con statistiche complete della simulazione Monte Carlo.
    """
    if distribuzioni is None:
        distribuzioni = {
            "wacc": {
                "tipo": "normale",
                "media": 0.09,
                "deviazione_standard": 0.01,
            },
            "crescita_alta": {
                "tipo": "normale",
                "media": 0.10,
                "deviazione_standard": 0.03,
            },
            "crescita_stabile": {
                "tipo": "triangolare",
                "minimo": 0.015,
                "moda": 0.025,
                "massimo": 0.035,
            },
        }

    def valuta(wacc: float, crescita_alta: float, crescita_stabile: float, **kwargs: Any) -> float:
        """DCF semplificato con convergenza della crescita."""
        if wacc <= crescita_stabile or wacc <= 0:
            return float("nan")
        fcff = fcff_base
        valore = 0.0
        for anno in range(1, 11):
            # Prima meta': crescita alta; seconda meta': convergenza a stabile
            if anno <= 5:
                g = crescita_alta
            else:
                g = crescita_stabile + (crescita_alta - crescita_stabile) * max(
                    0.0, (10 - anno) / 5
                )
            fcff = fcff * (1 + g)
            valore += fcff / (1 + wacc) ** anno
        # Terminal value (Gordon Growth Model)
        tv = fcff * (1 + crescita_stabile) / (wacc - crescita_stabile)
        valore += tv / (1 + wacc) ** 10
        # Da enterprise value a equity per azione
        equity = valore - debito_netto
        return equity / shares_outstanding if shares_outstanding > 0 else 0.0

    return simulazione_monte_carlo(valuta, distribuzioni, num_simulazioni, seed)


# ---------------------------------------------------------------------------
# Formattazione risultati
# ---------------------------------------------------------------------------

def formatta_monte_carlo(risultato: dict[str, Any], valuta: str = "USD") -> str:
    """Formatta i risultati Monte Carlo in markdown.

    Genera una tabella con le statistiche principali e gli intervalli
    di confidenza.

    Args:
        risultato: dizionario restituito da simulazione_monte_carlo.
        valuta: codice ISO della valuta per la formattazione.

    Returns:
        Stringa markdown con il riepilogo della simulazione.
    """
    lines = [
        "## Risultati Simulazione Monte Carlo",
        f"**Simulazioni eseguite:** {risultato['num_simulazioni']:,}",
        "",
        "| Statistica | Valore |",
        "|-----------|--------|",
        f"| Media | {formatta_valuta(risultato['media'], valuta)} |",
        f"| Mediana | {formatta_valuta(risultato['mediana'], valuta)} |",
        f"| Dev. Standard | {formatta_valuta(risultato['deviazione_standard'], valuta)} |",
        f"| Minimo | {formatta_valuta(risultato['minimo'], valuta)} |",
        f"| 5° Percentile | {formatta_valuta(risultato['percentili'][5], valuta)} |",
        f"| 25° Percentile | {formatta_valuta(risultato['percentili'][25], valuta)} |",
        f"| 75° Percentile | {formatta_valuta(risultato['percentili'][75], valuta)} |",
        f"| 95° Percentile | {formatta_valuta(risultato['percentili'][95], valuta)} |",
        f"| Massimo | {formatta_valuta(risultato['massimo'], valuta)} |",
        "",
        (
            f"**IC 90%:** "
            f"{formatta_valuta(risultato['intervallo_confidenza_90'][0], valuta)} - "
            f"{formatta_valuta(risultato['intervallo_confidenza_90'][1], valuta)}"
        ),
        (
            f"**IC 50%:** "
            f"{formatta_valuta(risultato['intervallo_confidenza_50'][0], valuta)} - "
            f"{formatta_valuta(risultato['intervallo_confidenza_50'][1], valuta)}"
        ),
    ]

    if risultato.get("probabilita_negativo", 0) > 0:
        lines.append(
            f"**Prob. valore negativo:** "
            f"{formatta_percentuale(risultato['probabilita_negativo'])}"
        )

    if risultato.get("num_errori", 0) > 0:
        lines.append(
            f"**Simulazioni con errore:** {risultato['num_errori']:,}"
        )

    return "\n".join(lines)


def istogramma_ascii(
    valori: np.ndarray,
    bins: int = 20,
    larghezza: int = 50,
) -> str:
    """Genera un istogramma ASCII della distribuzione.

    Utile per una visualizzazione rapida in terminale o in report
    testuali della distribuzione dei valori simulati.

    Args:
        valori: array numpy con i valori da rappresentare.
        bins: numero di intervalli dell'istogramma.
        larghezza: larghezza massima delle barre in caratteri.

    Returns:
        Stringa con l'istogramma formattato.
    """
    conteggi, bordi = np.histogram(valori, bins=bins)
    max_conteggio = max(conteggi) if max(conteggi) > 0 else 1

    linee: list[str] = []
    for i, conteggio in enumerate(conteggi):
        num_barre = int(conteggio / max_conteggio * larghezza)
        barre = "\u2588" * num_barre
        etichetta = f"{bordi[i]:8.1f} - {bordi[i + 1]:8.1f}"
        linee.append(f"{etichetta} | {barre} ({conteggio})")

    return "\n".join(linee)
