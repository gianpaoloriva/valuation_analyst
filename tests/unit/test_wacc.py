"""Test per il modulo WACC."""
import pytest
from valuation_analyst.tools.wacc import calcola_wacc, calcola_wacc_completo


class TestWACC:
    def test_wacc_base(self):
        """WACC = 0.8*0.10 + 0.2*0.05*(1-0.25) = 0.08 + 0.0075 = 0.0875."""
        result = calcola_wacc(0.10, 0.05, 0.25, 0.80, 0.20)
        assert result == pytest.approx(0.0875, abs=0.001)

    def test_wacc_all_equity(self):
        """100% equity: WACC = costo equity."""
        result = calcola_wacc(0.10, 0.05, 0.25, 1.0, 0.0)
        assert result == pytest.approx(0.10, abs=0.001)

    def test_wacc_completo(self):
        """WACC completo con restituzione di oggetto CostoCapitale."""
        cc = calcola_wacc_completo(
            risk_free_rate=0.042, beta=1.2, equity_risk_premium=0.055,
            costo_debito_pre_tax=0.05, tax_rate=0.25,
            market_cap=1000, total_debt=200,
        )
        assert cc.wacc > 0
        assert cc.peso_equity + cc.peso_debito == pytest.approx(1.0, abs=0.01)
