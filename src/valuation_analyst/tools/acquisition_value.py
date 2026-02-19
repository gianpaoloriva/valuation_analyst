"""Modulo per il calcolo del valore di acquisizione e analisi M&A.

Valore Acquisizione = Valore Standalone Target + Sinergie - Costi Integrazione
"""

from __future__ import annotations

from valuation_analyst.models.valuation_result import ValuationResult
from valuation_analyst.tools.synergy_valuation import stima_sinergie_totali
from valuation_analyst.utils.validators import valida_non_negativo, valida_positivo


# ---------------------------------------------------------------------------
# Valore di acquisizione
# ---------------------------------------------------------------------------

def calcola_valore_acquisizione(
    valore_standalone_target: float,
    valore_sinergie: float,
    costi_integrazione: float = 0.0,
) -> dict:
    """Calcola il valore totale dell'acquisizione.

    Formula: V_acquisizione = V_standalone + Sinergie - Costi integrazione

    Parametri
    ---------
    valore_standalone_target : float
        Valore standalone del target (deve essere > 0).
    valore_sinergie : float
        Valore attuale delle sinergie attese.
    costi_integrazione : float, opzionale
        Costi una tantum di integrazione (default 0).

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - valore_standalone: float
        - sinergie: float
        - costi_integrazione: float
        - valore_acquisizione: float
    """
    valida_positivo(valore_standalone_target, "valore_standalone_target")
    valida_non_negativo(costi_integrazione, "costi_integrazione")

    valore_acquisizione = (
        valore_standalone_target + valore_sinergie - costi_integrazione
    )

    return {
        "valore_standalone": valore_standalone_target,
        "sinergie": valore_sinergie,
        "costi_integrazione": costi_integrazione,
        "valore_acquisizione": valore_acquisizione,
    }


# ---------------------------------------------------------------------------
# Analisi accretion / dilution
# ---------------------------------------------------------------------------

