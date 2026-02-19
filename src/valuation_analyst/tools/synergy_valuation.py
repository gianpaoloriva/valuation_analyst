"""Modulo per la stima del valore delle sinergie in operazioni M&A.

Sinergie operative (costo e ricavo) e finanziarie.
"""

from __future__ import annotations

from valuation_analyst.utils.math_helpers import npv
from valuation_analyst.utils.validators import valida_non_negativo, valida_positivo


# ---------------------------------------------------------------------------
# Sinergie di costo
# ---------------------------------------------------------------------------

def stima_sinergie_costo(
    costi_combinati: float,
    percentuale_risparmio: float = 0.05,
    anni_realizzazione: int = 3,
    wacc: float = 0.09,
    costi_integrazione: float = 0.0,
) -> dict:
    """Stima il valore delle sinergie di costo.

    Assume realizzazione graduale lineare: anno1 = 33%, anno2 = 67%,
    anno3 = 100% (linear ramp su `anni_realizzazione`).
    Il valore attuale (PV) e' calcolato come NPV dei risparmi meno
    i costi di integrazione.

    Parametri
    ---------
    costi_combinati : float
        Base di costo combinata delle due aziende (deve essere > 0).
    percentuale_risparmio : float, opzionale
        Percentuale di risparmio atteso sui costi combinati (default 5%).
    anni_realizzazione : int, opzionale
        Numero di anni per raggiungere il pieno risparmio (default 3).
    wacc : float, opzionale
        Tasso di sconto (WACC) per il calcolo del valore attuale.
    costi_integrazione : float, opzionale
        Costi una tantum di integrazione (sostenuti al tempo 0).

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - risparmio_annuo_pieno: float
        - profilo_realizzazione: list[float] (flussi annuali)
        - pv_sinergie: float (valore attuale dei soli risparmi)
        - costi_integrazione: float
        - valore_netto_sinergie: float (pv_sinergie - costi_integrazione)
    """
    valida_positivo(costi_combinati, "costi_combinati")
    valida_non_negativo(percentuale_risparmio, "percentuale_risparmio")
    valida_non_negativo(costi_integrazione, "costi_integrazione")

    risparmio_annuo_pieno = costi_combinati * percentuale_risparmio

    # Profilo di realizzazione graduale (linear ramp)
    # Anno i: risparmio * (i / anni_realizzazione), poi pieno dal completamento
    profilo: list[float] = []
    for anno in range(1, anni_realizzazione + 1):
        pct_realizzazione = anno / anni_realizzazione
        profilo.append(risparmio_annuo_pieno * pct_realizzazione)

    # Dopo la rampa, i risparmi sono pienamente realizzati a perpetuita'.
    # Per il calcolo del PV usiamo i flussi della rampa + terminal value
    # del risparmio pieno a regime (perpetuita' a partire dall'anno N).
    # Terminal value all'anno N: risparmio_pieno / wacc
    tv_anno_n = risparmio_annuo_pieno / wacc if wacc > 0 else 0.0

    # Flussi per il calcolo NPV: [0, flusso1, flusso2, ..., flusso_N + TV]
    flussi_npv: list[float] = [0.0]  # Tempo 0 (costi integrazione gestiti a parte)
    for i, flusso in enumerate(profilo):
        if i == len(profilo) - 1:
            # Ultimo anno: flusso + terminal value
            flussi_npv.append(flusso + tv_anno_n)
        else:
            flussi_npv.append(flusso)

    pv_sinergie = npv(wacc, flussi_npv)
    valore_netto = pv_sinergie - costi_integrazione

    return {
        "risparmio_annuo_pieno": risparmio_annuo_pieno,
        "profilo_realizzazione": profilo,
        "pv_sinergie": pv_sinergie,
        "costi_integrazione": costi_integrazione,
        "valore_netto_sinergie": valore_netto,
    }


# ---------------------------------------------------------------------------
# Sinergie di ricavo
# ---------------------------------------------------------------------------

