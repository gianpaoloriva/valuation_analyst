"""Modello dati per gli input del modello Black-Scholes applicato alla valutazione.

Contiene la dataclass InputBlackScholes per la valutazione
dell'equity come opzione call sul valore delle attivita'
dell'impresa (modello di Merton).
"""

import math
from dataclasses import dataclass


@dataclass
class InputBlackScholes:
    """Input per il modello Black-Scholes applicato alla valutazione dell'equity.

    Nel modello di Merton, l'equity di un'azienda viene trattata
    come un'opzione call europea sul valore delle attivita' dell'impresa,
    con prezzo di esercizio pari al valore nominale del debito.

    Attributes:
        valore_attivita: V - Valore corrente delle attivita'/dell'impresa (in milioni).
        valore_nominale_debito: K - Valore nominale del debito (strike price, in milioni).
        scadenza_debito: T - Scadenza media ponderata del debito (in anni).
        risk_free_rate: Tasso risk-free annuale.
        volatilita: Sigma - Volatilita' annualizzata del valore dell'impresa.
        dividendo_yield: Rendimento da dividendo annuale dell'impresa (tasso continuo).
    """

    valore_attivita: float
    valore_nominale_debito: float
    scadenza_debito: float
    risk_free_rate: float
    volatilita: float
    dividendo_yield: float = 0.0

    def __post_init__(self) -> None:
        """Valida gli input dopo l'inizializzazione.

        Raises:
            ValueError: Se uno degli input non rispetta i vincoli.
        """
        if self.valore_attivita <= 0:
            raise ValueError(
                f"Il valore delle attivita' deve essere positivo, ricevuto: {self.valore_attivita}"
            )
        if self.valore_nominale_debito <= 0:
            raise ValueError(
                f"Il valore nominale del debito deve essere positivo, ricevuto: {self.valore_nominale_debito}"
            )
        if self.scadenza_debito <= 0:
            raise ValueError(
                f"La scadenza del debito deve essere positiva, ricevuto: {self.scadenza_debito}"
            )
        if self.volatilita <= 0:
            raise ValueError(
                f"La volatilita' deve essere positiva, ricevuto: {self.volatilita}"
            )
        if self.dividendo_yield < 0:
            raise ValueError(
                f"Il dividend yield non puo' essere negativo, ricevuto: {self.dividendo_yield}"
            )

    @property
    def d1(self) -> float:
        """Calcola d1 della formula di Black-Scholes.

        d1 = [ln(V/K) + (r - y + sigma^2/2) * T] / (sigma * sqrt(T))

        dove y e' il dividendo_yield.

        Returns:
            Valore di d1.
        """
        numeratore = (
            math.log(self.valore_attivita / self.valore_nominale_debito)
            + (self.risk_free_rate - self.dividendo_yield + self.volatilita**2 / 2)
            * self.scadenza_debito
        )
        denominatore = self.volatilita * math.sqrt(self.scadenza_debito)
        return numeratore / denominatore

    @property
    def d2(self) -> float:
        """Calcola d2 della formula di Black-Scholes.

        d2 = d1 - sigma * sqrt(T)

        Returns:
            Valore di d2.
        """
        return self.d1 - self.volatilita * math.sqrt(self.scadenza_debito)

    @property
    def rapporto_debito_attivita(self) -> float:
        """Rapporto tra valore nominale del debito e valore delle attivita'.

        Returns:
            K/V come valore decimale.
        """
        return self.valore_nominale_debito / self.valore_attivita

    @property
    def leva_finanziaria(self) -> float:
        """Leva finanziaria implicita (D/V).

        Returns:
            Rapporto debito/valore delle attivita'.
        """
        return self.valore_nominale_debito / self.valore_attivita

    def riepilogo(self) -> str:
        """Genera un riepilogo testuale degli input del modello.

        Returns:
            Stringa formattata con tutti i parametri e i valori intermedi.
        """
        righe = [
            "Input Black-Scholes (Modello di Merton)",
            "=" * 45,
            f"Valore Attivita' (V):     {self.valore_attivita:,.2f}M",
            f"Debito Nominale (K):      {self.valore_nominale_debito:,.2f}M",
            f"Scadenza Debito (T):      {self.scadenza_debito:.2f} anni",
            f"Risk-Free Rate (r):       {self.risk_free_rate:.2%}",
            f"Volatilita' (sigma):      {self.volatilita:.2%}",
            f"Dividend Yield (y):       {self.dividendo_yield:.2%}",
            "-" * 45,
            f"Rapporto D/V:             {self.rapporto_debito_attivita:.2%}",
            f"d1:                       {self.d1:.6f}",
            f"d2:                       {self.d2:.6f}",
        ]
        return "\n".join(righe)

    def __str__(self) -> str:
        """Rappresentazione leggibile degli input."""
        return (
            f"BS Input: V={self.valore_attivita:,.0f}M, "
            f"K={self.valore_nominale_debito:,.0f}M, "
            f"T={self.scadenza_debito:.1f}y, "
            f"sigma={self.volatilita:.1%}"
        )
