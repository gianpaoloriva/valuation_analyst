"""Test per i validatori di input."""
import pytest
from valuation_analyst.utils.validators import (
    valida_ticker, valida_tasso, valida_positivo,
    valida_non_negativo, valida_percentuale, valida_anni, valida_peso,
)


class TestValidaTicker:
    def test_ticker_valido(self):
        """Ticker valido restituito in maiuscolo."""
        assert valida_ticker("AAPL") == "AAPL"

    def test_lowercase(self):
        """Ticker minuscolo convertito in maiuscolo."""
        assert valida_ticker("aapl") == "AAPL"

    def test_con_punto(self):
        """Ticker con punto (es. BRK.B) ammesso."""
        assert valida_ticker("BRK.B") == "BRK.B"

    def test_vuoto(self):
        """Ticker vuoto deve generare errore."""
        with pytest.raises(ValueError):
            valida_ticker("")

    def test_troppo_lungo(self):
        """Ticker troppo lungo deve generare errore."""
        with pytest.raises(ValueError):
            valida_ticker("A" * 11)


class TestValidaTasso:
    def test_tasso_valido(self):
        """Tasso nel range ammesso restituito invariato."""
        assert valida_tasso(0.10) == 0.10

    def test_tasso_troppo_basso(self):
        """Tasso sotto -1 deve generare errore."""
        with pytest.raises(ValueError):
            valida_tasso(-2.0)

    def test_tasso_troppo_alto(self):
        """Tasso sopra 5 deve generare errore."""
        with pytest.raises(ValueError):
            valida_tasso(6.0)


class TestValidaPositivo:
    def test_positivo(self):
        """Valore positivo restituito invariato."""
        assert valida_positivo(1.0) == 1.0

    def test_zero(self):
        """Zero non e' strettamente positivo: deve dare errore."""
        with pytest.raises(ValueError):
            valida_positivo(0.0)

    def test_negativo(self):
        """Valore negativo deve generare errore."""
        with pytest.raises(ValueError):
            valida_positivo(-1.0)


class TestValidaNonNegativo:
    def test_positivo(self):
        """Valore positivo restituito invariato."""
        assert valida_non_negativo(1.0) == 1.0

    def test_zero(self):
        """Zero e' ammesso per non-negativo."""
        assert valida_non_negativo(0.0) == 0.0

    def test_negativo(self):
        """Valore negativo deve generare errore."""
        with pytest.raises(ValueError):
            valida_non_negativo(-1.0)


class TestValidaPercentuale:
    def test_valida(self):
        """Percentuale nel range [0, 1] restituita invariata."""
        assert valida_percentuale(0.5) == 0.5

    def test_troppo_bassa(self):
        """Percentuale negativa deve generare errore."""
        with pytest.raises(ValueError):
            valida_percentuale(-0.1)

    def test_troppo_alta(self):
        """Percentuale sopra 1 deve generare errore."""
        with pytest.raises(ValueError):
            valida_percentuale(1.1)


class TestValidaAnni:
    def test_valido(self):
        """Numero di anni nel range [1, 100] restituito invariato."""
        assert valida_anni(10) == 10

    def test_zero(self):
        """Zero anni deve generare errore."""
        with pytest.raises(ValueError):
            valida_anni(0)

    def test_troppi(self):
        """Oltre 100 anni deve generare errore."""
        with pytest.raises(ValueError):
            valida_anni(101)


class TestValidaPeso:
    def test_valido(self):
        """Peso nel range [0, 1] restituito invariato."""
        assert valida_peso(0.6) == 0.6

    def test_invalido(self):
        """Peso sopra 1 deve generare errore."""
        with pytest.raises(ValueError):
            valida_peso(1.1)
