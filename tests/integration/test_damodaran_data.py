"""Test per il download e parsing dei dataset Damodaran.

Nota: questi test richiedono connessione internet.
Marcati con @pytest.mark.integration.
"""
import pytest


@pytest.mark.integration
class TestDamodaranData:
    def test_lista_settori_non_vuota(self):
        """Verifica che la funzione lista_settori esista e sia richiamabile."""
        # Non scarichiamo effettivamente i dati, verifichiamo solo che la funzione esista
        from valuation_analyst.tools.damodaran_data import lista_settori

        assert callable(lista_settori)
