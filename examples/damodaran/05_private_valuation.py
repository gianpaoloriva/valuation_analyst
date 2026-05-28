#!/usr/bin/env python3
"""Demo 05: Valutazione di un'Azienda Privata.

Dimostra il calcolo di:
- Sconto di illiquidita' secondo Damodaran
- Premio di controllo
- Valutazione privata completa (valore 'come se quotata' -> valore finale)
"""
from valuation_analyst.tools.illiquidity_discount import (
    applica_sconto_illiquidita,
    calcola_sconto_illiquidita,
    sconto_per_dimensione,
    sconto_restricted_stock,
)
from valuation_analyst.tools.control_premium import (
    applica_premio_controllo,
    calcola_premio_controllo,
    premio_da_transazioni,
    sconto_minoranza,
    valutazione_privata_completa,
)
from valuation_analyst.utils.formatting import formatta_milioni, formatta_percentuale, formatta_valuta


def main() -> None:
    print("=" * 70)
    print("DEMO 05: Valutazione Azienda Privata - Manifattura Esempio S.r.l.")
    print("=" * 70)

    # --- Dati dell'azienda privata ---
    ricavi = 50_000_000           # Ricavi: EUR 50M
    margine_ebitda = 0.16         # EBITDA Margin: 16%
    ebitda = ricavi * margine_ebitda  # EBITDA: EUR 8M
    ev_ebitda_settore = 7.5       # Multiplo EV/EBITDA medio settore
    debito_netto = 12_000_000     # Debito netto: EUR 12M

    # Valore stimato 'come se quotata' tramite multipli di settore
    enterprise_value = ebitda * ev_ebitda_settore
    equity_value_quotata = enterprise_value - debito_netto

    print(f"\n--- Dati Azienda ---")
    print(f"  Ragione Sociale:             Manifattura Esempio S.r.l.")
    print(f"  Settore:                     Industrial / Manifattura")
    print(f"  Ricavi:                      {formatta_milioni(ricavi, 'EUR')}")
    print(f"  Margine EBITDA:              {formatta_percentuale(margine_ebitda)}")
    print(f"  EBITDA:                      {formatta_milioni(ebitda, 'EUR')}")
    print(f"  Debito Netto:                {formatta_milioni(debito_netto, 'EUR')}")

    print(f"\n--- Passo 1: Valore 'Come se Quotata' ---")
    print(f"  EV/EBITDA settore mediano:   {ev_ebitda_settore:.1f}x")
    print(f"  Enterprise Value:            {formatta_milioni(enterprise_value, 'EUR')}")
    print(f"  Equity Value:                {formatta_milioni(equity_value_quotata, 'EUR')}")

    # --- Passo 2: Sconto di Illiquidita' ---
    risultato_sconto = calcola_sconto_illiquidita(
        ricavi=ricavi,
        margine_ebitda=margine_ebitda,
        tipo_investitore="finanziario",
        ha_distribuzione_utili=True,
        restrizioni_vendita=True,
    )

    print(f"\n--- Passo 2: Sconto di Illiquidita' (Damodaran) ---")
    print(f"  Ricavi in milioni:           {risultato_sconto['ricavi_milioni']:.1f}M")
    print(f"  Margine EBITDA:              {formatta_percentuale(risultato_sconto['margine_ebitda'])}")
    print(f"  Sconto Base:                 {formatta_percentuale(risultato_sconto['sconto_base'])}")
    if risultato_sconto["aggiustamenti"]:
        print(f"  Aggiustamenti:")
        for nome_agg, val_agg in risultato_sconto["aggiustamenti"].items():
            print(f"    {nome_agg:30s} {val_agg:+.2%}")
    print(f"  Sconto Finale:               {formatta_percentuale(risultato_sconto['sconto'])}")

    if risultato_sconto["note"]:
        for nota in risultato_sconto["note"]:
            print(f"  Nota: {nota}")

    # --- Confronto con sconto per dimensione ---
    sconto_dim = sconto_per_dimensione(ricavi)
    print(f"\n  Benchmark per dimensione:    {formatta_percentuale(sconto_dim)}")

    # --- Confronto con studi restricted stock ---
    sconto_rs = sconto_restricted_stock(ricavi, profittevole=True, block_size_pct=0.15)
    print(f"  Benchmark restricted stock:  {formatta_percentuale(sconto_rs)}")

    # --- Passo 3: Premio di Controllo ---
    risultato_premio = calcola_premio_controllo(
        valore_status_quo=equity_value_quotata,
        tipo_controllo="maggioranza",
        settore="Industrial",
        qualita_management="media",
    )

    print(f"\n--- Passo 3: Premio di Controllo ---")
    print(f"  Tipo Partecipazione:         Maggioranza")
    print(f"  Qualita' Management:         Media")
    print(f"  Premio di Controllo:         {formatta_percentuale(risultato_premio['premio'])}")
    if risultato_premio["note"]:
        for nota in risultato_premio["note"]:
            print(f"  Nota: {nota}")

    # --- Benchmark settoriale ---
    bench = premio_da_transazioni("Industrial")
    print(f"\n  Benchmark Settore ({bench['settore_utilizzato']}):")
    print(f"    Premio Medio:              {formatta_percentuale(bench['premio_medio'])}")
    print(f"    Premio Mediano:            {formatta_percentuale(bench['premio_mediano'])}")
    print(f"    Range:                     {formatta_percentuale(bench['range'][0])} - {formatta_percentuale(bench['range'][1])}")

    # --- Sconto di Minoranza (per riferimento) ---
    sm = sconto_minoranza(risultato_premio["premio"])
    print(f"\n  Sconto Minoranza Equivalente: {formatta_percentuale(sm)}")

    # --- Passo 4: Valutazione Privata Completa ---
    val_privata = valutazione_privata_completa(
        valore_quotata=equity_value_quotata,
        ricavi=ricavi,
        margine_ebitda=margine_ebitda,
        tipo_partecipazione="maggioranza",
        qualita_management="media",
    )

    print(f"\n--- Passo 4: Riepilogo Valutazione Privata ---")
    print(f"  Valore 'Come se Quotata':      {formatta_milioni(val_privata['valore_quotata'], 'EUR')}")
    print(f"  + Premio Controllo ({formatta_percentuale(val_privata['premio_controllo_pct'])}):  {formatta_milioni(val_privata['valore_quotata'] * val_privata['premio_controllo_pct'], 'EUR')}")
    print(f"  = Valore Dopo Controllo:       {formatta_milioni(val_privata['valore_dopo_controllo'], 'EUR')}")
    print(f"  - Sconto Illiquidita' ({formatta_percentuale(val_privata['sconto_illiquidita_pct'])}): {formatta_milioni(val_privata['valore_dopo_controllo'] * val_privata['sconto_illiquidita_pct'], 'EUR')}")
    print(f"  ═══════════════════════════════════════════════")
    print(f"  = Valore Finale Partecipazione: {formatta_milioni(val_privata['valore_finale'], 'EUR')}")

    # --- Impatto percentuale complessivo ---
    impatto_totale = (val_privata["valore_finale"] - equity_value_quotata) / equity_value_quotata
    print(f"\n  Impatto Netto sul Valore:    {impatto_totale:+.1%}")
    print(f"  (Premio Controllo parzialmente compensato dallo Sconto Illiquidita')")

    # --- Confronto maggioranza vs minoranza ---
    val_minoranza = valutazione_privata_completa(
        valore_quotata=equity_value_quotata,
        ricavi=ricavi,
        margine_ebitda=margine_ebitda,
        tipo_partecipazione="minoranza",
        qualita_management="media",
    )

    print(f"\n--- Confronto Maggioranza vs Minoranza ---")
    print(f"  {'':30s} {'Maggioranza':>14s} {'Minoranza':>14s}")
    print(f"  {'─' * 30} {'─' * 14} {'─' * 14}")
    print(f"  {'Premio Controllo':30s} {formatta_percentuale(val_privata['premio_controllo_pct']):>14s} {formatta_percentuale(val_minoranza['premio_controllo_pct']):>14s}")
    print(f"  {'Sconto Illiquidita':30s} {formatta_percentuale(val_privata['sconto_illiquidita_pct']):>14s} {formatta_percentuale(val_minoranza['sconto_illiquidita_pct']):>14s}")
    print(f"  {'Valore Finale':30s} {formatta_milioni(val_privata['valore_finale'], 'EUR'):>14s} {formatta_milioni(val_minoranza['valore_finale'], 'EUR'):>14s}")

    print("\n" + "=" * 70)
    print("Demo 05 completata!")
    print("=" * 70)


if __name__ == "__main__":
    main()
