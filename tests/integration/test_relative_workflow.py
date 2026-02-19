"""Test di integrazione per il workflow di valutazione relativa."""
import pytest


class TestRelativeWorkflow:
    def test_valutazione_relativa(self, sample_comparabili):
        """Test valutazione relativa con comparabili."""
        from valuation_analyst.tools.multiples import valutazione_relativa

        result = valutazione_relativa(
            ticker="AAPL", eps=6.23, ebitda=133_000_000_000,
            book_value_per_share=3.84, ricavi=383_000_000_000,
            debito_netto=49_000_000_000, shares_outstanding=15_500_000_000,
            comparabili=sample_comparabili,
        )
        assert result.valore_per_azione > 0
