"""Modulo per l'analisi per scenari (best/base/worst case).

Definisce scenari con probabilita' e calcola il valore atteso ponderato.
"""
from __future__ import annotations

from typing import Any, Callable

from valuation_analyst.models.scenario import AnalisiScenari, Scenario
from valuation_analyst.utils.formatting import formatta_valuta, tabella_markdown
from valuation_analyst.utils.validators import valida_positivo


def crea_scenari_standard(
    valore_base: float,
    upside_pct: float = 0.30,
    downside_pct: float = 0.25,
    prob_best: float = 0.20,
    prob_base: float = 0.55,
    prob_worst: float = 0.25,
) -> AnalisiScenari:
    """Crea set standard di 3 scenari (best/base/worst).

    Il valore best e' calcolato come base * (1 + upside_pct),
    il valore worst come base * (1 - downside_pct).

    Args:
        valore_base: valore per azione nello scenario base.
        upside_pct: percentuale di upside rispetto al base case.
        downside_pct: percentuale di downside rispetto al base case.
        prob_best: probabilita' dello scenario best.
        prob_base: probabilita' dello scenario base.
        prob_worst: probabilita' dello scenario worst.

    Returns:
        AnalisiScenari con i tre scenari configurati.

    Raises:
        ValueError: se la somma delle probabilita' non e' prossima a 1.
    """
    scenari = [
        Scenario(
            nome="Best Case",
            probabilita=prob_best,
            parametri={"upside": upside_pct},
            valore_risultante=valore_base * (1 + upside_pct),
        ),
        Scenario(
            nome="Base Case",
            probabilita=prob_base,
            parametri={},
            valore_risultante=valore_base,
        ),
        Scenario(
            nome="Worst Case",
            probabilita=prob_worst,
            parametri={"downside": downside_pct},
            valore_risultante=valore_base * (1 - downside_pct),
        ),
    ]
    return AnalisiScenari(scenari=scenari)


def analisi_scenari_dcf(
    funzione_dcf: Callable[..., float],
    scenari_parametri: list[dict[str, Any]],
    nomi_scenari: list[str],
    probabilita: list[float],
) -> AnalisiScenari:
    """Esegue analisi scenari con funzione DCF personalizzata.

    Per ogni scenario, chiama funzione_dcf(**parametri) e registra
    il valore risultante. La funzione DCF deve restituire il valore
    per azione.

    Args:
        funzione_dcf: funzione di valutazione DCF che accetta keyword
            arguments e restituisce il valore per azione.
        scenari_parametri: lista di dizionari, uno per scenario, con
            i parametri da passare alla funzione DCF.
        nomi_scenari: lista di nomi per ogni scenario.
        probabilita: lista di probabilita' per ogni scenario.

    Returns:
        AnalisiScenari con tutti gli scenari calcolati.

    Raises:
        ValueError: se le liste hanno lunghezze diverse.
    """
    # Validazione coerenza lunghezze
    n = len(nomi_scenari)
    if len(scenari_parametri) != n or len(probabilita) != n:
        raise ValueError(
            f"Le liste devono avere la stessa lunghezza: "
            f"nomi={n}, parametri={len(scenari_parametri)}, "
            f"probabilita={len(probabilita)}."
        )

    scenari: list[Scenario] = []
    for nome, params, prob in zip(nomi_scenari, scenari_parametri, probabilita):
        try:
            valore = funzione_dcf(**params)
        except (ValueError, ZeroDivisionError, TypeError) as e:
            # In caso di errore nel calcolo, registra None e aggiunge nota
            scenari.append(
                Scenario(
                    nome=nome,
                    probabilita=prob,
                    parametri=params,
                    valore_risultante=None,
                    note=f"Errore nel calcolo: {e}",
                )
            )
            continue

        scenari.append(
            Scenario(
                nome=nome,
                probabilita=prob,
                parametri=params,
                valore_risultante=valore,
            )
        )

    return AnalisiScenari(scenari=scenari)


def analisi_scenari_personalizzata(
    scenari: list[dict[str, Any]],
) -> AnalisiScenari:
    """Crea analisi da lista di dizionari.

    Ogni dizionario deve contenere le chiavi:
    - ``nome``: nome dello scenario (str)
    - ``probabilita``: probabilita' di accadimento (float, 0-1)
    - ``parametri``: dizionario dei parametri (dict)
    - ``valore``: valore risultante per azione (float)

    Opzionalmente:
    - ``valore_equity``: valore totale equity (float)
    - ``note``: note aggiuntive (str)

    Args:
        scenari: lista di dizionari con le specifiche sopra indicate.

    Returns:
        AnalisiScenari con gli scenari forniti.

    Raises:
        ValueError: se un dizionario non contiene le chiavi obbligatorie.
    """
    chiavi_obbligatorie = {"nome", "probabilita", "parametri", "valore"}
    lista_scenari: list[Scenario] = []

    for i, s in enumerate(scenari):
        mancanti = chiavi_obbligatorie - set(s.keys())
        if mancanti:
            raise ValueError(
                f"Lo scenario all'indice {i} non contiene le chiavi "
                f"obbligatorie: {mancanti}"
            )

        lista_scenari.append(
            Scenario(
                nome=s["nome"],
                probabilita=s["probabilita"],
                parametri=s["parametri"],
                valore_risultante=s["valore"],
                valore_equity=s.get("valore_equity"),
                note=s.get("note", ""),
            )
        )

    return AnalisiScenari(scenari=lista_scenari)


def formatta_scenari(analisi: AnalisiScenari, valuta: str = "USD") -> str:
    """Formatta l'analisi scenari in markdown leggibile.

    Genera una tabella markdown con colonne: Scenario, Probabilita',
    Valore per Azione, Valore Ponderato. In fondo aggiunge il valore
    atteso complessivo e un avviso se le probabilita' non sommano a 1.

    Args:
        analisi: oggetto AnalisiScenari da formattare.
        valuta: codice ISO della valuta per la formattazione.

    Returns:
        Stringa markdown con la tabella e il riepilogo.
    """
    # Intestazioni della tabella
    headers = ["Scenario", "Probabilita'", "Valore/Azione", "Contributo Ponderato"]

    # Righe
    rows: list[list[str]] = []
    for s in analisi.scenari:
        valore_str = (
            formatta_valuta(s.valore_risultante, valuta)
            if s.valore_risultante is not None
            else "N/D"
        )
        ponderato_str = (
            formatta_valuta(s.valore_ponderato, valuta)
            if s.valore_risultante is not None
            else "N/D"
        )
        rows.append([
            s.nome,
            f"{s.probabilita:.0%}",
            valore_str,
            ponderato_str,
        ])

    # Riga del valore atteso
    rows.append([
        "**Valore Atteso**",
        f"{analisi.somma_probabilita:.0%}",
        "",
        f"**{formatta_valuta(analisi.valore_atteso, valuta)}**",
    ])

    tabella = tabella_markdown(headers, rows)

    # Avviso probabilita'
    linee = [tabella]
    if not analisi.probabilita_valide:
        linee.append("")
        linee.append(
            f"**ATTENZIONE:** la somma delle probabilita' e' "
            f"{analisi.somma_probabilita:.2%}, dovrebbe essere 100%."
        )

    # Note degli scenari
    note_presenti = [s for s in analisi.scenari if s.note]
    if note_presenti:
        linee.append("")
        linee.append("**Note:**")
        for s in note_presenti:
            linee.append(f"- *{s.nome}*: {s.note}")

    return "\n".join(linee)
