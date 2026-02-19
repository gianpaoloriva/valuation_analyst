"""Test per il modulo di risk premium."""
import pytest
from valuation_analyst.tools.risk_premium import (
    spread_da_rating, costo_debito_sintetico, calcola_country_risk_premium,
)


class TestSpreadDaRating:
    def test_rating_bbb(self):
        """Rating BBB ha uno spread di 200 bps."""
        spread = spread_da_rating("BBB")
        assert spread == pytest.approx(0.020)

    def test_rating_aaa(self):
        """Rating AAA ha lo spread piu' basso."""
        spread = spread_da_rating("AAA")
        assert spread < 0.01

    def test_rating_non_valido(self):
        """Rating inesistente deve generare errore."""
        with pytest.raises(ValueError):
            spread_da_rating("ZZZ")

    def test_case_insensitive(self):
        """La ricerca del rating e' case-insensitive."""
        spread = spread_da_rating("bbb")
        assert spread == pytest.approx(0.020)


class TestCostoDebitoSintetico:
    def test_coverage_alta(self):
        """Coverage ratio alta produce rating AAA e costo basso."""
        result = costo_debito_sintetico(interest_coverage=10.0, risk_free_rate=0.04)
        assert result["rating_implicito"] == "AAA"
        assert result["costo_debito"] < 0.06

    def test_coverage_bassa(self):
        """Coverage ratio bassa produce rating basso e costo alto."""
        result = costo_debito_sintetico(interest_coverage=0.5, risk_free_rate=0.04)
        assert result["costo_debito"] > 0.10


class TestCalcolaCountryRiskPremium:
    def test_crp_da_rating(self):
        """CRP = spread * moltiplicatore = spread(BBB) * 1.5."""
        crp = calcola_country_risk_premium(rating_sovrano="BBB")
        assert crp == pytest.approx(0.020 * 1.5)

    def test_crp_senza_parametri(self):
        """Senza rating ne' spread deve generare errore."""
        with pytest.raises(ValueError):
            calcola_country_risk_premium()