def stima_sinergie_ricavo(
    ricavi_combinati: float,
    percentuale_crescita: float = 0.02,
    margine_incrementale: float = 0.30,
    anni_realizzazione: int = 4,
    wacc: float = 0.09,
) -> dict:
    """Stima il valore delle sinergie di ricavo.

    Ricavi incrementali * margine = cash flow incrementale.
    Realizzazione graduale lineare su `anni_realizzazione`.

    Parametri
    ---------
    ricavi_combinati : float
        Ricavi combinati delle due aziende (deve essere > 0).
    percentuale_crescita : float, opzionale
        Percentuale di crescita incrementale dei ricavi (default 2%).
    margine_incrementale : float, opzionale
        Margine sui ricavi incrementali (default 30%).
    anni_realizzazione : int, opzionale
        Numero di anni per la piena realizzazione (default 4).
    wacc : float, opzionale
        Tasso di sconto per il calcolo del valore attuale.

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - ricavi_incrementali_pieno: float
        - cf_incrementale: float (cash flow incrementale a regime)
        - profilo_realizzazione: list[float] (flussi annuali)
        - pv_sinergie: float
    """
    valida_positivo(ricavi_combinati, "ricavi_combinati")
    valida_non_negativo(percentuale_crescita, "percentuale_crescita")
    valida_non_negativo(margine_incrementale, "margine_incrementale")

    ricavi_incrementali_pieno = ricavi_combinati * percentuale_crescita
    cf_incrementale = ricavi_incrementali_pieno * margine_incrementale

    # Profilo graduale con linear ramp
    profilo: list[float] = []
    for anno in range(1, anni_realizzazione + 1):
        pct_realizzazione = anno / anni_realizzazione
        profilo.append(cf_incrementale * pct_realizzazione)

    # Terminal value del cash flow incrementale a regime
    tv_anno_n = cf_incrementale / wacc if wacc > 0 else 0.0

    # Flussi NPV: [0, cf1, cf2, ..., cf_N + TV]
    flussi_npv: list[float] = [0.0]
    for i, flusso in enumerate(profilo):
        if i == len(profilo) - 1:
            flussi_npv.append(flusso + tv_anno_n)
        else:
            flussi_npv.append(flusso)

    pv_sinergie = npv(wacc, flussi_npv)

    return {
        "ricavi_incrementali_pieno": ricavi_incrementali_pieno,
        "cf_incrementale": cf_incrementale,
        "profilo_realizzazione": profilo,
        "pv_sinergie": pv_sinergie,
    }


# ---------------------------------------------------------------------------
# Sinergie finanziarie
# ---------------------------------------------------------------------------

def stima_sinergie_finanziarie(
    debito_target: float,
    risparmio_spread: float = 0.005,
    tax_rate: float = 0.25,
    perdite_fiscali_target: float = 0.0,
    additional_debt_capacity: float = 0.0,
    costo_debito_acquirente: float = 0.05,
    wacc: float = 0.09,
) -> dict:
    """Stima sinergie finanziarie (tax shields, capacita' debito).

    Tre componenti:
    1. Risparmio interessi: il target paga meno spread sul debito
       grazie al rating migliore dell'acquirente.
    2. Tax shields da NOL: le perdite fiscali del target possono essere
       utilizzate dall'acquirente per ridurre le tasse.
    3. Capacita' di debito aggiuntiva: l'entita' combinata puo' sostenere
       piu' debito, generando tax shields addizionali.

    Parametri
    ---------
    debito_target : float
        Debito totale del target.
    risparmio_spread : float, opzionale
        Riduzione dello spread sugli interessi (default 50 bps).
    tax_rate : float, opzionale
        Aliquota fiscale (default 25%).
    perdite_fiscali_target : float, opzionale
        Net Operating Losses (NOL) del target utilizzabili.
    additional_debt_capacity : float, opzionale
        Capacita' di debito aggiuntiva dell'entita' combinata.
    costo_debito_acquirente : float, opzionale
        Costo del debito dell'acquirente (default 5%).
    wacc : float, opzionale
        Tasso di sconto per il calcolo del valore attuale.

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - pv_risparmio_interessi: float
        - pv_tax_shields_nol: float
        - pv_debt_capacity: float
        - totale: float
    """
    valida_non_negativo(debito_target, "debito_target")
    valida_non_negativo(perdite_fiscali_target, "perdite_fiscali_target")
    valida_non_negativo(additional_debt_capacity, "additional_debt_capacity")

    # 1. PV del risparmio sugli interessi (perpetuita')
    # Risparmio annuo al netto delle tasse: debito * spread_saving * (1 - t)
    risparmio_interessi_annuo = debito_target * risparmio_spread * (1.0 - tax_rate)
    pv_risparmio_interessi = (
        risparmio_interessi_annuo / wacc if wacc > 0 else 0.0
    )

    # 2. PV dei tax shields dalle perdite fiscali (NOL)
    # Beneficio immediato: NOL * tax_rate (assumiamo utilizzo istantaneo)
    pv_tax_shields_nol = perdite_fiscali_target * tax_rate

    # 3. PV della capacita' di debito aggiuntiva
    # Tax shield annuo: debito_aggiuntivo * costo_debito * tax_rate
    tax_shield_debito_annuo = (
        additional_debt_capacity * costo_debito_acquirente * tax_rate
    )
    pv_debt_capacity = (
        tax_shield_debito_annuo / wacc if wacc > 0 else 0.0
    )

    totale = pv_risparmio_interessi + pv_tax_shields_nol + pv_debt_capacity

    return {
        "pv_risparmio_interessi": pv_risparmio_interessi,
        "pv_tax_shields_nol": pv_tax_shields_nol,
        "pv_debt_capacity": pv_debt_capacity,
        "totale": totale,
    }


