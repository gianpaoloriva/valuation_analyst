#!/usr/bin/env python3
"""Demo 04: Valutazione Equity come Opzione (Modello di Merton).

Dimostra l'applicazione del modello di Merton per un'azienda in distress:
- Equity vista come call option europea sugli asset aziendali
- Calcolo probabilita' di default
- Yield implicito del debito e default spread
"""
from valuation_analyst.tools.equity_as_option import (
    analisi_distress,
    stima_volatilita_asset,
    valuta_equity_come_opzione,
)
from valuation_analyst.utils.formatting import formatta_milioni, formatta_percentuale, formatta_valuta


def main() -> None:
    print("=" * 70)
    print("DEMO 04: Equity come Opzione - Azienda in Distress")
    print("=" * 70)

    # --- Parametri dell'azienda ipotetica in distress ---
    # Un'azienda manifatturiera con leva elevata e alta volatilita'
    valore_asset = 500_000_000    # Valore totale asset: $500M
    debito_nominale = 400_000_000 # Debito nominale: $400M
    scadenza_debito = 5.0         # Scadenza media ponderata: 5 anni
    risk_free_rate = 0.042        # Risk-free rate: 4.2%
    volatilita_asset = 0.40       # Volatilita' annualizzata asset: 40%
    shares_outstanding = 10       # 10 milioni di azioni (in milioni per coerenza)

    print(f"\n--- Parametri Azienda ---")
    print(f"  Valore Asset (V):            {formatta_milioni(valore_asset)}")
    print(f"  Debito Nominale (K):         {formatta_milioni(debito_nominale)}")
    print(f"  Scadenza Media Debito (T):   {scadenza_debito:.1f} anni")
    print(f"  Risk-Free Rate (r):          {formatta_percentuale(risk_free_rate)}")
    print(f"  Volatilita' Asset (sigma):   {formatta_percentuale(volatilita_asset)}")
    print(f"  Rapporto V/K:                {valore_asset / debito_nominale:.2f}x")

    # --- Analogia con le opzioni ---
    print(f"\n--- Analogia Black-Scholes ---")
    print(f"  Sottostante (S) = Valore Asset     = {formatta_milioni(valore_asset)}")
    print(f"  Strike (K)      = Debito Nominale   = {formatta_milioni(debito_nominale)}")
    print(f"  Scadenza (T)    = Maturity Debito    = {scadenza_debito:.0f} anni")
    print(f"  Volatilita'     = Vol. Asset         = {formatta_percentuale(volatilita_asset)}")
    print(f"  Risk-Free (r)   = Tasso Privo Rischio= {formatta_percentuale(risk_free_rate)}")
    print(f"  Equity = Call Option su asset con strike = debito")

    # --- Calcolo ---
    risultato = valuta_equity_come_opzione(
        valore_asset=valore_asset,
        debito_nominale=debito_nominale,
        scadenza_debito=scadenza_debito,
        risk_free_rate=risk_free_rate,
        volatilita_asset=volatilita_asset,
    )

    print(f"\n--- Risultati del Modello di Merton ---")
    print(f"  d1:                          {risultato['d1']:+.4f}")
    print(f"  d2:                          {risultato['d2']:+.4f}")
    print(f"  N(d1):                       {risultato['N_d1']:.4f}")
    print(f"  N(d2):                       {risultato['N_d2']:.4f}")

    print(f"\n--- Valutazione ---")
    print(f"  Valore Equity:               {formatta_milioni(risultato['valore_equity'])}")
    print(f"  Valore Debito (mercato):     {formatta_milioni(risultato['valore_debito'])}")
    print(f"  Valore Asset (verifica):     {formatta_milioni(risultato['valore_equity'] + risultato['valore_debito'])}")
    print(f"  Valore per Azione:           {formatta_valuta(risultato['valore_equity'] / (shares_outstanding * 1e6))}")

    print(f"\n--- Analisi del Rischio ---")
    print(f"  Probabilita' di Default:     {formatta_percentuale(risultato['probabilita_default'])}")
    print(f"  Prob. Sopravvivenza:         {formatta_percentuale(1 - risultato['probabilita_default'])}")
    print(f"  Yield Implicito Debito:      {formatta_percentuale(risultato['yield_implicito_debito'])}")
    print(f"  Default Spread:              {formatta_percentuale(risultato['default_spread'])}")

    # --- Nota interpretativa ---
    recovery = risultato['valore_debito'] / debito_nominale
    print(f"  Recovery Rate Implicito:     {formatta_percentuale(recovery)}")

    # --- Analisi di Distress ---
    distress = analisi_distress(
        valore_asset=valore_asset,
        debito_nominale=debito_nominale,
        scadenza_debito=scadenza_debito,
        risk_free_rate=risk_free_rate,
        volatilita_asset=volatilita_asset,
    )

    print(f"\n--- Diagnosi di Distress ---")
    stato = "SI'" if distress["in_distress"] else "NO"
    print(f"  In Distress (V < K)?         {stato}")
    print(f"  Rapporto di Copertura (V/K): {distress['rapporto_copertura']:.2f}x")
    print(f"  Recovery Rate:               {formatta_percentuale(distress['recovery_rate_implicito'])}")
    print(f"  Equity Residuo:              {formatta_milioni(distress['valore_equity_residuo'])}")

    # --- Confronto con scenario di asset piu' elevato ---
    print(f"\n--- Analisi di Sensitivita': Valore Asset ---")
    print(f"  {'Asset ($M)':>12s}  {'Equity ($M)':>14s}  {'P(Default)':>12s}  {'Spread':>10s}")
    print(f"  {'─' * 12}  {'─' * 14}  {'─' * 12}  {'─' * 10}")

    for v in [300e6, 350e6, 400e6, 450e6, 500e6, 600e6, 700e6, 800e6]:
        res = valuta_equity_come_opzione(v, debito_nominale, scadenza_debito, risk_free_rate, volatilita_asset)
        print(
            f"  ${v / 1e6:>10,.0f}  "
            f"{formatta_milioni(res['valore_equity']):>14s}  "
            f"{formatta_percentuale(res['probabilita_default']):>12s}  "
            f"{formatta_percentuale(res['default_spread']):>10s}"
        )

    # --- Stima volatilita' asset da equity ---
    print(f"\n--- Stima Volatilita' Asset da Volatilita' Equity ---")
    vol_equity = 0.65  # Ipotetica volatilita' equity osservata
    market_cap = risultato["valore_equity"]
    debito_mercato = risultato["valore_debito"]
    vol_asset_stimata = stima_volatilita_asset(vol_equity, market_cap, debito_mercato)
    print(f"  Volatilita' Equity (osservata):  {formatta_percentuale(vol_equity)}")
    print(f"  Market Cap (da modello):         {formatta_milioni(market_cap)}")
    print(f"  Debito Mercato (da modello):     {formatta_milioni(debito_mercato)}")
    print(f"  Volatilita' Asset (stimata):     {formatta_percentuale(vol_asset_stimata)}")

    print("\n" + "=" * 70)
    print("Demo 04 completata!")
    print("=" * 70)


if __name__ == "__main__":
    main()
