#!/usr/bin/env python3
"""Demo 07: Analisi di Sensitivita' e Monte Carlo per Apple Inc.

Dimostra il calcolo di:
- Tabella di sensitivita' WACC vs Terminal Growth Rate
- Tabella di sensitivita' Crescita Ricavi vs Margine Operativo
- Simulazione Monte Carlo semplificata per il DCF
"""
import random
import statistics

from valuation_analyst.tools.sensitivity_table import (
    sensitivity_crescita_margine,
    sensitivity_wacc_growth,
)
from valuation_analyst.tools.scenario_analysis import crea_scenari_standard
from valuation_analyst.tools.dcf_fcff import calcola_dcf_fcff
from valuation_analyst.utils.formatting import formatta_percentuale, formatta_valuta


def main() -> None:
    print("=" * 75)
    print("DEMO 07: Analisi di Sensitivita' e Monte Carlo - Apple Inc. (AAPL)")
    print("=" * 75)

    # --- Parametri Apple (coerenti con demo 02) ---
    fcff_base = 103_650       # FCFF base in milioni $
    total_debt = 111_000
    cash = 62_000
    debito_netto = total_debt - cash
    shares = 15_400           # Azioni in milioni
    wacc_base = 0.0935
    crescita_alta = 0.10
    crescita_stabile = 0.025

    # --- Sezione 1: Sensitivity WACC vs Terminal Growth ---
    print(f"\n{'=' * 75}")
    print("SEZIONE 1: Sensitivity WACC vs Terminal Growth Rate")
    print(f"{'=' * 75}")

    wacc_range = [0.075, 0.080, 0.085, 0.090, 0.095, 0.100, 0.110]
    growth_range = [0.015, 0.020, 0.025, 0.030, 0.035]

    ris_wg = sensitivity_wacc_growth(
        fcff_base=fcff_base,
        debito_netto=debito_netto,
        shares_outstanding=shares,
        wacc_range=wacc_range,
        growth_range=growth_range,
        anni_proiezione=10,
        crescita_alta=crescita_alta,
    )

    # Stampa manuale formattata (piu' leggibile in terminale)
    print(f"\n  Valore per Azione ($) - WACC (righe) vs Terminal Growth (colonne)")
    print()

    # Intestazione
    header = f"  {'WACC':>8s}"
    for g in growth_range:
        header += f"  {formatta_percentuale(g):>10s}"
    print(header)
    print(f"  {'─' * 8}" + f"  {'─' * 10}" * len(growth_range))

    # Righe
    for i, w in enumerate(wacc_range):
        riga = f"  {formatta_percentuale(w):>8s}"
        for j, _g in enumerate(growth_range):
            val = ris_wg.matrice_risultati[i][j]
            if val != val:  # NaN
                riga += f"  {'N/A':>10s}"
            else:
                riga += f"  {formatta_valuta(val):>10s}"
        print(riga)

    print(f"\n  Range valori:    {formatta_valuta(ris_wg.valore_minimo)} - {formatta_valuta(ris_wg.valore_massimo)}")
    print(f"  Valore centrale: {formatta_valuta(ris_wg.valore_centrale)}")

    # --- Sezione 2: Sensitivity Crescita vs Margine Operativo ---
    print(f"\n{'=' * 75}")
    print("SEZIONE 2: Sensitivity Crescita Ricavi vs Margine Operativo")
    print(f"{'=' * 75}")

    ricavi_base = 383_000  # Ricavi Apple in milioni
    crescita_range = [0.03, 0.05, 0.08, 0.10, 0.15]
    margine_range = [0.25, 0.28, 0.30, 0.33, 0.35]

    ris_cm = sensitivity_crescita_margine(
        ricavi_base=ricavi_base,
        debito_netto=debito_netto,
        shares_outstanding=shares,
        wacc=wacc_base,
        tax_rate=0.153,
        capex_pct_ricavi=0.03,
        depr_pct_ricavi=0.03,
        crescita_range=crescita_range,
        margine_range=margine_range,
    )

    print(f"\n  Valore per Azione ($) - Crescita (righe) vs Margine (colonne)")
    print()

    header = f"  {'Crescita':>10s}"
    for m in margine_range:
        header += f"  {formatta_percentuale(m):>10s}"
    print(header)
    print(f"  {'─' * 10}" + f"  {'─' * 10}" * len(margine_range))

    for i, cr in enumerate(crescita_range):
        riga = f"  {formatta_percentuale(cr):>10s}"
        for j, _m in enumerate(margine_range):
            val = ris_cm.matrice_risultati[i][j]
            if val != val:
                riga += f"  {'N/A':>10s}"
            else:
                riga += f"  {formatta_valuta(val):>10s}"
        print(riga)

    print(f"\n  Range valori:    {formatta_valuta(ris_cm.valore_minimo)} - {formatta_valuta(ris_cm.valore_massimo)}")

    # --- Sezione 3: Analisi per Scenari (Best/Base/Worst) ---
    print(f"\n{'=' * 75}")
    print("SEZIONE 3: Analisi per Scenari (Best / Base / Worst)")
    print(f"{'=' * 75}")

    # Calcola il valore base
    dcf_base = calcola_dcf_fcff(fcff_base, wacc_base, crescita_alta, crescita_stabile, 5, 5)
    ev_base = dcf_base.valore_totale
    eq_base = ev_base - debito_netto
    val_base = eq_base / shares

    scenari = crea_scenari_standard(
        valore_base=val_base,
        upside_pct=0.35,       # +35% nello scenario best
        downside_pct=0.25,     # -25% nello scenario worst
        prob_best=0.20,
        prob_base=0.55,
        prob_worst=0.25,
    )

    print(f"\n  {'Scenario':<15s} {'Prob.':>8s} {'Valore/Azione':>16s} {'Contributo':>14s}")
    print(f"  {'─' * 15} {'─' * 8} {'─' * 16} {'─' * 14}")
    for s in scenari.scenari:
        val_str = formatta_valuta(s.valore_risultante) if s.valore_risultante else "N/D"
        pond_str = formatta_valuta(s.valore_ponderato)
        print(f"  {s.nome:<15s} {formatta_percentuale(s.probabilita):>8s} {val_str:>16s} {pond_str:>14s}")
    print(f"  {'─' * 15} {'─' * 8} {'─' * 16} {'─' * 14}")
    print(f"  {'Valore Atteso':<15s} {'100.00%':>8s} {'':<16s} {formatta_valuta(scenari.valore_atteso):>14s}")

    # --- Sezione 4: Simulazione Monte Carlo ---
    print(f"\n{'=' * 75}")
    print("SEZIONE 4: Simulazione Monte Carlo (10.000 iterazioni)")
    print(f"{'=' * 75}")

    # Parametri per il Monte Carlo
    n_simulazioni = 10_000
    random.seed(42)  # Riproducibilita'

    risultati_mc: list[float] = []

    for _ in range(n_simulazioni):
        # Varia casualmente i parametri chiave (distribuzione triangolare)
        wacc_sim = random.triangular(0.075, 0.11, wacc_base)
        g_alta_sim = random.triangular(0.03, 0.18, crescita_alta)
        g_stabile_sim = random.triangular(0.015, 0.04, crescita_stabile)
        fcff_sim = fcff_base * random.triangular(0.85, 1.15, 1.0)

        # Verifica che wacc > g_stabile (necessario per Gordon)
        if wacc_sim <= g_stabile_sim:
            continue

        try:
            # DCF semplificato
            dcf_sim = calcola_dcf_fcff(
                fcff_base=fcff_sim,
                wacc=wacc_sim,
                crescita_alta=g_alta_sim,
                crescita_stabile=g_stabile_sim,
                anni_alta=5,
                anni_transizione=5,
            )
            ev_sim = dcf_sim.valore_totale
            eq_sim = ev_sim - debito_netto
            val_sim = eq_sim / shares
            if val_sim > 0:
                risultati_mc.append(val_sim)
        except (ValueError, ZeroDivisionError):
            continue

    # --- Statistiche Monte Carlo ---
    risultati_mc.sort()
    n = len(risultati_mc)
    media_mc = statistics.mean(risultati_mc)
    mediana_mc = statistics.median(risultati_mc)
    dev_std_mc = statistics.stdev(risultati_mc)
    p5 = risultati_mc[int(n * 0.05)]
    p25 = risultati_mc[int(n * 0.25)]
    p75 = risultati_mc[int(n * 0.75)]
    p95 = risultati_mc[int(n * 0.95)]

    print(f"\n  Simulazioni valide: {n:,d} / {n_simulazioni:,d}")
    print(f"\n  {'Statistica':<25s} {'Valore':>12s}")
    print(f"  {'─' * 25} {'─' * 12}")
    print(f"  {'Media':25s} {formatta_valuta(media_mc):>12s}")
    print(f"  {'Mediana':25s} {formatta_valuta(mediana_mc):>12s}")
    print(f"  {'Deviazione Standard':25s} {formatta_valuta(dev_std_mc):>12s}")
    print(f"  {'Minimo':25s} {formatta_valuta(risultati_mc[0]):>12s}")
    print(f"  {'5o Percentile':25s} {formatta_valuta(p5):>12s}")
    print(f"  {'25o Percentile (Q1)':25s} {formatta_valuta(p25):>12s}")
    print(f"  {'75o Percentile (Q3)':25s} {formatta_valuta(p75):>12s}")
    print(f"  {'95o Percentile':25s} {formatta_valuta(p95):>12s}")
    print(f"  {'Massimo':25s} {formatta_valuta(risultati_mc[-1]):>12s}")

    # --- Distribuzione grafica semplificata ---
    print(f"\n  Distribuzione dei valori (istogramma semplificato):")
    n_bins = 15
    val_min_mc = risultati_mc[0]
    val_max_mc = risultati_mc[-1]
    bin_width = (val_max_mc - val_min_mc) / n_bins
    bins: list[int] = [0] * n_bins

    for v in risultati_mc:
        idx = min(int((v - val_min_mc) / bin_width), n_bins - 1)
        bins[idx] += 1

    max_count = max(bins)
    for i in range(n_bins):
        lower = val_min_mc + i * bin_width
        upper = lower + bin_width
        count = bins[i]
        bar_len = int(count / max_count * 40) if max_count > 0 else 0
        bar = "#" * bar_len
        print(f"  {formatta_valuta(lower):>8s}-{formatta_valuta(upper):>8s} | {bar:<40s} {count:>5d}")

    # --- Intervallo di confidenza al 90% ---
    print(f"\n  Intervallo di Confidenza al 90%: {formatta_valuta(p5)} - {formatta_valuta(p95)}")
    print(f"  Valore Mediano:                  {formatta_valuta(mediana_mc)}")

    print("\n" + "=" * 75)
    print("Demo 07 completata!")
    print("=" * 75)


if __name__ == "__main__":
    main()
