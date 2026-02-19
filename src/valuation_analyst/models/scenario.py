"""Modelli dati per l'analisi degli scenari e la sensitivity analysis.

Contiene le dataclass Scenario e RisultatoSensitivity per
gestire scenari di valutazione (best/base/worst) e matrici
di sensitivita' bidimensionali.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Scenario:
    """Rappresenta uno scenario di valutazione.

    Ogni scenario e' caratterizzato da un nome, una probabilita'
    di accadimento, un insieme di parametri e il valore risultante
    dalla valutazione con quei parametri.

    Attributes:
        nome: Nome descrittivo dello scenario (es. "Best", "Base", "Worst").
        probabilita: Probabilita' di accadimento (valore tra 0 e 1).
        parametri: Dizionario dei parametri dello scenario
                   (chiave = nome parametro, valore = valore del parametro).
        valore_risultante: Valore per azione risultante dalla valutazione
                           con i parametri di questo scenario.
        valore_equity: Valore totale dell'equity risultante (in milioni).
        note: Note o commenti sullo scenario.
    """

    nome: str
    probabilita: float
    parametri: dict[str, Any] = field(default_factory=dict)
    valore_risultante: float | None = None
    valore_equity: float | None = None
    note: str = ""

    def __post_init__(self) -> None:
        """Valida la probabilita' dopo l'inizializzazione.

        Raises:
            ValueError: Se la probabilita' non e' compresa tra 0 e 1.
        """
        if not 0.0 <= self.probabilita <= 1.0:
            raise ValueError(
                f"La probabilita' deve essere compresa tra 0 e 1, ricevuto: {self.probabilita}"
            )

    @property
    def valore_ponderato(self) -> float:
        """Valore risultante ponderato per la probabilita'.

        Returns:
            Valore per azione moltiplicato per la probabilita',
            oppure 0.0 se il valore risultante non e' disponibile.
        """
        if self.valore_risultante is not None:
            return self.valore_risultante * self.probabilita
        return 0.0

    def __str__(self) -> str:
        """Rappresentazione leggibile dello scenario."""
        valore_str = f"{self.valore_risultante:,.2f}" if self.valore_risultante is not None else "N/D"
        return (
            f"Scenario {self.nome}: P={self.probabilita:.0%}, "
            f"Valore={valore_str}"
        )


@dataclass
class AnalisiScenari:
    """Raccoglie piu' scenari e calcola il valore atteso ponderato.

    Attributes:
        scenari: Lista degli scenari di valutazione.
        ticker: Ticker dell'azienda oggetto di valutazione.
        metodo: Metodo di valutazione utilizzato.
    """

    scenari: list[Scenario] = field(default_factory=list)
    ticker: str = ""
    metodo: str = ""

    @property
    def valore_atteso(self) -> float:
        """Calcola il valore atteso ponderato per le probabilita'.

        Returns:
            Media ponderata dei valori risultanti per le probabilita'.
        """
        return sum(s.valore_ponderato for s in self.scenari)

    @property
    def somma_probabilita(self) -> float:
        """Verifica che le probabilita' sommino a 1.

        Returns:
            Somma delle probabilita' di tutti gli scenari.
        """
        return sum(s.probabilita for s in self.scenari)

    @property
    def probabilita_valide(self) -> bool:
        """Controlla se le probabilita' sono coerenti (sommano a ~1).

        Returns:
            True se la somma delle probabilita' e' prossima a 1.0.
        """
        return abs(self.somma_probabilita - 1.0) < 0.001

    def ottieni_scenario(self, nome: str) -> Scenario | None:
        """Restituisce lo scenario con il nome specificato.

        Args:
            nome: Nome dello scenario da cercare.

        Returns:
            Istanza Scenario se trovato, None altrimenti.
        """
        for scenario in self.scenari:
            if scenario.nome.lower() == nome.lower():
                return scenario
        return None

    def riepilogo(self) -> str:
        """Genera un riepilogo testuale dell'analisi degli scenari.

        Returns:
            Stringa formattata con tutti gli scenari e il valore atteso.
        """
        righe = [
            f"Analisi Scenari - {self.ticker} ({self.metodo})",
            "=" * 50,
        ]

        for scenario in self.scenari:
            righe.append(f"  {scenario}")

        righe.extend([
            "-" * 50,
            f"Valore Atteso Ponderato: {self.valore_atteso:,.2f}",
            f"Somma Probabilita': {self.somma_probabilita:.2%}"
            + (" [OK]" if self.probabilita_valide else " [ATTENZIONE]"),
        ])

        return "\n".join(righe)

    def __str__(self) -> str:
        """Rappresentazione leggibile dell'analisi scenari."""
        return (
            f"Scenari {self.ticker}: {len(self.scenari)} scenari, "
            f"VA={self.valore_atteso:,.2f}"
        )


