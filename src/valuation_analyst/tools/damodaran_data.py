"""Scaricamento e analisi dei dataset di Aswath Damodaran.

Fornisce funzioni per scaricare, memorizzare in cache e interrogare
i dataset pubblicati da Aswath Damodaran (NYU Stern) sul suo sito.
I dati includono beta settoriali, premi per il rischio paese, WACC
e multipli di mercato per settore industriale.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import requests

from valuation_analyst.config.damodaran_urls import (
    DAMODARAN_DATASETS,
    DamodaranDataset,
)
from valuation_analyst.config.settings import CACHE_DIR
from valuation_analyst.tools.data_cache import is_cached, leggi_cache, salva_cache
from valuation_analyst.utils.excel_parser import (
    cerca_settore,
    estrai_beta_settore,
    estrai_erp_paese,
    parse_damodaran_excel,
)

logger = logging.getLogger(__name__)

# Timeout di default per il download dei file (in secondi)
_TIMEOUT_DOWNLOAD: int = 60


# ---------------------------------------------------------------------------
# Scaricamento dei dataset
# ---------------------------------------------------------------------------

def scarica_dataset(nome: str, forza_download: bool = False) -> Path:
    """Scarica un dataset Damodaran e lo salva nella cache locale.

    Se il file e' gia' presente in cache e non scaduto, restituisce
    il percorso del file esistente senza effettuare un nuovo download.

    Parametri
    ---------
    nome : str
        Nome identificativo del dataset (es. ``"betas_by_industry"``,
        ``"erp"``, ``"wacc"``). Deve corrispondere a una chiave in
        ``DAMODARAN_DATASETS``.
    forza_download : bool, opzionale
        Se ``True``, scarica il file anche se gia' presente in cache
        (default: ``False``).

    Restituisce
    -----------
    Path
        Percorso del file scaricato nella directory di cache.

    Solleva
    -------
    KeyError
        Se il nome del dataset non e' riconosciuto.
    ConnectionError
        Se il download fallisce per problemi di rete.
    RuntimeError
        Se la risposta HTTP ha un codice di errore.
    """
    if nome not in DAMODARAN_DATASETS:
        nomi_disponibili = ", ".join(sorted(DAMODARAN_DATASETS.keys()))
        raise KeyError(
            f"Dataset '{nome}' non riconosciuto. "
            f"Dataset disponibili: {nomi_disponibili}"
        )

    dataset: DamodaranDataset = DAMODARAN_DATASETS[nome]
    # Determina il nome del file dalla URL
    estensione = Path(dataset.percorso_excel).suffix
    nome_file_cache = f"damodaran_{nome}{estensione}"

    # Verifica se il file e' gia' in cache
    if not forza_download and is_cached(nome_file_cache, max_age_days=7):
        percorso_cache = CACHE_DIR / nome_file_cache
        logger.info(
            "Dataset '%s' trovato in cache: %s", nome, percorso_cache,
        )
        return percorso_cache

    # Scarica il file
    url = dataset.url_excel
    logger.info("Scaricamento dataset '%s' da %s ...", nome, url)

    try:
        risposta = requests.get(url, timeout=_TIMEOUT_DOWNLOAD, stream=True)
    except requests.ConnectionError as e:
        raise ConnectionError(
            f"Impossibile connettersi al sito di Damodaran per scaricare "
            f"il dataset '{nome}'. Verifica la connessione di rete. "
            f"Dettaglio: {e}"
        ) from e
    except requests.Timeout as e:
        raise ConnectionError(
            f"Timeout durante lo scaricamento del dataset '{nome}' "
            f"(limite: {_TIMEOUT_DOWNLOAD}s). Riprova piu' tardi."
        ) from e

    if risposta.status_code != 200:
        raise RuntimeError(
            f"Errore nello scaricamento del dataset '{nome}': "
            f"codice HTTP {risposta.status_code}. URL: {url}"
        )

    # Salva in cache
    contenuto = risposta.content
    percorso = salva_cache(nome_file_cache, contenuto)

    dimensione_kb = len(contenuto) / 1024.0
    logger.info(
        "Dataset '%s' scaricato e salvato in cache (%.1f KB): %s",
        nome, dimensione_kb, percorso,
    )

    return percorso


# ---------------------------------------------------------------------------
# Interrogazione: Beta per settore
# ---------------------------------------------------------------------------

def get_beta_settore(settore: str) -> dict[str, Any]:
    """Restituisce i dati di beta per un settore industriale.

    Scarica (se necessario) il dataset dei beta settoriali di
    Damodaran ed estrae i dati per il settore richiesto.

    Parametri
    ---------
    settore : str
        Nome del settore/industria (es. ``"Technology"``,
        ``"Consumer Electronics"``). La ricerca e' fuzzy,
        quindi nomi approssimati vengono comunque trovati.

    Restituisce
    -----------
    dict[str, Any]
        Dizionario con le chiavi:
        - ``unlevered_beta``: Beta unlevered (asset beta)
        - ``levered_beta``: Beta levered (equity beta)
        - ``d_e_ratio``: Rapporto debito/equity medio del settore
        - ``effective_tax_rate``: Aliquota fiscale effettiva media
        - ``num_firms``: Numero di imprese nel campione

    Solleva
    -------
    ValueError
        Se il settore non e' trovato nel dataset.
    """
    percorso = scarica_dataset("betas_by_industry")
    risultato = estrai_beta_settore(percorso, settore)

    if risultato is None:
        raise ValueError(
            f"Settore '{settore}' non trovato nel dataset dei beta di Damodaran. "
            f"Usa lista_settori() per vedere i settori disponibili."
        )

    logger.info(
        "Beta per settore '%s': unlevered=%.3f, levered=%.3f, D/E=%.3f",
        settore,
        risultato.get("unlevered_beta", 0),
        risultato.get("levered_beta", 0),
        risultato.get("d_e_ratio", 0),
    )

    return risultato


# ---------------------------------------------------------------------------
# Interrogazione: ERP per paese
# ---------------------------------------------------------------------------

def get_erp_paese(paese: str) -> dict[str, Any]:
    """Restituisce il premio per il rischio (ERP) per un paese.

    Scarica (se necessario) il dataset dell'Equity Risk Premium
    di Damodaran ed estrae i dati per il paese richiesto.

    Parametri
    ---------
    paese : str
        Nome del paese (es. ``"Italy"``, ``"United States"``).
        La ricerca e' fuzzy.

    Restituisce
    -----------
    dict[str, Any]
        Dizionario con le chiavi:
        - ``country_risk_premium``: Premio per il rischio specifico del paese
        - ``equity_risk_premium``: Equity Risk Premium totale
        - ``default_spread``: Default spread del debito sovrano

    Solleva
    -------
    ValueError
        Se il paese non e' trovato nel dataset.
    """
    percorso = scarica_dataset("erp")
    risultato = estrai_erp_paese(percorso, paese)

    if risultato is None:
        raise ValueError(
            f"Paese '{paese}' non trovato nel dataset ERP di Damodaran. "
            f"Usa lista_paesi() per vedere i paesi disponibili."
        )

    logger.info(
        "ERP per '%s': CRP=%.4f, ERP=%.4f, default_spread=%.4f",
        paese,
        risultato.get("country_risk_premium", 0) or 0,
        risultato.get("equity_risk_premium", 0) or 0,
        risultato.get("default_spread", 0) or 0,
    )

    return risultato


# ---------------------------------------------------------------------------
# Interrogazione: WACC per settore
# ---------------------------------------------------------------------------

def get_wacc_settore(settore: str) -> dict[str, Any]:
    """Restituisce i dati di WACC per un settore industriale.

    Scarica (se necessario) il dataset del WACC settoriale di
    Damodaran ed estrae i dati per il settore richiesto.

    Parametri
    ---------
    settore : str
        Nome del settore/industria. La ricerca e' fuzzy.

    Restituisce
    -----------
    dict[str, Any]
        Dizionario con le chiavi:
        - ``wacc``: Costo medio ponderato del capitale
        - ``cost_of_equity``: Costo dell'equity
        - ``cost_of_debt``: Costo del debito (pre-tax)
        - ``d_e_ratio``: Rapporto debito/equity

    Solleva
    -------
    ValueError
        Se il settore non e' trovato nel dataset.
    """
    percorso = scarica_dataset("wacc")
    df = parse_damodaran_excel(percorso)
    riga = cerca_settore(df, settore)

    if riga is None:
        raise ValueError(
            f"Settore '{settore}' non trovato nel dataset WACC di Damodaran. "
            f"Usa lista_settori() per vedere i settori disponibili."
        )

    risultato: dict[str, Any] = {
        "wacc": _estrai_float(riga, df.columns, [
            "cost_of_capital", "wacc", "cost of capital",
        ]),
        "cost_of_equity": _estrai_float(riga, df.columns, [
            "cost_of_equity", "cost of equity",
        ]),
        "cost_of_debt": _estrai_float(riga, df.columns, [
            "cost_of_debt", "cost of debt", "after_tax_cost_of_debt",
            "pre_tax_cost_of_debt",
        ]),
        "d_e_ratio": _estrai_float(riga, df.columns, [
            "d/e_ratio", "d_e_ratio", "de_ratio", "debt/equity",
        ]),
    }

    logger.info(
        "WACC per settore '%s': wacc=%s, ke=%s, kd=%s",
        settore,
        f"{risultato['wacc']:.4f}" if risultato["wacc"] else "N/D",
        f"{risultato['cost_of_equity']:.4f}" if risultato["cost_of_equity"] else "N/D",
        f"{risultato['cost_of_debt']:.4f}" if risultato["cost_of_debt"] else "N/D",
    )

    return risultato


# ---------------------------------------------------------------------------
# Interrogazione: Multipli per settore
# ---------------------------------------------------------------------------

def get_multipli_settore(settore: str) -> dict[str, Any]:
    """Restituisce i multipli di valutazione per un settore.

    Scarica (se necessario) i dataset dei multipli di Damodaran
    (P/E, EV/EBITDA, P/BV, EV/Sales) ed estrae i valori per il
    settore richiesto.

    Parametri
    ---------
    settore : str
        Nome del settore/industria. La ricerca e' fuzzy.

    Restituisce
    -----------
    dict[str, Any]
        Dizionario con le chiavi:
        - ``pe``: Rapporto prezzo/utili medio del settore
        - ``ev_ebitda``: Multiplo EV/EBITDA medio del settore
        - ``pb``: Rapporto prezzo/valore contabile
        - ``ev_sales``: Multiplo EV/Ricavi

    Solleva
    -------
    ValueError
        Se il settore non e' trovato in nessuno dei dataset.
    """
    multipli: dict[str, Any] = {
        "pe": None,
        "ev_ebitda": None,
        "pb": None,
        "ev_sales": None,
    }

    # Mappa: chiave del multiplo -> nome del dataset Damodaran
    dataset_multipli: dict[str, str] = {
        "pe": "pe_ratios",
        "ev_ebitda": "ev_ebitda",
        "pb": "pb_ratios",
        "ev_sales": "revenue_multiples",
    }

    trovato_almeno_uno = False

    for chiave_multiplo, nome_dataset in dataset_multipli.items():
        try:
            percorso = scarica_dataset(nome_dataset)
            df = parse_damodaran_excel(percorso)
            riga = cerca_settore(df, settore)

            if riga is not None:
                trovato_almeno_uno = True
                # Cerca il valore del multiplo nelle colonne
                # (la seconda o terza colonna contiene tipicamente il valore)
                for i in range(1, min(len(riga), 6)):
                    val = riga.iloc[i]
                    if val is not None and isinstance(val, (int, float)):
                        import math
                        if not math.isnan(float(val)) and float(val) > 0:
                            multipli[chiave_multiplo] = float(val)
                            break

        except (KeyError, ConnectionError, RuntimeError) as e:
            logger.warning(
                "Impossibile recuperare il multiplo '%s' per il settore '%s': %s",
                chiave_multiplo, settore, e,
            )

    if not trovato_almeno_uno:
        raise ValueError(
            f"Settore '{settore}' non trovato nei dataset dei multipli di Damodaran. "
            f"Usa lista_settori() per vedere i settori disponibili."
        )

    logger.info(
        "Multipli per settore '%s': PE=%s, EV/EBITDA=%s, PB=%s, EV/Sales=%s",
        settore,
        f"{multipli['pe']:.1f}" if multipli["pe"] else "N/D",
        f"{multipli['ev_ebitda']:.1f}" if multipli["ev_ebitda"] else "N/D",
        f"{multipli['pb']:.1f}" if multipli["pb"] else "N/D",
        f"{multipli['ev_sales']:.1f}" if multipli["ev_sales"] else "N/D",
    )

    return multipli


# ---------------------------------------------------------------------------
# Liste di settori e paesi disponibili
# ---------------------------------------------------------------------------

def lista_settori() -> list[str]:
    """Restituisce la lista dei settori disponibili nel dataset Damodaran.

    Scarica (se necessario) il dataset dei beta settoriali e
    restituisce tutti i nomi di settore presenti nella prima colonna.

    Restituisce
    -----------
    list[str]
        Lista ordinata dei nomi dei settori/industrie.
    """
    try:
        percorso = scarica_dataset("betas_by_industry")
        df = parse_damodaran_excel(percorso)
    except (KeyError, ConnectionError, RuntimeError) as e:
        logger.error("Impossibile recuperare la lista dei settori: %s", e)
        return []

    if df.empty:
        return []

    prima_col = df.columns[0]
    settori = (
        df[prima_col]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )

    # Rimuovi eventuali intestazioni residue
    settori = [
        s for s in settori
        if s.lower() not in ("industry name", "total market", "", "nan")
    ]

    return sorted(settori)


def lista_paesi() -> list[str]:
    """Restituisce la lista dei paesi disponibili nel dataset ERP di Damodaran.

    Scarica (se necessario) il dataset dell'Equity Risk Premium
    per paese e restituisce tutti i nomi di paese presenti.

    Restituisce
    -----------
    list[str]
        Lista ordinata dei nomi dei paesi.
    """
    try:
        percorso = scarica_dataset("erp")
        df = parse_damodaran_excel(percorso)
    except (KeyError, ConnectionError, RuntimeError) as e:
        logger.error("Impossibile recuperare la lista dei paesi: %s", e)
        return []

    if df.empty:
        return []

    prima_col = df.columns[0]
    paesi = (
        df[prima_col]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )

    # Rimuovi eventuali intestazioni residue
    paesi = [
        p for p in paesi
        if p.lower() not in ("country", "region", "", "nan")
    ]

    return sorted(paesi)


# ---------------------------------------------------------------------------
# Utilita' interne
# ---------------------------------------------------------------------------

def _estrai_float(
    riga: Any,
    colonne: Any,
    nomi_possibili: list[str],
) -> float | None:
    """Estrae un valore float da una riga cercando tra diversi nomi di colonna.

    Parametri
    ---------
    riga : pd.Series
        Riga del DataFrame.
    colonne : pd.Index
        Nomi delle colonne del DataFrame.
    nomi_possibili : list[str]
        Lista di nomi candidati per la colonna.

    Restituisce
    -----------
    float | None
        Il valore numerico trovato, oppure ``None``.
    """
    import pandas as pd

    colonne_lower = [str(c).lower().strip() for c in colonne]

    for nome in nomi_possibili:
        nome_lower = nome.lower().strip()

        # Corrispondenza esatta
        if nome_lower in colonne_lower:
            idx = colonne_lower.index(nome_lower)
            val = riga.iloc[idx]
            if pd.notna(val):
                try:
                    risultato = float(val)
                    if not (risultato != risultato):  # NaN check
                        return risultato
                except (ValueError, TypeError):
                    pass

        # Corrispondenza parziale
        for j, col in enumerate(colonne_lower):
            if nome_lower in col:
                val = riga.iloc[j]
                if pd.notna(val):
                    try:
                        risultato = float(val)
                        if not (risultato != risultato):
                            return risultato
                    except (ValueError, TypeError):
                        pass

    return None
