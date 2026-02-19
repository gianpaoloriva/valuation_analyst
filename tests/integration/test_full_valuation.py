"""Test di integrazione per la valutazione completa."""
import pytest


class TestFullValuation:
    def test_full_pipeline(self, apple_company):
        """Test che tutti i moduli si integrino correttamente."""
        # 1. WACC
        from valuation_analyst.tools.wacc import calcola_wacc

        wacc = calcola_wacc(0.11, 0.055, 0.153, 0.96, 0.04)
        assert 0.05 < wacc < 0.15

        # 2. DCF
        from valuation_analyst.tools.dcf_fcff import calcola_fcff

        fcff = calcola_fcff(
            apple_company.ebit, apple_company.tax_rate,
            apple_company.capex, apple_company.deprezzamento,
            apple_company.delta_working_capital,
        )
        assert fcff > 0
