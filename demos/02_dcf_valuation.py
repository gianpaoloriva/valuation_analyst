#!/usr/bin/env python3
"""Demo 02: Valutazione DCF FCFF per Apple Inc.

Dimostra il calcolo di:
- FCFF (Free Cash Flow to Firm) a partire dai fondamentali
- Proiezione 10 anni con modello a 3 fasi (alta, transizione, stabile)
- Terminal Value con metodo Gordon Growth
- Enterprise Value, Equity Value e Valore per Azione
"""
from valuation_analyst.tools.dcf_fcff import calcola_fcff, calcola_dcf_fcff, valutazione_fcff
from valuation_analyst.tools.growth_models import crescita_3_fasi
from valuation_analyst.utils.formatting import (
    formatta_miliardi,
    formatta_milioni,
    formatta_percentuale,
    formatta_valuta,
)


def main() -> None:
    print("=" * 70)
    print("DEMO 02: Valutazione DCF FCFF - Apple Inc. (AAPL)")
    print("=" * 70)

    # --- Dati fondamentali Apple (sample, in milioni $) ---
    ebit = 120_000           # EBIT ~$120B
    tax_rate = 0.153         # Tax rate effettivo
    capex = 11_000           # CapEx ~$11B
    deprezzamento = 11_500   # D&A ~$11.5B
    delta_wc = -2_000        # Variazione WC (negativa = liberazione cassa)
    total_debt = 111_000     # Debito totale $111B
    cash = 62_000            # Cassa e investimenti $62B
    shares_outstanding = 15_400  # Azioni in circolazione (milioni)
    prezzo_corrente = 182.0  # Prezzo per azione

    # Parametri di crescita e sconto
    wacc = 0.0935            # WACC calcolato nella demo 01
    crescita_alta = 0.10     # Crescita nella fase di alta crescita
    crescita_stabile = 0.025 # Crescita perpetua (stabile)
    anni_alta = 5            # Anni di alta crescita
    anni_transizione = 5     # Anni di transizione

    # --- Passo 1: Calcolo FCFF Base ---
    fcff_base = calcola_fcff(ebit, tax_rate, capex, deprezzamento, delta_wc)
    print(f"\n--- Passo 1: Calcolo FCFF Base ---")
    print(f"  EBIT:                {formatta_milioni(ebit * 1e6)}")
    print(f"  EBIT * (1 - t):     {formatta_milioni(ebit * (1 - tax_rate) * 1e6)}")
    print(f"  + Deprezzamento:    {formatta_milioni(deprezzamento * 1e6)}")
    print(f"  - CapEx:            {formatta_milioni(capex * 1e6)}")
    print(f"  - Delta WC:         {formatta_milioni(delta_wc * 1e6)}")
    print(f"  ────────────────────────────────")
    print(f"  = FCFF Base:        {formatta_milioni(fcff_base * 1e6)}")

    # --- Passo 2: Tassi di crescita a 3 fasi ---
    tassi = crescita_3_fasi(crescita_alta, crescita_stabile, anni_alta, anni_transizione)
    print(f"\n--- Passo 2: Tassi di Crescita (3 Fasi) ---")
    print(f"  Fase 1 (Alta):       {formatta_percentuale(crescita_alta)} per {anni_alta} anni")
    print(f"  Fase 2 (Transizione): convergenza lineare per {anni_transizione} anni")
    print(f"  Fase 3 (Stabile):    {formatta_percentuale(crescita_stabile)} perpetua")
    print()
    print(f"  {'Anno':>6s}  {'Tasso':>8s}  {'Fase':<15s}")
    print(f"  {'─' * 6}  {'─' * 8}  {'─' * 15}")
    for i, t in enumerate(tassi, 1):
        if i <= anni_alta:
            fase = "Alta crescita"
        elif i <= anni_alta + anni_transizione:
            fase = "Transizione"
        else:
            fase = "Stabile"
        print(f"  {i:6d}  {formatta_percentuale(t):>8s}  {fase:<15s}")

    # --- Passo 3: DCF Completo ---
    dcf = calcola_dcf_fcff(
        fcff_base=fcff_base,
        wacc=wacc,
        crescita_alta=crescita_alta,
        crescita_stabile=crescita_stabile,
        anni_alta=anni_alta,
        anni_transizione=anni_transizione,
    )

    print(f"\n--- Passo 3: Proiezione Flussi di Cassa ---")
    print(f"  {'Anno':>6s}  {'Crescita':>10s}  {'FCFF':>14s}  {'VA':>14s}")
    print(f"  {'─' * 6}  {'─' * 10}  {'─' * 14}  {'─' * 14}")
    for p in dcf.proiezioni:
        fcff_val = p.fcff if p.fcff is not None else 0.0
        print(
            f"  {p.anno:6d}  "
            f"{formatta_percentuale(p.tasso_crescita):>10s}  "
            f"{formatta_milioni(fcff_val * 1e6):>14s}  "
            f"{formatta_milioni(p.valore_attuale * 1e6):>14s}"
        )

    print(f"\n--- Passo 4: Valore Terminale ---")
    print(f"  Metodo:                       Gordon Growth Model")
    print(f"  FCFF ultimo anno:             {formatta_milioni(dcf.proiezioni[-1].fcff * 1e6)}")  # type: ignore[union-attr]
    print(f"  Crescita perpetua:            {formatta_percentuale(crescita_stabile)}")
    print(f"  Tasso di sconto (WACC):       {formatta_percentuale(wacc)}")
    print(f"  Valore Terminale:             {formatta_milioni(dcf.valore_terminale * 1e6)}")
    print(f"  VA Valore Terminale:          {formatta_milioni(dcf.valore_terminale_attuale * 1e6)}")
    print(f"  Peso Terminal Value:          {formatta_percentuale(dcf.percentuale_valore_terminale)}")

    # --- Passo 5: Dall'Enterprise Value al Valore per Azione ---
    enterprise_value = dcf.valore_totale
    debito_netto = total_debt - cash
    equity_value = enterprise_value - debito_netto
    valore_per_azione = equity_value / shares_outstanding

    print(f"\n--- Passo 5: Dal Valore d'Impresa al Valore per Azione ---")
    print(f"  VA Flussi Espliciti:          {formatta_milioni(dcf.valore_attuale_flussi * 1e6)}")
    print(f"  VA Valore Terminale:          {formatta_milioni(dcf.valore_terminale_attuale * 1e6)}")
    print(f"  ────────────────────────────────────────────")
    print(f"  Enterprise Value:             {formatta_milioni(enterprise_value * 1e6)}")
    print(f"  - Debito Totale:              {formatta_milioni(total_debt * 1e6)}")
    print(f"  + Cassa:                      {formatta_milioni(cash * 1e6)}")
    print(f"  ────────────────────────────────────────────")
    print(f"  Equity Value:                 {formatta_milioni(equity_value * 1e6)}")
    print(f"  / Azioni in circolazione:     {shares_outstanding:,.0f}M")
    print(f"  ════════════════════════════════════════════")
    print(f"  Valore per Azione:            {formatta_valuta(valore_per_azione)}")
    print(f"  Prezzo di Mercato:            {formatta_valuta(prezzo_corrente)}")
    upside = (valore_per_azione - prezzo_corrente) / prezzo_corrente
    print(f"  Upside/Downside:              {upside:+.1%}")

    # --- Passo 6: Valutazione completa con ValuationResult ---
    risultato = valutazione_fcff(
        ticker="AAPL",
        ebit=ebit,
        tax_rate=tax_rate,
        capex=capex,
        deprezzamento=deprezzamento,
        delta_wc=delta_wc,
        wacc=wacc,
        total_debt=total_debt,
        cash=cash,
        shares_outstanding=shares_outstanding,
        crescita_alta=crescita_alta,
        crescita_stabile=crescita_stabile,
        anni_alta=anni_alta,
        anni_transizione=anni_transizione,
        prezzo_corrente=prezzo_corrente,
    )

    print(f"\n--- Riepilogo ValuationResult ---")
    print(risultato.riepilogo())

    print("\n" + "=" * 70)
    print("Demo 02 completata!")
    print("=" * 70)


if __name__ == "__main__":
    main()
