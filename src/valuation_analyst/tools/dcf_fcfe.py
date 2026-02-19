"""Modello DCF basato su FCFE (Free Cash Flow to Equity).

FCFE = Utile Netto + Deprezzamento - CapEx - Delta WC - Rimborso Debito Netto
Sconta al Costo dell'Equity per ottenere direttamente il valore
dell'equity, senza passare dall'enterprise value.
"""

from __future__ import annotations

from valuation_analyst.models.cash_flows import CashFlowProjection, ProiezioneCashFlow
from valuation_analyst.models.valuation_result import ValuationResult
from valuation_analyst.tools.growth_models import crescita_3_fasi
from valuation_analyst.tools.terminal_value import (
    terminal_value_gordon,
    verifica_terminal_value,
)
from valuation_analyst.utils.math_helpers import pv


# ---------------------------------------------------------------------------
# Calcolo FCFE per singolo anno
# ---------------------------------------------------------------------------

def calcola_fcfe(
    utile_netto: float,
    deprezzamento: float,
    capex: float,
    delta_wc: float,
    rimborso_debito_netto: float = 0.0,
) -> float:
    """Calcola il Free Cash Flow to Equity per un singolo anno.

    Formula: FCFE = Utile Netto + Deprezzamento - CapEx - Delta WC
                    - Rimborso Debito Netto

    Il rimborso debito netto e' positivo se l'azienda rimborsa piu'
    debito di quanto ne emetta (riduzione dell'indebitamento), negativo
    nel caso contrario (aumento dell'indebitamento).

    Parametri
    ---------
    utile_netto : float
        Utile netto (net income).
    deprezzamento : float
        Ammortamenti e svalutazioni (valore positivo).
    capex : float
        Capital Expenditure (valore positivo).
    delta_wc : float
        Variazione del capitale circolante netto
        (positivo = assorbimento di cassa).
    rimborso_debito_netto : float
        Rimborso netto del debito (rimborsi - nuove emissioni).
        Default 0.0 (struttura del capitale costante).

    Restituisce
    -----------
    float
        Il FCFE calcolato.
    """
    return utile_netto + deprezzamento - capex - delta_wc - rimborso_debito_netto


# ---------------------------------------------------------------------------
# Calcolo FCFE partendo da FCFF
# ---------------------------------------------------------------------------

def calcola_fcfe_da_fcff(
    fcff: float,
    interessi: float,
    tax_rate: float,
    nuovo_debito_netto: float = 0.0,
) -> float:
    """Calcola il FCFE partendo dal FCFF.

    Formula: FCFE = FCFF - Interessi * (1 - t) + Nuovo Debito Netto

    Parametri
    ---------
    fcff : float
        Free Cash Flow to Firm.
    interessi : float
        Interessi passivi (valore positivo).
    tax_rate : float
        Aliquota fiscale effettiva (es. 0.25 per il 25 %).
    nuovo_debito_netto : float
        Nuovo debito emesso al netto dei rimborsi. Positivo se
        l'azienda si indebita di piu', negativo se rimborsa.
        Default 0.0.

    Restituisce
    -----------
    float
        Il FCFE calcolato.
    """
    interessi_after_tax = interessi * (1.0 - tax_rate)
    return fcff - interessi_after_tax + nuovo_debito_netto


# ---------------------------------------------------------------------------
# Proiezione FCFE multi-anno
# ---------------------------------------------------------------------------

