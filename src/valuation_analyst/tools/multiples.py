"""Modulo per il calcolo e l'analisi dei multipli di mercato.

Multipli supportati: P/E, EV/EBITDA, P/B, EV/Sales, PEG, EV/EBIT.
Fornisce funzioni per calcolare singoli multipli, statistiche descrittive
e valori impliciti per la valutazione relativa tramite comparabili.
"""

from __future__ import annotations

import logging
import statistics
from datetime import date

from valuation_analyst.models.comparable import (
    AnalisiComparabili,
    Comparabile,
    StatisticheMultiplo,
)
from valuation_analyst.models.valuation_result import ValuationResult

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Calcolo dei singoli multipli
# ---------------------------------------------------------------------------

def calcola_pe(prezzo: float, eps: float) -> float | None:
    """Calcola P/E ratio. Ritorna None se EPS <= 0."""
    if eps <= 0:
        return None
    return prezzo / eps


def calcola_ev_ebitda(enterprise_value: float, ebitda: float) -> float | None:
    """Calcola EV/EBITDA. Ritorna None se EBITDA <= 0."""
    if ebitda <= 0:
        return None
    return enterprise_value / ebitda


def calcola_pb(market_cap: float, book_value: float) -> float | None:
    """Calcola P/B ratio. Ritorna None se BV <= 0."""
    if book_value <= 0:
        return None
    return market_cap / book_value


def calcola_ev_sales(enterprise_value: float, ricavi: float) -> float | None:
    """Calcola EV/Sales. Ritorna None se ricavi <= 0."""
    if ricavi <= 0:
        return None
    return enterprise_value / ricavi


def calcola_peg(pe: float | None, crescita_eps_pct: float) -> float | None:
    """Calcola PEG ratio. crescita_eps_pct e' in percentuale (es. 15 per 15%).

    Ritorna None se P/E o crescita non validi.
    """
    if pe is None or pe <= 0 or crescita_eps_pct <= 0:
        return None
    return pe / crescita_eps_pct


def calcola_ev_ebit(enterprise_value: float, ebit: float) -> float | None:
    """Calcola EV/EBIT. Ritorna None se EBIT <= 0."""
    if ebit <= 0:
        return None
    return enterprise_value / ebit


# ---------------------------------------------------------------------------
# Statistiche descrittive e pulizia dei dati
# ---------------------------------------------------------------------------

def statistiche_multiplo(
    valori: list[float | None],
    nome: str = "",
) -> StatisticheMultiplo:
    """Calcola statistiche descrittive per un multiplo.

    Filtra None e valori negativi. Calcola media, mediana, min, max,
    deviazione standard e quartili.

    Parametri
    ---------
    valori : list[float | None]
        Lista dei valori grezzi del multiplo (puo' contenere None).
    nome : str, opzionale
        Nome identificativo del multiplo (es. ``"pe_ratio"``).

    Restituisce
    -----------
    StatisticheMultiplo
        Dataclass con tutte le statistiche descrittive calcolate.
    """
    # Pulizia: rimuovi None e valori non positivi
    valori_puliti = [v for v in valori if v is not None and v > 0]

    if not valori_puliti:
        return StatisticheMultiplo(
            nome_multiplo=nome,
            mediana=0.0,
            media=0.0,
            minimo=0.0,
            massimo=0.0,
            deviazione_standard=0.0,
            primo_quartile=0.0,
            terzo_quartile=0.0,
            num_osservazioni=0,
        )

    valori_ordinati = sorted(valori_puliti)
    n = len(valori_ordinati)

    # Calcolo media e mediana con il modulo statistics
    media = statistics.mean(valori_ordinati)
    mediana = statistics.median(valori_ordinati)

    # Deviazione standard (campionaria se n > 1, altrimenti 0)
    dev_std = statistics.stdev(valori_ordinati) if n > 1 else 0.0

    # Calcolo quartili tramite indici sulla lista ordinata
    q1_idx = n // 4
    q3_idx = (3 * n) // 4

    primo_q = valori_ordinati[q1_idx]
    terzo_q = valori_ordinati[min(q3_idx, n - 1)]

    return StatisticheMultiplo(
        nome_multiplo=nome,
        mediana=mediana,
        media=media,
        minimo=valori_ordinati[0],
        massimo=valori_ordinati[-1],
        deviazione_standard=dev_std,
        primo_quartile=primo_q,
        terzo_quartile=terzo_q,
        num_osservazioni=n,
    )


