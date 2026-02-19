"""Modulo per il calcolo dello sconto di illiquidita' per societa' private.

Segue la metodologia Damodaran per stimare lo sconto appropriato
in base a dimensione, profittabilita' e caratteristiche dell'azienda.
"""

from __future__ import annotations

import math

from valuation_analyst.utils.validators import valida_non_negativo, valida_positivo


# ---------------------------------------------------------------------------
# Sconto di illiquidita' - Metodo Damodaran
# ---------------------------------------------------------------------------

def calcola_sconto_illiquidita(
    ricavi: float,
    margine_ebitda: float,
    tipo_investitore: str = "finanziario",
    settore: str | None = None,
    ha_distribuzione_utili: bool = False,
    restrizioni_vendita: bool = True,
) -> dict:
    """Calcola lo sconto di illiquidita' secondo Damodaran.

    Formula approssimativa:
    Sconto = 0.35 - 0.15 * ln(Ricavi in milioni) - 0.10 * margine_EBITDA

    Con aggiustamenti per:
    - tipo investitore (strategico vs finanziario)
    - distribuzione utili (riduce sconto)
    - restrizioni vendita (aumenta sconto)

    Floor: 5%, Cap: 50%

    Parametri
    ---------
    ricavi : float
        Ricavi totali dell'azienda in euro (non in milioni).
    margine_ebitda : float
        Margine EBITDA espresso come decimale (es. 0.15 per 15%).
    tipo_investitore : str, opzionale
        Tipo di investitore: "finanziario" (default) o "strategico".
    settore : str | None, opzionale
        Settore dell'azienda (riservato per futuri aggiustamenti settoriali).
    ha_distribuzione_utili : bool, opzionale
        Se l'azienda distribuisce regolarmente utili o dividendi.
    restrizioni_vendita : bool, opzionale
        Se sono presenti restrizioni alla vendita della partecipazione.

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - sconto: float (percentuale, es. 0.25 per 25%)
        - sconto_base: float (prima di aggiustamenti)
        - aggiustamenti: dict (dettaglio ogni aggiustamento)
        - ricavi_milioni: float
        - margine_ebitda: float
        - note: list[str]
    """
    # Conversione ricavi in milioni, con floor per evitare log(0)
    ricavi_milioni = ricavi / 1_000_000
    if ricavi_milioni <= 0:
        ricavi_milioni = 0.001

    # Formula base Damodaran
    sconto_base = 0.35 - 0.15 * math.log(ricavi_milioni) - 0.10 * margine_ebitda
    aggiustamenti: dict[str, float] = {}

    # Aggiustamento per investitore strategico (ha meno bisogno di liquidita')
    if tipo_investitore == "strategico":
        aggiustamenti["tipo_investitore"] = -0.05

    # La distribuzione di utili riduce la necessita' di exit
    if ha_distribuzione_utili:
        aggiustamenti["distribuzione_utili"] = -0.03

    # L'assenza di restrizioni alla vendita riduce l'illiquidita'
    if not restrizioni_vendita:
        aggiustamenti["no_restrizioni"] = -0.02

    # Applicazione aggiustamenti e clamp nel range [5%, 50%]
    sconto_finale = sconto_base + sum(aggiustamenti.values())
    sconto_finale = max(0.05, min(0.50, sconto_finale))

    note: list[str] = []
    if sconto_finale > 0.35:
        note.append(
            "Sconto elevato: verificare se giustificato da illiquidita' effettiva"
        )
    if sconto_finale < 0.10:
        note.append(
            "Sconto contenuto: l'azienda ha caratteristiche vicine a una quotata"
        )

    return {
        "sconto": sconto_finale,
        "sconto_base": max(0.05, min(0.50, sconto_base)),
        "aggiustamenti": aggiustamenti,
        "ricavi_milioni": ricavi_milioni,
        "margine_ebitda": margine_ebitda,
        "note": note,
    }


# ---------------------------------------------------------------------------
# Sconto basato solo sulla dimensione
# ---------------------------------------------------------------------------

