#!/usr/bin/env python3
"""Demo 08: Report di Valutazione Completo per Apple Inc. (AAPL).

Esegue tutte le metodologie di valutazione e produce un riepilogo finale:
1. WACC (Costo del Capitale)
2. DCF FCFF (Flussi di Cassa Scontati)
3. Valutazione Relativa (Comparabili)
4. Analisi di Sensitivita'
5. Riepilogo Multi-Metodo con raccomandazione finale
"""
from valuation_analyst.tools.capm import calcola_costo_equity
from valuation_analyst.tools.beta_estimation import beta_levered
from valuation_analyst.tools.wacc import calcola_wacc_completo
from valuation_analyst.tools.risk_premium import spread_da_rating
from valuation_analyst.tools.dcf_fcff import calcola_fcff, calcola_dcf_fcff, valutazione_fcff
from valuation_analyst.tools.multiples import valutazione_relativa
from valuation_analyst.tools.sensitivity_table import sensitivity_wacc_growth
from valuation_analyst.tools.scenario_analysis import crea_scenari_standard
from valuation_analyst.models.comparable import Comparabile
from valuation_analyst.utils.formatting import (
    formatta_miliardi,
    formatta_milioni,
    formatta_multiplo,
    formatta_percentuale,
    formatta_valuta,
)


