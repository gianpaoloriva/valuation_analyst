"""Test per il modulo CAPM."""
import pytest
from valuation_analyst.tools.capm import calcola_costo_equity, calcola_costo_equity_dettagliato


class TestCostoEquity:
    def test_capm_base(self):
        """Re = 0.042 + 1.0 * 0.055 = 0.097."""
        re = calcola_costo_equity(risk_free_rate=0.042, beta=1.0, equity_risk_premium=0.055)
        assert re == pytest.approx(0.097, abs=0.001)

    def test_capm_con_crp(self):
        """Re = 0.042 + 1.2 * 0.055 + 0.02 = 0.128."""
        re = calcola_costo_equity(0.042, 1.2, 0.055, country_risk_premium=0.02)
        assert re == pytest.approx(0.128, abs=0.001)

    def test_beta_zero(self):
        """Beta 0 = risk free + premi."""
        re = calcola_costo_equity(0.042, 0.0, 0.055)
        assert re == pytest.approx(0.042, abs=0.001)

    def test_dettagliato(self):
        """La versione dettagliata restituisce un dizionario con costo_equity."""
        result = calcola_costo_equity_dettagliato(0.042, 1.0, 0.055)
        assert "costo_equity" in result
