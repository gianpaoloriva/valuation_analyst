# Riferimento Metodologico: M&A Valuation (Damodaran)

## Valore di Acquisizione

### Formula Fondamentale
```
Valore Acquisizione = Valore Standalone Target + Valore Sinergie - Costi Integrazione
```

### Prezzo Massimo
```
Prezzo Max = Valore Acquisizione
```
Oltre questo prezzo, l'acquisizione distrugge valore per l'acquirente.

## Sinergie Operative

### Sinergie di Costo (piu' prevedibili)
- Eliminazione duplicati (sede, IT, admin)
- Economie di scala (procurement, produzione)
- Range tipico: 3-7% dei costi combinati

### Sinergie di Ricavo (meno prevedibili)
- Cross-selling prodotti
- Accesso a nuovi mercati/canali
- Range tipico: 1-3% dei ricavi combinati

### Valutazione
```
PV(Sinergie) = Σ [Sinergia_annua_t / (1 + WACC)^t]
```

Considerare:
- **Tempo di realizzazione**: Tipicamente 2-3 anni per pieno regime
- **Probabilita'**: Non tutte le sinergie si realizzano (50-70% tipico)
- **Costi di integrazione**: One-time costs per realizzare le sinergie

## Sinergie Finanziarie

### Tax Benefits
- Utilizzo perdite fiscali del target
- Aumento capacita' di debito (interest tax shield)

### Diversificazione
- Riduzione volatilita' cash flow combinati
- Potenziale riduzione costo del debito

### Formula
```
Sinergia_finanziaria = Tax_savings + Riduzione_costo_debito * Debito
```

## Analisi Accretion/Dilution

### Concetto
L'acquisizione e' "accretive" se l'EPS dell'acquirente aumenta post-deal.

### Formula
```
EPS_pro_forma = (Utile_acquirente + Utile_target + Sinergie - Costi) / Azioni_totali
```

Se pagato in azioni:
```
Azioni_totali = Azioni_acquirente + Nuove_azioni_emesse
```

## Premio Offerto

### Calcolo
```
Premio = (Prezzo Offerta - Prezzo Pre-Annuncio) / Prezzo Pre-Annuncio
```

### Benchmark
- Premio medio storico M&A: 25-35%
- Range tipico: 15-50%
- Premi > 50% richiedono sinergie molto significative

## Framework Decisionale
```
Se Prezzo_offerta < Valore_standalone + Sinergie - Costi_integrazione:
    → Acquisizione crea valore per acquirente
Se Prezzo_offerta > Valore_standalone + Sinergie - Costi_integrazione:
    → Acquisizione distrugge valore (overpaying)
```