def analisi_accretion_dilution(
    utile_acquirente: float,
    utile_target: float,
    azioni_acquirente: float,
    prezzo_offerta: float,
    azioni_target: float,
    sinergie_annue: float = 0.0,
    costi_integrazione_annui: float = 0.0,
    struttura_deal: str = "cash",
    prezzo_azione_acquirente: float | None = None,
) -> dict:
    """Analisi accretion/dilution dell'EPS post-acquisizione.

    Per un cash deal:
        EPS_post = (Utile_A + Utile_T + Sinergie - Costi) / Azioni_A

    Per uno stock deal:
        Nuove_Azioni = (Prezzo_offerta * Azioni_T) / Prezzo_azione_A
        EPS_post = (Utile_A + Utile_T + Sinergie - Costi) / (Azioni_A + Nuove_Azioni)

    Parametri
    ---------
    utile_acquirente : float
        Utile netto dell'acquirente.
    utile_target : float
        Utile netto del target.
    azioni_acquirente : float
        Numero di azioni dell'acquirente in circolazione (deve essere > 0).
    prezzo_offerta : float
        Prezzo offerto per azione del target (deve essere > 0).
    azioni_target : float
        Numero di azioni del target in circolazione (deve essere > 0).
    sinergie_annue : float, opzionale
        Sinergie annuali attese a regime (default 0).
    costi_integrazione_annui : float, opzionale
        Costi di integrazione annualizzati (default 0).
    struttura_deal : str, opzionale
        Struttura del deal: "cash", "stock" o "misto" (default "cash").
    prezzo_azione_acquirente : float | None, opzionale
        Prezzo per azione dell'acquirente (necessario per stock deal).

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - eps_pre: float (EPS pre-acquisizione dell'acquirente)
        - eps_post: float (EPS post-acquisizione)
        - accretion_dilution_pct: float (variazione % dell'EPS)
        - is_accretive: bool
        - dettagli: dict (utile_combinato, azioni_post, nuove_azioni, ecc.)
    """
    valida_positivo(azioni_acquirente, "azioni_acquirente")
    valida_positivo(prezzo_offerta, "prezzo_offerta")
    valida_positivo(azioni_target, "azioni_target")

    # EPS pre-acquisizione dell'acquirente
    eps_pre = utile_acquirente / azioni_acquirente

    # Utile combinato
    utile_combinato = (
        utile_acquirente + utile_target + sinergie_annue - costi_integrazione_annui
    )

    nuove_azioni = 0.0
    azioni_post = azioni_acquirente

    if struttura_deal in ("stock", "misto"):
        if prezzo_azione_acquirente is None or prezzo_azione_acquirente <= 0:
            raise ValueError(
                "Il prezzo per azione dell'acquirente e' necessario "
                "per un deal in azioni (stock o misto)."
            )
        # Valore totale dell'offerta
        valore_offerta_totale = prezzo_offerta * azioni_target

        if struttura_deal == "stock":
            # Tutto in azioni
            nuove_azioni = valore_offerta_totale / prezzo_azione_acquirente
        else:
            # Misto: assumiamo 50% cash e 50% azioni
            nuove_azioni = (valore_offerta_totale * 0.5) / prezzo_azione_acquirente

        azioni_post = azioni_acquirente + nuove_azioni

    # EPS post-acquisizione
    eps_post = utile_combinato / azioni_post

    # Accretion / Dilution
    if eps_pre != 0:
        accretion_dilution_pct = (eps_post - eps_pre) / abs(eps_pre)
    else:
        accretion_dilution_pct = 0.0

    is_accretive = eps_post > eps_pre

    return {
        "eps_pre": eps_pre,
        "eps_post": eps_post,
        "accretion_dilution_pct": accretion_dilution_pct,
        "is_accretive": is_accretive,
        "dettagli": {
            "utile_acquirente": utile_acquirente,
            "utile_target": utile_target,
            "sinergie_annue": sinergie_annue,
            "costi_integrazione_annui": costi_integrazione_annui,
            "utile_combinato": utile_combinato,
            "azioni_acquirente": azioni_acquirente,
            "nuove_azioni": nuove_azioni,
            "azioni_post": azioni_post,
            "struttura_deal": struttura_deal,
            "prezzo_offerta": prezzo_offerta,
            "valore_offerta_totale": prezzo_offerta * azioni_target,
        },
    }


# ---------------------------------------------------------------------------
# Premio dell'offerta
# ---------------------------------------------------------------------------

def premio_offerta(
    prezzo_offerta: float,
    prezzo_pre_annuncio: float,
) -> dict:
    """Calcola il premio dell'offerta rispetto al prezzo pre-annuncio.

    Parametri
    ---------
    prezzo_offerta : float
        Prezzo offerto per azione del target (deve essere > 0).
    prezzo_pre_annuncio : float
        Prezzo di mercato del target prima dell'annuncio (deve essere > 0).

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - premio_pct: float (percentuale, es. 0.30 per 30%)
        - prezzo_offerta: float
        - prezzo_pre_annuncio: float
        - confronto_benchmark: str (commento rispetto ai benchmark di mercato)
    """
    valida_positivo(prezzo_offerta, "prezzo_offerta")
    valida_positivo(prezzo_pre_annuncio, "prezzo_pre_annuncio")

    premio_pct = (prezzo_offerta - prezzo_pre_annuncio) / prezzo_pre_annuncio

    # Confronto con benchmark storici (mediana premi M&A ~25-30%)
    if premio_pct < 0:
        confronto = (
            f"Premio negativo ({premio_pct:.1%}): l'offerta e' inferiore al prezzo "
            "di mercato. Potrebbe essere un'offerta ostile non competitiva."
        )
    elif premio_pct < 0.15:
        confronto = (
            f"Premio contenuto ({premio_pct:.1%}): inferiore alla mediana storica "
            "(~25-30%). Rischio di rifiuto da parte del target."
        )
    elif premio_pct <= 0.35:
        confronto = (
            f"Premio nella norma ({premio_pct:.1%}): in linea con la mediana storica "
            "delle transazioni M&A (25-30%)."
        )
    elif premio_pct <= 0.50:
        confronto = (
            f"Premio elevato ({premio_pct:.1%}): superiore alla mediana storica. "
            "Verificare che le sinergie giustifichino il sovrapprezzo."
        )
    else:
        confronto = (
            f"Premio molto elevato ({premio_pct:.1%}): ben oltre la mediana storica. "
            "Rischio di overpaying significativo."
        )

    return {
        "premio_pct": premio_pct,
        "prezzo_offerta": prezzo_offerta,
        "prezzo_pre_annuncio": prezzo_pre_annuncio,
        "confronto_benchmark": confronto,
    }


