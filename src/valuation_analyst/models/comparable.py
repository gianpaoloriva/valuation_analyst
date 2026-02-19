"""Modelli dati per l'analisi dei comparabili (valutazione relativa).

Contiene le dataclass Comparabile e AnalisiComparabili
per rappresentare i dati delle aziende comparabili e
le statistiche aggregate dei multipli di mercato.
"""

from dataclasses import dataclass, field
from statistics import mean, median, stdev


@dataclass
class Comparabile:
    """Dati di un'azienda comparabile per la valutazione relativa.

    Rappresenta un singolo peer con i principali multipli di mercato
    e indicatori finanziari utilizzati nella valutazione per comparabili.

    Attributes:
        ticker: Simbolo di borsa dell'azienda comparabile.
        nome: Ragione sociale completa.
        settore: Settore di appartenenza.
        market_cap: Capitalizzazione di mercato (in milioni).
        pe_ratio: Rapporto Prezzo/Utili (P/E).
        ev_ebitda: Multiplo EV/EBITDA.
        pb_ratio: Rapporto Prezzo/Valore Contabile (P/BV).
        ev_sales: Multiplo EV/Ricavi.
        ps_ratio: Rapporto Prezzo/Ricavi (P/S).
        roe: Return on Equity.
        margine_operativo: Margine operativo (EBIT/Ricavi).
        crescita_ricavi: Tasso di crescita dei ricavi (anno su anno).
        ev_ebit: Multiplo EV/EBIT.
        dividend_yield: Rendimento da dividendo.
        paese: Paese di quotazione.
    """

    ticker: str
    nome: str
    settore: str
    market_cap: float
    pe_ratio: float | None = None
    ev_ebitda: float | None = None
    pb_ratio: float | None = None
    ev_sales: float | None = None
    ps_ratio: float | None = None
    roe: float | None = None
    margine_operativo: float | None = None
    crescita_ricavi: float | None = None
    ev_ebit: float | None = None
    dividend_yield: float | None = None
    paese: str = ""

    def multipli_disponibili(self) -> dict[str, float]:
        """Restituisce un dizionario dei multipli non-None.

        Returns:
            Dizionario con nome_multiplo -> valore per tutti i multipli disponibili.
        """
        multipli: dict[str, float] = {}
        campi_multipli = [
            ("pe_ratio", self.pe_ratio),
            ("ev_ebitda", self.ev_ebitda),
            ("pb_ratio", self.pb_ratio),
            ("ev_sales", self.ev_sales),
            ("ps_ratio", self.ps_ratio),
            ("ev_ebit", self.ev_ebit),
        ]
        for nome, valore in campi_multipli:
            if valore is not None:
                multipli[nome] = valore
        return multipli

    def __str__(self) -> str:
        """Rappresentazione leggibile del comparabile."""
        multipli = []
        if self.pe_ratio is not None:
            multipli.append(f"P/E={self.pe_ratio:.1f}")
        if self.ev_ebitda is not None:
            multipli.append(f"EV/EBITDA={self.ev_ebitda:.1f}")
        if self.pb_ratio is not None:
            multipli.append(f"P/BV={self.pb_ratio:.1f}")
        multipli_str = ", ".join(multipli) if multipli else "N/D"
        return f"{self.nome} ({self.ticker}) - Cap: {self.market_cap:,.0f}M | {multipli_str}"


@dataclass
class StatisticheMultiplo:
    """Statistiche descrittive per un singolo multiplo.

    Attributes:
        nome_multiplo: Nome identificativo del multiplo.
        mediana: Valore mediano.
        media: Valore medio (media aritmetica).
        minimo: Valore minimo osservato.
        massimo: Valore massimo osservato.
        deviazione_standard: Deviazione standard.
        primo_quartile: Primo quartile (25mo percentile).
        terzo_quartile: Terzo quartile (75mo percentile).
        num_osservazioni: Numero di osservazioni valide.
    """

    nome_multiplo: str
    mediana: float
    media: float
    minimo: float
    massimo: float
    deviazione_standard: float = 0.0
    primo_quartile: float = 0.0
    terzo_quartile: float = 0.0
    num_osservazioni: int = 0

    def __str__(self) -> str:
        """Rappresentazione leggibile delle statistiche."""
        return (
            f"{self.nome_multiplo}: "
            f"Med={self.mediana:.2f}, Media={self.media:.2f}, "
            f"Min={self.minimo:.2f}, Max={self.massimo:.2f} "
            f"(n={self.num_osservazioni})"
        )


