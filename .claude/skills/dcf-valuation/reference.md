# Riferimento Metodologico: DCF Valuation (Damodaran)

## FCFF - Free Cash Flow to Firm

### Formula
```
FCFF = EBIT * (1 - t) + Deprezzamento - CapEx - Delta Working Capital
```

Equivalentemente:
```
FCFF = EBIT * (1 - t) - Reinvestimento Netto
```

Dove Reinvestimento Netto = CapEx - Deprezzamento + Delta WC

### Valore Firm (Enterprise Value)
```
V_firm = Σ [FCFF_t / (1 + WACC)^t] + TV / (1 + WACC)^n
```

### Valore Equity
```
V_equity = V_firm - Debito Netto
V_per_azione = V_equity / Azioni Outstanding
```

## FCFE - Free Cash Flow to Equity

### Formula
```
FCFE = Utile Netto + Deprezzamento - CapEx - Delta WC - Rimborso Debito Netto
```

O partendo da FCFF:
```
FCFE = FCFF - Interessi * (1 - t) + Nuovo Debito Netto
```

### Valore Equity (diretto)
```
V_equity = Σ [FCFE_t / (1 + Re)^t] + TV_equity / (1 + Re)^n
```

Nota: FCFE si sconta al costo equity (Re), NON al WACC.

## Terminal Value

### Metodo Gordon Growth (perpetuita')
```
TV = FCFF_{n+1} / (WACC - g)
   = FCFF_n * (1 + g) / (WACC - g)
```

Vincoli:
- g < WACC (altrimenti TV infinito)
- g <= crescita nominale economia (tipicamente 2-3%)
- Il reinvestment rate deve essere coerente: g = RIR * ROIC

### Metodo Exit Multiple
```
TV = EBITDA_n * Multiplo_uscita
```

Il multiplo uscita dovrebbe riflettere un'azienda stabile (tipicamente multiplo settore maturo).

## Modelli di Crescita Multi-Fase

### Modello 2 Fasi
1. **Fase alta** (5-10 anni): crescita superiore al mercato
2. **Fase stabile** (perpetuita'): crescita = economia

### Modello 3 Fasi (preferito)
1. **Fase alta** (5 anni): crescita basata su fondamentali attuali
2. **Fase transizione** (5 anni): convergenza lineare da alta a stabile
3. **Fase stabile** (perpetuita'): crescita = risk-free rate reale + inflazione

### Stima Crescita
- **Crescita fondamentale**: g = Reinvestment Rate * ROIC
- **Crescita storica**: CAGR ricavi ultimi 3-5 anni
- **Consenso analisti**: Crescita attesa prossimi 3-5 anni
- La crescita stabile NON deve superare la crescita nominale del GDP

## Reinvestment Rate
```
Reinvestment Rate = (CapEx - Depr + Delta WC) / EBIT(1-t)
```

In fase stabile:
```
RIR_stabile = g_stabile / ROIC_stabile
```

## Check di Coerenza
1. ROIC in fase stabile dovrebbe convergere verso WACC
2. Reinvestment Rate dovrebbe essere coerente con crescita
3. Margini in fase stabile dovrebbero essere sostenibili
4. Terminal Value non dovrebbe essere >75% del valore totale (se lo e', rivedere le assunzioni)

## Fonti Dati
- Bilanci e cash flow storici: Massive.com API
- WACC: Modulo cost-of-capital
- Crescita settore: Dataset Damodaran
- CapEx/Depr ratio settore: Dataset Damodaran `capex.xlsx`