def sconto_per_dimensione(ricavi: float) -> float:
    """Stima sconto illiquidita' basato solo sulla dimensione.

    Intervalli di riferimento:
    - Ricavi < 10M    -> 30-40%  (punto medio 0.35)
    - Ricavi 10-50M   -> 25-30%  (punto medio 0.275)
    - Ricavi 50-200M  -> 20-25%  (punto medio 0.225)
    - Ricavi 200M-1B  -> 15-20%  (punto medio 0.175)
    - Ricavi > 1B     -> 10-15%  (punto medio 0.125)

    Parametri
    ---------
    ricavi : float
        Ricavi totali dell'azienda in euro.

    Restituisce
    -----------
    float
        Sconto di illiquidita' stimato (punto medio dell'intervallo).
    """
    ricavi_milioni = ricavi / 1_000_000

    if ricavi_milioni < 10:
        return 0.35
    elif ricavi_milioni < 50:
        return 0.275
    elif ricavi_milioni < 200:
        return 0.225
    elif ricavi_milioni < 1_000:
        return 0.175
    else:
        return 0.125


# ---------------------------------------------------------------------------
# Sconto da studi restricted stock
# ---------------------------------------------------------------------------

def sconto_restricted_stock(
    ricavi: float,
    profittevole: bool,
    block_size_pct: float = 0.0,
) -> float:
    """Sconto basato su studi restricted stock (Silber, FMV opinions).

    Le azioni restricted sono titoli non registrati che non possono
    essere scambiati liberamente per un certo periodo. Lo sconto
    osservato negli studi empirici e' un proxy per l'illiquidita'.

    Parametri
    ---------
    ricavi : float
        Ricavi totali dell'azienda in euro.
    profittevole : bool
        Se l'azienda genera utili positivi.
    block_size_pct : float, opzionale
        Dimensione del blocco come percentuale del flottante (0.0 - 1.0).
        Blocchi piu' grandi hanno sconti maggiori.

    Restituisce
    -----------
    float
        Sconto percentuale stimato (es. 0.30 per 30%).
    """
    valida_non_negativo(block_size_pct, "block_size_pct")

    # Sconto base dagli studi Silber (mediana ~33% per restricted stock)
    ricavi_milioni = ricavi / 1_000_000

    # Partenza dalla mediana degli studi empirici
    sconto = 0.33

    # Aggiustamento dimensionale: aziende piu' grandi -> sconto minore
    if ricavi_milioni > 500:
        sconto -= 0.08
    elif ricavi_milioni > 100:
        sconto -= 0.05
    elif ricavi_milioni > 50:
        sconto -= 0.03

    # Aziende profittevoli hanno sconto minore (maggiore certezza sui flussi)
    if profittevole:
        sconto -= 0.05

    # Blocchi piu' grandi sono piu' difficili da liquidare
    if block_size_pct > 0.10:
        sconto += 0.05
    elif block_size_pct > 0.05:
        sconto += 0.02

    # Clamp nel range ragionevole
    return max(0.10, min(0.45, sconto))


# ---------------------------------------------------------------------------
# Applicazione sconto al valore
# ---------------------------------------------------------------------------

def applica_sconto_illiquidita(
    valore_quotata: float,
    sconto: float,
) -> dict:
    """Applica lo sconto di illiquidita' al valore 'come se quotata'.

    Parametri
    ---------
    valore_quotata : float
        Valore dell'azienda stimato come se fosse quotata (deve essere > 0).
    sconto : float
        Sconto di illiquidita' da applicare (es. 0.25 per 25%).

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - valore_originale: float
        - sconto_applicato: float (importo assoluto dello sconto)
        - valore_scontato: float
        - sconto_percentuale: float
    """
    valida_positivo(valore_quotata, "valore_quotata")
    valida_non_negativo(sconto, "sconto")

    sconto_applicato = valore_quotata * sconto
    valore_scontato = valore_quotata - sconto_applicato

    return {
        "valore_originale": valore_quotata,
        "sconto_applicato": sconto_applicato,
        "valore_scontato": valore_scontato,
        "sconto_percentuale": sconto,
    }
