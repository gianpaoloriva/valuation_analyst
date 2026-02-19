"""Test per i modelli di crescita multi-fase."""
import pytest
from valuation_analyst.tools.growth_models import (
    crescita_2_fasi, crescita_3_fasi,
    crescita_da_fondamentali, reinvestment_rate_stabile,
)


class TestCrescita2Fasi:
    def test_lunghezza_output(self):
        """Il modello a 2 fasi produce esattamente anni_alta tassi."""
        tassi = crescita_2_fasi(tasso_alta=0.15, tasso_stabile=0.025, anni_alta=5)
        assert len(tassi) == 5

    def test_tutti_tassi_alta(self):
        """Nella fase alta tutti i tassi sono uguali."""
        tassi = crescita_2_fasi(tasso_alta=0.20, tasso_stabile=0.03, anni_alta=3)
        assert all(t == pytest.approx(0.20) for t in tassi)


class TestCrescita3Fasi:
    def test_lunghezza_output(self):
        """Il modello a 3 fasi produce anni_alta + anni_transizione tassi."""
        tassi = crescita_3_fasi(tasso_alta=0.15, tasso_stabile=0.025, anni_alta=5, anni_transizione=5)
        assert len(tassi) == 10

    def test_convergenza(self):
        """L'ultimo tasso della transizione deve essere pari al tasso stabile."""
        tassi = crescita_3_fasi(tasso_alta=0.20, tasso_stabile=0.03, anni_alta=3, anni_transizione=4)
        assert tassi[-1] == pytest.approx(0.03, abs=0.001)

    def test_fase_alta_costante(self):
        """I primi anni_alta tassi sono costanti e pari a tasso_alta."""
        tassi = crescita_3_fasi(tasso_alta=0.15, tasso_stabile=0.025, anni_alta=5, anni_transizione=5)
        for t in tassi[:5]:
            assert t == pytest.approx(0.15)


class TestCrescitaDaFondamentali:
    def test_crescita_fondamentale(self):
        """g = RIR * ROIC = 0.50 * 0.15 = 0.075."""
        g = crescita_da_fondamentali(reinvestment_rate=0.50, roic=0.15)
        assert g == pytest.approx(0.075)


class TestReinvestmentRateStabile:
    def test_rir_stabile(self):
        """RIR = g / ROIC = 0.025 / 0.10 = 0.25."""
        rir = reinvestment_rate_stabile(tasso_crescita_stabile=0.025, roic_stabile=0.10)
        assert rir == pytest.approx(0.25)
