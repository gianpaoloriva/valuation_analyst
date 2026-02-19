"""Modello DCF basato su FCFF (Free Cash Flow to Firm).

FCFF = EBIT(1-t) + Deprezzamento - CapEx - Delta WC
Sconta al WACC per ottenere il valore dell'impresa (enterprise value),
da cui si sottrae il debito netto per arrivare all'equity value.
"""

from __future__ import annotations

from valuation_analyst.models.cash_flows import CashFlowProjection, ProiezioneCashFlow
from valuation_analyst.models.valuation_result import ValuationResult
from valuation_analyst.tools.growth_models import crescita_3_fasi
from valuation_analyst.tools.terminal_value import (
    terminal_value_exit_multiple,
    terminal_value_gordon,
    verifica_terminal_value,
)
from valuation_analyst.utils.math_helpers import pv


# ---------------------------------------------------------------------------
# Calcolo FCFF per singolo anno
# ---------------------------------------------------------------------------

def calcola_fcff(
    ebit: float,
    tax_rate: float,
    capex: float,
    deprezzamento: float,
    delta_wc: float,
) -> float:
    """Calcola il Free Cash Flow to Firm per un singolo anno.

    Formula: FCFF = EBIT * (1 - t) + Deprezzamento - CapEx - Delta WC

    Parametri
    ---------
    ebit : float
        Earnings Before Interest and Taxes.
    tax_rate : float
        Aliquota fiscale effettiva (es. 0.25 per il 25 %).
    capex : float
        Capital Expenditure (valore positivo).
    deprezzamento : float
        Ammortamenti e svalutazioni (valore positivo).
    delta_wc : float
        Variazione del capitale circolante netto
        (positivo = assorbimento di cassa).

    Restituisce
    -----------
    float
        Il FCFF calcolato.
    """
    ebit_after_tax = ebit * (1.0 - tax_rate)
    return ebit_after_tax + deprezzamento - capex - delta_wc


# ---------------------------------------------------------------------------
# Proiezione FCFF multi-anno
# ---------------------------------------------------------------------------

def proietta_fcff(
    fcff_base: float,
    tassi_crescita: list[float],
    wacc: float,
) -> list[ProiezioneCashFlow]:
    """Proietta il FCFF per N anni con tassi di crescita variabili e sconta al WACC.

    Per ogni anno applica il tasso di crescita corrispondente al FCFF
    dell'anno precedente, poi sconta il flusso al valore attuale usando
    il WACC come tasso di sconto.

    Parametri
    ---------
    fcff_base : float
        FCFF dell'anno 0 (anno base, non proiettato). Deve essere > 0.
    tassi_crescita : list[float]
        Lista dei tassi di crescita, uno per ogni anno di proiezione.
    wacc : float
        Weighted Average Cost of Capital (tasso di sconto).

    Restituisce
    -----------
    list[ProiezioneCashFlow]
        Lista di proiezioni annuali con flussi scontati.
    """
    if fcff_base <= 0:
        raise ValueError(
            f"Il FCFF base deve essere positivo (ricevuto: {fcff_base})."
        )
    if not tassi_crescita:
        raise ValueError("La lista dei tassi di crescita non puo' essere vuota.")

    proiezioni: list[ProiezioneCashFlow] = []
    fcff_corrente = fcff_base

    for anno_idx, tasso_g in enumerate(tassi_crescita, start=1):
        # Applica la crescita
        fcff_corrente = fcff_corrente * (1.0 + tasso_g)

        # Sconta al valore attuale
        va = pv(fv=fcff_corrente, tasso=wacc, periodi=anno_idx)

        proiezione = ProiezioneCashFlow(
            anno=anno_idx,
            fcff=fcff_corrente,
            tasso_crescita=tasso_g,
            tasso_sconto=wacc,
            valore_attuale=va,
        )
        proiezioni.append(proiezione)

    return proiezioni


# ---------------------------------------------------------------------------
# DCF FCFF completo (multi-stage)
# ---------------------------------------------------------------------------

