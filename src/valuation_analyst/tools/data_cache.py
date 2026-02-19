"""Gestione della cache locale per i dati scaricati.

Fornisce un sistema di cache basato su file per memorizzare
i dataset Damodaran, le risposte API e altri dati scaricati,
evitando download ripetuti e migliorando le prestazioni.

I file vengono salvati nella directory ``data/cache/`` con
metadati temporali per la verifica della scadenza.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

from valuation_analyst.config.settings import CACHE_DIR

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Percorsi e verifica cache
# ---------------------------------------------------------------------------

def cache_path(nome: str) -> Path:
    """Restituisce il percorso completo di un file nella cache.

    Parametri
    ---------
    nome : str
        Nome del file (es. ``"damodaran_betas_by_industry.xls"``).

    Restituisce
    -----------
    Path
        Percorso completo del file nella directory di cache.
    """
    # Assicura che la directory di cache esista
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / nome


def is_cached(nome: str, max_age_days: int = 7) -> bool:
    """Verifica se un file e' presente in cache e non scaduto.

    Controlla l'esistenza del file e la sua data di ultima
    modifica per determinare se e' ancora valido.

    Parametri
    ---------
    nome : str
        Nome del file nella cache.
    max_age_days : int, opzionale
        Numero massimo di giorni di validita' del file
        (default: 7).

    Restituisce
    -----------
    bool
        ``True`` se il file esiste e non e' scaduto,
        ``False`` altrimenti.
    """
    percorso = cache_path(nome)

    if not percorso.exists():
        return False

    # Verifica la dimensione: file vuoti non sono validi
    if percorso.stat().st_size == 0:
        logger.debug("File in cache vuoto (0 byte): %s", nome)
        return False

    # Verifica l'eta' del file
    eta_secondi = time.time() - percorso.stat().st_mtime
    eta_giorni = eta_secondi / (60 * 60 * 24)

    if eta_giorni > max_age_days:
        logger.debug(
            "File in cache scaduto (%.1f giorni > %d giorni): %s",
            eta_giorni, max_age_days, nome,
        )
        return False

    logger.debug(
        "File in cache valido (%.1f giorni, max %d): %s",
        eta_giorni, max_age_days, nome,
    )
    return True


# ---------------------------------------------------------------------------
# Salvataggio e lettura della cache
# ---------------------------------------------------------------------------

def salva_cache(nome: str, data: bytes) -> Path:
    """Salva dei dati binari nella cache.

    Crea il file nella directory di cache, sovrascrivendo eventuali
    file esistenti con lo stesso nome.

    Parametri
    ---------
    nome : str
        Nome del file nella cache.
    data : bytes
        Contenuto binario da salvare.

    Restituisce
    -----------
    Path
        Percorso del file salvato.
    """
    percorso = cache_path(nome)

    # Assicura che la directory esista
    percorso.parent.mkdir(parents=True, exist_ok=True)

    percorso.write_bytes(data)

    dimensione_kb = len(data) / 1024.0
    logger.info(
        "File salvato in cache: %s (%.1f KB)", nome, dimensione_kb,
    )

    return percorso


def leggi_cache(nome: str) -> bytes | None:
    """Legge il contenuto di un file dalla cache.

    Parametri
    ---------
    nome : str
        Nome del file nella cache.

    Restituisce
    -----------
    bytes | None
        Il contenuto binario del file, oppure ``None`` se il file
        non esiste o non e' leggibile.
    """
    percorso = cache_path(nome)

    if not percorso.exists():
        logger.debug("File non trovato in cache: %s", nome)
        return None

    try:
        contenuto = percorso.read_bytes()
        logger.debug(
            "File letto dalla cache: %s (%.1f KB)",
            nome, len(contenuto) / 1024.0,
        )
        return contenuto
    except OSError as e:
        logger.warning(
            "Errore nella lettura del file dalla cache '%s': %s", nome, e,
        )
        return None


# ---------------------------------------------------------------------------
# Manutenzione della cache
# ---------------------------------------------------------------------------

def pulisci_cache(max_age_days: int = 30) -> int:
    """Rimuove i file scaduti dalla cache.

    Elimina tutti i file nella directory di cache che sono piu'
    vecchi del numero di giorni specificato.

    Parametri
    ---------
    max_age_days : int, opzionale
        Eta' massima in giorni. I file piu' vecchi vengono eliminati
        (default: 30).

    Restituisce
    -----------
    int
        Numero di file eliminati.
    """
    if not CACHE_DIR.exists():
        return 0

    eliminati = 0
    soglia_secondi = max_age_days * 24 * 60 * 60
    adesso = time.time()

    for file in CACHE_DIR.iterdir():
        # Salta file nascosti e .gitkeep
        if file.name.startswith("."):
            continue

        if not file.is_file():
            continue

        eta_secondi = adesso - file.stat().st_mtime
        if eta_secondi > soglia_secondi:
            try:
                file.unlink()
                eliminati += 1
                logger.debug("File rimosso dalla cache: %s", file.name)
            except OSError as e:
                logger.warning(
                    "Impossibile rimuovere il file '%s' dalla cache: %s",
                    file.name, e,
                )

    if eliminati > 0:
        logger.info(
            "Pulizia cache completata: %d file rimossi (soglia: %d giorni).",
            eliminati, max_age_days,
        )
    else:
        logger.info("Nessun file scaduto trovato nella cache.")

    return eliminati


def dimensione_cache() -> str:
    """Calcola la dimensione totale della cache in formato leggibile.

    Restituisce
    -----------
    str
        Dimensione totale formattata (es. ``"12.3 MB"``, ``"456 KB"``).
    """
    if not CACHE_DIR.exists():
        return "0 B"

    totale_bytes = 0
    num_file = 0

    for file in CACHE_DIR.iterdir():
        if file.is_file() and not file.name.startswith("."):
            totale_bytes += file.stat().st_size
            num_file += 1

    return _formatta_dimensione(totale_bytes, num_file)


# ---------------------------------------------------------------------------
# Utilita' interne
# ---------------------------------------------------------------------------

def _formatta_dimensione(byte: int, num_file: int = 0) -> str:
    """Formatta una dimensione in byte in formato leggibile.

    Parametri
    ---------
    byte : int
        Dimensione in byte.
    num_file : int, opzionale
        Numero di file (per il messaggio descrittivo).

    Restituisce
    -----------
    str
        Dimensione formattata con unita' appropriata.
    """
    suffisso_file = f" ({num_file} file)" if num_file > 0 else ""

    if byte == 0:
        return f"0 B{suffisso_file}"
    elif byte < 1024:
        return f"{byte} B{suffisso_file}"
    elif byte < 1024 * 1024:
        return f"{byte / 1024:.1f} KB{suffisso_file}"
    elif byte < 1024 * 1024 * 1024:
        return f"{byte / (1024 * 1024):.1f} MB{suffisso_file}"
    else:
        return f"{byte / (1024 * 1024 * 1024):.2f} GB{suffisso_file}"
