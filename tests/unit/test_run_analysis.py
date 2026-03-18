"""Test per le funzionalita' di run_analysis.py.

Verifica:
- _safe_div: divisione sicura con denominatori <= 0
- _fmt_multiplo: formattazione multipli con None
- carica_config: caricamento config dal nuovo path
- genera_report: gestione aziende in perdita (EBIT/EPS negativi)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Importa le funzioni helper dallo script
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


class TestSafeDiv:
    """Test per la funzione _safe_div."""

    def test_divisione_normale(self) -> None:
        from run_analysis import _safe_div
        assert _safe_div(100.0, 10.0) == 10.0

    def test_denominatore_zero(self) -> None:
        from run_analysis import _safe_div
        assert _safe_div(100.0, 0.0) is None

    def test_denominatore_negativo(self) -> None:
        from run_analysis import _safe_div
        assert _safe_div(100.0, -5.0) is None

    def test_multiplo_anomalo(self) -> None:
        """Multipli > 10000x sono considerati anomali."""
        from run_analysis import _safe_div
        assert _safe_div(1_000_000.0, 0.01) is None

    def test_divisione_piccola(self) -> None:
        from run_analysis import _safe_div
        result = _safe_div(10.0, 0.5)
        assert result == 20.0


class TestFmtMultiplo:
    """Test per la funzione _fmt_multiplo."""

    def test_valore_normale(self) -> None:
        from run_analysis import _fmt_multiplo
        assert _fmt_multiplo(25.3) == "25.3"

    def test_valore_none(self) -> None:
        from run_analysis import _fmt_multiplo
        assert _fmt_multiplo(None) == "N/A"

    def test_valore_zero(self) -> None:
        from run_analysis import _fmt_multiplo
        assert _fmt_multiplo(0.0) == "0.0"


class TestCaricaConfig:
    """Test per il caricamento dei config JSON."""

    def test_config_esistente(self) -> None:
        from run_analysis import carica_config
        config = carica_config("AAPL")
        assert config["ticker"] == "AAPL"
        assert "comparabili" in config
        assert "sensitivity" in config
        assert "scenari" in config
        assert "fondamentali_fallback" in config

    def test_config_inesistente(self) -> None:
        from run_analysis import carica_config
        with pytest.raises(SystemExit):
            carica_config("ZZZZZ_NON_ESISTE")

    def test_config_rblx_ha_campi_extra(self) -> None:
        """RBLX ha campi extra come sbc, fcf, bookings nei fallback."""
        from run_analysis import carica_config
        config = carica_config("RBLX")
        fb = config["fondamentali_fallback"]
        assert fb["ricavi"] > 0
        assert "beta_levered" in fb

    def test_tutti_i_config_hanno_campi_obbligatori(self) -> None:
        """Verifica che tutti i config abbiano i campi minimi richiesti."""
        from valuation_analyst.config.settings import CONFIGS_DIR
        campi_obbligatori = [
            "ticker", "erp", "rating_credito", "crescita_alta", "crescita_stabile",
            "anni_alta", "anni_transizione", "comparabili", "sensitivity",
            "scenari", "monte_carlo", "rischi_rialzo", "rischi_ribasso",
            "fondamentali_fallback",
        ]
        for config_file in CONFIGS_DIR.glob("*.json"):
            if config_file.name.startswith("_"):
                continue  # Salta il template
            with open(config_file, encoding="utf-8") as f:
                config = json.load(f)
            for campo in campi_obbligatori:
                assert campo in config, (
                    f"Campo '{campo}' mancante in {config_file.name}"
                )


class TestCostruttoreComparabili:
    """Test per la costruzione dei comparabili dal JSON."""

    def test_costruisci_da_config(self) -> None:
        from run_analysis import carica_config, costruisci_comparabili
        config = carica_config("AAPL")
        comparabili = costruisci_comparabili(config)
        assert len(comparabili) > 0
        assert comparabili[0].ticker != ""
        assert comparabili[0].market_cap > 0


class TestAziendaInPerdita:
    """Test che il flow non crashi con dati negativi."""

    def test_safe_div_con_eps_negativo(self) -> None:
        from run_analysis import _safe_div
        # EPS negativo -> P/E non applicabile
        result = _safe_div(71.40, -1.32)
        assert result is None

    def test_safe_div_con_ebitda_negativo(self) -> None:
        from run_analysis import _safe_div
        # EBITDA negativo -> EV/EBITDA non applicabile
        result = _safe_div(50000.0, -837.0)
        assert result is None

    def test_safe_div_con_bvps_negativo(self) -> None:
        from run_analysis import _safe_div
        # BV/S negativo (deficit di patrimonio netto)
        result = _safe_div(50.0, -2.0)
        assert result is None


class TestNuovaStruttura:
    """Test che la nuova struttura delle directory sia corretta."""

    def test_configs_dir_esiste(self) -> None:
        from valuation_analyst.config.settings import CONFIGS_DIR
        assert CONFIGS_DIR.exists()
        assert (CONFIGS_DIR / "_template.json").exists()

    def test_reports_dir_corretta(self) -> None:
        from valuation_analyst.config.settings import REPORTS_DIR
        assert "output/markdown" in str(REPORTS_DIR)

    def test_pdf_dir_corretta(self) -> None:
        from valuation_analyst.config.settings import PDF_DIR
        assert "output/pdf" in str(PDF_DIR)

    def test_prompt_log_in_data_logs(self) -> None:
        from valuation_analyst.config.settings import PROMPT_LOG_PATH
        assert "data/logs" in str(PROMPT_LOG_PATH)

    def test_template_ha_doc(self) -> None:
        from valuation_analyst.config.settings import CONFIGS_DIR
        with open(CONFIGS_DIR / "_template.json", encoding="utf-8") as f:
            template = json.load(f)
        assert "_doc" in template
        assert template["ticker"] == "TICKER"

    def test_fetch_dati_nel_package(self) -> None:
        """fetch_dati e' ora nel package, non piu' in scripts/."""
        from valuation_analyst.tools.fetch_dati import fetch_dati_azienda
        assert callable(fetch_dati_azienda)

    def test_no_archive_dir(self) -> None:
        """La cartella archive/ e' stata rimossa."""
        assert not (ROOT / "archive").exists()

    def test_no_script_adhoc_nella_root(self) -> None:
        """Non devono esserci script .py di analisi nella root."""
        root_py = list(ROOT.glob("analisi_*.py"))
        assert root_py == [], f"Script ad-hoc trovati nella root: {root_py}"

    def test_no_prompts_dir(self) -> None:
        """La cartella prompts/ (non usata) e' stata rimossa."""
        assert not (ROOT / "src" / "valuation_analyst" / "prompts").exists()

    def test_no_old_output(self) -> None:
        """Non devono esserci report con vecchio naming."""
        old = list((ROOT / "output" / "markdown").glob("*_valuation_report_*.md"))
        assert old == [], f"Report con vecchio naming trovati: {old}"
