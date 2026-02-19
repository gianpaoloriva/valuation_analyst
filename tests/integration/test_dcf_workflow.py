"""Test di integrazione per il workflow DCF completo."""
import pytest


class TestDCFWorkflow:
    def test_fcff_workflow_apple(self, apple_company):
        """Test workflow FCFF con dati Apple."""
        from valuation_analyst.tools.dcf_fcff import calcola_fcff, calcola_dcf_fcff

        # Calcolo FCFF base dai dati fondamentali
        fcff = calcola_fcff(
            ebit=apple_company.ebit,
            tax_rate=apple_company.tax_rate,
            capex=apple_company.capex,
            deprezzamento=apple_company.deprezzamento,
            delta_wc=apple_company.delta_working_capital,
        )
        assert fcff > 0

        # DCF completo con proiezione multi-stage
        projection = calcola_dcf_fcff(fcff_base=fcff, wacc=0.09)
        assert projection.valore_totale > 0
