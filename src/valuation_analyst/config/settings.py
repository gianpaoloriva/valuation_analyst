"""Impostazioni globali e percorsi del progetto.

Carica le variabili d'ambiente dal file .env e definisce
tutti i percorsi e le configurazioni di base utilizzate
nell'intero progetto di valuation_analyst.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Carica variabili d'ambiente dal file .env nella radice del progetto
load_dotenv()

# --- Percorsi principali del progetto ---

ROOT_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
"""Percorso della radice del progetto (dove si trova pyproject.toml)."""

DATA_DIR: Path = ROOT_DIR / "data"
"""Percorso della directory dati principale."""

CACHE_DIR: Path = DATA_DIR / "cache"
"""Percorso della directory per i file di cache (dati Damodaran, API, ecc.)."""

REPORTS_DIR: Path = DATA_DIR / "reports"
"""Percorso della directory dove vengono salvati i report di valutazione."""

LOGS_DIR: Path = DATA_DIR / "logs"
"""Percorso della directory per i file di log."""

SAMPLES_DIR: Path = DATA_DIR / "samples"
"""Percorso della directory con i dati di esempio."""

# --- Configurazione API Massive ---

MASSIVE_API_KEY: str = os.getenv("MASSIVE_API_KEY", "")
"""Chiave API per il servizio Massive (caricata da variabile d'ambiente)."""

MASSIVE_BASE_URL: str = "https://api.massive.com/v1"
"""URL base per le chiamate API a Massive."""

# --- Configurazione Damodaran ---

DAMODARAN_BASE_URL: str = "https://pages.stern.nyu.edu/~adamodar/"
"""URL base del sito di Aswath Damodaran (NYU Stern)."""

# --- Log dei prompt ---

PROMPT_LOG_PATH: Path = ROOT_DIR / "prompt_log.md"
"""Percorso del file di log dei prompt utilizzati durante l'analisi."""

# --- Impostazioni di cache ---

CACHE_EXPIRY_HOURS: int = int(os.getenv("CACHE_EXPIRY_HOURS", "24"))
"""Durata di validita' della cache in ore (default: 24)."""

# --- Impostazioni di logging ---

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
"""Livello di logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)."""

LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
"""Formato dei messaggi di log."""


def assicura_directory() -> None:
    """Crea le directory di lavoro se non esistono gia'.

    Viene invocata all'avvio per garantire che tutte le
    directory necessarie al funzionamento siano presenti.
    """
    for directory in (DATA_DIR, CACHE_DIR, REPORTS_DIR, LOGS_DIR, SAMPLES_DIR):
        directory.mkdir(parents=True, exist_ok=True)
