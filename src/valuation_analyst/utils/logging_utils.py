"""Utilita' per il logging dei prompt in formato Markdown.

Registra ogni interazione (skill, input, agente, riepilogo) nel
file ``prompt_log.md`` definito nelle impostazioni del progetto,
consentendo la tracciabilita' completa delle operazioni eseguite.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from valuation_analyst.config.settings import PROMPT_LOG_PATH


def log_prompt(
    skill: str,
    input_text: str,
    agent: str,
    summary: str,
) -> None:
    """Registra un'interazione nel file di log dei prompt.

    Aggiunge in coda al file ``prompt_log.md`` un blocco formattato
    in Markdown con timestamp, skill invocata, testo di input,
    agente responsabile e riepilogo del risultato.

    Parametri
    ---------
    skill : str
        Nome della skill o del modulo che ha generato il prompt.
    input_text : str
        Testo dell'input (o riassunto dell'input) inviato.
    agent : str
        Identificativo dell'agente che ha gestito la richiesta.
    summary : str
        Riepilogo sintetico del risultato o dell'output prodotto.

    Note
    ----
    Se il file non esiste, viene creato automaticamente. Le directory
    intermedie vengono create se necessario.
    """
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    voce = (
        f"\n### {timestamp}\n"
        f"**Skill:** {skill}\n"
        f"**Input:** {input_text}\n"
        f"**Agent:** {agent}\n"
        f"**Summary:** {summary}\n"
        f"---\n"
    )

    # Assicura che la directory del file di log esista
    percorso = Path(PROMPT_LOG_PATH)
    percorso.parent.mkdir(parents=True, exist_ok=True)

    with percorso.open("a", encoding="utf-8") as f:
        f.write(voce)


def leggi_log() -> str:
    """Legge e restituisce il contenuto del file di log dei prompt.

    Restituisce
    -----------
    str
        Il contenuto completo di ``prompt_log.md``. Se il file non
        esiste, restituisce una stringa vuota.
    """
    percorso = Path(PROMPT_LOG_PATH)

    if not percorso.exists():
        return ""

    return percorso.read_text(encoding="utf-8")
