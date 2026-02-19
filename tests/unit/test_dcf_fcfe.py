"""Test per il modulo DCF FCFE."""
import pytest
from valuation_analyst.tools.dcf_fcfe import calcola_fcfe, calcola_fcfe_da_fcff


class TestCalcolaFCFE:
    def test_formula_base(self):
        """FCFE = Utile Netto + D&A - CapEx - Delta WC - Rimborso Debito Netto."""
        # FCFE = 80 + 20 - 30 - 5 - 0 = 65
        fcfe = calcola_fcfe(utile_netto=80, deprezzamento=20, capex=30, delta_wc=5)
        assert fcfe == pytest.approx(65.0)

    def test_rimborso_debito_riduce_fcfe(self):
        """Un rimborso netto di debito riduce il FCFE."""
        fcfe_base = calcola_fcfe(utile_netto=80, deprezzamento=20, capex=30, delta_wc=5)
        fcfe_rimborso = calcola_fcfe(
            utile_netto=80, deprezzamento=20, capex=30,
            delta_wc=5, rimborso_debito_netto=10,
        )
        assert fcfe_rimborso < fcfe_base

    def test_fcfe_negativo_possibile(self):
        """Se il capex e' molto alto, il FCFE puo' diventare negativo."""
        fcfe = calcola_fcfe(utile_netto=10, deprezzamento=5, capex=50, delta_wc=5)
        assert fcfe < 0


class TestCalcolaFCFEDaFCFF:
    def test_conversione_base(self):
        """FCFE = FCFF - Interessi*(1-t) + Nuovo Debito Netto."""
        # FCFE = 100 - 10*(1-0.25) + 0 = 100 - 7.5 = 92.5
        fcfe = calcola_fcfe_da_fcff(fcff=100, interessi=10, tax_rate=0.25)
        assert fcfe == pytest.approx(92.5)

    def test_nuovo_debito_aumenta_fcfe(self):
        """Emissione netta di debito aumenta il FCFE."""
        fcfe = calcola_fcfe_da_fcff(fcff=100, interessi=10, tax_rate=0.25, nuovo_debito_netto=20)
        assert fcfe == pytest.approx(112.5)
