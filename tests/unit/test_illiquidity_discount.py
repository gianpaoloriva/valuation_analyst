"""Test per il modulo dello sconto di illiquidita'."""
import pytest
from valuation_analyst.tools.illiquidity_discount import (
    calcola_sconto_illiquidita, sconto_per_dimensione, applica_sconto_illiquidita,
)


class TestCalcolaScontoIlliquidita:
    def test_sconto_piccola_azienda(self):
        """Un'azienda piccola con margini bassi ha sconto maggiore di una grande."""
        result = calcola_sconto_illiquidita(ricavi=5_000_000, margine_ebitda=0.10)
        assert result["sconto"] >= 0.05  # almeno il floor

    def test_sconto_grande_azienda(self):
        """Un'azienda grande con margini alti ha sconto ridotto."""
        result = calcola_sconto_illiquidita(ricavi=500_000_000, margine_ebitda=0.30)
        assert result["sconto"] < 0.20

    def test_floor_e_cap(self):
        """Lo sconto deve essere nel range [5%, 50%]."""
        result = calcola_sconto_illiquidita(ricavi=10_000_000_000, margine_ebitda=0.50)
        assert 0.05 <= result["sconto"] <= 0.50


class TestScontoPerDimensione:
    def test_micro_azienda(self):
        """Micro azienda (<10M ricavi) -> sconto ~35%."""
        sconto = sconto_per_dimensione(ricavi=5_000_000)
        assert sconto == pytest.approx(0.35)

    def test_grande_azienda(self):
        """Azienda grande (>1B ricavi) -> sconto ~12.5%."""
        sconto = sconto_per_dimensione(ricavi=2_000_000_000)
        assert sconto == pytest.approx(0.125)


class TestApplicaScontoIlliquidita:
    def test_applicazione_base(self):
        """Lo sconto riduce il valore nella giusta misura."""
        result = applica_sconto_illiquidita(valore_quotata=1000, sconto=0.25)
        assert result["valore_scontato"] == pytest.approx(750.0)
        assert result["sconto_applicato"] == pytest.approx(250.0)
