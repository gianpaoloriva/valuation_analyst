"""Modello dati per un'azienda oggetto di valutazione.

Contiene la dataclass Company che rappresenta tutti i dati
fondamentali di un'azienda necessari per eseguire una
valutazione finanziaria completa.
"""

from dataclasses import dataclass, field
from typing import Any

from valuation_analyst.config.constants import MARKET_CAP_THRESHOLDS, SECTOR_NAMES


@dataclass
class Company:
    """Rappresenta un'azienda con tutti i suoi dati finanziari fondamentali.

    Questa dataclass raccoglie le informazioni anagrafiche e i dati
    finanziari dell'ultimo esercizio necessari per alimentare i diversi
    modelli di valutazione (DCF, comparabili, opzioni reali, ecc.).

    Attributes:
        ticker: Simbolo di borsa dell'azienda (es. "AAPL").
        nome: Ragione sociale completa.
        settore: Settore di appartenenza (es. "Technology").
        industria: Sotto-industria specifica (es. "Consumer Electronics").
        paese: Paese di quotazione principale (codice ISO o nome).
        valuta: Valuta di riferimento dei dati finanziari.
        market_cap: Capitalizzazione di mercato (in milioni).
        enterprise_value: Enterprise Value (in milioni).
        shares_outstanding: Numero di azioni in circolazione (in milioni).
        prezzo_corrente: Prezzo corrente dell'azione.
        ricavi: Ricavi totali dell'ultimo esercizio (in milioni).
        ebit: Utile operativo / EBIT (in milioni).
        ebitda: EBITDA (in milioni).
        utile_netto: Utile netto (in milioni).
        total_debt: Debito totale (in milioni).
        cash: Disponibilita' liquide e investimenti a breve (in milioni).
        capex: Investimenti in conto capitale (in milioni, valore positivo).
        deprezzamento: Ammortamenti e svalutazioni (in milioni).
        delta_working_capital: Variazione del capitale circolante netto (in milioni).
        tax_rate: Aliquota fiscale effettiva.
        beta: Beta levered dell'azione.
        dividendo_per_azione: Dividendo annuo per azione.
        dati_aggiuntivi: Dizionario per dati supplementari non strutturati.
    """

    ticker: str
    nome: str
    settore: str
    industria: str
    paese: str
    valuta: str = "USD"
    market_cap: float | None = None
    enterprise_value: float | None = None
    shares_outstanding: float | None = None
    prezzo_corrente: float | None = None
    ricavi: float | None = None
    ebit: float | None = None
    ebitda: float | None = None
    utile_netto: float | None = None
    total_debt: float | None = None
    cash: float | None = None
    capex: float | None = None
    deprezzamento: float | None = None
    delta_working_capital: float | None = None
    tax_rate: float | None = None
    beta: float | None = None
    dividendo_per_azione: float | None = None
    dati_aggiuntivi: dict[str, Any] = field(default_factory=dict)

    @property
    def categoria_capitalizzazione(self) -> str | None:
        """Restituisce la categoria di capitalizzazione di mercato.

        Classifica l'azienda in micro, small, mid, large o mega cap
        secondo le soglie definite in MARKET_CAP_THRESHOLDS.

        Returns:
            Nome della categoria, oppure None se market_cap non e' disponibile.
        """
        if self.market_cap is None:
            return None
        for categoria, (limite_inf, limite_sup) in MARKET_CAP_THRESHOLDS.items():
            if limite_inf <= self.market_cap < limite_sup:
                return categoria
        return None

    @property
    def settore_italiano(self) -> str:
        """Restituisce il nome del settore tradotto in italiano.

        Returns:
            Nome del settore in italiano, oppure il nome originale
            se la traduzione non e' disponibile.
        """
        return SECTOR_NAMES.get(self.settore, self.settore)

    @property
    def debito_netto(self) -> float | None:
        """Calcola il debito netto (debito totale meno liquidita').

        Returns:
            Debito netto in milioni, oppure None se i dati non sono disponibili.
        """
        if self.total_debt is not None and self.cash is not None:
            return self.total_debt - self.cash
        return None

    @property
    def rapporto_debito_equity(self) -> float | None:
        """Calcola il rapporto Debito/Equity (D/E).

        Usa market_cap come proxy del valore dell'equity.

        Returns:
            Rapporto D/E, oppure None se i dati non sono disponibili.
        """
        if self.total_debt is not None and self.market_cap is not None and self.market_cap > 0:
            return self.total_debt / self.market_cap
        return None

    @property
    def margine_operativo(self) -> float | None:
        """Calcola il margine operativo (EBIT/Ricavi).

        Returns:
            Margine operativo come valore decimale, oppure None.
        """
        if self.ebit is not None and self.ricavi is not None and self.ricavi > 0:
            return self.ebit / self.ricavi
        return None

    @property
    def margine_ebitda(self) -> float | None:
        """Calcola il margine EBITDA (EBITDA/Ricavi).

        Returns:
            Margine EBITDA come valore decimale, oppure None.
        """
        if self.ebitda is not None and self.ricavi is not None and self.ricavi > 0:
            return self.ebitda / self.ricavi
        return None

    @property
    def margine_netto(self) -> float | None:
        """Calcola il margine netto (Utile Netto/Ricavi).

        Returns:
            Margine netto come valore decimale, oppure None.
        """
        if self.utile_netto is not None and self.ricavi is not None and self.ricavi > 0:
            return self.utile_netto / self.ricavi
        return None

    @property
    def fcff_approssimato(self) -> float | None:
        """Calcola un FCFF approssimato dai dati disponibili.

        FCFF = EBIT * (1 - tax_rate) + D&A - CapEx - Delta WC

        Returns:
            FCFF stimato in milioni, oppure None se mancano dati essenziali.
        """
        if (
            self.ebit is not None
            and self.tax_rate is not None
            and self.deprezzamento is not None
            and self.capex is not None
        ):
            nopat = self.ebit * (1 - self.tax_rate)
            dwc = self.delta_working_capital if self.delta_working_capital is not None else 0.0
            return nopat + self.deprezzamento - self.capex - dwc
        return None

    @property
    def fcfe_approssimato(self) -> float | None:
        """Calcola un FCFE approssimato dai dati disponibili.

        FCFE = Utile Netto + D&A - CapEx - Delta WC - Rimborso Debito Netto
        (semplificato senza variazione debito)

        Returns:
            FCFE stimato in milioni, oppure None se mancano dati essenziali.
        """
        if (
            self.utile_netto is not None
            and self.deprezzamento is not None
            and self.capex is not None
        ):
            dwc = self.delta_working_capital if self.delta_working_capital is not None else 0.0
            return self.utile_netto + self.deprezzamento - self.capex - dwc
        return None

    def ha_dati_completi_dcf(self) -> bool:
        """Verifica se i dati sono sufficienti per un'analisi DCF.

        Returns:
            True se tutti i campi essenziali per il DCF sono presenti.
        """
        campi_richiesti = [
            self.ricavi,
            self.ebit,
            self.tax_rate,
            self.deprezzamento,
            self.capex,
            self.total_debt,
            self.cash,
            self.beta,
            self.shares_outstanding,
        ]
        return all(campo is not None for campo in campi_richiesti)

    def __str__(self) -> str:
        """Rappresentazione leggibile dell'azienda."""
        cap_str = f" - Cap: {self.market_cap:,.0f}M {self.valuta}" if self.market_cap else ""
        return f"{self.nome} ({self.ticker}){cap_str} [{self.settore}]"