def calcola_dcf_fcff(
    fcff_base: float,
    wacc: float,
    crescita_alta: float = 0.15,
    crescita_stabile: float = 0.025,
    anni_alta: int = 5,
    anni_transizione: int = 5,
    metodo_terminale: str = "gordon",
    exit_multiple: float | None = None,
    ebitda_ultimo: float | None = None,
    roic_stabile: float | None = None,
) -> CashFlowProjection:
    """Calcola il DCF FCFF completo con modello multi-stage a 3 fasi.

    1. Genera i tassi di crescita (3 fasi: alta, transizione, stabile).
    2. Proietta il FCFF per il periodo esplicito.
    3. Calcola il terminal value (Gordon Growth o Exit Multiple).
    4. Sconta tutti i flussi e il TV al valore attuale.

    Parametri
    ---------
    fcff_base : float
        FCFF dell'anno base (anno 0).
    wacc : float
        Weighted Average Cost of Capital.
    crescita_alta : float
        Tasso di crescita nella fase di alta crescita (default 15 %).
    crescita_stabile : float
        Tasso di crescita perpetua (default 2.5 %).
    anni_alta : int
        Anni di alta crescita (default 5).
    anni_transizione : int
        Anni di transizione (default 5).
    metodo_terminale : str
        Metodo per il terminal value: "gordon" o "exit_multiple".
    exit_multiple : float | None
        Multiplo di uscita (richiesto se metodo_terminale == "exit_multiple").
    ebitda_ultimo : float | None
        EBITDA dell'ultimo anno (richiesto se metodo_terminale == "exit_multiple").
    roic_stabile : float | None
        ROIC nella fase stabile. Se fornito, il terminal value viene calcolato
        con reinvestment rate esplicito nel caso Gordon.

    Restituisce
    -----------
    CashFlowProjection
        Struttura completa con proiezioni annuali, TV e totali.
    """
    # Passo 1: genera i tassi di crescita a 3 fasi
    tassi = crescita_3_fasi(
        tasso_alta=crescita_alta,
        tasso_stabile=crescita_stabile,
        anni_alta=anni_alta,
        anni_transizione=anni_transizione,
    )

    # Passo 2: proietta FCFF
    proiezioni = proietta_fcff(
        fcff_base=fcff_base,
        tassi_crescita=tassi,
        wacc=wacc,
    )

    # FCFF dell'ultimo anno proiettato
    fcff_ultimo = proiezioni[-1].fcff
    assert fcff_ultimo is not None  # garantito dalla proiezione

    numero_anni = len(proiezioni)

    # Passo 3: calcola il terminal value
    metodo_tv_label: str
    exit_mult_val: float | None = None

    if metodo_terminale == "exit_multiple":
        # Metodo Exit Multiple
        if exit_multiple is None or ebitda_ultimo is None:
            raise ValueError(
                "Per il metodo exit_multiple servono sia 'exit_multiple' "
                "che 'ebitda_ultimo'."
            )
        # Proietta EBITDA dell'ultimo anno con lo stesso tasso di crescita complessivo
        # Si assume che ebitda_ultimo sia gia' il valore dell'ultimo anno proiettato
        tv = terminal_value_exit_multiple(
            metrica_ultimo_anno=ebitda_ultimo,
            multiplo_uscita=exit_multiple,
        )
        metodo_tv_label = "exit_multiple"
        exit_mult_val = exit_multiple
    else:
        # Metodo Gordon Growth (default)
        if roic_stabile is not None and roic_stabile > 0:
            # Variante Damodaran: reinvestment rate esplicito
            # RIR = g / ROIC
            rir = crescita_stabile / roic_stabile
            fcff_terminal = fcff_ultimo * (1.0 + crescita_stabile) * (1.0 - rir)
            denominatore = wacc - crescita_stabile
            if denominatore <= 0:
                raise ValueError(
                    f"Il WACC ({wacc:.4f}) deve essere superiore al tasso di "
                    f"crescita stabile ({crescita_stabile:.4f})."
                )
            tv = fcff_terminal / denominatore
        else:
            # Gordon Growth standard
            tv = terminal_value_gordon(
                cash_flow_ultimo=fcff_ultimo,
                tasso_crescita_stabile=crescita_stabile,
                tasso_sconto=wacc,
            )
        metodo_tv_label = "gordon_growth"

    # Passo 4: sconta il terminal value al presente
    tv_attuale = pv(fv=tv, tasso=wacc, periodi=numero_anni)

    # Costruisci l'oggetto CashFlowProjection
    risultato = CashFlowProjection(
        proiezioni=proiezioni,
        valore_terminale=tv,
        valore_terminale_attuale=tv_attuale,
        tipo_flusso="FCFF",
        tasso_crescita_terminale=crescita_stabile,
        tasso_sconto_terminale=wacc,
        metodo_valore_terminale=metodo_tv_label,
        exit_multiple=exit_mult_val,
    )

    return risultato


# ---------------------------------------------------------------------------
# Valutazione FCFF completa (fino al valore per azione)
# ---------------------------------------------------------------------------

