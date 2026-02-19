"""Test per il modulo dei multipli di mercato."""
import pytest
from valuation_analyst.tools.multiples import (
    calcola_pe, calcola_ev_ebitda, calcola_pb,
    valore_implicito_pe, valore_implicito_ev_ebitda,
)


class TestCalcolaPE:
    def test_pe_positivo(self):
        """P/E = 180 / 6 = 30."""
        pe = calcola_pe(prezzo=180, eps=6.0)
        assert pe == pytest.approx(30.0)

    def test_pe_eps_negativo(self):
        """EPS negativo restituisce None."""
        pe = calcola_pe(prezzo=180, eps=-2.0)
        assert pe is None


class TestCalcolaEVEBITDA:
    def test_ev_ebitda_positivo(self):
        """EV/EBITDA = 1000 / 100 = 10."""
        mult = calcola_ev_ebitda(enterprise_value=1000, ebitda=100)
        assert mult == pytest.approx(10.0)

    def test_ebitda_zero(self):
        """EBITDA zero restituisce None."""
        mult = calcola_ev_ebitda(enterprise_value=1000, ebitda=0)
        assert mult is None


class TestCalcolaPB:
    def test_pb_positivo(self):
        """P/B = 500 / 100 = 5."""
        pb = calcola_pb(market_cap=500, book_value=100)
        assert pb == pytest.approx(5.0)


class TestValoreImplicitoPE:
    def test_valore_implicito(self):
        """Valore implicito = EPS * PE mediano = 6 * 25 = 150."""
        valore = valore_implicito_pe(eps_target=6.0, pe_mediano=25.0)
        assert valore == pytest.approx(150.0)


class TestValoreImplicitoEVEBITDA:
    def test_valore_implicito(self):
        """EV = EBITDA*multiplo, poi sottrai debito netto e dividi per azioni."""
        # EV = 100 * 10 = 1000; Equity = 1000 - 200 = 800; per azione = 800/10 = 80
        valore = valore_implicito_ev_ebitda(
            ebitda_target=100, ev_ebitda_mediano=10,
            debito_netto=200, shares_outstanding=10,
        )
        assert valore == pytest.approx(80.0)