def proietta_fcfe(
    fcfe_base: float,
    tassi_crescita: list[float],
    costo_equity: float,
) -> list[ProiezioneCashFlow]:
    """Proietta il FCFE per N anni con tassi di crescita variabili e sconta al costo equity.

    Per ogni anno applica il tasso di crescita corrispondente al FCFE
    dell'anno precedente, poi sconta il flusso al valore attuale usando
    il costo dell'equity come tasso di sconto.

    Parametri
    ---------
    fcfe_base : float
        FCFE dell'anno 0 (anno base, non proiettato). Deve essere > 0.
    tassi_crescita : list[float]
        Lista dei tassi di crescita, uno per ogni anno di proiezione.
    costo_equity : float
        Costo dell'equity (Ke), usato come tasso di sconto.

    Restituisce
    -----------
    list[ProiezioneCashFlow]
        Lista di proiezioni annuali con flussi scontati.
    """
    if fcfe_base <= 0:
        raise ValueError(
            f"Il FCFE base deve essere positivo (ricevuto: {fcfe_base})."
        )
    if not tassi_crescita:
        raise ValueError("La lista dei tassi di crescita non puo' essere vuota.")

    proiezioni: list[ProiezioneCashFlow] = []
    fcfe_corrente = fcfe_base

    for anno_idx, tasso_g in enumerate(tassi_crescita, start=1):
        # Applica la crescita
        fcfe_corrente = fcfe_corrente * (1.0 + tasso_g)

        # Sconta al valore attuale
        va = pv(fv=fcfe_corrente, tasso=costo_equity, periodi=anno_idx)

        proiezione = ProiezioneCashFlow(
            anno=anno_idx,
            fcfe=fcfe_corrente,
            tasso_crescita=tasso_g,
            tasso_sconto=costo_equity,
            valore_attuale=va,
        )
        proiezioni.append(proiezione)

    return proiezioni


# ---------------------------------------------------------------------------
# DCF FCFE completo (multi-stage)
# ---------------------------------------------------------------------------