def rimuovi_outlier(
    valori: list[float],
    num_deviazioni: float = 3.0,
) -> list[float]:
    """Rimuove outlier oltre N deviazioni standard dalla mediana.

    Parametri
    ---------
    valori : list[float]
        Lista di valori numerici da filtrare.
    num_deviazioni : float, opzionale
        Numero di deviazioni standard dalla mediana oltre il quale
        un valore viene considerato outlier (default: 3.0).

    Restituisce
    -----------
    list[float]
        Lista filtrata senza gli outlier.
    """
    if len(valori) < 3:
        # Con meno di 3 valori non ha senso rimuovere outlier
        return list(valori)

    mediana = statistics.median(valori)
    dev_std = statistics.stdev(valori)

    # Se la deviazione standard e' nulla, tutti i valori sono uguali
    if dev_std == 0:
        return list(valori)

    soglia_inf = mediana - num_deviazioni * dev_std
    soglia_sup = mediana + num_deviazioni * dev_std

    risultato = [v for v in valori if soglia_inf <= v <= soglia_sup]

    num_rimossi = len(valori) - len(risultato)
    if num_rimossi > 0:
        logger.debug(
            "Rimossi %d outlier su %d valori (soglia: %.1f dev.std dalla mediana)",
            num_rimossi, len(valori), num_deviazioni,
        )

    return risultato


# ---------------------------------------------------------------------------
# Valori impliciti da singoli multipli
# ---------------------------------------------------------------------------

def valore_implicito_pe(eps_target: float, pe_mediano: float) -> float:
    """Calcola valore per azione implicito dal P/E mediano dei comparabili.

    Parametri
    ---------
    eps_target : float
        Utile per azione dell'azienda target.
    pe_mediano : float
        P/E mediano del campione di comparabili.

    Restituisce
    -----------
    float
        Valore per azione implicito.
    """
    return eps_target * pe_mediano


def valore_implicito_ev_ebitda(
    ebitda_target: float,
    ev_ebitda_mediano: float,
    debito_netto: float,
    shares_outstanding: float,
) -> float:
    """Calcola valore per azione implicito dall'EV/EBITDA.

    EV = EBITDA * multiplo -> Equity = EV - debito_netto -> per azione.

    Parametri
    ---------
    ebitda_target : float
        EBITDA dell'azienda target (in milioni).
    ev_ebitda_mediano : float
        EV/EBITDA mediano dei comparabili.
    debito_netto : float
        Posizione finanziaria netta (debito - cassa, in milioni).
    shares_outstanding : float
        Numero di azioni in circolazione (in milioni).

    Restituisce
    -----------
    float
        Valore per azione implicito.
    """
    ev = ebitda_target * ev_ebitda_mediano
    equity = ev - debito_netto
    return equity / shares_outstanding if shares_outstanding > 0 else 0.0


def valore_implicito_pb(
    book_value_per_share: float,
    pb_mediano: float,
) -> float:
    """Calcola valore implicito dal P/B.

    Parametri
    ---------
    book_value_per_share : float
        Valore contabile per azione dell'azienda target.
    pb_mediano : float
        P/B mediano dei comparabili.

    Restituisce
    -----------
    float
        Valore per azione implicito.
    """
    return book_value_per_share * pb_mediano


def valore_implicito_ev_sales(
    ricavi: float,
    ev_sales_mediano: float,
    debito_netto: float,
    shares_outstanding: float,
) -> float:
    """Calcola valore per azione implicito dall'EV/Sales.

    Parametri
    ---------
    ricavi : float
        Ricavi totali dell'azienda target (in milioni).
    ev_sales_mediano : float
        EV/Sales mediano dei comparabili.
    debito_netto : float
        Posizione finanziaria netta (in milioni).
    shares_outstanding : float
        Numero di azioni in circolazione (in milioni).

    Restituisce
    -----------
    float
        Valore per azione implicito.
    """
    ev = ricavi * ev_sales_mediano
    equity = ev - debito_netto
    return equity / shares_outstanding if shares_outstanding > 0 else 0.0


# ---------------------------------------------------------------------------
# Valutazione relativa completa
# ---------------------------------------------------------------------------

