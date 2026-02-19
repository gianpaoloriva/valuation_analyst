"""Test per la stima del beta."""
import pytest
from valuation_analyst.tools.beta_estimation import beta_levered, beta_unlevered, total_beta


class TestBetaLevered:
    def test_hamada(self):
        """Beta_L = 1.0 * (1 + (1-0.25) * 0.5) = 1.375."""
        bl = beta_levered(1.0, 0.25, 0.5)
        assert bl == pytest.approx(1.375)

    def test_zero_debt(self):
        """Senza debito il beta levered coincide con l'unlevered."""
        bl = beta_levered(1.0, 0.25, 0.0)
        assert bl == pytest.approx(1.0)


class TestBetaUnlevered:
    def test_hamada_inversa(self):
        """Operazione inversa di Hamada per ricavare il beta unlevered."""
        bu = beta_unlevered(1.375, 0.25, 0.5)
        assert bu == pytest.approx(1.0, abs=0.001)


class TestTotalBeta:
    def test_total_beta(self):
        """Total beta = beta / correlazione = 1.0 / 0.5 = 2.0."""
        tb = total_beta(1.0, 0.5)
        assert tb == pytest.approx(2.0)
