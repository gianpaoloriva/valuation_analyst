"""Script per analisi completa MSFT (Microsoft Corporation).

Esegue tutti i moduli di valutazione e genera il report in formato markdown
nella cartella data/reports/.
"""
from __future__ import annotations

import sys
import os
from datetime import date
from pathlib import Path

# Assicura che src/ sia nel path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from fetch_dati import fetch_dati_azienda
from valuation_analyst.tools.capm import calcola_costo_equity, calcola_costo_equity_dettagliato
from valuation_analyst.tools.wacc import calcola_wacc, calcola_wacc_completo
from valuation_analyst.tools.beta_estimation import beta_levered, beta_unlevered, total_beta
from valuation_analyst.tools.risk_premium import spread_da_rating, costo_debito_sintetico
from valuation_analyst.tools.dcf_fcff import calcola_fcff, calcola_dcf_fcff, valutazione_fcff
from valuation_analyst.tools.growth_models import crescita_3_fasi
from valuation_analyst.tools.multiples import (
    valutazione_relativa, statistiche_multiplo, valore_implicito_pe,
    valore_implicito_ev_ebitda, valore_implicito_pb, valore_implicito_ev_sales,
)
from valuation_analyst.tools.sensitivity_table import (
    sensitivity_wacc_growth, sensitivity_crescita_margine,
    formatta_sensitivity,
)
from valuation_analyst.tools.scenario_analysis import (
    crea_scenari_standard, formatta_scenari,
)
from valuation_analyst.tools.monte_carlo import (
    monte_carlo_dcf, formatta_monte_carlo, istogramma_ascii,
)
from valuation_analyst.models.comparable import Comparabile
from valuation_analyst.utils.formatting import (
    formatta_valuta, formatta_percentuale, formatta_numero,
    formatta_milioni, formatta_miliardi, tabella_markdown,
)

# ===========================================================================
# DATI LIVE DA MASSIVE.COM
# ===========================================================================

TICKER = "MSFT"
dati = fetch_dati_azienda(TICKER)

NOME = dati["nome"]
SETTORE = dati["settore"]
PAESE = dati["paese"]
VALUTA = dati["valuta"]

# Dati di mercato (in milioni, eccetto prezzo per azione)
PREZZO_CORRENTE = dati["prezzo_corrente"]
SHARES_OUTSTANDING = dati["shares_outstanding"]
MARKET_CAP = dati["market_cap"]

# Conto economico (TTM, in milioni USD)
RICAVI = dati["ricavi"]
EBIT = dati["ebit"]
EBITDA = dati["ebitda"]
UTILE_NETTO = dati["utile_netto"]
EPS = dati["eps"]

# Stato patrimoniale (in milioni USD)
TOTAL_DEBT = dati["total_debt"]
CASH = dati["cash"]
BOOK_VALUE_EQUITY = dati["book_value_equity"]
BOOK_VALUE_PER_SHARE = dati["book_value_per_share"]

# Cash flow (in milioni USD)
CAPEX = dati["capex"]
DEPREZZAMENTO = dati["deprezzamento"]
DELTA_WC = dati["delta_wc"]

# Parametri fiscali
TAX_RATE = dati["tax_rate"]

# Parametri di mercato (live + stime analista)
RISK_FREE_RATE = dati["risk_free_rate"]
BETA_LEVERED = dati["beta_levered"]
ERP = 0.055                  # Equity Risk Premium (Damodaran US) - stima analista
RATING_CREDITO = "AAA"       # Rating S&P di Microsoft - stima analista

# Parametri di crescita (stime analista)
CRESCITA_ALTA = 0.12         # 12% fase alta (AI/Cloud growth)
CRESCITA_STABILE = 0.025     # 2.5% crescita perpetua
ANNI_ALTA = 5
ANNI_TRANSIZIONE = 5

# Derivati
DEBITO_NETTO = dati["debito_netto"]
ENTERPRISE_VALUE = dati["enterprise_value"]