# ---------------------------------------------------------------------------
# Valutazione M&A completa
# ---------------------------------------------------------------------------

def valutazione_ma_completa(
    ticker_acquirente: str,
    ticker_target: str,
    valore_standalone_acquirente: float,
    valore_standalone_target: float,
    sinergie_totali: float,
    costi_integrazione: float,
    prezzo_offerta_per_azione: float,
    azioni_target: float,
    utile_acquirente: float,
    utile_target: float,
    azioni_acquirente: float,
    struttura_deal: str = "cash",
    prezzo_azione_acquirente: float | None = None,
    prezzo_pre_annuncio: float | None = None,
) -> ValuationResult:
    """Valutazione M&A completa con tutti i dettagli.

    Integra:
    - Calcolo del valore di acquisizione
    - Analisi accretion/dilution dell'EPS
    - Calcolo del premio dell'offerta (se prezzo pre-annuncio disponibile)

    Parametri
    ---------
    ticker_acquirente : str
        Ticker dell'acquirente.
    ticker_target : str
        Ticker del target.
    valore_standalone_acquirente : float
        Valore standalone dell'acquirente (deve essere > 0).
    valore_standalone_target : float
        Valore standalone del target (deve essere > 0).
    sinergie_totali : float
        Valore attuale delle sinergie totali attese.
    costi_integrazione : float
        Costi una tantum di integrazione.
    prezzo_offerta_per_azione : float
        Prezzo offerto per azione del target (deve essere > 0).
    azioni_target : float
        Numero di azioni del target in circolazione (deve essere > 0).
    utile_acquirente : float
        Utile netto dell'acquirente.
    utile_target : float
        Utile netto del target.
    azioni_acquirente : float
        Numero di azioni dell'acquirente in circolazione (deve essere > 0).
    struttura_deal : str, opzionale
        Struttura del deal: "cash", "stock" o "misto" (default "cash").
    prezzo_azione_acquirente : float | None, opzionale
        Prezzo per azione dell'acquirente (necessario per stock deal).
    prezzo_pre_annuncio : float | None, opzionale
        Prezzo del target prima dell'annuncio (per calcolo premio offerta).

    Restituisce
    -----------
    ValuationResult
        Risultato completo della valutazione M&A.
    """
    valida_positivo(valore_standalone_acquirente, "valore_standalone_acquirente")
    valida_positivo(valore_standalone_target, "valore_standalone_target")

    # 1. Valore di acquisizione
    risultato_acq = calcola_valore_acquisizione(
        valore_standalone_target=valore_standalone_target,
        valore_sinergie=sinergie_totali,
        costi_integrazione=costi_integrazione,
    )

    # 2. Valore totale dell'offerta
    valore_offerta_totale = prezzo_offerta_per_azione * azioni_target

    # 3. Valore creato/distrutto per l'acquirente
    # Se il prezzo pagato e' superiore al valore di acquisizione,
    # il deal distrugge valore per l'acquirente
    valore_creato = risultato_acq["valore_acquisizione"] - valore_offerta_totale

    # 4. Analisi accretion/dilution
    # Stimiamo le sinergie annue come approssimazione (sinergie/10 come proxy annuale)
    sinergie_annue_stimate = sinergie_totali * 0.09  # wacc * PV ~ flusso annuo
    risultato_ad = analisi_accretion_dilution(
        utile_acquirente=utile_acquirente,
        utile_target=utile_target,
        azioni_acquirente=azioni_acquirente,
        prezzo_offerta=prezzo_offerta_per_azione,
        azioni_target=azioni_target,
        sinergie_annue=sinergie_annue_stimate,
        struttura_deal=struttura_deal,
        prezzo_azione_acquirente=prezzo_azione_acquirente,
    )

    # 5. Premio dell'offerta (se prezzo pre-annuncio disponibile)
    risultato_premio = None
    if prezzo_pre_annuncio is not None and prezzo_pre_annuncio > 0:
        risultato_premio = premio_offerta(
            prezzo_offerta=prezzo_offerta_per_azione,
            prezzo_pre_annuncio=prezzo_pre_annuncio,
        )

    # 6. Valore equity combinato post-deal
    valore_equity_combinato = (
        valore_standalone_acquirente
        + risultato_acq["valore_acquisizione"]
        - valore_offerta_totale
    )

    # Valore per azione post-deal
    azioni_post = risultato_ad["dettagli"]["azioni_post"]
    valore_per_azione_post = valore_equity_combinato / azioni_post

    # Note
    note: list[str] = []
    if valore_creato > 0:
        note.append(
            f"Deal crea valore per l'acquirente: {valore_creato:,.0f} "
            f"(valore acquisizione > prezzo pagato)"
        )
    elif valore_creato < 0:
        note.append(
            f"Deal distrugge valore per l'acquirente: {valore_creato:,.0f} "
            f"(prezzo pagato > valore acquisizione)"
        )
    else:
        note.append("Deal a fair value: prezzo pagato = valore acquisizione")

    if risultato_ad["is_accretive"]:
        note.append(
            f"EPS accretive: +{risultato_ad['accretion_dilution_pct']:.1%}"
        )
    else:
        note.append(
            f"EPS dilutive: {risultato_ad['accretion_dilution_pct']:.1%}"
        )

    if risultato_premio is not None:
        note.append(risultato_premio["confronto_benchmark"])

    # Dettagli completi
    dettagli: dict[str, float | str | list[float]] = {
        "ticker_acquirente": ticker_acquirente,
        "ticker_target": ticker_target,
        "valore_standalone_acquirente": valore_standalone_acquirente,
        "valore_standalone_target": valore_standalone_target,
        "sinergie_totali": sinergie_totali,
        "costi_integrazione": costi_integrazione,
        "valore_acquisizione": risultato_acq["valore_acquisizione"],
        "valore_offerta_totale": valore_offerta_totale,
        "valore_creato_distrutto": valore_creato,
        "prezzo_offerta_per_azione": prezzo_offerta_per_azione,
        "eps_pre": risultato_ad["eps_pre"],
        "eps_post": risultato_ad["eps_post"],
        "accretion_dilution_pct": risultato_ad["accretion_dilution_pct"],
        "struttura_deal": struttura_deal,
    }

    if risultato_premio is not None:
        dettagli["premio_offerta_pct"] = risultato_premio["premio_pct"]

    # Parametri
    parametri: dict[str, float | str | int | bool] = {
        "ticker_acquirente": ticker_acquirente,
        "ticker_target": ticker_target,
        "struttura_deal": struttura_deal,
        "prezzo_offerta_per_azione": prezzo_offerta_per_azione,
        "azioni_target": azioni_target,
    }

    return ValuationResult(
        ticker=f"{ticker_acquirente}+{ticker_target}",
        metodo="M&A_ACQUISITION",
        valore_equity=valore_equity_combinato,
        valore_per_azione=valore_per_azione_post,
        parametri=parametri,
        dettagli=dettagli,
        note=note,
    )
