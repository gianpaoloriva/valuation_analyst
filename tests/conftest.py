"""Fixture condivise per i test del progetto valuation_analyst."""
import pytest
import json
from pathlib import Path
from valuation_analyst.models.company import Company
from valuation_analyst.models.cost_of_capital import CostoCapitale
from valuation_analyst.models.comparable import Comparabile
from valuation_analyst.models.option_inputs import InputBlackScholes
from valuation_analyst.models.scenario import Scenario


@pytest.fixture
def apple_company() -> Company:
    """Fixture con dati Apple Inc. per test."""
    return Company(
        ticker="AAPL", nome="Apple Inc.", settore="Technology",
        industria="Consumer Electronics", paese="US", valuta="USD",
        market_cap=2_800_000_000_000, enterprise_value=2_850_000_000_000,
        shares_outstanding=15_500_000_000, prezzo_corrente=180.65,
        ricavi=383_000_000_000, ebit=120_000_000_000, ebitda=133_000_000_000,
        utile_netto=97_000_000_000, total_debt=111_000_000_000,
        cash=62_000_000_000, capex=11_000_000_000, deprezzamento=13_000_000_000,
        delta_working_capital=-3_000_000_000, tax_rate=0.153, beta=1.24,
        dividendo_per_azione=0.96,
    )


@pytest.fixture
def sample_wacc() -> CostoCapitale:
    """Fixture WACC tipico per test."""
    return CostoCapitale(
        risk_free_rate=0.042, beta_levered=1.24, beta_unlevered=0.95,
        equity_risk_premium=0.055, country_risk_premium=0.0,
        costo_equity=0.1102, costo_debito_pre_tax=0.055,
        costo_debito_post_tax=0.0466, tax_rate=0.153,
        peso_equity=0.96, peso_debito=0.04, wacc=0.1076,
    )


@pytest.fixture
def sample_comparabili() -> list[Comparabile]:
    """Fixture con comparabili Tech per test."""
    return [
        Comparabile(ticker="MSFT", nome="Microsoft", settore="Technology", market_cap=2_900_000, pe_ratio=35.0, ev_ebitda=25.0, pb_ratio=12.5, ev_sales=13.0, roe=0.38, margine_operativo=0.43, crescita_ricavi=0.15),
        Comparabile(ticker="GOOGL", nome="Alphabet", settore="Technology", market_cap=1_900_000, pe_ratio=25.0, ev_ebitda=17.0, pb_ratio=6.5, ev_sales=6.5, roe=0.28, margine_operativo=0.27, crescita_ricavi=0.13),
        Comparabile(ticker="META", nome="Meta Platforms", settore="Technology", market_cap=1_200_000, pe_ratio=23.0, ev_ebitda=14.0, pb_ratio=8.0, ev_sales=8.5, roe=0.33, margine_operativo=0.35, crescita_ricavi=0.22),
        Comparabile(ticker="AMZN", nome="Amazon", settore="Technology", market_cap=1_800_000, pe_ratio=60.0, ev_ebitda=20.0, pb_ratio=8.0, ev_sales=3.2, roe=0.19, margine_operativo=0.07, crescita_ricavi=0.12),
        Comparabile(ticker="NVDA", nome="NVIDIA", settore="Technology", market_cap=1_500_000, pe_ratio=65.0, ev_ebitda=55.0, pb_ratio=40.0, ev_sales=25.0, roe=0.90, margine_operativo=0.55, crescita_ricavi=1.22),
    ]


@pytest.fixture
def sample_option_inputs() -> InputBlackScholes:
    """Input Black-Scholes per azienda in distress."""
    return InputBlackScholes(
        valore_attivita=100_000_000, valore_nominale_debito=80_000_000,
        scadenza_debito=5.0, risk_free_rate=0.042, volatilita=0.40,
    )


@pytest.fixture
def sample_data_dir() -> Path:
    """Path alla directory dei dati sample."""
    return Path(__file__).parent.parent / "data" / "samples"