def valutazione_fcff(
    ticker: str,
    ebit: float,
    tax_rate: float,
    capex: float,
    deprezzamento: float,
    delta_wc: float,
    wacc: float,
    total_debt: float,
    cash: float,
    shares_outstanding: float,
    crescita_alta: float = 0.15,
    crescita_stabile: float = 0.025,
    anni_alta: int = 5,
    anni_transizione: int = 5,
    prezzo_corrente: float | None = None,
) -> ValuationResult:
    """Esegue la valutazione DCF FCFF completa e restituisce un ValuationResult.

    Passi:
    1. Calcola il FCFF base a partire dai dati fondamentali.
    2. Proietta i flussi con il modello a 3 fasi e calcola il TV.
    3. Somma i valori attuali per ottenere l'enterprise value.
    4. Sottrae il debito netto (debito - cassa) per arrivare all'equity value.
    5. Divide per il numero di azioni per ottenere il valore per azione.
    6. Confronta con il prezzo di mercato (se disponibile).

    Parametri
    ---------
    ticker : str
        Simbolo di borsa dell'azienda.
    ebit : float
        EBIT dell'anno base.
    tax_rate : float
        Aliquota fiscale effettiva.
    capex : float
        Capital Expenditure dell'anno base.
    deprezzamento : float
        Ammortamenti dell'anno base.
    delta_wc : float
        Variazione del capitale circolante dell'anno base.
    wacc : float
        Weighted Average Cost of Capital.
    total_debt : float
        Debito totale.
    cash : float
        Cassa e equivalenti.
    shares_outstanding : float
        Numero di azioni in circolazione (in milioni o unita' coerenti).
    crescita_alta : float
        Tasso di crescita nella fase alta (default 15 %).
    crescita_stabile : float
        Tasso di crescita perpetua (default 2.5 %).
    anni_alta : int
        Anni di alta crescita (default 5).
    anni_transizione : int
        Anni di transizione (default 5).
    prezzo_corrente : float | None
        Prezzo corrente di mercato per il confronto (facoltativo).

    Restituisce
    -----------
    ValuationResult
        Risultato completo della valutazione.
    """
    # Passo 1: calcola FCFF base
    fcff_base = calcola_fcff(
        ebit=ebit,
        tax_rate=tax_rate,
        capex=capex,
        deprezzamento=deprezzamento,
        delta_wc=delta_wc,
    )

    if fcff_base <= 0:
        raise ValueError(
            f"Il FCFF base calcolato e' negativo o zero ({fcff_base:.2f}). "
            "Non e' possibile eseguire una valutazione DCF standard con FCFF <= 0."
        )

    # Passo 2: DCF multi-stage
    dcf = calcola_dcf_fcff(
        fcff_base=fcff_base,
        wacc=wacc,
        crescita_alta=crescita_alta,
        crescita_stabile=crescita_stabile,
        anni_alta=anni_alta,
        anni_transizione=anni_transizione,
        metodo_terminale="gordon",
    )

    # Passo 3: enterprise value
    enterprise_value = dcf.valore_totale

    # Passo 4: equity value = EV - debito netto
    debito_netto = total_debt - cash
    equity_value = enterprise_value - debito_netto

    # Passo 5: valore per azione
    if shares_outstanding <= 0:
        raise ValueError(
            f"Il numero di azioni deve essere positivo (ricevuto: {shares_outstanding})."
        )
    valore_per_azione = equity_value / shares_outstanding

    # Passo 6: verifica terminal value
    tv_check = verifica_terminal_value(
        tv=dcf.valore_terminale_attuale,
        valore_totale=enterprise_value,
    )

    # Costruisci le note
    note: list[str] = []
    if not tv_check["accettabile"]:
        note.append(tv_check["messaggio"])

    if equity_value < 0:
        note.append(
            f"ATTENZIONE: l'equity value e' negativo ({equity_value:,.2f}M). "
            "Il debito netto supera l'enterprise value."
        )

    # Parametri utilizzati
    parametri: dict[str, float | str | int | bool] = {
        "wacc": wacc,
        "crescita_alta": crescita_alta,
        "crescita_stabile": crescita_stabile,
        "anni_alta": anni_alta,
        "anni_transizione": anni_transizione,
        "tax_rate": tax_rate,
        "metodo_terminale": "gordon_growth",
    }
    if prezzo_corrente is not None:
        parametri["prezzo_corrente"] = prezzo_corrente

    # Dettagli intermedi
    dettagli: dict[str, float | str | list[float]] = {
        "fcff_base": fcff_base,
        "enterprise_value": enterprise_value,
        "debito_netto": debito_netto,
        "valore_attuale_flussi": dcf.valore_attuale_flussi,
        "valore_terminale": dcf.valore_terminale,
        "valore_terminale_attuale": dcf.valore_terminale_attuale,
        "percentuale_tv": dcf.percentuale_valore_terminale,
        "flussi_proiettati": [
            p.fcff for p in dcf.proiezioni if p.fcff is not None
        ],
    }

    return ValuationResult(
        ticker=ticker.upper(),
        metodo="DCF_FCFF",
        valore_equity=equity_value,
        valore_per_azione=valore_per_azione,
        parametri=parametri,
        dettagli=dettagli,
        note=note,
    )
