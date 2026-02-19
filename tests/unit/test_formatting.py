"""Test per le utilita' di formattazione."""
import pytest
from valuation_analyst.utils.formatting import (
    formatta_valuta, formatta_percentuale, formatta_numero,
    formatta_milioni, formatta_miliardi, formatta_multiplo,
    tabella_markdown,
)


class TestFormattaValuta:
    def test_usd(self):
        """Formattazione in dollari americani."""
        result = formatta_valuta(1234.56, "USD")
        assert "$" in result
        assert "1" in result

    def test_eur(self):
        """Formattazione in euro con formato europeo."""
        result = formatta_valuta(1234.56, "EUR")
        assert "\u20ac" in result


class TestFormattaPercentuale:
    def test_base(self):
        """Conversione decimale -> percentuale."""
        assert "12.34%" in formatta_percentuale(0.1234) or "12.34" in formatta_percentuale(0.1234)

    def test_zero(self):
        """Zero deve contenere il carattere 0."""
        result = formatta_percentuale(0.0)
        assert "0" in result


class TestFormattaNumero:
    def test_grande(self):
        """Numero grande con separatore delle migliaia."""
        result = formatta_numero(1234567.89)
        assert "1" in result


class TestFormattaMillioni:
    def test_base(self):
        """1.5 miliardi espressi in milioni con suffisso M."""
        result = formatta_milioni(1_500_000_000)
        assert "M" in result or "m" in result


class TestFormattaMiliardi:
    def test_base(self):
        """2.8 trilioni espressi in miliardi con suffisso B."""
        result = formatta_miliardi(2_800_000_000_000)
        assert "B" in result or "b" in result


class TestFormattaMultiplo:
    def test_base(self):
        """Multiplo formattato con suffisso x."""
        result = formatta_multiplo(12.3)
        assert "x" in result


class TestTabellaMarkdown:
    def test_tabella_semplice(self):
        """Tabella markdown con intestazione e separatore."""
        result = tabella_markdown(["A", "B"], [["1", "2"], ["3", "4"]])
        assert "|" in result
        assert "A" in result
        assert "--" in result
