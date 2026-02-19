"""Test per il modulo del premio di controllo."""
import pytest
from valuation_analyst.tools.control_premium import (
    calcola_premio_controllo, sconto_minoranza, applica_premio_controllo,
)


class TestCalcolaPremioControllo:
    def test_minoranza_premio_zero(self):
        """Per una partecipazione di minoranza il premio e' zero."""
        result = calcola_premio_controllo(
            valore_status_quo=1000, tipo_controllo="minoranza",
        )
        assert result["premio"] == 0.0

    def test_maggioranza_management_scarso(self):
        """Management scarso genera premio piu' alto."""
        result = calcola_premio_controllo(
            valore_status_quo=1000, tipo_controllo="maggioranza",
            qualita_management="scarso",
        )
        # Range benchmark: 25-40%, punto medio ~32.5%
        assert result["premio"] > 0.20

    def test_analitico(self):
        """Calcolo analitico: (V_ottimale - V_status_quo) / V_status_quo."""
        result = calcola_premio_controllo(
            valore_status_quo=100, valore_ottimale=130,
        )
        assert result["premio"] == pytest.approx(0.30)


class TestScontoMinoranza:
    def test_sconto_da_premio(self):
        """Sconto = 1 - 1/(1+0.25) = 0.20."""
        sconto = sconto_minoranza(premio_controllo=0.25)
        assert sconto == pytest.approx(0.20)

    def test_premio_zero(self):
        """Senza premio di controllo, sconto di minoranza e' zero."""
        sconto = sconto_minoranza(premio_controllo=0.0)
        assert sconto == 0.0


class TestApplicaPremioControllo:
    def test_applicazione_base(self):
        """Il premio aumenta il valore nella giusta misura."""
        result = applica_premio_controllo(valore_base=1000, premio=0.20)
        assert result["valore_con_premio"] == pytest.approx(1200.0)
        assert result["premio_applicato"] == pytest.approx(200.0)
