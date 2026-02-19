"""Test per il modulo Black-Scholes."""
import math
import pytest
from valuation_analyst.tools.black_scholes import prezzo_call, prezzo_put, calcola_d1, calcola_d2


class TestPrezzoCall:
    def test_call_atm(self):
        """Call at-the-money deve avere un valore positivo significativo."""
        # V=100, K=100, r=0.05, sigma=0.20, T=1
        call = prezzo_call(V=100, K=100, r=0.05, sigma=0.20, T=1.0)
        assert call > 0
        # La call ATM a 1 anno con sigma=20% dovrebbe essere circa 10-12
        assert 5 < call < 20

    def test_call_deep_itm(self):
        """Call deep in-the-money ~ valore intrinseco attualizzato."""
        call = prezzo_call(V=200, K=100, r=0.05, sigma=0.20, T=1.0)
        # Il valore deve essere almeno il valore intrinseco scontato
        assert call > 200 - 100 * math.exp(-0.05)

    def test_call_deep_otm(self):
        """Call deep out-of-the-money ha valore vicino a zero."""
        call = prezzo_call(V=50, K=200, r=0.05, sigma=0.20, T=1.0)
        assert call < 1.0


class TestPrezzoPut:
    def test_put_call_parity(self):
        """Verifica la parita' put-call: C - P = V*e^(-qT) - K*e^(-rT)."""
        V, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
        call = prezzo_call(V, K, r, sigma, T)
        put = prezzo_put(V, K, r, sigma, T)
        # Senza dividendi: C - P = V - K*e^(-rT)
        lato_destro = V - K * math.exp(-r * T)
        assert (call - put) == pytest.approx(lato_destro, abs=0.01)


class TestD1D2:
    def test_d2_minore_d1(self):
        """d2 e' sempre minore di d1 (differenza = sigma*sqrt(T))."""
        d1 = calcola_d1(V=100, K=100, r=0.05, sigma=0.30, T=2.0)
        d2 = calcola_d2(d1, sigma=0.30, T=2.0)
        assert d2 < d1
        assert (d1 - d2) == pytest.approx(0.30 * math.sqrt(2.0), abs=0.001)
