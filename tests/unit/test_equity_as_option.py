"""Test per il modulo di valutazione dell'equity come opzione."""
import pytest
from valuation_analyst.tools.equity_as_option import (
    valuta_equity_come_opzione, stima_volatilita_asset, analisi_distress,
)


class TestValutaEquityComeOpzione:
    def test_equity_positivo(self):
        """Anche se V > K, l'equity deve essere positiva."""
        result = valuta_equity_come_opzione(
            valore_asset=100, debito_nominale=80,
            scadenza_debito=5.0, risk_free_rate=0.05,
            volatilita_asset=0.30,
        )
        assert result["valore_equity"] > 0

    def test_equity_in_distress(self):
        """Anche con V < K l'equity ha valore positivo (valore temporale)."""
        result = valuta_equity_come_opzione(
            valore_asset=70, debito_nominale=100,
            scadenza_debito=5.0, risk_free_rate=0.05,
            volatilita_asset=0.40,
        )
        assert result["valore_equity"] > 0
        assert result["probabilita_default"] > 0.20

    def test_somma_equity_debito_uguale_asset(self):
        """Valore equity + valore debito = valore asset."""
        result = valuta_equity_come_opzione(
            valore_asset=100, debito_nominale=80,
            scadenza_debito=5.0, risk_free_rate=0.05,
            volatilita_asset=0.30,
        )
        somma = result["valore_equity"] + result["valore_debito"]
        assert somma == pytest.approx(100, abs=0.01)


class TestStimaVolatilitaAsset:
    def test_volatilita_ridotta_dalla_leva(self):
        """La volatilita' degli asset e' minore di quella dell'equity."""
        sigma_v = stima_volatilita_asset(
            volatilita_equity=0.40, market_cap=800, debito_mercato=200,
        )
        assert sigma_v < 0.40
        # sigma_V = 0.40 * 800 / 1000 = 0.32
        assert sigma_v == pytest.approx(0.32)


class TestAnalisiDistress:
    def test_azienda_sana(self):
        """Azienda con V > K non e' in distress."""
        result = analisi_distress(
            valore_asset=150, debito_nominale=100,
            scadenza_debito=5.0, risk_free_rate=0.05,
            volatilita_asset=0.25,
        )
        assert result["in_distress"] is False
        assert result["rapporto_copertura"] > 1.0
