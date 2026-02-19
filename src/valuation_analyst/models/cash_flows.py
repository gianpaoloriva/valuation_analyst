"""Modelli dati per le proiezioni dei flussi di cassa.

Contiene le dataclass per rappresentare le proiezioni annuali
dei flussi di cassa (FCFF e FCFE) e l'intera struttura di
un'analisi DCF con valore terminale.
"""

from dataclasses import dataclass, field


@dataclass
class ProiezioneCashFlow:
    """Proiezione di un singolo anno di flussi di cassa.

    Rappresenta i flussi di cassa previsti per un anno specifico
    all'interno del periodo di proiezione esplicita del DCF.

    Attributes:
        anno: Anno della proiezione (1, 2, 3, ... N).
        fcff: Free Cash Flow to Firm (in milioni).
        fcfe: Free Cash Flow to Equity (in milioni).
        tasso_crescita: Tasso di crescita applicato per questo anno.
        tasso_sconto: Tasso di sconto applicato (WACC per FCFF, Ke per FCFE).
        valore_attuale: Valore attuale del flusso di cassa scontato.
        ricavi: Ricavi previsti per l'anno (in milioni).
        ebit: EBIT previsto per l'anno (in milioni).
        ebitda: EBITDA previsto per l'anno (in milioni).
        capex: CapEx previsto per l'anno (in milioni).
        deprezzamento: D&A previsto per l'anno (in milioni).
        delta_wc: Variazione del capitale circolante (in milioni).
        utile_netto: Utile netto previsto per l'anno (in milioni).
    """

    anno: int
    fcff: float | None = None
    fcfe: float | None = None
    tasso_crescita: float = 0.0
    tasso_sconto: float = 0.0
    valore_attuale: float = 0.0
    ricavi: float | None = None
    ebit: float | None = None
    ebitda: float | None = None
    capex: float | None = None
    deprezzamento: float | None = None
    delta_wc: float | None = None
    utile_netto: float | None = None

    @property
    def flusso_principale(self) -> float:
        """Restituisce il flusso di cassa principale (FCFF se disponibile, altrimenti FCFE).

        Returns:
            Valore del flusso di cassa principale, oppure 0.0 se nessuno e' disponibile.
        """
        if self.fcff is not None:
            return self.fcff
        if self.fcfe is not None:
            return self.fcfe
        return 0.0

    def __str__(self) -> str:
        """Rappresentazione leggibile della proiezione annuale."""
        flusso = self.flusso_principale
        return (
            f"Anno {self.anno}: Flusso={flusso:,.2f}M | "
            f"Crescita={self.tasso_crescita:.1%} | "
            f"VA={self.valore_attuale:,.2f}M"
        )


@dataclass
class CashFlowProjection:
    """Proiezione completa dei flussi di cassa per un'analisi DCF.

    Raccoglie tutte le proiezioni annuali, il valore terminale
    e i totali calcolati per una valutazione DCF completa.

    Attributes:
        proiezioni: Lista delle proiezioni annuali ordinate per anno.
        valore_terminale: Valore terminale (non scontato, in milioni).
        valore_terminale_attuale: Valore terminale scontato al presente (in milioni).
        tipo_flusso: Tipo di flusso di cassa utilizzato ("FCFF" o "FCFE").
        tasso_crescita_terminale: Tasso di crescita perpetua usato per il valore terminale.
        tasso_sconto_terminale: Tasso di sconto usato per il valore terminale.
        metodo_valore_terminale: Metodo usato per il valore terminale
                                 ("gordon_growth" o "exit_multiple").
        exit_multiple: Multiplo di uscita se metodo_valore_terminale == "exit_multiple".
    """

    proiezioni: list[ProiezioneCashFlow] = field(default_factory=list)
    valore_terminale: float = 0.0
    valore_terminale_attuale: float = 0.0
    tipo_flusso: str = "FCFF"
    tasso_crescita_terminale: float = 0.0
    tasso_sconto_terminale: float = 0.0
    metodo_valore_terminale: str = "gordon_growth"
    exit_multiple: float | None = None

    @property
    def valore_attuale_flussi(self) -> float:
        """Somma dei valori attuali dei flussi di cassa espliciti.

        Returns:
            Somma dei valori attuali di tutte le proiezioni annuali (in milioni).
        """
        return sum(p.valore_attuale for p in self.proiezioni)

    @property
    def valore_totale(self) -> float:
        """Valore totale dell'impresa (flussi espliciti + valore terminale scontato).

        Returns:
            Valore totale in milioni.
        """
        return self.valore_attuale_flussi + self.valore_terminale_attuale

    @property
    def percentuale_valore_terminale(self) -> float:
        """Percentuale del valore totale attribuibile al valore terminale.

        Returns:
            Percentuale come valore decimale (es. 0.65 = 65%).
            Restituisce 0.0 se il valore totale e' zero.
        """
        totale = self.valore_totale
        if totale == 0:
            return 0.0
        return self.valore_terminale_attuale / totale

    @property
    def numero_anni(self) -> int:
        """Numero di anni nel periodo di proiezione esplicita.

        Returns:
            Numero di proiezioni annuali.
        """
        return len(self.proiezioni)

    def riepilogo(self) -> str:
        """Genera un riepilogo testuale della proiezione dei flussi di cassa.

        Returns:
            Stringa formattata con i risultati principali.
        """
        righe = [
            f"Proiezione DCF ({self.tipo_flusso}) - {self.numero_anni} anni",
            f"Metodo valore terminale: {self.metodo_valore_terminale}",
            "",
            "Proiezioni annuali:",
        ]

        for proiezione in self.proiezioni:
            righe.append(f"  {proiezione}")

        righe.extend([
            "",
            f"VA Flussi Espliciti: {self.valore_attuale_flussi:,.2f}M",
            f"Valore Terminale: {self.valore_terminale:,.2f}M",
            f"VA Valore Terminale: {self.valore_terminale_attuale:,.2f}M",
            f"Peso Valore Terminale: {self.percentuale_valore_terminale:.1%}",
            f"Valore Totale: {self.valore_totale:,.2f}M",
        ])

        return "\n".join(righe)

    def __str__(self) -> str:
        """Rappresentazione leggibile della proiezione."""
        return (
            f"DCF {self.tipo_flusso}: {self.numero_anni} anni | "
            f"Totale={self.valore_totale:,.2f}M "
            f"(TV={self.percentuale_valore_terminale:.0%})"
        )
