"""Utilita' di formattazione per valori finanziari e tabelle.

Contiene funzioni per la formattazione di valute, percentuali,
numeri, multipli e per la generazione di tabelle Markdown.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Mappe simbolo valuta e configurazione locale
# ---------------------------------------------------------------------------

_SIMBOLO_VALUTA: dict[str, str] = {
    "USD": "$",
    "EUR": "\u20ac",
    "GBP": "\u00a3",
    "JPY": "\u00a5",
    "CHF": "CHF\u00a0",
    "CNY": "\u00a5",
    "CAD": "CA$",
    "AUD": "AU$",
}

# Valute che utilizzano il formato europeo (punto come separatore migliaia,
# virgola per i decimali)
_VALUTE_FORMATO_EUROPEO: set[str] = {"EUR", "CHF"}


# ---------------------------------------------------------------------------
# Funzioni di formattazione
# ---------------------------------------------------------------------------

def formatta_valuta(
    valore: float,
    valuta: str = "USD",
    decimali: int = 2,
) -> str:
    """Formatta un importo monetario con il simbolo della valuta.

    Parametri
    ---------
    valore : float
        L'importo da formattare.
    valuta : str, opzionale
        Codice ISO 4217 della valuta (default: ``"USD"``).
    decimali : int, opzionale
        Numero di cifre decimali (default: 2).

    Restituisce
    -----------
    str
        Stringa formattata, es. ``"$1,234.56"`` oppure ``"€1.234,56"``.

    Esempi
    ------
    >>> formatta_valuta(1234.5, "USD")
    '$1,234.50'
    >>> formatta_valuta(1234.5, "EUR")
    '€1.234,50'
    """
    simbolo = _SIMBOLO_VALUTA.get(valuta.upper(), valuta + "\u00a0")

    if valuta.upper() in _VALUTE_FORMATO_EUROPEO:
        # Formato europeo: punto per migliaia, virgola per decimali
        testo = _formatta_europeo(valore, decimali)
    else:
        # Formato anglosassone: virgola per migliaia, punto per decimali
        testo = f"{valore:,.{decimali}f}"

    # Gestione segno negativo: il simbolo viene sempre prima del numero
    if valore < 0:
        return f"-{simbolo}{testo.lstrip('-')}"
    return f"{simbolo}{testo}"


def formatta_percentuale(valore: float, decimali: int = 2) -> str:
    """Formatta un valore come percentuale.

    Il valore in ingresso e' espresso come decimale
    (es. 0.1234 diventa ``"12.34%"``).

    Parametri
    ---------
    valore : float
        Valore decimale (es. 0.12 per 12 %).
    decimali : int, opzionale
        Numero di cifre decimali nella percentuale (default: 2).

    Restituisce
    -----------
    str
        Stringa formattata, es. ``"12.34%"``.
    """
    return f"{valore * 100:.{decimali}f}%"


def formatta_numero(valore: float, decimali: int = 2) -> str:
    """Formatta un numero con separatore delle migliaia.

    Parametri
    ---------
    valore : float
        Il numero da formattare.
    decimali : int, opzionale
        Numero di cifre decimali (default: 2).

    Restituisce
    -----------
    str
        Stringa formattata, es. ``"1,234.56"``.
    """
    return f"{valore:,.{decimali}f}"


def formatta_milioni(valore: float, valuta: str = "USD") -> str:
    """Formatta un importo in milioni con il simbolo della valuta.

    Parametri
    ---------
    valore : float
        L'importo da formattare (in unita', non in milioni).
    valuta : str, opzionale
        Codice ISO 4217 della valuta (default: ``"USD"``).

    Restituisce
    -----------
    str
        Stringa formattata, es. ``"$1,234.5M"``.
    """
    simbolo = _SIMBOLO_VALUTA.get(valuta.upper(), valuta + "\u00a0")
    milioni = valore / 1_000_000.0

    if abs(milioni) >= 1_000.0:
        testo = f"{milioni:,.1f}"
    elif abs(milioni) >= 1.0:
        testo = f"{milioni:,.1f}"
    else:
        testo = f"{milioni:,.2f}"

    if valore < 0:
        return f"-{simbolo}{testo.lstrip('-')}M"
    return f"{simbolo}{testo}M"


def formatta_miliardi(valore: float, valuta: str = "USD") -> str:
    """Formatta un importo in miliardi con il simbolo della valuta.

    Parametri
    ---------
    valore : float
        L'importo da formattare (in unita', non in miliardi).
    valuta : str, opzionale
        Codice ISO 4217 della valuta (default: ``"USD"``).

    Restituisce
    -----------
    str
        Stringa formattata, es. ``"$1.23B"``.
    """
    simbolo = _SIMBOLO_VALUTA.get(valuta.upper(), valuta + "\u00a0")
    miliardi = valore / 1_000_000_000.0

    testo = f"{miliardi:,.2f}"

    if valore < 0:
        return f"-{simbolo}{testo.lstrip('-')}B"
    return f"{simbolo}{testo}B"


def formatta_multiplo(valore: float, decimali: int = 1) -> str:
    """Formatta un valore come multiplo (es. EV/EBITDA).

    Parametri
    ---------
    valore : float
        Il multiplo da formattare.
    decimali : int, opzionale
        Numero di cifre decimali (default: 1).

    Restituisce
    -----------
    str
        Stringa formattata, es. ``"12.3x"``.
    """
    return f"{valore:.{decimali}f}x"


# ---------------------------------------------------------------------------
# Generazione tabella Markdown
# ---------------------------------------------------------------------------

def tabella_markdown(
    headers: list[str],
    rows: list[list[str]],
    allineamento: list[str] | None = None,
) -> str:
    """Genera una tabella in formato Markdown.

    Parametri
    ---------
    headers : list[str]
        Lista delle intestazioni di colonna.
    rows : list[list[str]]
        Lista di righe, ciascuna una lista di stringhe.
    allineamento : list[str] | None, opzionale
        Lista di allineamenti per ogni colonna. Valori ammessi:
        ``"left"`` (o ``"l"``), ``"right"`` (o ``"r"``),
        ``"center"`` (o ``"c"``). Se ``None``, viene usato ``"left"``
        per tutte le colonne.

    Restituisce
    -----------
    str
        La tabella Markdown come stringa.

    Solleva
    -------
    ValueError
        Se il numero di colonne nelle intestazioni non corrisponde
        all'allineamento, o se una riga ha un numero diverso di colonne.
    """
    num_colonne = len(headers)

    if allineamento is None:
        allineamento = ["left"] * num_colonne
    elif len(allineamento) != num_colonne:
        raise ValueError(
            f"Il numero di allineamenti ({len(allineamento)}) non corrisponde "
            f"al numero di colonne ({num_colonne})."
        )

    # Verifica righe
    for i, riga in enumerate(rows):
        if len(riga) != num_colonne:
            raise ValueError(
                f"La riga {i} ha {len(riga)} colonne, "
                f"ma le intestazioni ne hanno {num_colonne}."
            )

    # Calcola la larghezza massima per ogni colonna
    larghezze = [len(h) for h in headers]
    for riga in rows:
        for j, cella in enumerate(riga):
            larghezze[j] = max(larghezze[j], len(cella))

    # Assicura larghezza minima di 3 per il separatore
    larghezze = [max(l, 3) for l in larghezze]

    # Costruisci il separatore di allineamento
    separatori: list[str] = []
    for j, allin in enumerate(allineamento):
        larghezza = larghezze[j]
        codice = allin.lower().strip()
        if codice in ("left", "l"):
            separatori.append(":" + "-" * (larghezza - 1))
        elif codice in ("right", "r"):
            separatori.append("-" * (larghezza - 1) + ":")
        elif codice in ("center", "c"):
            separatori.append(":" + "-" * (larghezza - 2) + ":")
        else:
            separatori.append("-" * larghezza)

    # Costruisci le righe
    def _riga_md(celle: list[str]) -> str:
        parti = [cella.ljust(larghezze[j]) for j, cella in enumerate(celle)]
        return "| " + " | ".join(parti) + " |"

    linee: list[str] = []
    linee.append(_riga_md(headers))
    linee.append("| " + " | ".join(separatori) + " |")
    for riga in rows:
        linee.append(_riga_md(riga))

    return "\n".join(linee)


# ---------------------------------------------------------------------------
# Funzioni interne
# ---------------------------------------------------------------------------

def _formatta_europeo(valore: float, decimali: int) -> str:
    """Formatta un numero nel formato europeo (1.234,56).

    Parametri
    ---------
    valore : float
        Il numero da formattare.
    decimali : int
        Numero di cifre decimali.

    Restituisce
    -----------
    str
        Il numero formattato con punto per le migliaia e virgola per i
        decimali.
    """
    # Genera prima nel formato anglosassone
    testo_us = f"{valore:,.{decimali}f}"
    # Sostituzione: virgola -> placeholder, punto -> virgola, placeholder -> punto
    testo_eu = testo_us.replace(",", "_").replace(".", ",").replace("_", ".")
    return testo_eu