def main() -> None:
    print()
    print("#" * 75)
    print("#" + " " * 73 + "#")
    print("#" + "  REPORT DI VALUTAZIONE - Apple Inc. (AAPL)".center(73) + "#")
    print("#" + "  Data Sample - Scopo Dimostrativo".center(73) + "#")
    print("#" + " " * 73 + "#")
    print("#" * 75)

    # =====================================================================
    # DATI INPUT
    # =====================================================================
    # Parametri mercato
    rf = 0.042
    erp = 0.055
    beta_u_settore = 0.95
    de_ratio = 0.08
    tax_rate = 0.153

    # Dati fondamentali Apple (in milioni $)
    ebit = 120_000
    capex = 11_000
    deprezzamento = 11_500
    delta_wc = -2_000
    total_debt = 111_000
    cash = 62_000
    market_cap_val = 2_800_000   # $2.8T in milioni
    shares = 15_400
    prezzo_corrente = 182.0

    # Dati per comparabili
    eps = 6.42
    ebitda = 134_000
    bvps = 4.25
    ricavi = 383_000
    debito_netto = total_debt - cash

    # =====================================================================
    # SEZIONE 1: COSTO DEL CAPITALE
    # =====================================================================
    print(f"\n{'=' * 75}")
    print("  SEZIONE 1: COSTO DEL CAPITALE (WACC)")
    print(f"{'=' * 75}")

    bl = beta_levered(beta_u_settore, tax_rate, de_ratio)
    re = calcola_costo_equity(rf, bl, erp)
    spread = spread_da_rating("AA+")
    rd_pre = rf + spread

    cc = calcola_wacc_completo(
        rf, bl, erp, rd_pre, tax_rate,
        market_cap_val * 1e6,  # Converti in unita' per la funzione
        total_debt * 1e6,
    )
    wacc = cc.wacc

    print(f"\n  {'Componente':<35s} {'Valore':>12s}")
    print(f"  {'─' * 35} {'─' * 12}")
    print(f"  {'Risk-Free Rate (Rf)':<35s} {formatta_percentuale(rf):>12s}")
    print(f"  {'Beta Unlevered (settore)':<35s} {beta_u_settore:>12.2f}")
    print(f"  {'Beta Levered (AAPL)':<35s} {bl:>12.4f}")
    print(f"  {'Equity Risk Premium (ERP)':<35s} {formatta_percentuale(erp):>12s}")
    print(f"  {'Costo Equity (Re)':<35s} {formatta_percentuale(re):>12s}")
    print(f"  {'Rating Creditizio':<35s} {'AA+':>12s}")
    print(f"  {'Default Spread':<35s} {formatta_percentuale(spread):>12s}")
    print(f"  {'Costo Debito Pre-Tax (Rd)':<35s} {formatta_percentuale(rd_pre):>12s}")
    print(f"  {'Costo Debito Post-Tax':<35s} {formatta_percentuale(cc.costo_debito_post_tax):>12s}")
    print(f"  {'Peso Equity (E/V)':<35s} {formatta_percentuale(cc.peso_equity):>12s}")
    print(f"  {'Peso Debito (D/V)':<35s} {formatta_percentuale(cc.peso_debito):>12s}")
    print(f"  {'─' * 35} {'─' * 12}")
    print(f"  {'WACC':<35s} {formatta_percentuale(wacc):>12s}")

    # =====================================================================
    # SEZIONE 2: DCF FCFF
    # =====================================================================
    print(f"\n{'=' * 75}")
    print("  SEZIONE 2: VALUTAZIONE DCF FCFF")
    print(f"{'=' * 75}")

    crescita_alta = 0.10
    crescita_stabile = 0.025

    fcff_base = calcola_fcff(ebit, tax_rate, capex, deprezzamento, delta_wc)
    dcf = calcola_dcf_fcff(fcff_base, wacc, crescita_alta, crescita_stabile, 5, 5)

    ev = dcf.valore_totale
    eq_dcf = ev - debito_netto
    val_dcf = eq_dcf / shares

    print(f"\n  Parametri DCF:")
    print(f"    FCFF Base:                {formatta_milioni(fcff_base * 1e6)}")
    print(f"    Crescita Alta (5 anni):   {formatta_percentuale(crescita_alta)}")
    print(f"    Crescita Stabile:         {formatta_percentuale(crescita_stabile)}")
    print(f"    WACC:                     {formatta_percentuale(wacc)}")

    print(f"\n  Proiezione Flussi:")
    print(f"  {'Anno':>6s}  {'Crescita':>10s}  {'FCFF ($M)':>14s}  {'VA ($M)':>14s}")
    print(f"  {'─' * 6}  {'─' * 10}  {'─' * 14}  {'─' * 14}")
    for p in dcf.proiezioni:
        fcff_val = p.fcff if p.fcff is not None else 0.0
        print(
            f"  {p.anno:6d}  "
            f"{formatta_percentuale(p.tasso_crescita):>10s}  "
            f"${fcff_val:>12,.0f}  "
            f"${p.valore_attuale:>12,.0f}"
        )

    print(f"\n  Riepilogo DCF:")
    print(f"    VA Flussi Espliciti:      {formatta_milioni(dcf.valore_attuale_flussi * 1e6)}")
    print(f"    VA Terminal Value:        {formatta_milioni(dcf.valore_terminale_attuale * 1e6)}")
    print(f"    Peso Terminal Value:      {formatta_percentuale(dcf.percentuale_valore_terminale)}")
    print(f"    Enterprise Value:         {formatta_milioni(ev * 1e6)}")
    print(f"    - Debito Netto:           {formatta_milioni(debito_netto * 1e6)}")
    print(f"    = Equity Value:           {formatta_milioni(eq_dcf * 1e6)}")
    print(f"    Valore per Azione (DCF):  {formatta_valuta(val_dcf)}")

    # =====================================================================
    # SEZIONE 3: VALUTAZIONE RELATIVA
    # =====================================================================
    print(f"\n{'=' * 75}")
    print("  SEZIONE 3: VALUTAZIONE RELATIVA (COMPARABILI)")
    print(f"{'=' * 75}")

    comparabili = [
        Comparabile("MSFT", "Microsoft", "Technology", 2_800_000, pe_ratio=34.5, ev_ebitda=22.8, pb_ratio=12.1, ev_sales=12.5),
        Comparabile("GOOGL", "Alphabet", "Technology", 1_750_000, pe_ratio=25.2, ev_ebitda=16.4, pb_ratio=6.3, ev_sales=6.8),
        Comparabile("META", "Meta Platforms", "Technology", 900_000, pe_ratio=27.8, ev_ebitda=14.2, pb_ratio=7.5, ev_sales=7.2),
        Comparabile("AMZN", "Amazon", "Technology", 1_550_000, pe_ratio=58.0, ev_ebitda=19.5, pb_ratio=8.2, ev_sales=2.8),
        Comparabile("SAMSUNG", "Samsung", "Technology", 350_000, pe_ratio=14.2, ev_ebitda=5.8, pb_ratio=1.3, ev_sales=1.5),
    ]

    ris_rel = valutazione_relativa(
        ticker="AAPL",
        eps=eps,
        ebitda=ebitda,
        book_value_per_share=bvps,
        ricavi=ricavi,
        debito_netto=debito_netto,
        shares_outstanding=shares,
        comparabili=comparabili,
        prezzo_corrente=prezzo_corrente,
    )
    val_rel = ris_rel.valore_per_azione

    etichette = {"pe_ratio": "P/E", "ev_ebitda": "EV/EBITDA", "pb_ratio": "P/BV", "ev_sales": "EV/Sales", "ev_ebit": "EV/EBIT"}

    print(f"\n  {'Multiplo':<14s} {'Mediana Peers':>14s} {'Valore Impl.':>14s}")
    print(f"  {'─' * 14} {'─' * 14} {'─' * 14}")
    for chiave, valore in ris_rel.dettagli.items():
        if chiave.startswith("valore_implicito_"):
            nome_m = chiave.replace("valore_implicito_", "")
            etichetta = etichette.get(nome_m, nome_m)
            med_key = f"mediana_{nome_m}"
            med = ris_rel.dettagli.get(med_key, 0.0)
            if isinstance(med, (int, float)) and isinstance(valore, (int, float)):
                print(f"  {etichetta:<14s} {formatta_multiplo(med):>14s} {formatta_valuta(valore):>14s}")

    print(f"\n  Valore per Azione (Relativa): {formatta_valuta(val_rel)}")

    # =====================================================================
    # SEZIONE 4: SENSITIVITY
    # =====================================================================
    print(f"\n{'=' * 75}")
    print("  SEZIONE 4: ANALISI DI SENSITIVITA'")
    print(f"{'=' * 75}")

    wacc_range = [0.080, 0.085, 0.090, 0.095, 0.100, 0.105]
    growth_range = [0.020, 0.025, 0.030]

    ris_sens = sensitivity_wacc_growth(
        fcff_base=fcff_base,
        debito_netto=debito_netto,
        shares_outstanding=shares,
        wacc_range=wacc_range,
        growth_range=growth_range,
        anni_proiezione=10,
        crescita_alta=crescita_alta,
    )

    print(f"\n  Valore per Azione ($) - WACC vs Terminal Growth")
    print()
    header = f"  {'WACC':>8s}"
    for g in growth_range:
        header += f"  {formatta_percentuale(g):>10s}"
    print(header)
    print(f"  {'─' * 8}" + f"  {'─' * 10}" * len(growth_range))
    for i, w in enumerate(wacc_range):
        riga = f"  {formatta_percentuale(w):>8s}"
        for j, _g in enumerate(growth_range):
            val = ris_sens.matrice_risultati[i][j]
            if val != val:
                riga += f"  {'N/A':>10s}"
            else:
                riga += f"  {formatta_valuta(val):>10s}"
        print(riga)

    print(f"\n  Range:    {formatta_valuta(ris_sens.valore_minimo)} - {formatta_valuta(ris_sens.valore_massimo)}")
    print(f"  Centrale: {formatta_valuta(ris_sens.valore_centrale)}")

    # --- Analisi scenari ---
    scenari = crea_scenari_standard(val_dcf, upside_pct=0.30, downside_pct=0.25)

    print(f"\n  Scenari:")
    print(f"  {'Scenario':<15s} {'Prob.':>8s} {'Valore':>12s} {'Contributo':>12s}")
    print(f"  {'─' * 15} {'─' * 8} {'─' * 12} {'─' * 12}")
    for s in scenari.scenari:
        val_str = formatta_valuta(s.valore_risultante) if s.valore_risultante is not None else "N/D"
        print(f"  {s.nome:<15s} {formatta_percentuale(s.probabilita):>8s} {val_str:>12s} {formatta_valuta(s.valore_ponderato):>12s}")
    print(f"  {'─' * 15} {'─' * 8} {'─' * 12} {'─' * 12}")
    print(f"  {'Valore Atteso':<15s} {'':>8s} {'':>12s} {formatta_valuta(scenari.valore_atteso):>12s}")

    # =====================================================================
    # SEZIONE 5: RIEPILOGO MULTI-METODO
    # =====================================================================
    print(f"\n{'=' * 75}")
    print("  SEZIONE 5: RIEPILOGO E RACCOMANDAZIONE")
    print(f"{'=' * 75}")

    val_scenari = scenari.valore_atteso
    val_sensitivity_med = ris_sens.valore_centrale

    # Media dei metodi
    valori_metodi = {
        "DCF FCFF": val_dcf,
        "Comparabili (Mediana)": val_rel,
        "Scenari (Valore Atteso)": val_scenari,
        "Sensitivity (Centrale)": val_sensitivity_med,
    }

    print(f"\n  {'Metodo':<30s} {'Valore/Azione':>14s}")
    print(f"  {'─' * 30} {'─' * 14}")
    for metodo, valore in valori_metodi.items():
        print(f"  {metodo:<30s} {formatta_valuta(valore):>14s}")

    # Media e mediana dei metodi
    lista_valori = list(valori_metodi.values())
    import statistics
    media_metodi = statistics.mean(lista_valori)
    mediana_metodi = statistics.median(lista_valori)

    print(f"  {'─' * 30} {'─' * 14}")
    print(f"  {'Media Metodi':<30s} {formatta_valuta(media_metodi):>14s}")
    print(f"  {'Mediana Metodi':<30s} {formatta_valuta(mediana_metodi):>14s}")

    # Intervallo di valutazione
    val_min = min(lista_valori)
    val_max = max(lista_valori)
    print(f"\n  Intervallo di Valutazione:   {formatta_valuta(val_min)} - {formatta_valuta(val_max)}")
    print(f"  Prezzo di Mercato:           {formatta_valuta(prezzo_corrente)}")

    # Upside/downside
    upside_media = (media_metodi - prezzo_corrente) / prezzo_corrente
    upside_mediana = (mediana_metodi - prezzo_corrente) / prezzo_corrente

    print(f"\n  Upside/Downside (media):     {upside_media:+.1%}")
    print(f"  Upside/Downside (mediana):   {upside_mediana:+.1%}")

    # Raccomandazione
    if upside_mediana > 0.10:
        raccomandazione = "SOTTOVALUTATO - Potenziale di apprezzamento"
    elif upside_mediana < -0.10:
        raccomandazione = "SOPRAVVALUTATO - Rischio di correzione"
    else:
        raccomandazione = "FAIR VALUE - In linea con il valore intrinseco"

    print(f"\n  ╔═══════════════════════════════════════════════════════════════╗")
    print(f"  ║  RACCOMANDAZIONE: {raccomandazione:<45s}║")
    print(f"  ║  Valore Intrinseco Stimato: {formatta_valuta(mediana_metodi):<35s}║")
    print(f"  ║  Prezzo di Mercato:         {formatta_valuta(prezzo_corrente):<35s}║")
    print(f"  ╚═══════════════════════════════════════════════════════════════╝")

    # Avvertenze
    print(f"\n  Note e Avvertenze:")
    print(f"  - I dati utilizzati sono di esempio e non aggiornati in tempo reale")
    print(f"  - La valutazione e' sensibile alle ipotesi di crescita e tasso di sconto")
    print(f"  - Il peso del Terminal Value ({formatta_percentuale(dcf.percentuale_valore_terminale)}) e' significativo")
    print(f"  - Si consiglia di integrare con analisi qualitativa del business")

    print(f"\n{'#' * 75}")
    print(f"#{'  FINE REPORT  '.center(73)}#")
    print(f"{'#' * 75}")
    print()


if __name__ == "__main__":
    main()
