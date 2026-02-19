# Riferimento Metodologico: Valutazione Relativa (Damodaran)

## Principio Base

Il valore di un asset puo' essere stimato guardando come il mercato prezza
asset simili (comparabili). I multipli sono il ponte tra valore e fondamentali.

## Multipli Principali

### P/E - Price to Earnings
```
P/E = Prezzo per Azione / Utile per Azione (EPS)
Valore implicito = EPS_target * P/E_mediano_comparabili
```

**Quando usarlo**: Aziende profittevoli con utili stabili.
**Limitazioni**: Influenzato da struttura capitale, voci straordinarie, politiche contabili.

**Fondamentali che guidano il P/E** (Damodaran):
```
P/E = Payout Ratio * (1 + g) / (Re - g)
```
Un P/E piu' alto e' giustificato da: maggiore crescita, minor rischio, maggior payout.

### EV/EBITDA - Enterprise Value to EBITDA
```
EV/EBITDA = Enterprise Value / EBITDA
Valore implicito EV = EBITDA_target * EV/EBITDA_mediano
Valore Equity = EV - Debito Netto
```

**Quando usarlo**: Confronti cross-border (neutralizza tassazione), aziende capital-intensive.
**Limitazioni**: Ignora CapEx di mantenimento, differenze in D&A.

### P/B - Price to Book
```
P/B = Market Cap / Book Value of Equity
Valore implicito = BV_target * P/B_mediano
```

**Quando usarlo**: Banche, assicurazioni, aziende asset-heavy.
**Fondamentale**: P/B = (ROE - g) / (Re - g). P/B > 1 se ROE > Re.

### EV/Sales - Enterprise Value to Sales
```
EV/Sales = Enterprise Value / Ricavi
```

**Quando usarlo**: Aziende in perdita, startup, confronti tra aziende con margini diversi.
**Limitazione**: Ignora completamente la profittabilita'.

### PEG Ratio
```
PEG = P/E / Crescita attesa EPS (%)
```

PEG < 1 suggerisce sottovalutazione relativa alla crescita.

## Selezione Comparabili

### Criteri (in ordine di priorita')
1. **Stesso settore/industria**: Business model simile
2. **Dimensione**: Market cap comparabile (stessa fascia)
3. **Crescita**: Tasso crescita ricavi simile
4. **Profittabilita'**: Margini operativi simili
5. **Rischio**: Beta e leverage simili
6. **Geografia**: Stesso mercato principale

### Numero Minimo
- Ideale: 7-10 comparabili
- Minimo accettabile: 5
- Con meno di 5, i risultati sono poco affidabili

### Pulizia Dati
- Rimuovi outlier (>3 deviazioni standard dalla mediana)
- Escludi aziende con utili negativi dal P/E
- Normalizza per voci straordinarie se possibile

## Statistiche di Riferimento

### Quale Statistica Usare
- **Mediana**: Preferita (robusta a outlier)
- **Media**: Solo se distribuzione simmetrica
- **Media armonica**: Per P/E (gestisce meglio valori estremi)

### Range di Valutazione
- **Range stretto**: 25°-75° percentile dei comparabili
- **Range largo**: Min-Max (esclusi outlier)

## Aggiustamenti

### Per Differenze di Crescita
Se il target cresce piu' dei comparabili, merita un multiplo piu' alto:
```
Multiplo_aggiustato = Multiplo_mediano * (1 + g_target) / (1 + g_mediano)
```

### Per Differenze di Rischio
Se il target e' piu' rischioso (beta piu' alto):
```
Multiplo_aggiustato = Multiplo_mediano * Re_mediano / Re_target
```

## Fonti Dati Damodaran per Multipli Settoriali
| Dataset | Contenuto |
|---------|-----------|
| pedata.xlsx | P/E per settore |
| vebitda.xlsx | EV/EBITDA per settore |
| pbvdata.xlsx | P/B per settore |
| psdata.xlsx | Price/Sales per settore |
