"""Test per il modulo di valutazione delle sinergie."""
import pytest
from valuation_analyst.tools.synergy_valuation import (
    stima_sinergie_costo, stima_sinergie_ricavo, stima_sinergie_finanziarie,
)


class TestStimaSinergieCosto:
    def test_risparmio_positivo(self):
        """Le sinergie di costo devono produrre un valore attuale positivo."""
        result = stima_sinergie_costo(
            costi_combinati=1000, percentuale_risparmio=0.05, wacc=0.09,
        )
        assert result["pv_sinergie"] > 0
        assert result["risparmio_annuo_pieno"] == pytest.approx(50.0)

    def test_costi_integrazione_riducono_valore(self):
        """I costi di integrazione riducono il valore netto delle sinergie."""
        result = stima_sinergie_costo(
            costi_combinati=1000, percentuale_risparmio=0.05,
            wacc=0.09, costi_integrazione=100,
        )
        assert result["valore_netto_sinergie"] < result["pv_sinergie"]

    def test_profilo_graduale(self):
        """Il profilo di realizzazione cresce linearmente."""
        result = stima_sinergie_costo(
            costi_combinati=1000, percentuale_risparmio=0.10,
            anni_realizzazione=3, wacc=0.09,
        )
        profilo = result["profilo_realizzazione"]
        assert len(profilo) == 3
        # Ogni anno successivo deve avere un flusso maggiore
        assert profilo[0] < profilo[1] < profilo[2]


class TestStimaSinergieRicavo:
    def test_pv_positivo(self):
        """Le sinergie di ricavo devono generare un valore attuale positivo."""
        result = stima_sinergie_ricavo(
            ricavi_combinati=5000, percentuale_crescita=0.02,
            margine_incrementale=0.30, wacc=0.09,
        )
        assert result["pv_sinergie"] > 0


class TestStimaSinergieFinanziarie:
    def test_risparmio_interessi(self):
        """Il risparmio sugli interessi produce un valore positivo."""
        result = stima_sinergie_finanziarie(
            debito_target=500, risparmio_spread=0.01, tax_rate=0.25, wacc=0.09,
        )
        assert result["pv_risparmio_interessi"] > 0
        assert result["totale"] > 0
