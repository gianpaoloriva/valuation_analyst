"""Modello dati per i risultati di una valutazione.

Contiene la dataclass ValuationResult che rappresenta
l'output completo di qualsiasi metodo di valutazione,
inclusi parametri utilizzati, dettagli intermedi e note.
"""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class ValuationResult:
    """Risultato di una valutazione finanziaria.

    Questa dataclass rappresenta l'output di un singolo metodo
    di valutazione applicato a un'azienda. Puo' essere utilizzata
    per DCF, valutazione relativa, opzioni reali, ecc.

    Attributes:
        ticker: Simbolo di borsa dell'azienda valutata.
        metodo: Identificativo del metodo di valutazione utilizzato
                (DCF_FCFF, DCF_FCFE, RELATIVE_PE, RELATIVE_EV_EBITDA,
                 OPTION_EQUITY, DDM, APV, EVA, ecc.).
        valore_equity: Valore stimato dell'equity totale (in milioni).
        valore_per_azione: Valore stimato per singola azione.
        data_valutazione: Data in cui e' stata eseguita la valutazione (formato ISO).
        parametri: Dizionario dei parametri di input utilizzati nel calcolo
                   (es. tasso di sconto, crescita, beta, ecc.).
        dettagli: Dizionario con i risultati intermedi e i dettagli del calcolo
                  (es. valore terminale, valore attuale dei flussi, ecc.).
        note: Lista di note, avvertenze o commenti sulla valutazione.
        intervallo_confidenza: Tuple (min, max) per l'intervallo di confidenza
                               del valore per azione, se calcolato.
    """

    ticker: str
    metodo: str
    valore_equity: float
    valore_per_azione: float
    data_valutazione: str = field(default_factory=lambda: date.today().isoformat())
    parametri: dict[str, float | str | int | bool] = field(default_factory=dict)
    dettagli: dict[str, float | str | list[float]] = field(default_factory=dict)
    note: list[str] = field(default_factory=list)
    intervallo_confidenza: tuple[float, float] | None = None

    @property
    def upside_downside(self) -> float | None:
        """Calcola l'upside/downside rispetto al prezzo corrente.

        Richiede che 'prezzo_corrente' sia presente nei parametri.

        Returns:
            Percentuale di upside (positivo) o downside (negativo),
            oppure None se il prezzo corrente non e' disponibile.
        """
        prezzo = self.parametri.get("prezzo_corrente")
        if isinstance(prezzo, (int, float)) and prezzo > 0:
            return (self.valore_per_azione - prezzo) / prezzo
        return None

    @property
    def raccomandazione(self) -> str:
        """Genera una raccomandazione sintetica basata sull'upside/downside.

        Returns:
            Stringa con la raccomandazione: "SOTTOVALUTATO", "SOPRAVVALUTATO"
            o "FAIR VALUE" (entro +/-10%), oppure "N/D" se non calcolabile.
        """
        ud = self.upside_downside
        if ud is None:
            return "N/D"
        if ud > 0.10:
            return "SOTTOVALUTATO"
        elif ud < -0.10:
            return "SOPRAVVALUTATO"
        else:
            return "FAIR VALUE"

    def aggiungi_nota(self, nota: str) -> None:
        """Aggiunge una nota alla valutazione.

        Args:
            nota: Testo della nota da aggiungere.
        """
        self.note.append(nota)

    def riepilogo(self) -> str:
        """Genera un riepilogo testuale della valutazione.

        Returns:
            Stringa formattata con i risultati principali.
        """
        righe = [
            f"Valutazione {self.ticker} - Metodo: {self.metodo}",
            f"Data: {self.data_valutazione}",
            f"Valore Equity: {self.valore_equity:,.2f}M",
            f"Valore per Azione: {self.valore_per_azione:,.2f}",
        ]

        if self.intervallo_confidenza is not None:
            righe.append(
                f"Intervallo: {self.intervallo_confidenza[0]:,.2f} - "
                f"{self.intervallo_confidenza[1]:,.2f}"
            )

        ud = self.upside_downside
        if ud is not None:
            righe.append(f"Upside/Downside: {ud:+.1%}")
            righe.append(f"Raccomandazione: {self.raccomandazione}")

        if self.note:
            righe.append("Note:")
            for nota in self.note:
                righe.append(f"  - {nota}")

        return "\n".join(righe)

    def __str__(self) -> str:
        """Rappresentazione leggibile del risultato."""
        return (
            f"{self.ticker} [{self.metodo}]: "
            f"{self.valore_per_azione:,.2f}/azione "
            f"(Equity: {self.valore_equity:,.2f}M)"
        )
