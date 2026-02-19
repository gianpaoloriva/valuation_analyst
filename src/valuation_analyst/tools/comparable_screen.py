"""Modulo per lo screening e la selezione di societa' comparabili.

Criteri di selezione: settore, dimensione, crescita, profittabilita', rischio.
Fornisce funzioni di filtraggio progressivo, un sistema di punteggio di
comparabilita' e l'integrazione con i dati settoriali di Damodaran.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from valuation_analyst.models.comparable import AnalisiComparabili, Comparabile

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Filtri per singolo criterio
# ---------------------------------------------------------------------------

def filtra_per_settore(
    comparabili: list[Comparabile],
    settore: str,
) -> list[Comparabile]:
    """Filtra comparabili per settore (match case-insensitive e parziale).

    Il confronto avviene sia sull'uguaglianza esatta (ignorando maiuscole/
    minuscole) sia sulla presenza della stringa di ricerca all'interno
    del campo settore del comparabile.

    Parametri
    ---------
    comparabili : list[Comparabile]
        Lista di candidati da filtrare.
    settore : str
        Stringa del settore da cercare.

    Restituisce
    -----------
    list[Comparabile]
        Sotto-insieme dei comparabili il cui settore corrisponde.
    """
    settore_lower = settore.lower().strip()
    risultato = [
        c for c in comparabili
        if settore_lower in c.settore.lower()
    ]
    logger.debug(
        "Filtro settore '%s': %d/%d comparabili passano il filtro",
        settore, len(risultato), len(comparabili),
    )
    return risultato


def filtra_per_dimensione(
    comparabili: list[Comparabile],
    market_cap_target: float,
    range_fattore: float = 3.0,
) -> list[Comparabile]:
    """Filtra comparabili per dimensione simile.

    Mantiene quelli con market_cap compresa tra
    ``target / range_fattore`` e ``target * range_fattore``.

    Parametri
    ---------
    comparabili : list[Comparabile]
        Lista di candidati da filtrare.
    market_cap_target : float
        Capitalizzazione di mercato dell'azienda target (in milioni).
    range_fattore : float, opzionale
        Fattore moltiplicativo per definire l'intervallo accettabile
        (default: 3.0 => da target/3 a target*3).

    Restituisce
    -----------
    list[Comparabile]
        Sotto-insieme dei comparabili con dimensione simile.
    """
    if market_cap_target <= 0 or range_fattore <= 0:
        logger.warning(
            "Parametri non validi per filtro dimensione: target=%.0f, fattore=%.1f",
            market_cap_target, range_fattore,
        )
        return list(comparabili)

    soglia_inf = market_cap_target / range_fattore
    soglia_sup = market_cap_target * range_fattore

    risultato = [
        c for c in comparabili
        if soglia_inf <= c.market_cap <= soglia_sup
    ]
    logger.debug(
        "Filtro dimensione (%.0fM - %.0fM): %d/%d comparabili passano",
        soglia_inf, soglia_sup, len(risultato), len(comparabili),
    )
    return risultato


def filtra_per_crescita(
    comparabili: list[Comparabile],
    crescita_target: float,
    tolleranza: float = 0.10,
) -> list[Comparabile]:
    """Filtra per crescita ricavi simile (+/- tolleranza).

    Parametri
    ---------
    comparabili : list[Comparabile]
        Lista di candidati da filtrare.
    crescita_target : float
        Tasso di crescita dei ricavi dell'azienda target (es. 0.15 per 15%).
    tolleranza : float, opzionale
        Tolleranza assoluta intorno al target (default: 0.10, cioe' +/-10pp).

    Restituisce
    -----------
    list[Comparabile]
        Sotto-insieme dei comparabili con crescita simile.
    """
    soglia_inf = crescita_target - tolleranza
    soglia_sup = crescita_target + tolleranza

    risultato = [
        c for c in comparabili
        if c.crescita_ricavi is not None
        and soglia_inf <= c.crescita_ricavi <= soglia_sup
    ]
    logger.debug(
        "Filtro crescita (%.1f%% +/- %.1f%%): %d/%d comparabili passano",
        crescita_target * 100, tolleranza * 100,
        len(risultato), len(comparabili),
    )
    return risultato


def filtra_per_profittabilita(
    comparabili: list[Comparabile],
    margine_target: float,
    tolleranza: float = 0.10,
) -> list[Comparabile]:
    """Filtra per margine operativo simile (+/- tolleranza).

    Parametri
    ---------
    comparabili : list[Comparabile]
        Lista di candidati da filtrare.
    margine_target : float
        Margine operativo dell'azienda target (es. 0.25 per 25%).
    tolleranza : float, opzionale
        Tolleranza assoluta intorno al target (default: 0.10, cioe' +/-10pp).

    Restituisce
    -----------
    list[Comparabile]
        Sotto-insieme dei comparabili con margine operativo simile.
    """
    soglia_inf = margine_target - tolleranza
    soglia_sup = margine_target + tolleranza

    risultato = [
        c for c in comparabili
        if c.margine_operativo is not None
        and soglia_inf <= c.margine_operativo <= soglia_sup
    ]
    logger.debug(
        "Filtro profittabilita' (%.1f%% +/- %.1f%%): %d/%d comparabili passano",
        margine_target * 100, tolleranza * 100,
        len(risultato), len(comparabili),
    )
    return risultato


# ---------------------------------------------------------------------------
# Punteggio di comparabilita'
# ---------------------------------------------------------------------------

def punteggio_comparabilita(
    candidato: Comparabile,
    target_market_cap: float,
    target_crescita: float | None = None,
    target_margine: float | None = None,
    target_settore: str | None = None,
) -> float:
    """Calcola un punteggio di comparabilita' 0-100.

    Il punteggio pondera i seguenti criteri:
    - Settore (40%): corrispondenza esatta o parziale del settore
    - Dimensione (25%): prossimita' della capitalizzazione di mercato
    - Crescita (20%): prossimita' del tasso di crescita dei ricavi
    - Margini (15%): prossimita' del margine operativo

    Parametri
    ---------
    candidato : Comparabile
        Azienda candidata da valutare.
    target_market_cap : float
        Capitalizzazione di mercato dell'azienda target (in milioni).
    target_crescita : float | None, opzionale
        Tasso di crescita dei ricavi del target.
    target_margine : float | None, opzionale
        Margine operativo del target.
    target_settore : str | None, opzionale
        Settore dell'azienda target.

    Restituisce
    -----------
    float
        Punteggio da 0 a 100.
    """
    # Pesi dei criteri
    peso_settore = 40.0
    peso_dimensione = 25.0
    peso_crescita = 20.0
    peso_margine = 15.0

    punteggio = 0.0

    # --- Criterio Settore (40 punti) ---
    if target_settore is not None:
        settore_cand = candidato.settore.lower().strip()
        settore_tgt = target_settore.lower().strip()

        if settore_cand == settore_tgt:
            # Corrispondenza esatta: punteggio pieno
            punteggio += peso_settore
        elif settore_tgt in settore_cand or settore_cand in settore_tgt:
            # Corrispondenza parziale: 75% del punteggio
            punteggio += peso_settore * 0.75
        else:
            # Verifica se condividono almeno una parola chiave
            parole_cand = set(settore_cand.split())
            parole_tgt = set(settore_tgt.split())
            parole_comuni = parole_cand & parole_tgt
            # Rimuovi parole troppo generiche
            parole_generiche = {"and", "of", "the", "in", "for", "-", "&"}
            parole_comuni -= parole_generiche
            if parole_comuni:
                # Parole chiave in comune: 40% del punteggio
                punteggio += peso_settore * 0.40
            # Nessuna corrispondenza: 0 punti per il settore
    else:
        # Se non si specifica il settore, assegna il punteggio pieno
        punteggio += peso_settore

    # --- Criterio Dimensione (25 punti) ---
    if target_market_cap > 0 and candidato.market_cap > 0:
        # Calcola il rapporto tra la piu' grande e la piu' piccola
        rapporto = max(candidato.market_cap, target_market_cap) / min(
            candidato.market_cap, target_market_cap,
        )
        # rapporto = 1 => identiche => 25 punti
        # rapporto = 3 => 50% del punteggio
        # rapporto >= 10 => 0 punti
        if rapporto <= 1.0:
            punteggio += peso_dimensione
        elif rapporto <= 10.0:
            # Funzione decrescente lineare: da 1.0 (25pt) a 10.0 (0pt)
            score_dim = 1.0 - (rapporto - 1.0) / 9.0
            punteggio += peso_dimensione * max(score_dim, 0.0)
        # rapporto > 10 => 0 punti aggiuntivi
    else:
        # Se mancano i dati di market cap, assegna un punteggio neutro
        punteggio += peso_dimensione * 0.5

    # --- Criterio Crescita (20 punti) ---
    if target_crescita is not None and candidato.crescita_ricavi is not None:
        diff_crescita = abs(candidato.crescita_ricavi - target_crescita)
        # diff = 0 => 20 punti
        # diff >= 0.30 (30pp) => 0 punti
        # Scala lineare
        soglia_crescita = 0.30
        if diff_crescita <= soglia_crescita:
            score_crescita = 1.0 - diff_crescita / soglia_crescita
            punteggio += peso_crescita * score_crescita
        # diff > soglia => 0 punti
    elif target_crescita is None:
        # Se non si specifica la crescita target, punteggio pieno
        punteggio += peso_crescita
    else:
        # Il candidato non ha il dato di crescita: punteggio neutro
        punteggio += peso_crescita * 0.3

    # --- Criterio Margini (15 punti) ---
    if target_margine is not None and candidato.margine_operativo is not None:
        diff_margine = abs(candidato.margine_operativo - target_margine)
        # diff = 0 => 15 punti
        # diff >= 0.25 (25pp) => 0 punti
        soglia_margine = 0.25
        if diff_margine <= soglia_margine:
            score_margine = 1.0 - diff_margine / soglia_margine
            punteggio += peso_margine * score_margine
    elif target_margine is None:
        # Se non si specifica il margine target, punteggio pieno
        punteggio += peso_margine
    else:
        # Il candidato non ha il dato di margine: punteggio neutro
        punteggio += peso_margine * 0.3

    return round(punteggio, 2)


# ---------------------------------------------------------------------------
# Selezione ottimale dei comparabili
# ---------------------------------------------------------------------------

def seleziona_comparabili(
    candidati: list[Comparabile],
    target_market_cap: float,
    target_settore: str,
    target_crescita: float | None = None,
    target_margine: float | None = None,
    num_max: int = 10,
    punteggio_minimo: float = 30.0,
) -> AnalisiComparabili:
    """Seleziona i migliori comparabili ordinati per punteggio.

    Procedura:
    1. Calcola il punteggio di comparabilita' per ogni candidato
    2. Filtra quelli sotto il punteggio minimo
    3. Ordina per punteggio decrescente
    4. Seleziona i top ``num_max``
    5. Calcola le statistiche dei multipli sul campione selezionato

    Parametri
    ---------
    candidati : list[Comparabile]
        Lista completa dei candidati da valutare.
    target_market_cap : float
        Capitalizzazione di mercato dell'azienda target (in milioni).
    target_settore : str
        Settore dell'azienda target.
    target_crescita : float | None, opzionale
        Tasso di crescita dei ricavi del target.
    target_margine : float | None, opzionale
        Margine operativo del target.
    num_max : int, opzionale
        Numero massimo di comparabili da selezionare (default: 10).
    punteggio_minimo : float, opzionale
        Punteggio minimo per essere inclusi (default: 30.0).

    Restituisce
    -----------
    AnalisiComparabili
        Oggetto con i comparabili selezionati e le statistiche calcolate.
    """
    logger.info(
        "Selezione comparabili: %d candidati, settore='%s', market_cap=%.0fM",
        len(candidati), target_settore, target_market_cap,
    )

    # 1. Calcola punteggio per ogni candidato
    punteggi: list[tuple[Comparabile, float]] = []
    for candidato in candidati:
        score = punteggio_comparabilita(
            candidato,
            target_market_cap=target_market_cap,
            target_crescita=target_crescita,
            target_margine=target_margine,
            target_settore=target_settore,
        )
        punteggi.append((candidato, score))

    # 2. Filtra sotto punteggio minimo
    sopra_soglia = [
        (comp, score) for comp, score in punteggi if score >= punteggio_minimo
    ]

    num_scartati = len(punteggi) - len(sopra_soglia)
    if num_scartati > 0:
        logger.debug(
            "%d candidati scartati con punteggio < %.1f",
            num_scartati, punteggio_minimo,
        )

    # 3. Ordina per punteggio decrescente
    sopra_soglia.sort(key=lambda x: x[1], reverse=True)

    # 4. Prendi i top num_max
    selezionati = sopra_soglia[:num_max]

    # Estrai solo i Comparabile dalla lista di tuple
    comparabili_finali = [comp for comp, _ in selezionati]

    # Costruisci la descrizione dei criteri di selezione
    criteri_parti = [
        f"Settore: {target_settore}",
        f"Market Cap target: {target_market_cap:,.0f}M",
    ]
    if target_crescita is not None:
        criteri_parti.append(f"Crescita target: {target_crescita:.1%}")
    if target_margine is not None:
        criteri_parti.append(f"Margine target: {target_margine:.1%}")
    criteri_parti.append(f"Punteggio minimo: {punteggio_minimo:.0f}/100")
    criteri_descrizione = " | ".join(criteri_parti)

    # 5. Costruisci AnalisiComparabili e calcola statistiche
    analisi = AnalisiComparabili(
        comparabili=comparabili_finali,
        ticker_target="",
        criteri_selezione=criteri_descrizione,
    )
    analisi.calcola_statistiche()

    logger.info(
        "Selezionati %d comparabili su %d candidati (punteggi: %s)",
        len(comparabili_finali),
        len(candidati),
        ", ".join(
            f"{c.ticker}={s:.0f}" for c, s in selezionati
        ) if selezionati else "nessuno",
    )

    return analisi


# ---------------------------------------------------------------------------
# Caricamento dati da JSON
# ---------------------------------------------------------------------------

def carica_comparabili_da_json(filepath: str) -> list[Comparabile]:
    """Carica comparabili dal file JSON di sample o cache.

    Il file JSON deve avere una struttura con una chiave ``"comparabili"``
    contenente una lista di oggetti con i campi del comparabile.

    Parametri
    ---------
    filepath : str
        Percorso del file JSON da caricare.

    Restituisce
    -----------
    list[Comparabile]
        Lista di oggetti Comparabile costruiti dai dati JSON.

    Solleva
    -------
    FileNotFoundError
        Se il file non esiste.
    json.JSONDecodeError
        Se il file non e' un JSON valido.
    KeyError
        Se il JSON non contiene la struttura attesa.
    """
    percorso = Path(filepath)

    if not percorso.exists():
        raise FileNotFoundError(
            f"File comparabili non trovato: {filepath}"
        )

    logger.info("Caricamento comparabili da %s", filepath)

    with open(percorso, encoding="utf-8") as f:
        dati = json.load(f)

    # Supporta sia un dict con chiave "comparabili" sia una lista diretta
    if isinstance(dati, dict):
        lista_raw = dati.get("comparabili", [])
        settore_default = dati.get("settore", "")
    elif isinstance(dati, list):
        lista_raw = dati
        settore_default = ""
    else:
        raise KeyError(
            f"Formato JSON non supportato: atteso dict o list, "
            f"ricevuto {type(dati).__name__}"
        )

    comparabili: list[Comparabile] = []
    for item in lista_raw:
        if not isinstance(item, dict):
            logger.warning("Elemento non valido nel JSON (non e' un dict), saltato")
            continue

        # Mappa i nomi dei campi JSON ai campi della dataclass
        # Il JSON puo' usare nomi abbreviati (es. "pe" vs "pe_ratio")
        try:
            comp = Comparabile(
                ticker=item.get("ticker", ""),
                nome=item.get("nome", item.get("name", "")),
                settore=item.get("settore", item.get("sector", settore_default)),
                market_cap=float(item.get("market_cap", 0)),
                pe_ratio=_float_o_none(item.get("pe_ratio", item.get("pe"))),
                ev_ebitda=_float_o_none(item.get("ev_ebitda")),
                pb_ratio=_float_o_none(item.get("pb_ratio", item.get("pb"))),
                ev_sales=_float_o_none(item.get("ev_sales")),
                ps_ratio=_float_o_none(item.get("ps_ratio", item.get("ps"))),
                roe=_float_o_none(item.get("roe")),
                margine_operativo=_float_o_none(
                    item.get("margine_operativo", item.get("operating_margin")),
                ),
                crescita_ricavi=_float_o_none(
                    item.get("crescita_ricavi", item.get("revenue_growth")),
                ),
                ev_ebit=_float_o_none(item.get("ev_ebit")),
                dividend_yield=_float_o_none(
                    item.get("dividend_yield", item.get("div_yield")),
                ),
                paese=item.get("paese", item.get("country", "")),
            )
            comparabili.append(comp)
        except (ValueError, TypeError) as e:
            logger.warning(
                "Errore nella creazione del comparabile da JSON (ticker=%s): %s",
                item.get("ticker", "?"), e,
            )

    logger.info("Caricati %d comparabili da %s", len(comparabili), filepath)
    return comparabili


# ---------------------------------------------------------------------------
# Integrazione con dati Damodaran
# ---------------------------------------------------------------------------

def comparabili_da_settore_damodaran(settore: str) -> dict[str, Any]:
    """Ottiene multipli medi di settore dal dataset Damodaran.

    Utilizza la funzione ``get_multipli_settore`` dal modulo
    ``damodaran_data`` per recuperare i multipli aggregati.

    Parametri
    ---------
    settore : str
        Nome del settore/industria (es. ``"Technology"``,
        ``"Consumer Electronics"``).

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - ``pe_settore``: P/E medio del settore
        - ``ev_ebitda_settore``: EV/EBITDA medio del settore
        - ``pb_settore``: P/B medio del settore
        - ``ev_sales_settore``: EV/Sales medio del settore
        - ``fonte``: Indicazione della fonte dei dati

    Solleva
    -------
    ValueError
        Se il settore non e' trovato nei dataset Damodaran.
    ConnectionError
        Se non e' possibile scaricare i dataset.
    """
    # Importazione differita per evitare dipendenze circolari
    from valuation_analyst.tools.damodaran_data import get_multipli_settore

    logger.info("Recupero multipli Damodaran per settore '%s'", settore)

    multipli_raw = get_multipli_settore(settore)

    risultato: dict[str, Any] = {
        "pe_settore": multipli_raw.get("pe"),
        "ev_ebitda_settore": multipli_raw.get("ev_ebitda"),
        "pb_settore": multipli_raw.get("pb"),
        "ev_sales_settore": multipli_raw.get("ev_sales"),
        "fonte": f"Damodaran - Settore: {settore}",
    }

    logger.info(
        "Multipli Damodaran per '%s': PE=%s, EV/EBITDA=%s, PB=%s, EV/Sales=%s",
        settore,
        f"{risultato['pe_settore']:.1f}" if risultato["pe_settore"] else "N/D",
        f"{risultato['ev_ebitda_settore']:.1f}" if risultato["ev_ebitda_settore"] else "N/D",
        f"{risultato['pb_settore']:.1f}" if risultato["pb_settore"] else "N/D",
        f"{risultato['ev_sales_settore']:.1f}" if risultato["ev_sales_settore"] else "N/D",
    )

    return risultato


# ---------------------------------------------------------------------------
# Utilita' interne
# ---------------------------------------------------------------------------

def _float_o_none(valore: Any) -> float | None:
    """Converte un valore in float, restituendo None se non possibile.

    Parametri
    ---------
    valore : Any
        Valore da convertire (puo' essere None, str, int, float).

    Restituisce
    -----------
    float | None
        Il valore convertito in float, oppure None.
    """
    if valore is None:
        return None
    try:
        risultato = float(valore)
        # Controlla che non sia NaN
        if risultato != risultato:
            return None
        return risultato
    except (ValueError, TypeError):
        return None
