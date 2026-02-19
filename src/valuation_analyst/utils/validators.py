"""Funzioni di validazione degli input per l'analisi di valutazione.

Ogni funzione verifica che il valore fornito rientri in un intervallo
ragionevole e restituisce il valore normalizzato. In caso di errore
viene sollevata una ``ValueError`` con un messaggio descrittivo in
italiano.
"""

from __future__ import annotations

import re


def valida_ticker(ticker: str) -> str:
    """Valida e normalizza un ticker azionario.

    Il ticker viene convertito in maiuscolo, privato di spazi iniziali
    e finali, e verificato con un pattern alfanumerico (lettere, cifre
    e punto sono ammessi). Lunghezza consentita: da 1 a 10 caratteri.

    Parametri
    ---------
    ticker : str
        Il ticker da validare.

    Restituisce
    -----------
    str
        Il ticker normalizzato (maiuscolo, senza spazi).

    Solleva
    -------
    ValueError
        Se il ticker e' vuoto, troppo lungo o contiene caratteri non
        ammessi.
    """
    if not isinstance(ticker, str):
        raise ValueError(
            f"Il ticker deve essere una stringa (ricevuto: {type(ticker).__name__})."
        )

    ticker = ticker.strip().upper()

    if not ticker:
        raise ValueError("Il ticker non puo' essere vuoto.")

    if len(ticker) > 10:
        raise ValueError(
            f"Il ticker non puo' superare i 10 caratteri (ricevuto: '{ticker}', "
            f"lunghezza {len(ticker)})."
        )

    # Pattern: lettere, cifre e punti (es. "BRK.B")
    if not re.match(r"^[A-Z0-9.]+$", ticker):
        raise ValueError(
            f"Il ticker contiene caratteri non ammessi: '{ticker}'. "
            "Sono ammessi solo lettere, cifre e punti."
        )

    return ticker


def valida_tasso(valore: float, nome: str = "tasso") -> float:
    """Valida un tasso (rate) finanziario.

    L'intervallo ragionevole e' da -1 (escluso) a 5 (incluso),
    cioe' da -100 % a +500 %.

    Parametri
    ---------
    valore : float
        Il tasso da validare.
    nome : str, opzionale
        Nome del parametro, per il messaggio di errore.

    Restituisce
    -----------
    float
        Il tasso validato.

    Solleva
    -------
    ValueError
        Se il tasso non e' nell'intervallo ammesso.
    """
    if not isinstance(valore, (int, float)):
        raise ValueError(
            f"Il {nome} deve essere un numero (ricevuto: {type(valore).__name__})."
        )

    valore = float(valore)

    if valore <= -1.0 or valore > 5.0:
        raise ValueError(
            f"Il {nome} deve essere compreso tra -1 (escluso) e 5 (incluso). "
            f"Ricevuto: {valore}."
        )

    return valore


def valida_positivo(valore: float, nome: str = "valore") -> float:
    """Valida che un valore sia strettamente positivo (> 0).

    Parametri
    ---------
    valore : float
        Il valore da validare.
    nome : str, opzionale
        Nome del parametro, per il messaggio di errore.

    Restituisce
    -----------
    float
        Il valore validato.

    Solleva
    -------
    ValueError
        Se il valore non e' positivo.
    """
    if not isinstance(valore, (int, float)):
        raise ValueError(
            f"Il parametro '{nome}' deve essere un numero (ricevuto: {type(valore).__name__})."
        )

    valore = float(valore)

    if valore <= 0:
        raise ValueError(
            f"Il parametro '{nome}' deve essere strettamente positivo (> 0). "
            f"Ricevuto: {valore}."
        )

    return valore


def valida_non_negativo(valore: float, nome: str = "valore") -> float:
    """Valida che un valore sia non negativo (>= 0).

    Parametri
    ---------
    valore : float
        Il valore da validare.
    nome : str, opzionale
        Nome del parametro, per il messaggio di errore.

    Restituisce
    -----------
    float
        Il valore validato.

    Solleva
    -------
    ValueError
        Se il valore e' negativo.
    """
    if not isinstance(valore, (int, float)):
        raise ValueError(
            f"Il parametro '{nome}' deve essere un numero (ricevuto: {type(valore).__name__})."
        )

    valore = float(valore)

    if valore < 0:
        raise ValueError(
            f"Il parametro '{nome}' non puo' essere negativo. "
            f"Ricevuto: {valore}."
        )

    return valore


def valida_percentuale(valore: float, nome: str = "percentuale") -> float:
    """Valida che un valore sia compreso tra 0 e 1 (intervallo percentuale).

    Parametri
    ---------
    valore : float
        Il valore da validare (espresso come decimale, es. 0.25 per 25 %).
    nome : str, opzionale
        Nome del parametro, per il messaggio di errore.

    Restituisce
    -----------
    float
        Il valore validato.

    Solleva
    -------
    ValueError
        Se il valore non e' nell'intervallo [0, 1].
    """
    if not isinstance(valore, (int, float)):
        raise ValueError(
            f"Il parametro '{nome}' deve essere un numero (ricevuto: {type(valore).__name__})."
        )

    valore = float(valore)

    if valore < 0.0 or valore > 1.0:
        raise ValueError(
            f"Il parametro '{nome}' deve essere compreso tra 0 e 1 "
            f"(intervallo percentuale). Ricevuto: {valore}."
        )

    return valore


def valida_anni(anni: int, nome: str = "anni") -> int:
    """Valida un numero di anni.

    L'intervallo ammesso e' da 1 a 100 (inclusi).

    Parametri
    ---------
    anni : int
        Il numero di anni da validare.
    nome : str, opzionale
        Nome del parametro, per il messaggio di errore.

    Restituisce
    -----------
    int
        Il numero di anni validato.

    Solleva
    -------
    ValueError
        Se il valore non e' un intero nell'intervallo [1, 100].
    """
    if not isinstance(anni, int):
        raise ValueError(
            f"Il parametro '{nome}' deve essere un intero (ricevuto: {type(anni).__name__})."
        )

    if anni < 1 or anni > 100:
        raise ValueError(
            f"Il parametro '{nome}' deve essere compreso tra 1 e 100. "
            f"Ricevuto: {anni}."
        )

    return anni


def valida_peso(peso: float, nome: str = "peso") -> float:
    """Valida un peso nella struttura del capitale (tra 0 e 1).

    Parametri
    ---------
    peso : float
        Il peso da validare.
    nome : str, opzionale
        Nome del parametro, per il messaggio di errore.

    Restituisce
    -----------
    float
        Il peso validato.

    Solleva
    -------
    ValueError
        Se il peso non e' nell'intervallo [0, 1].
    """
    if not isinstance(peso, (int, float)):
        raise ValueError(
            f"Il parametro '{nome}' deve essere un numero (ricevuto: {type(peso).__name__})."
        )

    peso = float(peso)

    if peso < 0.0 or peso > 1.0:
        raise ValueError(
            f"Il parametro '{nome}' deve essere compreso tra 0 e 1. "
            f"Ricevuto: {peso}."
        )

    return peso
