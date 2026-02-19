#!/usr/bin/env python3
"""Demo 01: Calcolo del Costo del Capitale (WACC/CAPM) per Apple Inc.

Dimostra il calcolo di:
- Costo Equity via CAPM
- Beta bottom-up (levered/unlevered)
- WACC completo
"""
from valuation_analyst.tools.capm import calcola_costo_equity, calcola_costo_equity_dettagliato
from valuation_analyst.tools.beta_estimation import beta_levered, beta_unlevered
from valuation_analyst.tools.wacc import calcola_wacc, calcola_wacc_completo
from valuation_analyst.tools.risk_premium import spread_da_rating
from valuation_analyst.utils.formatting import formatta_percentuale


def main() -> None:
    print("=" * 60)
    print("DEMO 01: Costo del Capitale - Apple Inc. (AAPL)")
    print("=" * 60)

    # --- Parametri Apple (dati sample) ---
    rf = 0.042          # Risk-free rate (US Treasury 10Y)
    beta_u = 0.95       # Beta unlevered settore Technology
    de_ratio = 0.08     # D/E ratio Apple (basso leverage)
    tax_rate = 0.153    # Tax rate effettivo Apple
    erp = 0.055         # Equity Risk Premium
    market_cap = 2_800_000_000_000   # Capitalizzazione di mercato ($2.8T)
    total_debt = 111_000_000_000     # Debito totale ($111B)

    print("\n--- Parametri Input ---")
    print(f"  Risk-Free Rate:              {formatta_percentuale(rf)}")
    print(f"  Beta Unlevered (settore):    {beta_u:.2f}")
    print(f"  D/E Ratio:                   {de_ratio:.2f}")
    print(f"  Tax Rate:                    {formatta_percentuale(tax_rate)}")
    print(f"  ERP:                         {formatta_percentuale(erp)}")
    print(f"  Market Cap:                  ${market_cap / 1e9:,.0f}B")
    print(f"  Debito Totale:               ${total_debt / 1e9:,.0f}B")

    # --- Calcolo Beta Levered ---
    bl = beta_levered(beta_u, tax_rate, de_ratio)
    print(f"\n--- Beta (Formula di Hamada) ---")
    print(f"  Beta Unlevered:  {beta_u:.4f}")
    print(f"  Beta Levered:    {bl:.4f}")
    print(f"  Formula: {beta_u:.2f} * (1 + (1 - {tax_rate:.3f}) * {de_ratio:.2f}) = {bl:.4f}")

    # --- Verifica inversa ---
    bu_check = beta_unlevered(bl, tax_rate, de_ratio)
    print(f"  Verifica inversa (unlevering): {bu_check:.4f}")

    # --- Costo Equity via CAPM ---
    re = calcola_costo_equity(rf, bl, erp)
    print(f"\n--- Costo Equity (CAPM) ---")
    print(f"  Re = Rf + Beta * ERP")
    print(f"  Re = {formatta_percentuale(rf)} + {bl:.4f} * {formatta_percentuale(erp)}")
    print(f"  Re = {formatta_percentuale(re)}")

    # --- Versione dettagliata con scomposizione ---
    dettaglio = calcola_costo_equity_dettagliato(rf, bl, erp)
    print(f"\n--- Scomposizione Costo Equity ---")
    for componente, valore in dettaglio["componenti"].items():
        print(f"  {componente:35s} {formatta_percentuale(valore):>8s}")
    print(f"  {'TOTALE':35s} {formatta_percentuale(dettaglio['costo_equity']):>8s}")

    # --- Costo del Debito ---
    spread = spread_da_rating("AA+")
    rd_pre = rf + spread
    rd_post = rd_pre * (1 - tax_rate)
    print(f"\n--- Costo Debito ---")
    print(f"  Rating:                      AA+")
    print(f"  Default Spread:              {formatta_percentuale(spread)}")
    print(f"  Costo Debito Pre-Tax:        {formatta_percentuale(rd_pre)}")
    print(f"  Costo Debito Post-Tax:       {formatta_percentuale(rd_post)}")

    # --- WACC Completo ---
    cc = calcola_wacc_completo(rf, bl, erp, rd_pre, tax_rate, market_cap, total_debt)
    print(f"\n--- WACC ---")
    print(f"  Peso Equity (E/V):           {formatta_percentuale(cc.peso_equity)}")
    print(f"  Peso Debito (D/V):           {formatta_percentuale(cc.peso_debito)}")
    print(f"  Costo Equity (Re):           {formatta_percentuale(cc.costo_equity)}")
    print(f"  Costo Debito Post-Tax (Rd):  {formatta_percentuale(cc.costo_debito_post_tax)}")
    print()
    print(f"  WACC = We * Re + Wd * Rd*(1-t)")
    print(
        f"  WACC = {formatta_percentuale(cc.peso_equity)} * {formatta_percentuale(cc.costo_equity)}"
        f" + {formatta_percentuale(cc.peso_debito)} * {formatta_percentuale(cc.costo_debito_post_tax)}"
    )
    print(f"  WACC = {formatta_percentuale(cc.wacc)}")

    # --- Verifica con calcola_wacc base ---
    wacc_check = calcola_wacc(cc.costo_equity, rd_pre, tax_rate, cc.peso_equity, cc.peso_debito)
    print(f"\n  Verifica calcolo base: {formatta_percentuale(wacc_check)}")

    # --- Riepilogo struttura del capitale ---
    print(f"\n--- Riepilogo Completo ---")
    print(cc.riepilogo())

    print("\n" + "=" * 60)
    print("Demo 01 completata!")
    print("=" * 60)


if __name__ == "__main__":
    main()
