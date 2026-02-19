"""Test per le funzioni matematiche finanziarie."""
import pytest
import math
from valuation_analyst.utils.math_helpers import (
    npv, irr, pv, fv, cagr, gordon_growth,
    wacc_formula, levered_beta, unlevered_beta,
)


class TestNPV:
    def test_npv_positivo(self):
        """NPV di un investimento redditizio."""
        assert npv(0.10, [-1000, 300, 400, 500, 200]) == pytest.approx(115.57, abs=1)

    def test_npv_zero_rate(self):
        """NPV con tasso zero = somma dei flussi."""
        assert npv(0.0, [-100, 50, 50, 50]) == pytest.approx(50.0, abs=0.01)

    def test_npv_negativo(self):
        """NPV di un investimento in perdita."""
        result = npv(0.10, [-1000, 100, 100, 100])
        assert result < 0


class TestIRR:
    def test_irr_semplice(self):
        """IRR di un investimento semplice."""
        result = irr([-1000, 300, 400, 500, 200])
        assert 0.10 < result < 0.20

    def test_irr_validazione(self):
        """IRR richiede almeno un flusso negativo e uno positivo."""
        with pytest.raises(ValueError):
            irr([100, 200, 300])


class TestPV:
    def test_pv_base(self):
        """Valore attuale di 1000 scontato al 10% per 5 anni."""
        assert pv(1000, 0.10, 5) == pytest.approx(620.92, abs=1)

    def test_pv_zero_rate(self):
        """Con tasso zero il valore attuale e' uguale al valore futuro."""
        assert pv(1000, 0.0, 5) == pytest.approx(1000.0, abs=0.01)


class TestFV:
    def test_fv_base(self):
        """Valore futuro di 1000 capitalizzato al 10% per 5 anni."""
        assert fv(1000, 0.10, 5) == pytest.approx(1610.51, abs=1)


class TestCAGR:
    def test_cagr_raddoppio(self):
        """Raddoppio in ~7 anni al 10%."""
        assert cagr(100, 200, 7) == pytest.approx(0.1041, abs=0.001)

    def test_cagr_no_crescita(self):
        """Nessuna crescita implica CAGR pari a zero."""
        assert cagr(100, 100, 5) == pytest.approx(0.0)

    def test_cagr_validazione(self):
        """Valore iniziale zero deve generare errore."""
        with pytest.raises(ValueError):
            cagr(0, 100, 5)


class TestGordonGrowth:
    def test_gordon_base(self):
        """TV = 100*(1+0.03)/(0.10-0.03) = 1471.43."""
        assert gordon_growth(100, 0.10, 0.03) == pytest.approx(1471.43, abs=1)

    def test_gordon_tasso_uguale_crescita(self):
        """Tasso di sconto uguale alla crescita deve generare errore."""
        with pytest.raises(ValueError):
            gordon_growth(100, 0.05, 0.05)

    def test_gordon_crescita_maggiore_sconto(self):
        """Crescita maggiore del tasso di sconto deve generare errore."""
        with pytest.raises(ValueError):
            gordon_growth(100, 0.05, 0.06)


class TestWACC:
    def test_wacc_tipico(self):
        """WACC tipico US large cap ~8-10%."""
        result = wacc_formula(0.80, 0.10, 0.20, 0.05, 0.25)
        assert 0.08 < result < 0.10

    def test_wacc_pesi_errati(self):
        """Pesi che non sommano a 1 dovrebbero dare errore."""
        with pytest.raises(ValueError):
            wacc_formula(0.80, 0.10, 0.30, 0.05, 0.25)


class TestBeta:
    def test_levered_beta(self):
        """Beta_L = 1.0 * (1 + (1-0.25) * 0.5) = 1.375."""
        assert levered_beta(1.0, 0.25, 0.5) == pytest.approx(1.375)

    def test_unlevered_beta(self):
        """Inverso di levered."""
        assert unlevered_beta(1.375, 0.25, 0.5) == pytest.approx(1.0, abs=0.001)

    def test_roundtrip(self):
        """Lever e unlever devono essere inversi."""
        bu = 0.90
        bl = levered_beta(bu, 0.25, 0.6)
        bu_back = unlevered_beta(bl, 0.25, 0.6)
        assert bu_back == pytest.approx(bu, abs=0.001)
