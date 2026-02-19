#!/usr/bin/env python3
"""Demo 03: Analisi dei Comparabili per Apple Inc.

Dimostra il calcolo di:
- Costruzione del campione di comparabili con dati sample
- Statistiche descrittive per ogni multiplo (P/E, EV/EBITDA, P/BV, EV/Sales)
- Valori impliciti e valore per azione mediano
"""
from valuation_analyst.models.comparable import Comparabile
from valuation_analyst.tools.multiples import (
    statistiche_multiplo,
    valutazione_relativa,
    valore_implicito_ev_ebitda,
    valore_implicito_pe,
)
from valuation_analyst.utils.formatting import formatta_multiplo, formatta_valuta


def main() -> None:
    print("=" * 75)
    print("DEMO 03: Analisi dei Comparabili - Apple Inc. (AAPL)")
    print("=" * 75)

    # --- Dati comparabili (sample - Big Tech peers) ---
    comparabili = [
        Comparabile(
            ticker="MSFT", nome="Microsoft Corp", settore="Technology",
            market_cap=2_800_000, pe_ratio=34.5, ev_ebitda=22.8,
            pb_ratio=12.1, ev_sales=12.5, ev_ebit=27.0,
            margine_operativo=0.44, crescita_ricavi=0.16, paese="US",
        ),
        Comparabile(
            ticker="GOOGL", nome="Alphabet Inc", settore="Technology",
            market_cap=1_750_000, pe_ratio=25.2, ev_ebitda=16.4,
            pb_ratio=6.3, ev_sales=6.8, ev_ebit=20.5,
            margine_operativo=0.31, crescita_ricavi=0.12, paese="US",
        ),
        Comparabile(
            ticker="META", nome="Meta Platforms", settore="Technology",
            market_cap=900_000, pe_ratio=27.8, ev_ebitda=14.2,
            pb_ratio=7.5, ev_sales=7.2, ev_ebit=17.8,
            margine_operativo=0.35, crescita_ricavi=0.22, paese="US",
        ),
        Comparabile(
            ticker="AMZN", nome="Amazon.com Inc", settore="Technology",
            market_cap=1_550_000, pe_ratio=58.0, ev_ebitda=19.5,
            pb_ratio=8.2, ev_sales=2.8, ev_ebit=35.0,
            margine_operativo=0.08, crescita_ricavi=0.11, paese="US",
        ),
        Comparabile(
            ticker="NVDA", nome="NVIDIA Corp", settore="Technology",
            market_cap=1_200_000, pe_ratio=62.3, ev_ebitda=45.0,
            pb_ratio=38.0, ev_sales=35.0, ev_ebit=50.0,
            margine_operativo=0.55, crescita_ricavi=1.22, paese="US",
        ),
        Comparabile(
            ticker="SAMSUNG", nome="Samsung Electronics", settore="Technology",
            market_cap=350_000, pe_ratio=14.2, ev_ebitda=5.8,
            pb_ratio=1.3, ev_sales=1.5, ev_ebit=8.2,
            margine_operativo=0.15, crescita_ricavi=0.04, paese="KR",
        ),
    ]

    # --- Tabella Comparabili ---
    print(f"\n--- Campione di Comparabili ---")
    print(
        f"  {'Ticker':<10s} {'Nome':<25s} {'Cap ($M)':>12s} "
        f"{'P/E':>8s} {'EV/EBITDA':>10s} {'P/BV':>8s} {'EV/Sales':>10s}"
    )
    print(f"  {'─' * 10} {'─' * 25} {'─' * 12} {'─' * 8} {'─' * 10} {'─' * 8} {'─' * 10}")
    for c in comparabili:
        pe = formatta_multiplo(c.pe_ratio) if c.pe_ratio else "N/D"
        ev_eb = formatta_multiplo(c.ev_ebitda) if c.ev_ebitda else "N/D"
        pb = formatta_multiplo(c.pb_ratio) if c.pb_ratio else "N/D"
        ev_s = formatta_multiplo(c.ev_sales) if c.ev_sales else "N/D"
        print(
            f"  {c.ticker:<10s} {c.nome:<25s} {c.market_cap:>12,.0f} "
            f"{pe:>8s} {ev_eb:>10s} {pb:>8s} {ev_s:>10s}"
        )

    # --- Statistiche Multipli ---
    nomi_multipli = ["pe_ratio", "ev_ebitda", "pb_ratio", "ev_sales"]
    etichette = {"pe_ratio": "P/E", "ev_ebitda": "EV/EBITDA", "pb_ratio": "P/BV", "ev_sales": "EV/Sales"}

    print(f"\n--- Statistiche Multipli ---")
    print(
        f"  {'Multiplo':<12s} {'Mediana':>10s} {'Media':>10s} "
        f"{'Min':>10s} {'Max':>10s} {'Dev.Std':>10s} {'N':>4s}"
    )
    print(
        f"  {'─' * 12} {'─' * 10} {'─' * 10} {'─' * 10} {'─' * 10} {'─' * 10} {'─' * 4}"
    )

    for nome_m in nomi_multipli:
        valori = [getattr(c, nome_m) for c in comparabili if getattr(c, nome_m) is not None]
        stat = statistiche_multiplo(valori, nome_m)
        print(
            f"  {etichette[nome_m]:<12s} "
            f"{formatta_multiplo(stat.mediana):>10s} "
            f"{formatta_multiplo(stat.media):>10s} "
            f"{formatta_multiplo(stat.minimo):>10s} "
            f"{formatta_multiplo(stat.massimo):>10s} "
            f"{stat.deviazione_standard:>10.2f} "
            f"{stat.num_osservazioni:>4d}"
        )

    # --- Dati Apple (target) per il calcolo dei valori impliciti ---
    # Dati sample in milioni $
    eps_apple = 6.42
    ebitda_apple = 134_000      # EBITDA ~$134B
    bvps_apple = 4.25           # Book Value per azione
    ricavi_apple = 383_000      # Ricavi ~$383B
    debito_netto_apple = 49_000  # Debito netto $49B (111B debito - 62B cassa)
    shares_apple = 15_400       # Azioni in circolazione (milioni)
    prezzo_corrente = 182.0

    print(f"\n--- Dati Apple (Target) ---")
    print(f"  EPS:                    {formatta_valuta(eps_apple)}")
    print(f"  EBITDA:                 ${ebitda_apple:,.0f}M")
    print(f"  Book Value per Azione:  {formatta_valuta(bvps_apple)}")
    print(f"  Ricavi:                 ${ricavi_apple:,.0f}M")
    print(f"  Debito Netto:           ${debito_netto_apple:,.0f}M")
    print(f"  Azioni:                 {shares_apple:,.0f}M")

    # --- Valutazione Relativa Completa ---
    risultato = valutazione_relativa(
        ticker="AAPL",
        eps=eps_apple,
        ebitda=ebitda_apple,
        book_value_per_share=bvps_apple,
        ricavi=ricavi_apple,
        debito_netto=debito_netto_apple,
        shares_outstanding=shares_apple,
        comparabili=comparabili,
        prezzo_corrente=prezzo_corrente,
    )

    # --- Risultati per multiplo ---
    print(f"\n--- Valori Impliciti per Multiplo ---")
    print(f"  {'Multiplo':<14s} {'Mediana Peers':>14s} {'Valore/Azione':>16s}")
    print(f"  {'─' * 14} {'─' * 14} {'─' * 16}")

    for chiave, valore in risultato.dettagli.items():
        if chiave.startswith("valore_implicito_"):
            nome_mult = chiave.replace("valore_implicito_", "")
            etichetta = etichette.get(nome_mult, nome_mult.upper())
            mediana_chiave = f"mediana_{nome_mult}"
            mediana = risultato.dettagli.get(mediana_chiave, 0.0)
            if isinstance(mediana, (int, float)):
                print(
                    f"  {etichetta:<14s} "
                    f"{formatta_multiplo(mediana):>14s} "
                    f"{formatta_valuta(valore):>16s}"  # type: ignore[arg-type]
                )

    # --- Riepilogo ---
    mediana_valori = risultato.dettagli.get("valore_mediana_multipli", 0.0)
    media_valori = risultato.dettagli.get("valore_media_multipli", 0.0)

    print(f"\n--- Riepilogo Valutazione Relativa ---")
    print(f"  Mediana valori impliciti:   {formatta_valuta(mediana_valori)}")  # type: ignore[arg-type]
    print(f"  Media valori impliciti:     {formatta_valuta(media_valori)}")  # type: ignore[arg-type]
    print(f"  Valore per Azione Finale:   {formatta_valuta(risultato.valore_per_azione)}")
    print(f"  Prezzo di Mercato:          {formatta_valuta(prezzo_corrente)}")
    upside = risultato.upside_downside
    if upside is not None:
        print(f"  Upside/Downside:            {upside:+.1%}")
    print(f"  Raccomandazione:            {risultato.raccomandazione}")

    # --- Note ---
    if risultato.note:
        print(f"\n--- Note ---")
        for nota in risultato.note:
            print(f"  - {nota}")

    print("\n" + "=" * 75)
    print("Demo 03 completata!")
    print("=" * 75)


if __name__ == "__main__":
    main()
