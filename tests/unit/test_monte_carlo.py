"""Test per la simulazione Monte Carlo tramite analisi scenari.

Nota: il progetto non ha un modulo Monte Carlo dedicato.
Questi test verificano la creazione di scenari multipli e il
calcolo del valore atteso ponderato, che e' il nucleo della
simulazione per scenari.
"""
import pytest
from valuation_analyst.tools.scenario_analysis import (
    crea_scenari_standard, analisi_scenari_personalizzata,
)


class TestScenariStandard:
    def test_tre_scenari(self):
        """Lo scenario standard produce esattamente 3 scenari."""
        analisi = crea_scenari_standard(valore_base=100)
        assert len(analisi.scenari) == 3

    def test_valore_atteso_positivo(self):
        """Il valore atteso ponderato deve essere positivo."""
        analisi = crea_scenari_standard(valore_base=100)
        assert analisi.valore_atteso > 0

    def test_probabilita_sommano_a_uno(self):
        """Le probabilita' di default sommano a 1."""
        analisi = crea_scenari_standard(valore_base=100)
        assert analisi.probabilita_valide is True


class TestScenariPersonalizzati:
    def test_scenari_da_lista(self):
        """Creazione di scenari da lista di dizionari."""
        scenari_input = [
            {"nome": "Ottimista", "probabilita": 0.3, "parametri": {}, "valore": 150},
            {"nome": "Base", "probabilita": 0.5, "parametri": {}, "valore": 100},
            {"nome": "Pessimista", "probabilita": 0.2, "parametri": {}, "valore": 60},
        ]
        analisi = analisi_scenari_personalizzata(scenari_input)
        assert len(analisi.scenari) == 3
        # Valore atteso = 0.3*150 + 0.5*100 + 0.2*60 = 45 + 50 + 12 = 107
        assert analisi.valore_atteso == pytest.approx(107.0)
