"""Test per il modulo DCF FCFF."""
import pytest
from valuation_analyst.tools.dcf_fcff import calcola_fcff, calcola_dcf_fcff


class TestCalcolaFCFF:
    def test_formula_base(self):
        """FCFF = EBIT*(1-t) + D&A - CapEx - Delta WC."""
        # FCFF = 100*(1-0.25) + 20 - 30 - 5 = 75 + 20 - 30 - 5 = 60
        fcff = calcola_fcff(ebit=100, tax_rate=0.25, capex=30, deprezzamento=20, delta_wc=5)
        assert fcff == pytest.approx(60.0)

    def test_fcff_positivo_con_dati_apple(self):
        """Verifica che i dati Apple producano un FCFF positivo."""
        fcff = calcola_fcff(
            ebit=120_000_000_000, tax_rate=0.153,
            capex=11_000_000_000, deprezzamento=13_000_000_000,
            delta_wc=-3_000_000_000,
        )
        assert fcff > 0

    def test_delta_wc_negativo_aumenta_fcff(self):
        """Una riduzione del working capital libera cassa e aumenta il FCFF."""
        fcff_base = calcola_fcff(ebit=100, tax_rate=0.25, capex=30, deprezzamento=20, delta_wc=0)
        fcff_rilascio = calcola_fcff(ebit=100, tax_rate=0.25, capex=30, deprezzamento=20, delta_wc=-10)
        assert fcff_rilascio > fcff_base


class TestCalcolaDCFFCFF:
    def test_dcf_base(self):
        """Il DCF deve produrre un valore totale positivo."""
        projection = calcola_dcf_fcff(fcff_base=100, wacc=0.09)
        assert projection.valore_totale > 0

    def test_terminal_value_presente(self):
        """Il valore terminale attualizzato deve essere positivo."""
        projection = calcola_dcf_fcff(fcff_base=100, wacc=0.09)
        assert projection.valore_terminale_attuale > 0
