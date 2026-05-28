#!/usr/bin/env python3
"""Demo 06: Valutazione M&A e Sinergie.

Dimostra il calcolo di:
- Sinergie di costo, ricavo e finanziarie
- Valore di acquisizione
- Analisi accretion/dilution
- Premio dell'offerta e confronto con benchmark
"""
from valuation_analyst.tools.synergy_valuation import (
    stima_sinergie_costo,
    stima_sinergie_finanziarie,
    stima_sinergie_ricavo,
    stima_sinergie_totali,
)
from valuation_analyst.tools.acquisition_value import (
    analisi_accretion_dilution,
    calcola_valore_acquisizione,
    premio_offerta,
    valutazione_ma_completa,
)
from valuation_analyst.utils.formatting import formatta_milioni, formatta_percentuale, formatta_valuta


def main() -> None:
    print("=" * 70)
    print("DEMO 06: Analisi M&A e Sinergie")
    print("     Acquirente: TechGiant Corp  |  Target: InnoSoft Inc")
    print("=" * 70)

    # --- Dati Acquirente (Grande Tech) ---
    acq_ricavi = 200_000         # $200B di ricavi (in milioni)
    acq_costi_operativi = 150_000
    acq_utile_netto = 35_000     # $35B di utile netto
    acq_azioni = 5_000           # 5B di azioni
    acq_prezzo_azione = 150.0
    acq_market_cap = acq_azioni * acq_prezzo_azione  # $750B

    # --- Dati Target (Piccola Tech) ---
    tgt_ricavi = 8_000           # $8B di ricavi
    tgt_costi_operativi = 6_500
    tgt_utile_netto = 800        # $800M di utile netto
    tgt_azioni = 500             # 500M di azioni
    tgt_prezzo_pre = 25.0        # Prezzo pre-annuncio
    tgt_market_cap = tgt_azioni * tgt_prezzo_pre  # $12.5B
    tgt_debito = 2_000           # $2B di debito

    # --- Parametri dell'offerta ---
    prezzo_offerta = 32.0        # $32 per azione (premio del 28%)
    wacc = 0.09
    tax_rate = 0.21

    print(f"\n--- Profilo Acquirente: TechGiant Corp ---")
    print(f"  Ricavi:                      ${acq_ricavi:,.0f}M")
    print(f"  Utile Netto:                 ${acq_utile_netto:,.0f}M")
    print(f"  Market Cap:                  ${acq_market_cap:,.0f}M")
    print(f"  Azioni:                      {acq_azioni:,.0f}M")
    print(f"  Prezzo per Azione:           {formatta_valuta(acq_prezzo_azione)}")

    print(f"\n--- Profilo Target: InnoSoft Inc ---")
    print(f"  Ricavi:                      ${tgt_ricavi:,.0f}M")
    print(f"  Utile Netto:                 ${tgt_utile_netto:,.0f}M")
    print(f"  Market Cap:                  ${tgt_market_cap:,.0f}M")
    print(f"  Azioni:                      {tgt_azioni:,.0f}M")
    print(f"  Prezzo Pre-Annuncio:         {formatta_valuta(tgt_prezzo_pre)}")
    print(f"  Debito:                      ${tgt_debito:,.0f}M")

    print(f"\n--- Offerta ---")
    print(f"  Prezzo Offerta:              {formatta_valuta(prezzo_offerta)} / azione")
    print(f"  Valore Totale Offerta:       ${prezzo_offerta * tgt_azioni:,.0f}M")

    # --- Passo 1: Premio dell'Offerta ---
    ris_premio = premio_offerta(prezzo_offerta, tgt_prezzo_pre)
    print(f"\n--- Passo 1: Premio dell'Offerta ---")
    print(f"  Premio:                      {formatta_percentuale(ris_premio['premio_pct'])}")
    print(f"  {ris_premio['confronto_benchmark']}")

    # --- Passo 2: Sinergie di Costo ---
    costi_combinati = acq_costi_operativi + tgt_costi_operativi
    sin_costo = stima_sinergie_costo(
        costi_combinati=costi_combinati,
        percentuale_risparmio=0.04,      # 4% risparmi sui costi combinati
        anni_realizzazione=3,
        wacc=wacc,
        costi_integrazione=500,          # $500M costi integrazione
    )

    print(f"\n--- Passo 2: Sinergie di Costo ---")
    print(f"  Costi Combinati:             ${costi_combinati:,.0f}M")
    print(f"  Percentuale Risparmio:       {formatta_percentuale(0.04)}")
    print(f"  Risparmio Annuo (a regime):  ${sin_costo['risparmio_annuo_pieno']:,.0f}M")
    print(f"  Profilo Realizzazione:")
    for i, flusso in enumerate(sin_costo["profilo_realizzazione"], 1):
        pct = flusso / sin_costo["risparmio_annuo_pieno"] * 100
        barra = "#" * int(pct / 5)
        print(f"    Anno {i}: ${flusso:>8,.0f}M ({pct:4.0f}%) {barra}")
    print(f"  PV Sinergie Costo:           ${sin_costo['pv_sinergie']:,.0f}M")
    print(f"  Costi Integrazione:          ${sin_costo['costi_integrazione']:,.0f}M")
    print(f"  Valore Netto:                ${sin_costo['valore_netto_sinergie']:,.0f}M")

    # --- Passo 3: Sinergie di Ricavo ---
    ricavi_combinati = acq_ricavi + tgt_ricavi
    sin_ricavo = stima_sinergie_ricavo(
        ricavi_combinati=ricavi_combinati,
        percentuale_crescita=0.015,       # 1.5% crescita incrementale
        margine_incrementale=0.35,        # 35% margine sui ricavi incrementali
        anni_realizzazione=4,
        wacc=wacc,
    )

    print(f"\n--- Passo 3: Sinergie di Ricavo ---")
    print(f"  Ricavi Combinati:            ${ricavi_combinati:,.0f}M")
    print(f"  Crescita Incrementale:       {formatta_percentuale(0.015)}")
    print(f"  Margine Incrementale:        {formatta_percentuale(0.35)}")
    print(f"  Ricavi Incrementali (pieno): ${sin_ricavo['ricavi_incrementali_pieno']:,.0f}M")
    print(f"  CF Incrementale (pieno):     ${sin_ricavo['cf_incrementale']:,.0f}M")
    print(f"  PV Sinergie Ricavo:          ${sin_ricavo['pv_sinergie']:,.0f}M")

    # --- Passo 4: Sinergie Finanziarie ---
    sin_fin = stima_sinergie_finanziarie(
        debito_target=tgt_debito,
        risparmio_spread=0.008,           # 80 bps di risparmio sullo spread
        tax_rate=tax_rate,
        perdite_fiscali_target=500,       # $500M di NOL
        additional_debt_capacity=3_000,   # $3B di capacita' debito aggiuntiva
        costo_debito_acquirente=0.045,
        wacc=wacc,
    )

    print(f"\n--- Passo 4: Sinergie Finanziarie ---")
    print(f"  PV Risparmio Interessi:      ${sin_fin['pv_risparmio_interessi']:,.0f}M")
    print(f"  PV Tax Shields (NOL):        ${sin_fin['pv_tax_shields_nol']:,.0f}M")
    print(f"  PV Debt Capacity:            ${sin_fin['pv_debt_capacity']:,.0f}M")
    print(f"  Totale Finanziarie:          ${sin_fin['totale']:,.0f}M")

    # --- Passo 5: Riepilogo Sinergie Totali ---
    sin_totali = stima_sinergie_totali(
        costi_combinati=costi_combinati,
        ricavi_combinati=ricavi_combinati,
        debito_target=tgt_debito,
        pct_risparmio_costi=0.04,
        pct_crescita_ricavi=0.015,
        margine_incrementale=0.35,
        wacc=wacc,
        costi_integrazione=500,
        tax_rate=tax_rate,
        probabilita_realizzazione=0.65,
    )

    print(f"\n--- Passo 5: Riepilogo Sinergie ---")
    print(f"  {'Componente':<30s} {'PV ($M)':>12s} {'%':>8s}")
    print(f"  {'─' * 30} {'─' * 12} {'─' * 8}")
    totale_lordo = sin_totali["totale_lordo"]
    pv_costo = sin_totali["sinergie_costo"]["pv_sinergie"]
    pv_ricavo = sin_totali["sinergie_ricavo"]["pv_sinergie"]
    pv_fin = sin_totali["sinergie_finanziarie"]["totale"]
    print(f"  {'Sinergie di Costo':<30s} ${pv_costo:>10,.0f}  {pv_costo / totale_lordo:>7.1%}")
    print(f"  {'Sinergie di Ricavo':<30s} ${pv_ricavo:>10,.0f}  {pv_ricavo / totale_lordo:>7.1%}")
    print(f"  {'Sinergie Finanziarie':<30s} ${pv_fin:>10,.0f}  {pv_fin / totale_lordo:>7.1%}")
    print(f"  {'─' * 30} {'─' * 12}")
    print(f"  {'Totale Lordo':<30s} ${totale_lordo:>10,.0f}")
    print(f"  {'- Costi Integrazione':<30s} ${500:>10,.0f}")
    print(f"  {'= Totale Netto':<30s} ${sin_totali['totale_netto']:>10,.0f}")
    print(f"  {'x Prob. Realizzazione (65%)':<30s}")
    print(f"  {'= Totale Aggiustato':<30s} ${sin_totali['totale_aggiustato_probabilita']:>10,.0f}")

    # --- Passo 6: Valore di Acquisizione ---
    val_acq = calcola_valore_acquisizione(
        valore_standalone_target=tgt_market_cap,
        valore_sinergie=sin_totali["totale_aggiustato_probabilita"],
        costi_integrazione=0,  # Gia' inclusi nel calcolo sinergie
    )

    valore_offerta_totale = prezzo_offerta * tgt_azioni
    valore_creato = val_acq["valore_acquisizione"] - valore_offerta_totale

    print(f"\n--- Passo 6: Valore di Acquisizione ---")
    print(f"  Valore Standalone Target:    ${val_acq['valore_standalone']:,.0f}M")
    print(f"  + Sinergie (aggiustate):     ${val_acq['sinergie']:,.0f}M")
    print(f"  = Max Prezzo Giustificabile: ${val_acq['valore_acquisizione']:,.0f}M")
    print(f"  Prezzo Pagato (offerta):     ${valore_offerta_totale:,.0f}M")
    print(f"  Valore Creato/Distrutto:     ${valore_creato:>+,.0f}M")

    prezzo_max_per_azione = val_acq["valore_acquisizione"] / tgt_azioni
    print(f"\n  Prezzo Max per Azione:       {formatta_valuta(prezzo_max_per_azione)}")
    print(f"  Prezzo Offerta:              {formatta_valuta(prezzo_offerta)}")
    if prezzo_offerta <= prezzo_max_per_azione:
        print(f"  --> L'offerta e' SOTTO il prezzo massimo: deal crea valore")
    else:
        print(f"  --> L'offerta e' SOPRA il prezzo massimo: rischio overpaying")

    # --- Passo 7: Accretion/Dilution ---
    ris_ad = analisi_accretion_dilution(
        utile_acquirente=acq_utile_netto,
        utile_target=tgt_utile_netto,
        azioni_acquirente=acq_azioni,
        prezzo_offerta=prezzo_offerta,
        azioni_target=tgt_azioni,
        sinergie_annue=sin_totali["totale_aggiustato_probabilita"] * wacc,
        struttura_deal="cash",
    )

    print(f"\n--- Passo 7: Analisi Accretion/Dilution (Cash Deal) ---")
    print(f"  EPS Pre-Acquisizione:        {formatta_valuta(ris_ad['eps_pre'])}")
    print(f"  EPS Post-Acquisizione:       {formatta_valuta(ris_ad['eps_post'])}")
    print(f"  Variazione EPS:              {ris_ad['accretion_dilution_pct']:+.2%}")
    status = "ACCRETIVE" if ris_ad["is_accretive"] else "DILUTIVE"
    print(f"  Risultato:                   {status}")

    print("\n" + "=" * 70)
    print("Demo 06 completata!")
    print("=" * 70)


if __name__ == "__main__":
    main()
