"""Test per il modulo delle tabelle di sensitivita'."""
import pytest
from valuation_analyst.tools.sensitivity_table import (
    crea_tabella_sensitivity, sensitivity_wacc_growth,
)
from valuation_analyst.models.scenario import RisultatoSensitivity


class TestCreaTabellaSensitivity:
    def test_dimensioni_matrice(self):
        """La matrice risultante ha le dimensioni corrette."""
        def funzione_dummy(r: float, c: float) -> float:
            return r + c

        result = crea_tabella_sensitivity(
            funzione_valutazione=funzione_dummy,
            parametro_riga="riga",
            valori_riga=[1.0, 2.0, 3.0],
            parametro_colonna="colonna",
            valori_colonna=[10.0, 20.0],
        )
        assert len(result.matrice_risultati) == 3
        assert len(result.matrice_risultati[0]) == 2

    def test_valori_corretti(self):
        """I valori nella matrice corrispondono alla funzione."""
        def funzione_moltiplica(r: float, c: float) -> float:
            return r * c

        result = crea_tabella_sensitivity(
            funzione_valutazione=funzione_moltiplica,
            parametro_riga="riga",
            valori_riga=[2.0, 3.0],
            parametro_colonna="colonna",
            valori_colonna=[4.0, 5.0],
        )
        assert result.matrice_risultati[0][0] == pytest.approx(8.0)
        assert result.matrice_risultati[1][1] == pytest.approx(15.0)

    def test_gestione_errori(self):
        """Errori nella funzione di valutazione producono NaN."""
        import math

        def funzione_errore(r: float, c: float) -> float:
            if c == 0:
                raise ValueError("divisione per zero")
            return r / c

        result = crea_tabella_sensitivity(
            funzione_valutazione=funzione_errore,
            parametro_riga="riga",
            valori_riga=[1.0],
            parametro_colonna="colonna",
            valori_colonna=[0.0, 1.0],
        )
        assert math.isnan(result.matrice_risultati[0][0])
        assert result.matrice_risultati[0][1] == pytest.approx(1.0)


class TestSensitivityWACCGrowth:
    def test_output_valido(self):
        """La sensitivity WACC vs growth produce un risultato valido."""
        result = sensitivity_wacc_growth(
            fcff_base=100, debito_netto=200,
            shares_outstanding=10,
            wacc_range=[0.08, 0.09, 0.10],
            growth_range=[0.02, 0.025, 0.03],
        )
        assert isinstance(result, RisultatoSensitivity)
        assert len(result.matrice_risultati) == 3
        assert len(result.matrice_risultati[0]) == 3