# ===========================================================================
# COMPARABILI Big Tech
# ===========================================================================
COMPARABILI = [
    Comparabile(
        ticker="AAPL", nome="Apple Inc.", settore="Technology",
        market_cap=3_450_000, pe_ratio=33.5, ev_ebitda=26.8,
        pb_ratio=62.0, ev_sales=9.0, ev_ebit=31.5,
        margine_operativo=0.34, crescita_ricavi=0.05, paese="US",
    ),
    Comparabile(
        ticker="GOOGL", nome="Alphabet Inc.", settore="Technology",
        market_cap=2_150_000, pe_ratio=24.0, ev_ebitda=17.5,
        pb_ratio=7.8, ev_sales=7.2, ev_ebit=22.0,
        margine_operativo=0.32, crescita_ricavi=0.14, paese="US",
    ),
    Comparabile(
        ticker="AMZN", nome="Amazon.com Inc.", settore="Technology",
        market_cap=2_300_000, pe_ratio=42.0, ev_ebitda=18.5,
        pb_ratio=9.5, ev_sales=4.0, ev_ebit=35.0,
        margine_operativo=0.11, crescita_ricavi=0.12, paese="US",
    ),
    Comparabile(
        ticker="META", nome="Meta Platforms Inc.", settore="Technology",
        market_cap=1_600_000, pe_ratio=27.5, ev_ebitda=16.0,
        pb_ratio=9.0, ev_sales=11.5, ev_ebit=19.5,
        margine_operativo=0.41, crescita_ricavi=0.22, paese="US",
    ),
    Comparabile(
        ticker="NVDA", nome="NVIDIA Corporation", settore="Technology",
        market_cap=3_200_000, pe_ratio=55.0, ev_ebitda=45.0,
        pb_ratio=52.0, ev_sales=38.0, ev_ebit=48.0,
        margine_operativo=0.65, crescita_ricavi=0.122, paese="US",
    ),
    Comparabile(
        ticker="ORCL", nome="Oracle Corporation", settore="Technology",
        market_cap=480_000, pe_ratio=38.0, ev_ebitda=22.0,
        pb_ratio=28.0, ev_sales=9.5, ev_ebit=26.0,
        margine_operativo=0.30, crescita_ricavi=0.09, paese="US",
    ),
    Comparabile(
        ticker="CRM", nome="Salesforce Inc.", settore="Technology",
        market_cap=310_000, pe_ratio=48.0, ev_ebitda=26.0,
        pb_ratio=4.8, ev_sales=9.2, ev_ebit=32.0,
        margine_operativo=0.22, crescita_ricavi=0.11, paese="US",
    ),
]