@dataclass
class AnalisiComparabili:
    """Analisi completa dei comparabili per la valutazione relativa.

    Raccoglie l'insieme delle aziende comparabili e le statistiche
    aggregate dei multipli di mercato calcolate su di esse.

    Attributes:
        comparabili: Lista delle aziende comparabili selezionate.
        statistiche: Dizionario delle statistiche per ciascun multiplo.
        ticker_target: Ticker dell'azienda oggetto di valutazione.
        criteri_selezione: Descrizione dei criteri usati per selezionare i peer.
        outlier_rimossi: Lista dei ticker rimossi come outlier.
    """

    comparabili: list[Comparabile] = field(default_factory=list)
    statistiche: dict[str, StatisticheMultiplo] = field(default_factory=dict)
    ticker_target: str = ""
    criteri_selezione: str = ""
    outlier_rimossi: list[str] = field(default_factory=list)

    @property
    def numero_comparabili(self) -> int:
        """Numero di aziende comparabili nell'analisi.

        Returns:
            Numero totale di comparabili.
        """
        return len(self.comparabili)

    def calcola_statistiche(self) -> None:
        """Calcola le statistiche per tutti i multipli disponibili.

        Aggiorna il dizionario self.statistiche con mediana, media,
        min, max, deviazione standard e quartili per ciascun multiplo
        che ha almeno 2 osservazioni valide.
        """
        nomi_multipli = [
            "pe_ratio", "ev_ebitda", "pb_ratio",
            "ev_sales", "ps_ratio", "ev_ebit",
        ]

        for nome in nomi_multipli:
            valori = [
                getattr(comp, nome)
                for comp in self.comparabili
                if getattr(comp, nome) is not None
            ]

            if len(valori) < 2:
                continue

            valori_ordinati = sorted(valori)
            n = len(valori_ordinati)

            # Calcolo quartili semplificato
            q1_idx = n // 4
            q3_idx = (3 * n) // 4
            primo_q = valori_ordinati[q1_idx]
            terzo_q = valori_ordinati[q3_idx]

            self.statistiche[nome] = StatisticheMultiplo(
                nome_multiplo=nome,
                mediana=median(valori),
                media=mean(valori),
                minimo=min(valori),
                massimo=max(valori),
                deviazione_standard=stdev(valori) if len(valori) > 1 else 0.0,
                primo_quartile=primo_q,
                terzo_quartile=terzo_q,
                num_osservazioni=n,
            )

    def rimuovi_outlier(self, soglia_deviazioni: float = 2.0) -> list[str]:
        """Rimuove i comparabili con multipli anomali (outlier).

        Per ciascun multiplo, rimuove le aziende il cui valore
        si discosta dalla media di piu' di soglia_deviazioni
        deviazioni standard.

        Args:
            soglia_deviazioni: Numero di deviazioni standard per la soglia.

        Returns:
            Lista dei ticker rimossi come outlier.
        """
        ticker_da_rimuovere: set[str] = set()

        for nome, stat in self.statistiche.items():
            if stat.deviazione_standard == 0:
                continue
            for comp in self.comparabili:
                valore = getattr(comp, nome)
                if valore is not None:
                    z_score = abs(valore - stat.media) / stat.deviazione_standard
                    if z_score > soglia_deviazioni:
                        ticker_da_rimuovere.add(comp.ticker)

        # Rimuovi gli outlier dalla lista
        rimossi = list(ticker_da_rimuovere)
        self.comparabili = [
            c for c in self.comparabili if c.ticker not in ticker_da_rimuovere
        ]
        self.outlier_rimossi.extend(rimossi)

        # Ricalcola le statistiche dopo la rimozione
        if rimossi:
            self.calcola_statistiche()

        return rimossi

    def ottieni_mediana(self, nome_multiplo: str) -> float | None:
        """Restituisce la mediana di un multiplo specifico.

        Args:
            nome_multiplo: Nome del multiplo (es. "pe_ratio").

        Returns:
            Valore mediano, oppure None se non disponibile.
        """
        stat = self.statistiche.get(nome_multiplo)
        return stat.mediana if stat is not None else None

    def ottieni_media(self, nome_multiplo: str) -> float | None:
        """Restituisce la media di un multiplo specifico.

        Args:
            nome_multiplo: Nome del multiplo (es. "ev_ebitda").

        Returns:
            Valore medio, oppure None se non disponibile.
        """
        stat = self.statistiche.get(nome_multiplo)
        return stat.media if stat is not None else None

    def riepilogo(self) -> str:
        """Genera un riepilogo testuale dell'analisi dei comparabili.

        Returns:
            Stringa formattata con l'elenco dei comparabili e le statistiche.
        """
        righe = [
            f"Analisi Comparabili per {self.ticker_target}",
            f"Numero comparabili: {self.numero_comparabili}",
        ]

        if self.criteri_selezione:
            righe.append(f"Criteri: {self.criteri_selezione}")

        if self.outlier_rimossi:
            righe.append(f"Outlier rimossi: {', '.join(self.outlier_rimossi)}")

        righe.append("")
        righe.append("Comparabili:")
        for comp in self.comparabili:
            righe.append(f"  {comp}")

        if self.statistiche:
            righe.append("")
            righe.append("Statistiche Multipli:")
            for stat in self.statistiche.values():
                righe.append(f"  {stat}")

        return "\n".join(righe)

    def __str__(self) -> str:
        """Rappresentazione leggibile dell'analisi."""
        return (
            f"Analisi Comparabili ({self.ticker_target}): "
            f"{self.numero_comparabili} peer, "
            f"{len(self.statistiche)} multipli"
        )