@dataclass
class RisultatoSensitivity:
    """Risultato di un'analisi di sensitivita' bidimensionale.

    Rappresenta una matrice di risultati ottenuta variando
    due parametri lungo i rispettivi assi.

    Attributes:
        parametro_riga: Nome del parametro variato sulle righe.
        parametro_colonna: Nome del parametro variato sulle colonne.
        valori_riga: Lista dei valori assunti dal parametro riga.
        valori_colonna: Lista dei valori assunti dal parametro colonna.
        matrice_risultati: Matrice dei valori risultanti (righe x colonne).
        ticker: Ticker dell'azienda oggetto di valutazione.
        metodo: Metodo di valutazione utilizzato.
        tipo_risultato: Tipo di valore nella matrice ("valore_per_azione", "equity", "wacc", ecc.).
    """

    parametro_riga: str
    parametro_colonna: str
    valori_riga: list[float]
    valori_colonna: list[float]
    matrice_risultati: list[list[float]]
    ticker: str = ""
    metodo: str = ""
    tipo_risultato: str = "valore_per_azione"

    def __post_init__(self) -> None:
        """Valida la coerenza delle dimensioni della matrice.

        Raises:
            ValueError: Se le dimensioni della matrice non corrispondono
                        alla lunghezza dei vettori di valori.
        """
        num_righe = len(self.valori_riga)
        num_colonne = len(self.valori_colonna)

        if len(self.matrice_risultati) != num_righe:
            raise ValueError(
                f"Numero di righe della matrice ({len(self.matrice_risultati)}) "
                f"non corrisponde a valori_riga ({num_righe})"
            )

        for i, riga in enumerate(self.matrice_risultati):
            if len(riga) != num_colonne:
                raise ValueError(
                    f"Riga {i} ha {len(riga)} colonne, attese {num_colonne}"
                )

    @property
    def valore_minimo(self) -> float:
        """Valore minimo nella matrice dei risultati.

        Returns:
            Valore minimo trovato in tutta la matrice.
        """
        return min(min(riga) for riga in self.matrice_risultati)

    @property
    def valore_massimo(self) -> float:
        """Valore massimo nella matrice dei risultati.

        Returns:
            Valore massimo trovato in tutta la matrice.
        """
        return max(max(riga) for riga in self.matrice_risultati)

    @property
    def valore_centrale(self) -> float:
        """Valore al centro della matrice.

        Returns:
            Valore nella posizione centrale della matrice.
        """
        riga_centrale = len(self.valori_riga) // 2
        colonna_centrale = len(self.valori_colonna) // 2
        return self.matrice_risultati[riga_centrale][colonna_centrale]

    @property
    def range_valori(self) -> float:
        """Differenza tra valore massimo e minimo.

        Returns:
            Range dei valori nella matrice.
        """
        return self.valore_massimo - self.valore_minimo

    def ottieni_valore(self, indice_riga: int, indice_colonna: int) -> float:
        """Restituisce un singolo valore dalla matrice.

        Args:
            indice_riga: Indice della riga (0-based).
            indice_colonna: Indice della colonna (0-based).

        Returns:
            Valore nella posizione specificata.

        Raises:
            IndexError: Se gli indici sono fuori range.
        """
        return self.matrice_risultati[indice_riga][indice_colonna]

    def riepilogo(self) -> str:
        """Genera un riepilogo testuale della sensitivity analysis.

        Returns:
            Stringa formattata con la matrice dei risultati.
        """
        righe = [
            f"Sensitivity Analysis - {self.ticker} ({self.metodo})",
            f"Riga: {self.parametro_riga} | Colonna: {self.parametro_colonna}",
            f"Tipo risultato: {self.tipo_risultato}",
            "",
        ]

        # Intestazione colonne
        intestazione = f"{'':>12}"
        for val_col in self.valori_colonna:
            intestazione += f" {val_col:>10.4f}"
        righe.append(intestazione)
        righe.append("-" * len(intestazione))

        # Righe della matrice
        for i, val_riga in enumerate(self.valori_riga):
            riga_str = f"{val_riga:>12.4f}"
            for val in self.matrice_risultati[i]:
                riga_str += f" {val:>10.2f}"
            righe.append(riga_str)

        righe.extend([
            "",
            f"Range: {self.valore_minimo:,.2f} - {self.valore_massimo:,.2f}",
            f"Valore Centrale: {self.valore_centrale:,.2f}",
        ])

        return "\n".join(righe)

    def __str__(self) -> str:
        """Rappresentazione leggibile della sensitivity."""
        return (
            f"Sensitivity {self.parametro_riga} x {self.parametro_colonna}: "
            f"{len(self.valori_riga)}x{len(self.valori_colonna)} "
            f"[{self.valore_minimo:,.2f} - {self.valore_massimo:,.2f}]"
        )