# ---------------------------------------------------------------------------
# Stima sinergie totali
# ---------------------------------------------------------------------------

def stima_sinergie_totali(
    costi_combinati: float,
    ricavi_combinati: float,
    debito_target: float = 0.0,
    pct_risparmio_costi: float = 0.05,
    pct_crescita_ricavi: float = 0.02,
    margine_incrementale: float = 0.30,
    wacc: float = 0.09,
    costi_integrazione: float = 0.0,
    tax_rate: float = 0.25,
    probabilita_realizzazione: float = 0.65,
) -> dict:
    """Stima completa di tutte le sinergie con probabilita' di realizzazione.

    Aggrega sinergie di costo, ricavo e finanziarie, applicando un fattore
    di probabilita' di realizzazione al totale lordo.

    Parametri
    ---------
    costi_combinati : float
        Base di costo combinata delle due aziende (deve essere > 0).
    ricavi_combinati : float
        Ricavi combinati delle due aziende (deve essere > 0).
    debito_target : float, opzionale
        Debito totale del target (default 0).
    pct_risparmio_costi : float, opzionale
        Percentuale di risparmio sui costi (default 5%).
    pct_crescita_ricavi : float, opzionale
        Percentuale di crescita incrementale dei ricavi (default 2%).
    margine_incrementale : float, opzionale
        Margine sui ricavi incrementali (default 30%).
    wacc : float, opzionale
        Tasso di sconto (default 9%).
    costi_integrazione : float, opzionale
        Costi una tantum di integrazione (default 0).
    tax_rate : float, opzionale
        Aliquota fiscale (default 25%).
    probabilita_realizzazione : float, opzionale
        Probabilita' che le sinergie vengano effettivamente realizzate
        (default 65%). Applicata al totale lordo.

    Restituisce
    -----------
    dict
        Dizionario con le chiavi:
        - sinergie_costo: dict (risultato completo sinergie di costo)
        - sinergie_ricavo: dict (risultato completo sinergie di ricavo)
        - sinergie_finanziarie: dict (risultato completo sinergie finanziarie)
        - totale_lordo: float (somma PV di tutte le sinergie)
        - totale_netto: float (totale_lordo - costi_integrazione)
        - totale_aggiustato_probabilita: float (totale_netto * probabilita')
    """
    valida_positivo(costi_combinati, "costi_combinati")
    valida_positivo(ricavi_combinati, "ricavi_combinati")
    valida_non_negativo(costi_integrazione, "costi_integrazione")

    # Sinergie di costo
    sin_costo = stima_sinergie_costo(
        costi_combinati=costi_combinati,
        percentuale_risparmio=pct_risparmio_costi,
        wacc=wacc,
        costi_integrazione=0.0,  # I costi sono conteggiati a livello aggregato
    )

    # Sinergie di ricavo
    sin_ricavo = stima_sinergie_ricavo(
        ricavi_combinati=ricavi_combinati,
        percentuale_crescita=pct_crescita_ricavi,
        margine_incrementale=margine_incrementale,
        wacc=wacc,
    )

    # Sinergie finanziarie
    sin_fin = stima_sinergie_finanziarie(
        debito_target=debito_target,
        tax_rate=tax_rate,
        wacc=wacc,
    )

    # Aggregazione
    totale_lordo = sin_costo["pv_sinergie"] + sin_ricavo["pv_sinergie"] + sin_fin["totale"]
    totale_netto = totale_lordo - costi_integrazione
    totale_aggiustato = totale_netto * probabilita_realizzazione

    return {
        "sinergie_costo": sin_costo,
        "sinergie_ricavo": sin_ricavo,
        "sinergie_finanziarie": sin_fin,
        "totale_lordo": totale_lordo,
        "totale_netto": totale_netto,
        "totale_aggiustato_probabilita": totale_aggiustato,
    }
