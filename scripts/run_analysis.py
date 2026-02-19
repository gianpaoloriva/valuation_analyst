"""Script generico per analisi completa di un ticker.

Legge i parametri dell'analista da scripts/configs/{TICKER}.json e i dati
finanziari live da Massive.com, poi genera il report in report/.

Uso:
    python scripts/run_analysis.py GOOGL
    python scripts/run_analysis.py MSFT
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

# Assicura che src/ sia nel path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from fetch_dati import fetch_dati_azienda
from valuation_analyst.tools.capm import calcola_costo_equity_dettagliato
from valuation_analyst.tools.wacc import calcola_wacc_completo
from valuation_analyst.tools.beta_estimation import beta_unlevered
from valuation_analyst.tools.risk_premium import spread_da_rating
from valuation_analyst.tools.dcf_fcff import calcola_fcff, calcola_dcf_fcff
from valuation_analyst.tools.multiples import valutazione_relativa, statistiche_multiplo
from valuation_analyst.tools.sensitivity_table import (
    sensitivity_wacc_growth, sensitivity_crescita_margine, formatta_sensitivity,
)
from valuation_analyst.tools.scenario_analysis import crea_scenari_standard, formatta_scenari
from valuation_analyst.tools.monte_carlo import monte_carlo_dcf, formatta_monte_carlo, istogramma_ascii
from valuation_analyst.models.comparable import Comparabile
from valuation_analyst.utils.formatting import (
    formatta_valuta, formatta_percentuale, formatta_numero,
    formatta_miliardi, tabella_markdown,
)


# ===========================================================================
# CONFIGURAZIONE
# ===========================================================================

def carica_config(ticker: str) -> dict:
    """Legge scripts/configs/{TICKER}.json e restituisce il dict."""
    config_path = ROOT / "scripts" / "configs" / f"{ticker}.json"
    if not config_path.exists():
        print(f"ERRORE: file di configurazione non trovato: {config_path}")
        print(f"Crea il file configs/{ticker}.json con i parametri dell'analista.")
        sys.exit(1)
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def costruisci_comparabili(config: dict) -> list[Comparabile]:
    """Converte la lista di dict dal JSON in oggetti Comparabile."""
    return [Comparabile(**c) for c in config["comparabili"]]


# ===========================================================================
# GENERAZIONE REPORT
# ===========================================================================

def genera_report(dati: dict, config: dict) -> None:
    """Calcola tutto e scrive il report .md in report/."""
    ticker = config["ticker"]
    nome = dati["nome"]
    valuta = dati["valuta"]
    prezzo_corrente = dati["prezzo_corrente"]
    shares_outstanding = dati["shares_outstanding"]
    market_cap = dati["market_cap"]
    ricavi = dati["ricavi"]
    ebit = dati["ebit"]
    ebitda = dati["ebitda"]
    utile_netto = dati["utile_netto"]
    eps = dati["eps"]
    total_debt = dati["total_debt"]
    cash = dati["cash"]
    book_value_per_share = dati["book_value_per_share"]
    capex = dati["capex"]
    deprezzamento = dati["deprezzamento"]
    delta_wc = dati["delta_wc"]
    tax_rate = dati["tax_rate"]
    risk_free_rate = dati["risk_free_rate"]
    beta_levered = dati["beta_levered"]
    debito_netto = dati["debito_netto"]
    enterprise_value = dati["enterprise_value"]

    # Parametri analista dal config
    erp = config["erp"]
    rating_credito = config["rating_credito"]
    crescita_alta = config["crescita_alta"]
    crescita_stabile = config["crescita_stabile"]
    anni_alta = config["anni_alta"]
    anni_transizione = config["anni_transizione"]
    comparabili = costruisci_comparabili(config)
    sens = config["sensitivity"]
    sc = config["scenari"]
    mc = config["monte_carlo"]

    sezioni: list[str] = []

    # ==================================================================
    # INTESTAZIONE
    # ==================================================================
    sezioni.append(f"# Report di Valutazione - {nome} ({ticker})")
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
        ["Ticker", ticker],
        ["Settore", dati["settore"]],
        ["Paese", dati["paese"]],
        ["Prezzo Corrente", formatta_valuta(prezzo_corrente, valuta)],
        ["Market Cap", formatta_miliardi(market_cap * 1e6)],
        ["Enterprise Value", formatta_miliardi(enterprise_value * 1e6)],
        ["Azioni in Circolazione", f"{shares_outstanding:,.0f}M"],
        ["Ricavi (TTM)", formatta_miliardi(ricavi * 1e6)],
        ["EBITDA (TTM)", formatta_miliardi(ebitda * 1e6)],
        ["EBIT (TTM)", formatta_miliardi(ebit * 1e6)],
        ["Utile Netto (TTM)", formatta_miliardi(utile_netto * 1e6)],
        ["EPS", formatta_valuta(eps, valuta)],
        ["Book Value/Share", formatta_valuta(book_value_per_share, valuta)],
        ["Debito Totale", formatta_miliardi(total_debt * 1e6)],
        ["Cassa e Investimenti", formatta_miliardi(cash * 1e6)],
        ["Debito Netto", formatta_miliardi(debito_netto * 1e6)],
        ["Rating", rating_credito],
        ["Beta", f"{beta_levered:.2f}"],
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
    rapporto_de = total_debt / market_cap
    beta_u = beta_unlevered(beta_levered, tax_rate, rapporto_de)

    # Costo equity dettagliato
    ke_dettaglio = calcola_costo_equity_dettagliato(
        risk_free_rate=risk_free_rate,
        beta=beta_levered,
        equity_risk_premium=erp,
        country_risk_premium=0.0,
        small_cap_premium=0.0,
        company_specific_premium=0.0,
    )
    costo_equity = ke_dettaglio["costo_equity"]

    sezioni.append("**Formula CAPM:** `Re = Rf + Beta * ERP + CRP`")
    sezioni.append("")
    headers_capm = ["Componente", "Valore"]
    rows_capm = [
        ["Risk-Free Rate (US 10Y)", formatta_percentuale(risk_free_rate)],
        ["Beta Levered", f"{beta_levered:.2f}"],
        ["Beta Unlevered", f"{beta_u:.3f}"],
        ["Equity Risk Premium", formatta_percentuale(erp)],
        ["Premio Rischio Sistematico (Beta x ERP)", formatta_percentuale(ke_dettaglio["premio_rischio_sistematico"])],
        ["Country Risk Premium", formatta_percentuale(0.0)],
        ["**Costo Equity (Re)**", f"**{formatta_percentuale(costo_equity)}**"],
    ]
    sezioni.append(tabella_markdown(headers_capm, rows_capm))
    sezioni.append("")

    # Costo del debito
    sezioni.append("### 2.2 Costo del Debito")
    sezioni.append("")
    spread = spread_da_rating(rating_credito)
    kd_pre_tax = risk_free_rate + spread
    kd_post_tax = kd_pre_tax * (1 - tax_rate)

    headers_debt = ["Componente", "Valore"]
    rows_debt = [
        ["Rating Creditizio", rating_credito],
        ["Default Spread", formatta_percentuale(spread)],
        ["Costo Debito Pre-Tax (Kd)", formatta_percentuale(kd_pre_tax)],
        ["Tax Rate Effettivo", formatta_percentuale(tax_rate)],
        ["**Costo Debito Post-Tax**", f"**{formatta_percentuale(kd_post_tax)}**"],
    ]
    sezioni.append(tabella_markdown(headers_debt, rows_debt))
    sezioni.append("")

    # WACC completo
    sezioni.append("### 2.3 WACC")
    sezioni.append("")
    wacc_result = calcola_wacc_completo(
        risk_free_rate=risk_free_rate,
        beta=beta_levered,
        equity_risk_premium=erp,
        costo_debito_pre_tax=kd_pre_tax,
        tax_rate=tax_rate,
        market_cap=market_cap,
        total_debt=total_debt,
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
        ebit=ebit,
        tax_rate=tax_rate,
        capex=capex,
        deprezzamento=deprezzamento,
        delta_wc=delta_wc,
    )
    sezioni.append("### 3.1 FCFF Base")
    sezioni.append("")
    sezioni.append("**Formula:** `FCFF = EBIT*(1-t) + Deprezzamento - CapEx - Delta WC`")
    sezioni.append("")
    headers_fcff = ["Componente", "Valore (M USD)"]
    rows_fcff = [
        ["EBIT", formatta_numero(ebit)],
        ["EBIT * (1-t)", formatta_numero(ebit * (1 - tax_rate))],
        ["+ Deprezzamento", formatta_numero(deprezzamento)],
        ["- CapEx", formatta_numero(capex)],
        ["- Delta WC", formatta_numero(delta_wc)],
        ["**FCFF Base**", f"**{formatta_numero(fcff_base)}**"],
    ]
    sezioni.append(tabella_markdown(headers_fcff, rows_fcff))
    sezioni.append("")

    # DCF multi-stage
    sezioni.append("### 3.2 Proiezione Multi-Stage (3 fasi)")
    sezioni.append("")
    sezioni.append(f"- **Fase 1 (Alta crescita):** {crescita_alta:.0%} per {anni_alta} anni")
    sezioni.append(f"- **Fase 2 (Transizione):** convergenza lineare per {anni_transizione} anni")
    sezioni.append(f"- **Fase 3 (Stabile):** {crescita_stabile:.1%} in perpetuita'")
    sezioni.append(f"- **Tasso di sconto (WACC):** {formatta_percentuale(wacc_val)}")
    sezioni.append("")

    dcf_result = calcola_dcf_fcff(
        fcff_base=fcff_base,
        wacc=wacc_val,
        crescita_alta=crescita_alta,
        crescita_stabile=crescita_stabile,
        anni_alta=anni_alta,
        anni_transizione=anni_transizione,
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
    equity_value_dcf = enterprise_value_dcf - debito_netto
    valore_per_azione_dcf = equity_value_dcf / shares_outstanding
    upside_dcf = (valore_per_azione_dcf - prezzo_corrente) / prezzo_corrente

    headers_dcf_summary = ["Componente", "Valore"]
    rows_dcf_summary = [
        ["VA Flussi di Cassa Espliciti", formatta_miliardi(dcf_result.valore_attuale_flussi * 1e6)],
        ["Terminal Value (nominale)", formatta_miliardi(dcf_result.valore_terminale * 1e6)],
        ["VA Terminal Value", formatta_miliardi(dcf_result.valore_terminale_attuale * 1e6)],
        ["TV come % del Totale", formatta_percentuale(dcf_result.percentuale_valore_terminale / 100)],
        ["**Enterprise Value**", f"**{formatta_miliardi(enterprise_value_dcf * 1e6)}**"],
        ["- Debito Netto", formatta_miliardi(debito_netto * 1e6)],
        ["**Equity Value**", f"**{formatta_miliardi(equity_value_dcf * 1e6)}**"],
        ["Azioni in Circolazione", f"{shares_outstanding:,.0f}M"],
        ["**Valore per Azione (DCF)**", f"**{formatta_valuta(valore_per_azione_dcf, valuta)}**"],
        ["Prezzo Corrente", formatta_valuta(prezzo_corrente, valuta)],
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
    for c in comparabili:
        rows_comp.append([
            c.ticker,
            c.nome,
            f"${c.market_cap/1000:,.0f}B",
            f"{c.pe_ratio:.1f}" if c.pe_ratio else "N/D",
            f"{c.ev_ebitda:.1f}" if c.ev_ebitda else "N/D",
            f"{c.pb_ratio:.1f}" if c.pb_ratio else "N/D",
            f"{c.ev_sales:.1f}" if c.ev_sales else "N/D",
        ])
    # Aggiungi il ticker target per confronto
    pe_target = prezzo_corrente / eps
    ev_ebitda_target = enterprise_value / ebitda
    pb_target = prezzo_corrente / book_value_per_share
    ev_sales_target = enterprise_value / ricavi
    rows_comp.append([
        f"**{ticker}**", f"**{nome}**",
        f"**${market_cap/1000:,.0f}B**",
        f"**{pe_target:.1f}**",
        f"**{ev_ebitda_target:.1f}**",
        f"**{pb_target:.1f}**",
        f"**{ev_sales_target:.1f}**",
    ])
    sezioni.append(tabella_markdown(headers_comp, rows_comp))
    sezioni.append("")

    # Valutazione relativa
    rel_result = valutazione_relativa(
        ticker=ticker,
        eps=eps,
        ebitda=ebitda,
        book_value_per_share=book_value_per_share,
        ricavi=ricavi,
        debito_netto=debito_netto,
        shares_outstanding=shares_outstanding,
        comparabili=comparabili,
        prezzo_corrente=prezzo_corrente,
    )

    sezioni.append("### 4.2 Statistiche Multipli Comparabili")
    sezioni.append("")
    for mult_name, display_name in [
        ("pe_ratio", "P/E"), ("ev_ebitda", "EV/EBITDA"),
        ("pb_ratio", "P/B"), ("ev_sales", "EV/Sales"),
    ]:
        valori = [getattr(c, mult_name) for c in comparabili]
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
                rows_impl.append([nome_mult, formatta_valuta(valore, valuta)])
    if rows_impl:
        sezioni.append(tabella_markdown(headers_impl, rows_impl))
    sezioni.append("")

    valore_relativo = rel_result.valore_per_azione
    upside_rel = (valore_relativo - prezzo_corrente) / prezzo_corrente if prezzo_corrente > 0 else 0
    sezioni.append(f"**Valore Mediano Multipli:** {formatta_valuta(valore_relativo, valuta)}")
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
        debito_netto=debito_netto,
        shares_outstanding=shares_outstanding,
        wacc_range=sens["wacc_range"],
        growth_range=sens["growth_range"],
        anni_proiezione=10,
        crescita_alta=crescita_alta,
    )
    sezioni.append(formatta_sensitivity(sens_wacc_g, valuta))
    sezioni.append("")

    # 5.2 Crescita Ricavi vs Margine Operativo
    sezioni.append("### 5.2 Crescita Ricavi vs Margine Operativo")
    sezioni.append("")

    sens_crescita_margine = sensitivity_crescita_margine(
        ricavi_base=ricavi,
        debito_netto=debito_netto,
        shares_outstanding=shares_outstanding,
        wacc=wacc_val,
        tax_rate=tax_rate,
        capex_pct_ricavi=capex / ricavi,
        depr_pct_ricavi=deprezzamento / ricavi,
        crescita_range=sens["crescita_range"],
        margine_range=sens["margine_range"],
    )
    sezioni.append(formatta_sensitivity(sens_crescita_margine, valuta))
    sezioni.append("")

    # ==================================================================
    # SEZIONE 6: ANALISI PER SCENARI
    # ==================================================================
    sezioni.append("## 6. Analisi per Scenari")
    sezioni.append("")

    scenari = crea_scenari_standard(
        valore_base=valore_per_azione_dcf,
        upside_pct=sc["upside_pct"],
        downside_pct=sc["downside_pct"],
        prob_best=sc["prob_best"],
        prob_base=sc["prob_base"],
        prob_worst=sc["prob_worst"],
    )
    sezioni.append("**Scenari:**")
    sezioni.append(f"- **Best Case** ({sc['prob_best']:.0%}): {sc['desc_best']}")
    sezioni.append(f"- **Base Case** ({sc['prob_base']:.0%}): {sc['desc_base']}")
    sezioni.append(f"- **Worst Case** ({sc['prob_worst']:.0%}): {sc['desc_worst']}")
    sezioni.append("")
    sezioni.append(formatta_scenari(scenari, valuta))
    sezioni.append("")

    valore_atteso_scenari = scenari.valore_atteso
    sezioni.append(f"**Valore Atteso Ponderato:** {formatta_valuta(valore_atteso_scenari, valuta)}")
    sezioni.append("")

    # ==================================================================
    # SEZIONE 7: SIMULAZIONE MONTE CARLO
    # ==================================================================
    sezioni.append("## 7. Simulazione Monte Carlo")
    sezioni.append("")
    sezioni.append("**Parametri della simulazione:**")
    sezioni.append("- Iterazioni: 10.000")
    sezioni.append(f"- WACC: Distribuzione Normale (media={formatta_percentuale(wacc_val)}, std={mc['wacc_std']:.1%})")
    sezioni.append(f"- Crescita Alta: Distribuzione Normale (media={crescita_alta:.0%}, std={mc['crescita_alta_std']:.0%})")
    sezioni.append("- Crescita Stabile: Distribuzione Triangolare (1.5%, 2.5%, 3.5%)")
    sezioni.append("")

    mc_result = monte_carlo_dcf(
        fcff_base=fcff_base,
        debito_netto=debito_netto,
        shares_outstanding=shares_outstanding,
        distribuzioni={
            "wacc": {
                "tipo": "normale",
                "media": wacc_val,
                "deviazione_standard": mc["wacc_std"],
            },
            "crescita_alta": {
                "tipo": "normale",
                "media": crescita_alta,
                "deviazione_standard": mc["crescita_alta_std"],
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

    sezioni.append(formatta_monte_carlo(mc_result, valuta))
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
            formatta_valuta(valore_per_azione_dcf, valuta),
            f"{upside_dcf:+.1%}",
            "40%",
        ],
        [
            "Valutazione Relativa (Multipli)",
            formatta_valuta(valore_relativo, valuta),
            f"{upside_rel:+.1%}",
            "25%",
        ],
        [
            "Valore Atteso Scenari",
            formatta_valuta(valore_atteso_scenari, valuta),
            f"{(valore_atteso_scenari - prezzo_corrente) / prezzo_corrente:+.1%}",
            "15%",
        ],
        [
            "Monte Carlo (Mediana)",
            formatta_valuta(mc_result["mediana"], valuta),
            f"{(mc_result['mediana'] - prezzo_corrente) / prezzo_corrente:+.1%}",
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
    upside_totale = (valore_ponderato - prezzo_corrente) / prezzo_corrente

    sezioni.append("### Valore Intrinseco Stimato")
    sezioni.append("")
    sezioni.append(f"| | |")
    sezioni.append(f"|---|---|")
    sezioni.append(f"| **Valore Medio Ponderato** | **{formatta_valuta(valore_ponderato, valuta)}** |")
    sezioni.append(f"| Prezzo Corrente | {formatta_valuta(prezzo_corrente, valuta)} |")
    sezioni.append(f"| **Upside/Downside** | **{upside_totale:+.1%}** |")
    sezioni.append(f"| IC 90% Monte Carlo | {formatta_valuta(mc_result['intervallo_confidenza_90'][0], valuta)} - {formatta_valuta(mc_result['intervallo_confidenza_90'][1], valuta)} |")
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
    elif upside_totale > -0.30:
        raccomandazione = "SELL"
        commento = "Il titolo appare significativamente sopravvalutato."
    else:
        raccomandazione = "STRONG SELL"
        commento = "Il titolo appare fortemente sopravvalutato rispetto ai fondamentali."

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
    for rischio in config["rischi_rialzo"]:
        sezioni.append(f"- {rischio}")
    sezioni.append("")
    sezioni.append("### Rischi al Ribasso")
    for rischio in config["rischi_ribasso"]:
        sezioni.append(f"- {rischio}")
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
    report_dir = ROOT / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{ticker}_valuation_report_{date.today().isoformat()}.md"

    contenuto = "\n".join(sezioni)
    report_path.write_text(contenuto, encoding="utf-8")
    print(f"Report scritto in: {report_path}")
    print(f"Dimensione: {len(contenuto):,} caratteri")
    print(f"\nRiepilogo rapido:")
    print(f"  WACC:                {formatta_percentuale(wacc_val)}")
    print(f"  FCFF Base:           {formatta_numero(fcff_base)} M USD")
    print(f"  DCF Value/Share:     {formatta_valuta(valore_per_azione_dcf, valuta)}")
    print(f"  Relative Value:      {formatta_valuta(valore_relativo, valuta)}")
    print(f"  MC Mediana:          {formatta_valuta(mc_result['mediana'], valuta)}")
    print(f"  Valore Ponderato:    {formatta_valuta(valore_ponderato, valuta)}")
    print(f"  Prezzo Corrente:     {formatta_valuta(prezzo_corrente, valuta)}")
    print(f"  Upside/Downside:     {upside_totale:+.1%}")
    print(f"  Raccomandazione:     {raccomandazione}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python scripts/run_analysis.py <TICKER>")
        print("Esempio: python scripts/run_analysis.py GOOGL")
        sys.exit(1)

    ticker = sys.argv[1].upper()
    print(f"=== Analisi completa {ticker} ===\n")

    config = carica_config(ticker)
    print(f"Configurazione caricata da configs/{ticker}.json")

    print(f"Recupero dati live da Massive.com...")
    dati = fetch_dati_azienda(ticker)
    print(f"Dati ricevuti per {dati['nome']}\n")

    genera_report(dati, config)


if __name__ == "__main__":
    main()