def valutazione_relativa(
    ticker: str,
    eps: float,
    ebitda: float,
    book_value_per_share: float,
    ricavi: float,
    debito_netto: float,
    shares_outstanding: float,
    comparabili: list[Comparabile],
    prezzo_corrente: float | None = None,
) -> ValuationResult:
    """Esegue valutazione relativa completa usando i comparabili forniti.

    Procedura:
    1. Calcola statistiche per ogni multiplo disponibile nei comparabili
    2. Calcola il valore implicito per ogni multiplo
    3. Calcola la media e la mediana dei valori impliciti
    4. Confronta con il prezzo di mercato (se disponibile)

    Parametri
    ---------
    ticker : str
        Simbolo di borsa dell'azienda target.
    eps : float
        Utile per azione dell'azienda target.
    ebitda : float
        EBITDA dell'azienda target (in milioni).
    book_value_per_share : float
        Valore contabile per azione.
    ricavi : float
        Ricavi totali (in milioni).
    debito_netto : float
        Posizione finanziaria netta (in milioni).
    shares_outstanding : float
        Numero di azioni in circolazione (in milioni).
    comparabili : list[Comparabile]
        Lista delle aziende comparabili con i relativi multipli.
    prezzo_corrente : float | None, opzionale
        Prezzo corrente di mercato per il confronto.

    Restituisce
    -----------
    ValuationResult
        Risultato completo della valutazione relativa.
    """
    logger.info(
        "Avvio valutazione relativa per %s con %d comparabili",
        ticker, len(comparabili),
    )

    # --- 1. Costruisci AnalisiComparabili e calcola statistiche ---
    analisi = AnalisiComparabili(
        comparabili=list(comparabili),
        ticker_target=ticker,
        criteri_selezione="Valutazione relativa multi-multiplo",
    )
    analisi.calcola_statistiche()

    # Dizionario per raccogliere le statistiche calcolate nel dettaglio
    dettagli_statistiche: dict[str, dict[str, float]] = {}
    for nome_mult, stat in analisi.statistiche.items():
        dettagli_statistiche[nome_mult] = {
            "mediana": stat.mediana,
            "media": stat.media,
            "minimo": stat.minimo,
            "massimo": stat.massimo,
            "dev_std": stat.deviazione_standard,
            "num_osservazioni": float(stat.num_osservazioni),
        }

    # --- 2. Calcola valore implicito per ogni multiplo disponibile ---
    valori_impliciti: dict[str, float] = {}
    note: list[str] = []

    # P/E
    mediana_pe = analisi.ottieni_mediana("pe_ratio")
    if mediana_pe is not None and mediana_pe > 0 and eps > 0:
        valore_pe = valore_implicito_pe(eps, mediana_pe)
        valori_impliciti["pe_ratio"] = valore_pe
        logger.debug("Valore implicito P/E: %.2f (mediana PE=%.2f)", valore_pe, mediana_pe)
    else:
        note.append("P/E: non calcolabile (EPS non positivo o mediana non disponibile)")

    # EV/EBITDA
    mediana_ev_ebitda = analisi.ottieni_mediana("ev_ebitda")
    if mediana_ev_ebitda is not None and mediana_ev_ebitda > 0 and ebitda > 0:
        valore_ev_ebitda = valore_implicito_ev_ebitda(
            ebitda, mediana_ev_ebitda, debito_netto, shares_outstanding,
        )
        valori_impliciti["ev_ebitda"] = valore_ev_ebitda
        logger.debug(
            "Valore implicito EV/EBITDA: %.2f (mediana=%.2f)",
            valore_ev_ebitda, mediana_ev_ebitda,
        )
    else:
        note.append("EV/EBITDA: non calcolabile (EBITDA non positivo o mediana non disponibile)")

    # P/B
    mediana_pb = analisi.ottieni_mediana("pb_ratio")
    if mediana_pb is not None and mediana_pb > 0 and book_value_per_share > 0:
        valore_pb = valore_implicito_pb(book_value_per_share, mediana_pb)
        valori_impliciti["pb_ratio"] = valore_pb
        logger.debug("Valore implicito P/B: %.2f (mediana PB=%.2f)", valore_pb, mediana_pb)
    else:
        note.append("P/B: non calcolabile (BV non positivo o mediana non disponibile)")

    # EV/Sales
    mediana_ev_sales = analisi.ottieni_mediana("ev_sales")
    if mediana_ev_sales is not None and mediana_ev_sales > 0 and ricavi > 0:
        valore_ev_sales = valore_implicito_ev_sales(
            ricavi, mediana_ev_sales, debito_netto, shares_outstanding,
        )
        valori_impliciti["ev_sales"] = valore_ev_sales
        logger.debug(
            "Valore implicito EV/Sales: %.2f (mediana=%.2f)",
            valore_ev_sales, mediana_ev_sales,
        )
    else:
        note.append("EV/Sales: non calcolabile (ricavi non positivi o mediana non disponibile)")

    # EV/EBIT (usa EBITDA come proxy per EBIT se non disponibile separatamente;
    # qui usiamo un margine approssimativo: EBIT ~ EBITDA * 0.8 come fallback)
    mediana_ev_ebit = analisi.ottieni_mediana("ev_ebit")
    if mediana_ev_ebit is not None and mediana_ev_ebit > 0 and ebitda > 0:
        # Approssima EBIT come 80% dell'EBITDA per il target
        ebit_stimato = ebitda * 0.80
        ev_ebit_val = ebit_stimato * mediana_ev_ebit
        equity_ebit = ev_ebit_val - debito_netto
        valore_ev_ebit = equity_ebit / shares_outstanding if shares_outstanding > 0 else 0.0
        valori_impliciti["ev_ebit"] = valore_ev_ebit
        note.append("EV/EBIT: EBIT stimato come 80% dell'EBITDA fornito")
        logger.debug(
            "Valore implicito EV/EBIT: %.2f (mediana=%.2f, EBIT stimato=%.2f)",
            valore_ev_ebit, mediana_ev_ebit, ebit_stimato,
        )

    # --- 3. Calcola media e mediana dei valori impliciti ---
    if not valori_impliciti:
        logger.warning(
            "Nessun valore implicito calcolabile per %s: nessun multiplo utilizzabile",
            ticker,
        )
        return ValuationResult(
            ticker=ticker,
            metodo="RELATIVE_MULTI",
            valore_equity=0.0,
            valore_per_azione=0.0,
            parametri={
                "eps": eps,
                "ebitda": ebitda,
                "book_value_per_share": book_value_per_share,
                "ricavi": ricavi,
                "debito_netto": debito_netto,
                "shares_outstanding": shares_outstanding,
                "num_comparabili": len(comparabili),
            },
            note=note + ["Nessun multiplo utilizzabile per la valutazione"],
        )

    lista_valori = list(valori_impliciti.values())
    media_valori = statistics.mean(lista_valori)
    mediana_valori = statistics.median(lista_valori)

    # Il valore per azione finale e' la mediana dei valori impliciti
    valore_finale = mediana_valori
    valore_equity_totale = valore_finale * shares_outstanding

    # --- 4. Confronto con prezzo di mercato ---
    parametri: dict[str, float | str | int | bool] = {
        "eps": eps,
        "ebitda": ebitda,
        "book_value_per_share": book_value_per_share,
        "ricavi": ricavi,
        "debito_netto": debito_netto,
        "shares_outstanding": shares_outstanding,
        "num_comparabili": len(comparabili),
        "num_multipli_usati": len(valori_impliciti),
    }

    if prezzo_corrente is not None and prezzo_corrente > 0:
        parametri["prezzo_corrente"] = prezzo_corrente
        upside = (valore_finale - prezzo_corrente) / prezzo_corrente
        note.append(
            f"Upside/downside rispetto al prezzo corrente ({prezzo_corrente:.2f}): "
            f"{upside:+.1%}"
        )

    # Costruisci il dizionario dei dettagli
    dettagli: dict[str, float | str | list[float]] = {
        "valore_mediana_multipli": mediana_valori,
        "valore_media_multipli": media_valori,
    }

    # Aggiungi i singoli valori impliciti
    for nome_mult, valore in valori_impliciti.items():
        dettagli[f"valore_implicito_{nome_mult}"] = valore

    # Aggiungi le mediane dei multipli usate
    for nome_mult in valori_impliciti:
        med = analisi.ottieni_mediana(nome_mult)
        if med is not None:
            dettagli[f"mediana_{nome_mult}"] = med

    # Aggiungi i ticker dei comparabili come stringa
    dettagli["comparabili_tickers"] = ", ".join(c.ticker for c in comparabili)

    # Calcola intervallo di confidenza (min e max dei valori impliciti)
    intervallo: tuple[float, float] | None = None
    if len(lista_valori) >= 2:
        intervallo = (min(lista_valori), max(lista_valori))

    note.append(
        f"Valutazione basata su {len(valori_impliciti)} multipli: "
        f"{', '.join(valori_impliciti.keys())}"
    )

    logger.info(
        "Valutazione relativa %s completata: %.2f/azione (equity %.2fM), "
        "%d multipli utilizzati",
        ticker, valore_finale, valore_equity_totale, len(valori_impliciti),
    )

    return ValuationResult(
        ticker=ticker,
        metodo="RELATIVE_MULTI",
        valore_equity=valore_equity_totale,
        valore_per_azione=valore_finale,
        data_valutazione=date.today().isoformat(),
        parametri=parametri,
        dettagli=dettagli,
        note=note,
        intervallo_confidenza=intervallo,
    )