def calcola_dcf_fcfe(
    fcfe_base: float,
    costo_equity: float,
    crescita_alta: float = 0.12,
    crescita_stabile: float = 0.025,
    anni_alta: int = 5,
    anni_transizione: int = 5,
) -> CashFlowProjection:
    """Calcola il DCF FCFE completo con modello multi-stage a 3 fasi.

    1. Genera i tassi di crescita (3 fasi: alta, transizione, stabile).
    2. Proietta il FCFE per il periodo esplicito.
    3. Calcola il terminal value con Gordon Growth Model.
    4. Sconta tutti i flussi e il TV al valore attuale.

    Parametri
    ---------
    fcfe_base : float
        FCFE dell'anno base (anno 0).
    costo_equity : float
        Costo dell'equity (Ke).
    crescita_alta : float
        Tasso di crescita nella fase di alta crescita (default 12 %).
    crescita_stabile : float
        Tasso di crescita perpetua (default 2.5 %).
    anni_alta : int
        Anni di alta crescita (default 5).
    anni_transizione : int
        Anni di transizione (default 5).

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

    # Passo 2: proietta FCFE
    proiezioni = proietta_fcfe(
        fcfe_base=fcfe_base,
        tassi_crescita=tassi,
        costo_equity=costo_equity,
    )

    # FCFE dell'ultimo anno proiettato
    fcfe_ultimo = proiezioni[-1].fcfe
    assert fcfe_ultimo is not None  # garantito dalla proiezione

    numero_anni = len(proiezioni)

    # Passo 3: terminal value con Gordon Growth
    tv = terminal_value_gordon(
        cash_flow_ultimo=fcfe_ultimo,
        tasso_crescita_stabile=crescita_stabile,
        tasso_sconto=costo_equity,
    )

    # Passo 4: sconta il terminal value al presente
    tv_attuale = pv(fv=tv, tasso=costo_equity, periodi=numero_anni)

    # Costruisci l'oggetto CashFlowProjection
    risultato = CashFlowProjection(
        proiezioni=proiezioni,
        valore_terminale=tv,
        valore_terminale_attuale=tv_attuale,
        tipo_flusso="FCFE",
        tasso_crescita_terminale=crescita_stabile,
        tasso_sconto_terminale=costo_equity,
        metodo_valore_terminale="gordon_growth",
    )

    return risultato


# ---------------------------------------------------------------------------
# Valutazione FCFE completa (fino al valore per azione)
# ---------------------------------------------------------------------------

def valutazione_fcfe(
    ticker: str,
    utile_netto: float,
    deprezzamento: float,
    capex: float,
    delta_wc: float,
    costo_equity: float,
    shares_outstanding: float,
    rimborso_debito_netto: float = 0.0,
    crescita_alta: float = 0.12,
    crescita_stabile: float = 0.025,
    anni_alta: int = 5,
    anni_transizione: int = 5,
    prezzo_corrente: float | None = None,
) -> ValuationResult:
    """Esegue la valutazione DCF FCFE completa e restituisce un ValuationResult.

    A differenza del modello FCFF, il modello FCFE sconta i flussi al
    costo dell'equity e produce direttamente l'equity value, senza
    bisogno di sottrarre il debito netto.

    Passi:
    1. Calcola il FCFE base a partire dai dati fondamentali.
    2. Proietta i flussi con il modello a 3 fasi e calcola il TV.
    3. Somma i valori attuali per ottenere l'equity value.
    4. Divide per il numero di azioni per il valore per azione.
    5. Confronta con il prezzo di mercato (se disponibile).

    Parametri
    ---------
    ticker : str
        Simbolo di borsa dell'azienda.
    utile_netto : float
        Utile netto dell'anno base.
    deprezzamento : float
        Ammortamenti dell'anno base.
    capex : float
        Capital Expenditure dell'anno base.
    delta_wc : float
        Variazione del capitale circolante dell'anno base.
    costo_equity : float
        Costo dell'equity (Ke).
    shares_outstanding : float
        Numero di azioni in circolazione.
    rimborso_debito_netto : float
        Rimborso netto del debito (default 0.0).
    crescita_alta : float
        Tasso di crescita nella fase alta (default 12 %).
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
    # Passo 1: calcola FCFE base
    fcfe_base = calcola_fcfe(
        utile_netto=utile_netto,
        deprezzamento=deprezzamento,
        capex=capex,
        delta_wc=delta_wc,
        rimborso_debito_netto=rimborso_debito_netto,
    )

    if fcfe_base <= 0:
        raise ValueError(
            f"Il FCFE base calcolato e' negativo o zero ({fcfe_base:.2f}). "
            "Non e' possibile eseguire una valutazione DCF standard con FCFE <= 0."
        )

    # Passo 2: DCF multi-stage
    dcf = calcola_dcf_fcfe(
        fcfe_base=fcfe_base,
        costo_equity=costo_equity,
        crescita_alta=crescita_alta,
        crescita_stabile=crescita_stabile,
        anni_alta=anni_alta,
        anni_transizione=anni_transizione,
    )

    # Passo 3: equity value (diretto, senza sottrarre debito netto)
    equity_value = dcf.valore_totale

    # Passo 4: valore per azione
    if shares_outstanding <= 0:
        raise ValueError(
            f"Il numero di azioni deve essere positivo (ricevuto: {shares_outstanding})."
        )
    valore_per_azione = equity_value / shares_outstanding

    # Passo 5: verifica terminal value
    tv_check = verifica_terminal_value(
        tv=dcf.valore_terminale_attuale,
        valore_totale=equity_value,
    )

    # Costruisci le note
    note: list[str] = []
    if not tv_check["accettabile"]:
        note.append(tv_check["messaggio"])

    if equity_value < 0:
        note.append(
            f"ATTENZIONE: l'equity value e' negativo ({equity_value:,.2f}M). "
            "Verificare le ipotesi di crescita e il costo dell'equity."
        )

    # Parametri utilizzati
    parametri: dict[str, float | str | int | bool] = {
        "costo_equity": costo_equity,
        "crescita_alta": crescita_alta,
        "crescita_stabile": crescita_stabile,
        "anni_alta": anni_alta,
        "anni_transizione": anni_transizione,
        "rimborso_debito_netto": rimborso_debito_netto,
        "metodo_terminale": "gordon_growth",
    }
    if prezzo_corrente is not None:
        parametri["prezzo_corrente"] = prezzo_corrente

    # Dettagli intermedi
    dettagli: dict[str, float | str | list[float]] = {
        "fcfe_base": fcfe_base,
        "equity_value": equity_value,
        "valore_attuale_flussi": dcf.valore_attuale_flussi,
        "valore_terminale": dcf.valore_terminale,
        "valore_terminale_attuale": dcf.valore_terminale_attuale,
        "percentuale_tv": dcf.percentuale_valore_terminale,
        "flussi_proiettati": [
            p.fcfe for p in dcf.proiezioni if p.fcfe is not None
        ],
    }

    return ValuationResult(
        ticker=ticker.upper(),
        metodo="DCF_FCFE",
        valore_equity=equity_value,
        valore_per_azione=valore_per_azione,
        parametri=parametri,
        dettagli=dettagli,
        note=note,
    )
