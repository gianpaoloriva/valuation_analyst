"""Modello dati per il costo del capitale.

Contiene la dataclass CostoCapitale che rappresenta
tutti i componenti del costo del capitale di un'azienda,
inclusi il costo dell'equity (CAPM), il costo del debito
e il WACC.
"""

from dataclasses import dataclass

from valuation_analyst.config.constants import (
    DEFAULT_ERP,
    DEFAULT_RISK_FREE_RATE,
    DEFAULT_TAX_RATE,
)


@dataclass
class CostoCapitale:
    """Struttura completa del costo del capitale di un'azienda.

    Raccoglie tutti i componenti necessari per calcolare il WACC
    (Weighted Average Cost of Capital) e il costo dell'equity
    secondo il modello CAPM.

    Attributes:
        risk_free_rate: Tasso risk-free (rendimento titoli di stato a lungo termine).
        beta_levered: Beta levered (con effetto della leva finanziaria).
        beta_unlevered: Beta unlevered (senza effetto della leva finanziaria).
        equity_risk_premium: Premio per il rischio azionario del mercato maturo.
        country_risk_premium: Premio aggiuntivo per il rischio paese.
        costo_equity: Costo dell'equity calcolato con il CAPM.
        costo_debito_pre_tax: Costo del debito al lordo delle imposte.
        costo_debito_post_tax: Costo del debito al netto del beneficio fiscale.
        tax_rate: Aliquota fiscale marginale utilizzata.
        peso_equity: Peso dell'equity nella struttura del capitale (valore di mercato).
        peso_debito: Peso del debito nella struttura del capitale (valore di mercato).
        wacc: Costo medio ponderato del capitale.
        small_cap_premium: Premio aggiuntivo per le piccole capitalizzazioni.
        company_specific_premium: Premio aggiuntivo per rischi specifici dell'azienda.
    """

    risk_free_rate: float
    beta_levered: float
    beta_unlevered: float
    equity_risk_premium: float
    country_risk_premium: float = 0.0
    costo_equity: float = 0.0
    costo_debito_pre_tax: float = 0.0
    costo_debito_post_tax: float = 0.0
    tax_rate: float = DEFAULT_TAX_RATE
    peso_equity: float = 1.0
    peso_debito: float = 0.0
    wacc: float = 0.0
    small_cap_premium: float = 0.0
    company_specific_premium: float = 0.0

    def __post_init__(self) -> None:
        """Ricalcola i valori derivati dopo l'inizializzazione.

        Se il costo dell'equity o il WACC non sono stati forniti
        esplicitamente (valore 0.0), vengono calcolati automaticamente
        dai componenti.
        """
        # Calcola il costo dell'equity se non fornito
        if self.costo_equity == 0.0:
            self.costo_equity = self.calcola_costo_equity()

        # Calcola il costo del debito post-tax se non fornito
        if self.costo_debito_post_tax == 0.0 and self.costo_debito_pre_tax > 0:
            self.costo_debito_post_tax = self.costo_debito_pre_tax * (1 - self.tax_rate)

        # Calcola il WACC se non fornito
        if self.wacc == 0.0:
            self.wacc = self.calcola_wacc()

    def calcola_costo_equity(self) -> float:
        """Calcola il costo dell'equity usando il CAPM esteso.

        Ke = Rf + Beta * ERP + CRP + Small Cap Premium + Company Specific Premium

        Returns:
            Costo dell'equity come valore decimale.
        """
        return (
            self.risk_free_rate
            + self.beta_levered * self.equity_risk_premium
            + self.country_risk_premium
            + self.small_cap_premium
            + self.company_specific_premium
        )

    def calcola_wacc(self) -> float:
        """Calcola il WACC (Weighted Average Cost of Capital).

        WACC = Ke * We + Kd * (1 - t) * Wd

        Returns:
            WACC come valore decimale.
        """
        costo_debito_netto = self.costo_debito_pre_tax * (1 - self.tax_rate)
        return (
            self.costo_equity * self.peso_equity
            + costo_debito_netto * self.peso_debito
        )

    @staticmethod
    def beta_unlevered_da_levered(
        beta_levered: float,
        rapporto_de: float,
        tax_rate: float = DEFAULT_TAX_RATE,
    ) -> float:
        """Calcola il beta unlevered dal beta levered (formula di Hamada).

        Beta_u = Beta_l / (1 + (1 - t) * D/E)

        Args:
            beta_levered: Beta con effetto leva.
            rapporto_de: Rapporto Debito/Equity.
            tax_rate: Aliquota fiscale marginale.

        Returns:
            Beta unlevered.
        """
        return beta_levered / (1 + (1 - tax_rate) * rapporto_de)

    @staticmethod
    def beta_levered_da_unlevered(
        beta_unlevered: float,
        rapporto_de: float,
        tax_rate: float = DEFAULT_TAX_RATE,
    ) -> float:
        """Calcola il beta levered dal beta unlevered (formula di Hamada).

        Beta_l = Beta_u * (1 + (1 - t) * D/E)

        Args:
            beta_unlevered: Beta senza effetto leva.
            rapporto_de: Rapporto Debito/Equity target.
            tax_rate: Aliquota fiscale marginale.

        Returns:
            Beta levered.
        """
        return beta_unlevered * (1 + (1 - tax_rate) * rapporto_de)

    @classmethod
    def da_parametri_base(
        cls,
        beta_levered: float,
        rapporto_de: float,
        costo_debito_pre_tax: float,
        risk_free_rate: float = DEFAULT_RISK_FREE_RATE,
        equity_risk_premium: float = DEFAULT_ERP,
        country_risk_premium: float = 0.0,
        tax_rate: float = DEFAULT_TAX_RATE,
        small_cap_premium: float = 0.0,
        company_specific_premium: float = 0.0,
    ) -> "CostoCapitale":
        """Crea un'istanza CostoCapitale a partire dai parametri di base.

        Metodo factory che calcola automaticamente tutti i valori
        derivati (beta unlevered, pesi, costo equity, WACC) a partire
        dai parametri fondamentali.

        Args:
            beta_levered: Beta con effetto leva finanziaria.
            rapporto_de: Rapporto Debito/Equity (D/E) a valori di mercato.
            costo_debito_pre_tax: Costo del debito al lordo delle imposte.
            risk_free_rate: Tasso risk-free.
            equity_risk_premium: Equity Risk Premium maturo.
            country_risk_premium: Premio per rischio paese.
            tax_rate: Aliquota fiscale marginale.
            small_cap_premium: Premio per piccola capitalizzazione.
            company_specific_premium: Premio per rischi specifici.

        Returns:
            Istanza di CostoCapitale con tutti i valori calcolati.
        """
        # Calcola pesi dalla struttura del capitale
        peso_debito = rapporto_de / (1 + rapporto_de)
        peso_equity = 1 - peso_debito

        # Calcola beta unlevered
        beta_unlevered = cls.beta_unlevered_da_levered(
            beta_levered, rapporto_de, tax_rate
        )

        return cls(
            risk_free_rate=risk_free_rate,
            beta_levered=beta_levered,
            beta_unlevered=beta_unlevered,
            equity_risk_premium=equity_risk_premium,
            country_risk_premium=country_risk_premium,
            costo_debito_pre_tax=costo_debito_pre_tax,
            tax_rate=tax_rate,
            peso_equity=peso_equity,
            peso_debito=peso_debito,
            small_cap_premium=small_cap_premium,
            company_specific_premium=company_specific_premium,
        )

    def riepilogo(self) -> str:
        """Genera un riepilogo testuale della struttura del costo del capitale.

        Returns:
            Stringa formattata con tutti i componenti.
        """
        righe = [
            "Costo del Capitale",
            "=" * 40,
            f"Risk-Free Rate:         {self.risk_free_rate:.2%}",
            f"Beta Levered:           {self.beta_levered:.4f}",
            f"Beta Unlevered:         {self.beta_unlevered:.4f}",
            f"Equity Risk Premium:    {self.equity_risk_premium:.2%}",
            f"Country Risk Premium:   {self.country_risk_premium:.2%}",
        ]
        if self.small_cap_premium > 0:
            righe.append(f"Small Cap Premium:      {self.small_cap_premium:.2%}")
        if self.company_specific_premium > 0:
            righe.append(f"Company Specific Prem:  {self.company_specific_premium:.2%}")
        righe.extend([
            f"Costo Equity (Ke):      {self.costo_equity:.2%}",
            "-" * 40,
            f"Costo Debito (pre-tax): {self.costo_debito_pre_tax:.2%}",
            f"Costo Debito (post-tax):{self.costo_debito_post_tax:.2%}",
            f"Aliquota Fiscale:       {self.tax_rate:.2%}",
            "-" * 40,
            f"Peso Equity:            {self.peso_equity:.1%}",
            f"Peso Debito:            {self.peso_debito:.1%}",
            "=" * 40,
            f"WACC:                   {self.wacc:.2%}",
        ])
        return "\n".join(righe)

    def __str__(self) -> str:
        """Rappresentazione leggibile del costo del capitale."""
        return (
            f"WACC: {self.wacc:.2%} "
            f"(Ke={self.costo_equity:.2%}, "
            f"Kd={self.costo_debito_post_tax:.2%}, "
            f"We={self.peso_equity:.0%}, "
            f"Wd={self.peso_debito:.0%})"
        )