def main() -> None:
    """Esegue l'analisi completa e genera il report."""
    sezioni: list[str] = []

    # ==================================================================
    # INTESTAZIONE
    # ==================================================================
    sezioni.append(f"# Report di Valutazione - {NOME} ({TICKER})")
    sezioni.append(f"**Data:** {date.today().isoformat()}")
    sezioni.append(f"**Analista:** Valuation Analyst Multi-Agent System")
    sezioni.append(f"**Metodologia:** Damodaran (NYU Stern)")
    sezioni.append("")
    sezioni.append("---")
    sezioni.append("")

    # ==================================================================
    # SEZIONE 1: PANORAMICA AZIENDALE
    # ==================================================================
    sezioni.append("## 1. Panoramica Aziendale")
    sezioni.append("")
    headers_overview = ["Indicatore", "Valore"]
    rows_overview = [
        ["Ticker", TICKER],
        ["Settore", SETTORE],
        ["Paese", PAESE],
        ["Prezzo Corrente", formatta_valuta(PREZZO_CORRENTE, VALUTA)],
        ["Market Cap", formatta_miliardi(MARKET_CAP * 1e6)],
        ["Enterprise Value", formatta_miliardi(ENTERPRISE_VALUE * 1e6)],
        ["Azioni in Circolazione", f"{SHARES_OUTSTANDING:,.0f}M"],
        ["Ricavi (TTM)", formatta_miliardi(RICAVI * 1e6)],
        ["EBITDA (TTM)", formatta_miliardi(EBITDA * 1e6)],
        ["EBIT (TTM)", formatta_miliardi(EBIT * 1e6)],
        ["Utile Netto (TTM)", formatta_miliardi(UTILE_NETTO * 1e6)],
        ["EPS", formatta_valuta(EPS, VALUTA)],
        ["Book Value/Share", formatta_valuta(BOOK_VALUE_PER_SHARE, VALUTA)],
        ["Debito Totale", formatta_miliardi(TOTAL_DEBT * 1e6)],
        ["Cassa", formatta_miliardi(CASH * 1e6)],
        ["Debito Netto", formatta_miliardi(DEBITO_NETTO * 1e6)],
        ["Rating", RATING_CREDITO],
        ["Beta", f"{BETA_LEVERED:.2f}"],
    ]
    sezioni.append(tabella_markdown(headers_overview, rows_overview))
    sezioni.append("")

    # ==================================================================
    # SEZIONE 2: COSTO DEL CAPITALE (WACC)
    # ==================================================================
    sezioni.append("## 2. Costo del Capitale (WACC)")
    sezioni.append("")
    sezioni.append("### 2.1 Costo dell'Equity (CAPM)")
    sezioni.append("")

    # Beta unlevered
    rapporto_de = TOTAL_DEBT / MARKET_CAP
    beta_u = beta_unlevered(BETA_LEVERED, TAX_RATE, rapporto_de)

    # Costo equity dettagliato
    ke_dettaglio = calcola_costo_equity_dettagliato(
        risk_free_rate=RISK_FREE_RATE,
        beta=BETA_LEVERED,
        equity_risk_premium=ERP,
        country_risk_premium=0.0,
        small_cap_premium=0.0,
        company_specific_premium=0.0,
    )
    costo_equity = ke_dettaglio["costo_equity"]

    sezioni.append("**Formula CAPM:** `Re = Rf + Beta * ERP + CRP`")
    sezioni.append("")
    headers_capm = ["Componente", "Valore"]
    rows_capm = [
        ["Risk-Free Rate (US 10Y)", formatta_percentuale(RISK_FREE_RATE)],
        ["Beta Levered", f"{BETA_LEVERED:.2f}"],
        ["Beta Unlevered", f"{beta_u:.3f}"],
        ["Equity Risk Premium", formatta_percentuale(ERP)],
        ["Premio Rischio Sistematico (Beta x ERP)", formatta_percentuale(ke_dettaglio["premio_rischio_sistematico"])],
        ["Country Risk Premium", formatta_percentuale(0.0)],
        ["**Costo Equity (Re)**", f"**{formatta_percentuale(costo_equity)}**"],
    ]
    sezioni.append(tabella_markdown(headers_capm, rows_capm))
    sezioni.append("")

    # Costo del debito
    sezioni.append("### 2.2 Costo del Debito")
    sezioni.append("")
    spread = spread_da_rating(RATING_CREDITO)
    kd_pre_tax = RISK_FREE_RATE + spread
    kd_post_tax = kd_pre_tax * (1 - TAX_RATE)

    headers_debt = ["Componente", "Valore"]
    rows_debt = [
        ["Rating Creditizio", RATING_CREDITO],
        ["Default Spread", formatta_percentuale(spread)],
        ["Costo Debito Pre-Tax (Kd)", formatta_percentuale(kd_pre_tax)],
        ["Tax Rate Effettivo", formatta_percentuale(TAX_RATE)],
        ["**Costo Debito Post-Tax**", f"**{formatta_percentuale(kd_post_tax)}**"],
    ]
    sezioni.append(tabella_markdown(headers_debt, rows_debt))
    sezioni.append("")

    # WACC completo
    sezioni.append("### 2.3 WACC")
    sezioni.append("")
    wacc_result = calcola_wacc_completo(
        risk_free_rate=RISK_FREE_RATE,
        beta=BETA_LEVERED,
        equity_risk_premium=ERP,
        costo_debito_pre_tax=kd_pre_tax,
        tax_rate=TAX_RATE,
        market_cap=MARKET_CAP,
        total_debt=TOTAL_DEBT,
    )
    wacc_val = wacc_result.wacc

    sezioni.append("**Formula:** `WACC = (E/V) * Re + (D/V) * Rd * (1-t)`")
    sezioni.append("")
    headers_wacc = ["Componente", "Valore"]
    rows_wacc = [
        ["Peso Equity (E/V)", formatta_percentuale(wacc_result.peso_equity)],
        ["Peso Debito (D/V)", formatta_percentuale(wacc_result.peso_debito)],
        ["Costo Equity (Re)", formatta_percentuale(wacc_result.costo_equity)],
        ["Costo Debito Post-Tax", formatta_percentuale(wacc_result.costo_debito_post_tax)],
        ["**WACC**", f"**{formatta_percentuale(wacc_val)}**"],
    ]
    sezioni.append(tabella_markdown(headers_wacc, rows_wacc))
    sezioni.append("")

    # ==================================================================
    # SEZIONE 3: DCF FCFF
    # ==================================================================
    sezioni.append("## 3. Valutazione DCF (FCFF)")
    sezioni.append("")

    # Calcolo FCFF base
    fcff_base = calcola_fcff(
        ebit=EBIT,
        tax_rate=TAX_RATE,
        capex=CAPEX,
        deprezzamento=DEPREZZAMENTO,
        delta_wc=DELTA_WC,
    )
    sezioni.append(f"### 3.1 FCFF Base")
    sezioni.append("")
    sezioni.append("**Formula:** `FCFF = EBIT*(1-t) + Deprezzamento - CapEx - Delta WC`")
    sezioni.append("")
    headers_fcff = ["Componente", "Valore (M USD)"]
    rows_fcff = [
        ["EBIT", formatta_numero(EBIT)],
        ["EBIT * (1-t)", formatta_numero(EBIT * (1 - TAX_RATE))],
        ["+ Deprezzamento", formatta_numero(DEPREZZAMENTO)],
        ["- CapEx", formatta_numero(CAPEX)],
        ["- Delta WC", formatta_numero(DELTA_WC)],
        ["**FCFF Base**", f"**{formatta_numero(fcff_base)}**"],
    ]
    sezioni.append(tabella_markdown(headers_fcff, rows_fcff))
    sezioni.append("")

    # DCF multi-stage
    sezioni.append("### 3.2 Proiezione Multi-Stage (3 fasi)")
    sezioni.append("")
    sezioni.append(f"- **Fase 1 (Alta crescita):** {CRESCITA_ALTA:.0%} per {ANNI_ALTA} anni")
    sezioni.append(f"- **Fase 2 (Transizione):** convergenza lineare per {ANNI_TRANSIZIONE} anni")
    sezioni.append(f"- **Fase 3 (Stabile):** {CRESCITA_STABILE:.1%} in perpetuita'")
    sezioni.append(f"- **Tasso di sconto (WACC):** {formatta_percentuale(wacc_val)}")
    sezioni.append("")

    dcf_result = calcola_dcf_fcff(
        fcff_base=fcff_base,
        wacc=wacc_val,
        crescita_alta=CRESCITA_ALTA,
        crescita_stabile=CRESCITA_STABILE,
        anni_alta=ANNI_ALTA,
        anni_transizione=ANNI_TRANSIZIONE,
    )

    # Tabella proiezioni anno per anno
    headers_proj = ["Anno", "Tasso Crescita", "FCFF (M)", "Valore Attuale (M)"]
    rows_proj = []
    for p in dcf_result.proiezioni:
        rows_proj.append([
            str(p.anno),
            formatta_percentuale(p.tasso_crescita),
            formatta_numero(p.fcff) if p.fcff else "N/D",
            formatta_numero(p.valore_attuale) if p.valore_attuale else "N/D",
        ])
    sezioni.append(tabella_markdown(headers_proj, rows_proj))
    sezioni.append("")

    # Riepilogo DCF
    sezioni.append("### 3.3 Riepilogo Valutazione DCF")
    sezioni.append("")
    enterprise_value_dcf = dcf_result.valore_totale
    equity_value_dcf = enterprise_value_dcf - DEBITO_NETTO
    valore_per_azione_dcf = equity_value_dcf / SHARES_OUTSTANDING
    upside_dcf = (valore_per_azione_dcf - PREZZO_CORRENTE) / PREZZO_CORRENTE

    headers_dcf_summary = ["Componente", "Valore"]
    rows_dcf_summary = [
        ["VA Flussi di Cassa Espliciti", formatta_miliardi(dcf_result.valore_attuale_flussi * 1e6)],
        ["Terminal Value (nominale)", formatta_miliardi(dcf_result.valore_terminale * 1e6)],
        ["VA Terminal Value", formatta_miliardi(dcf_result.valore_terminale_attuale * 1e6)],
        ["TV come % del Totale", formatta_percentuale(dcf_result.percentuale_valore_terminale / 100)],
        ["**Enterprise Value**", f"**{formatta_miliardi(enterprise_value_dcf * 1e6)}**"],
        ["- Debito Netto", formatta_miliardi(DEBITO_NETTO * 1e6)],
        ["**Equity Value**", f"**{formatta_miliardi(equity_value_dcf * 1e6)}**"],
        ["Azioni in Circolazione", f"{SHARES_OUTSTANDING:,.0f}M"],
        ["**Valore per Azione (DCF)**", f"**{formatta_valuta(valore_per_azione_dcf, VALUTA)}**"],
        ["Prezzo Corrente", formatta_valuta(PREZZO_CORRENTE, VALUTA)],
        ["**Upside/Downside**", f"**{upside_dcf:+.1%}**"],
    ]
    sezioni.append(tabella_markdown(headers_dcf_summary, rows_dcf_summary))
    sezioni.append("")

    # ==================================================================
    # SEZIONE 4: VALUTAZIONE RELATIVA
    # ==================================================================
    sezioni.append("## 4. Valutazione Relativa (Multipli)")
    sezioni.append("")

    sezioni.append("### 4.1 Campione Comparabili")
    sezioni.append("")
    headers_comp = ["Ticker", "Nome", "Market Cap (B)", "P/E", "EV/EBITDA", "P/B", "EV/Sales"]
    rows_comp = []
    for c in COMPARABILI:
        rows_comp.append([
            c.ticker,
            c.nome,
            f"${c.market_cap/1000:,.0f}B",
            f"{c.pe_ratio:.1f}" if c.pe_ratio else "N/D",
            f"{c.ev_ebitda:.1f}" if c.ev_ebitda else "N/D",
            f"{c.pb_ratio:.1f}" if c.pb_ratio else "N/D",
            f"{c.ev_sales:.1f}" if c.ev_sales else "N/D",
        ])
    # Aggiungi MSFT per confronto
    pe_msft = PREZZO_CORRENTE / EPS
    ev_ebitda_msft = ENTERPRISE_VALUE / EBITDA
    pb_msft = PREZZO_CORRENTE / BOOK_VALUE_PER_SHARE
    ev_sales_msft = ENTERPRISE_VALUE / RICAVI
    rows_comp.append([
        f"**{TICKER}**", f"**{NOME}**",
        f"**${MARKET_CAP/1000:,.0f}B**",
        f"**{pe_msft:.1f}**",
        f"**{ev_ebitda_msft:.1f}**",
        f"**{pb_msft:.1f}**",
        f"**{ev_sales_msft:.1f}**",
    ])
    sezioni.append(tabella_markdown(headers_comp, rows_comp))
    sezioni.append("")

    # Valutazione relativa
    rel_result = valutazione_relativa(
        ticker=TICKER,
        eps=EPS,
        ebitda=EBITDA,
        book_value_per_share=BOOK_VALUE_PER_SHARE,
        ricavi=RICAVI,
        debito_netto=DEBITO_NETTO,
        shares_outstanding=SHARES_OUTSTANDING,
        comparabili=COMPARABILI,
        prezzo_corrente=PREZZO_CORRENTE,
    )

    sezioni.append("### 4.2 Statistiche Multipli Comparabili")
    sezioni.append("")

    # Statistiche per multiplo
    for mult_name, display_name in [
        ("pe_ratio", "P/E"), ("ev_ebitda", "EV/EBITDA"),
        ("pb_ratio", "P/B"), ("ev_sales", "EV/Sales"),
    ]:
        valori = [getattr(c, mult_name) for c in COMPARABILI]
        stat = statistiche_multiplo(valori, mult_name)
        if stat.num_osservazioni > 0:
            sezioni.append(f"**{display_name}:** Media={stat.media:.1f}, Mediana={stat.mediana:.1f}, "
                          f"Min={stat.minimo:.1f}, Max={stat.massimo:.1f} (n={stat.num_osservazioni})")

    sezioni.append("")
    sezioni.append("### 4.3 Valori Impliciti")
    sezioni.append("")

    headers_impl = ["Multiplo", "Valore Implicito/Azione"]
    rows_impl = []
    if rel_result.dettagli:
        for chiave, valore in rel_result.dettagli.items():
            if chiave.startswith("valore_implicito_") and isinstance(valore, (int, float)):
                nome_mult = chiave.replace("valore_implicito_", "").upper().replace("_", "/")
                rows_impl.append([nome_mult, formatta_valuta(valore, VALUTA)])
    if rows_impl:
        sezioni.append(tabella_markdown(headers_impl, rows_impl))
    sezioni.append("")

    valore_relativo = rel_result.valore_per_azione
    upside_rel = (valore_relativo - PREZZO_CORRENTE) / PREZZO_CORRENTE if PREZZO_CORRENTE > 0 else 0
    sezioni.append(f"**Valore Mediano Multipli:** {formatta_valuta(valore_relativo, VALUTA)}")
    sezioni.append(f"**Upside/Downside:** {upside_rel:+.1%}")
    sezioni.append("")

    # ==================================================================
    # SEZIONE 5: SENSITIVITY ANALYSIS
    # ==================================================================
    sezioni.append("## 5. Analisi di Sensitivita'")
    sezioni.append("")

    # 5.1 WACC vs Terminal Growth
    sezioni.append("### 5.1 WACC vs Tasso di Crescita Terminale")
    sezioni.append("")
    sezioni.append("Valore per azione al variare di WACC e crescita terminale:")
    sezioni.append("")

    sens_wacc_g = sensitivity_wacc_growth(
        fcff_base=fcff_base,
        debito_netto=DEBITO_NETTO,
        shares_outstanding=SHARES_OUTSTANDING,
        wacc_range=[0.07, 0.08, 0.085, 0.09, 0.095, 0.10, 0.11],
        growth_range=[0.015, 0.020, 0.025, 0.030, 0.035],
        anni_proiezione=10,
        crescita_alta=CRESCITA_ALTA,
    )
    sezioni.append(formatta_sensitivity(sens_wacc_g, VALUTA))
    sezioni.append("")

    # 5.2 Crescita Ricavi vs Margine Operativo
    sezioni.append("### 5.2 Crescita Ricavi vs Margine Operativo")
    sezioni.append("")

    sens_crescita_margine = sensitivity_crescita_margine(
        ricavi_base=RICAVI,
        debito_netto=DEBITO_NETTO,
        shares_outstanding=SHARES_OUTSTANDING,
        wacc=wacc_val,
        tax_rate=TAX_RATE,
        capex_pct_ricavi=CAPEX / RICAVI,
        depr_pct_ricavi=DEPREZZAMENTO / RICAVI,
        crescita_range=[0.05, 0.08, 0.10, 0.12, 0.15],
        margine_range=[0.35, 0.40, 0.45, 0.50, 0.55],
    )
    sezioni.append(formatta_sensitivity(sens_crescita_margine, VALUTA))
    sezioni.append("")

    # ==================================================================
    # SEZIONE 6: ANALISI PER SCENARI
    # ==================================================================
    sezioni.append("## 6. Analisi per Scenari")
    sezioni.append("")

    scenari = crea_scenari_standard(
        valore_base=valore_per_azione_dcf,
        upside_pct=0.30,
        downside_pct=0.25,
        prob_best=0.20,
        prob_base=0.55,
        prob_worst=0.25,
    )
    sezioni.append("**Scenari:**")
    sezioni.append(f"- **Best Case** (20%): crescita AI/Cloud superiore, margini in espansione (+30%)")
    sezioni.append(f"- **Base Case** (55%): continuazione trend attuale")
    sezioni.append(f"- **Worst Case** (25%): rallentamento macro, pressione competitiva (-25%)")
    sezioni.append("")
    sezioni.append(formatta_scenari(scenari, VALUTA))
    sezioni.append("")

    valore_atteso_scenari = scenari.valore_atteso
    sezioni.append(f"**Valore Atteso Ponderato:** {formatta_valuta(valore_atteso_scenari, VALUTA)}")
    sezioni.append("")

    # ==================================================================
    # SEZIONE 7: SIMULAZIONE MONTE CARLO
    # ==================================================================
    sezioni.append("## 7. Simulazione Monte Carlo")
    sezioni.append("")
    sezioni.append("**Parametri della simulazione:**")
    sezioni.append("- Iterazioni: 10.000")
    sezioni.append("- WACC: Distribuzione Normale (media=WACC calcolato, std=1%)")
    sezioni.append("- Crescita Alta: Distribuzione Normale (media=12%, std=3%)")
    sezioni.append("- Crescita Stabile: Distribuzione Triangolare (1.5%, 2.5%, 3.5%)")
    sezioni.append("")

    mc_result = monte_carlo_dcf(
        fcff_base=fcff_base,
        debito_netto=DEBITO_NETTO,
        shares_outstanding=SHARES_OUTSTANDING,
        distribuzioni={
            "wacc": {
                "tipo": "normale",
                "media": wacc_val,
                "deviazione_standard": 0.01,
            },
            "crescita_alta": {
                "tipo": "normale",
                "media": CRESCITA_ALTA,
                "deviazione_standard": 0.03,
            },
            "crescita_stabile": {
                "tipo": "triangolare",
                "minimo": 0.015,
                "moda": 0.025,
                "massimo": 0.035,
            },
        },
        num_simulazioni=10_000,
        seed=42,
    )

    sezioni.append(formatta_monte_carlo(mc_result, VALUTA))
    sezioni.append("")

    # Istogramma ASCII
    sezioni.append("### Distribuzione dei Valori Simulati")
    sezioni.append("")
    sezioni.append("```")
    sezioni.append(istogramma_ascii(mc_result["valori"], bins=25, larghezza=50))
    sezioni.append("```")
    sezioni.append("")

    # ==================================================================
    # SEZIONE 8: SINTESI E RACCOMANDAZIONE
    # ==================================================================
    sezioni.append("## 8. Sintesi Multi-Metodo e Raccomandazione")
    sezioni.append("")

    # Tabella sintesi
    headers_sintesi = ["Metodo", "Valore/Azione", "Upside/Downside", "Peso"]
    rows_sintesi = [
        [
            "DCF FCFF (3-stage)",
            formatta_valuta(valore_per_azione_dcf, VALUTA),
            f"{upside_dcf:+.1%}",
            "40%",
        ],
        [
            "Valutazione Relativa (Multipli)",
            formatta_valuta(valore_relativo, VALUTA),
            f"{upside_rel:+.1%}",
            "25%",
        ],
        [
            "Valore Atteso Scenari",
            formatta_valuta(valore_atteso_scenari, VALUTA),
            f"{(valore_atteso_scenari - PREZZO_CORRENTE) / PREZZO_CORRENTE:+.1%}",
            "15%",
        ],
        [
            "Monte Carlo (Mediana)",
            formatta_valuta(mc_result["mediana"], VALUTA),
            f"{(mc_result['mediana'] - PREZZO_CORRENTE) / PREZZO_CORRENTE:+.1%}",
            "20%",
        ],
    ]
    sezioni.append(tabella_markdown(headers_sintesi, rows_sintesi))
    sezioni.append("")

    # Valore medio ponderato
    valore_ponderato = (
        valore_per_azione_dcf * 0.40
        + valore_relativo * 0.25
        + valore_atteso_scenari * 0.15
        + mc_result["mediana"] * 0.20
    )
    upside_totale = (valore_ponderato - PREZZO_CORRENTE) / PREZZO_CORRENTE

    sezioni.append("### Valore Intrinseco Stimato")
    sezioni.append("")
    sezioni.append(f"| | |")
    sezioni.append(f"|---|---|")
    sezioni.append(f"| **Valore Medio Ponderato** | **{formatta_valuta(valore_ponderato, VALUTA)}** |")
    sezioni.append(f"| Prezzo Corrente | {formatta_valuta(PREZZO_CORRENTE, VALUTA)} |")
    sezioni.append(f"| **Upside/Downside** | **{upside_totale:+.1%}** |")
    sezioni.append(f"| IC 90% Monte Carlo | {formatta_valuta(mc_result['intervallo_confidenza_90'][0], VALUTA)} - {formatta_valuta(mc_result['intervallo_confidenza_90'][1], VALUTA)} |")
    sezioni.append("")

    # Raccomandazione
    if upside_totale > 0.15:
        raccomandazione = "BUY"
        commento = "Il titolo appare significativamente sottovalutato rispetto al valore intrinseco stimato."
    elif upside_totale > 0.05:
        raccomandazione = "MODERATE BUY"
        commento = "Il titolo appare moderatamente sottovalutato. Potenziale di apprezzamento contenuto."
    elif upside_totale > -0.05:
        raccomandazione = "HOLD"
        commento = "Il titolo e' prezzato vicino al suo valore intrinseco stimato."
    elif upside_totale > -0.15:
        raccomandazione = "MODERATE SELL"
        commento = "Il titolo appare moderatamente sopravvalutato rispetto al valore intrinseco."
    else:
        raccomandazione = "SELL"
        commento = "Il titolo appare significativamente sopravvalutato."

    sezioni.append(f"### Raccomandazione: **{raccomandazione}**")
    sezioni.append("")
    sezioni.append(f"> {commento}")
    sezioni.append("")

    # ==================================================================
    # SEZIONE 9: RISCHI E DISCLAIMER
    # ==================================================================
    sezioni.append("## 9. Fattori di Rischio e Considerazioni")
    sezioni.append("")
    sezioni.append("### Rischi al Rialzo")
    sezioni.append("- Accelerazione della crescita AI (Copilot, Azure OpenAI)")
    sezioni.append("- Espansione dei margini da economie di scala nel cloud")
    sezioni.append("- Successo nell'integrazione di Activision Blizzard")
    sezioni.append("- Aumento della quota di mercato nel cloud vs AWS/GCP")
    sezioni.append("")
    sezioni.append("### Rischi al Ribasso")
    sezioni.append("- Rallentamento della spesa IT enterprise")
    sezioni.append("- Pressione competitiva nel cloud (AWS, GCP)")
    sezioni.append("- Rischi regolatori (antitrust, privacy)")
    sezioni.append("- Compressione dei multipli del settore Technology")
    sezioni.append("- CapEx elevato per infrastruttura AI senza ritorno proporzionale")
    sezioni.append("")

    sezioni.append("---")
    sezioni.append("")
    sezioni.append("### Disclaimer")
    sezioni.append("")
    sezioni.append("*Questa analisi e' stata generata dal sistema multi-agente Valuation Analyst "
                  "a scopo educativo e dimostrativo. Non costituisce consulenza finanziaria "
                  "o raccomandazione di investimento. I dati finanziari utilizzati sono "
                  "approssimativi e basati su informazioni pubblicamente disponibili. "
                  "Consultare un consulente finanziario qualificato prima di prendere "
                  "decisioni di investimento.*")
    sezioni.append("")
    sezioni.append("---")
    sezioni.append(f"*Report generato il {date.today().isoformat()} dal Valuation Analyst Multi-Agent System*")

    # ==================================================================
    # SCRIVI IL REPORT
    # ==================================================================
    report_dir = ROOT / "data" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"MSFT_valuation_report_{date.today().isoformat()}.md"

    contenuto = "\n".join(sezioni)
    report_path.write_text(contenuto, encoding="utf-8")
    print(f"Report scritto in: {report_path}")
    print(f"Dimensione: {len(contenuto):,} caratteri")
    print(f"\nRiepilogo rapido:")
    print(f"  WACC:                {formatta_percentuale(wacc_val)}")
    print(f"  FCFF Base:           {formatta_numero(fcff_base)} M USD")
    print(f"  DCF Value/Share:     {formatta_valuta(valore_per_azione_dcf, VALUTA)}")
    print(f"  Relative Value:      {formatta_valuta(valore_relativo, VALUTA)}")
    print(f"  MC Mediana:          {formatta_valuta(mc_result['mediana'], VALUTA)}")
    print(f"  Valore Ponderato:    {formatta_valuta(valore_ponderato, VALUTA)}")
    print(f"  Prezzo Corrente:     {formatta_valuta(PREZZO_CORRENTE, VALUTA)}")
    print(f"  Upside/Downside:     {upside_totale:+.1%}")
    print(f"  Raccomandazione:     {raccomandazione}")


if __name__ == "__main__":
    main()
