# Metodologia - Valuation Analyst

## Fonte: Aswath Damodaran (NYU Stern)

Tutte le metodologie implementate seguono l'approccio di Aswath Damodaran,
professore di Corporate Finance alla NYU Stern School of Business.

Riferimento principale: "Investment Valuation" (3rd Edition, Wiley)
Dataset: [https://pages.stern.nyu.edu/~adamodar/](https://pages.stern.nyu.edu/~adamodar/)

## 1. Discounted Cash Flow (DCF)

### FCFF - Free Cash Flow to Firm

```text
FCFF = EBIT * (1 - t) + Deprezzamento - CapEx - Delta Working Capital
```

**Quando usare FCFF**:

- Struttura capitale non stabile
- Aziende con leverage significativo
- Quando si vuole il valore della firm

**Tasso di sconto**: WACC

**Nota**: Il sistema gestisce anche FCFF negativi per aziende in perdita.
Il DCF proietta la convergenza verso la profittabilita' secondo le
assunzioni dell'analista nel config JSON.

### FCFE - Free Cash Flow to Equity

```text
FCFE = Utile Netto + Deprezzamento - CapEx - Delta WC - Rimborso Debito Netto
```

**Quando usare FCFE**:

- Struttura capitale stabile
- Aziende finanziarie (banche, assicurazioni)
- Quando si vuole direttamente il valore equity

**Tasso di sconto**: Costo Equity (Re)

### Modello Multi-Stage

**3 Fasi** (preferito):

1. **Alta crescita** (5 anni): basata su fondamentali attuali
2. **Transizione** (5 anni): convergenza lineare verso stabile
3. **Stabile** (perpetuita'): g <= crescita economia

**Crescita fondamentale**: g = Reinvestment Rate x ROIC

### Terminal Value

```text
TV = FCF_(n+1) / (r - g) = FCF_n * (1 + g) / (r - g)
```

Il TV non dovrebbe superare il 75-80% del valore totale.

## 2. Costo del Capitale

### CAPM

```text
Re = Rf + Beta * ERP + CRP
```

### WACC

```text
WACC = (E/V) * Re + (D/V) * Rd * (1 - t)
```

### Beta Bottom-Up

1. Beta unlevered settore (da Damodaran)
2. Relever per D/E target: Beta_L = Beta_U * (1 + (1-t) * D/E)

## 3. Valutazione Relativa

### Multipli Principali

- **P/E**: Prezzo / Utile per Azione
- **EV/EBITDA**: Enterprise Value / EBITDA
- **P/B**: Prezzo / Valore Contabile
- **EV/Sales**: Enterprise Value / Ricavi

### Processo

1. Seleziona 5-10 comparabili (definiti nel config JSON)
2. Calcola multipli per ciascuno
3. Usa la mediana (robusta a outlier)
4. Applica al target per derivare il valore

**Nota**: Per aziende in perdita, P/E e EV/EBITDA vengono automaticamente
segnalati come N/A. Il sistema usa EV/Sales e P/B come alternativa.

## 4. Option Pricing (Black-Scholes)

### Equity come Call Option

```text
E = V * N(d1) - K * e^(-rT) * N(d2)
```

**Quando usare**:

- Alto leverage (D/E > 2)
- Distress finanziario
- Utili negativi

## 5. Valutazione Societa' Private

### Sconto Illiquidita'

```text
Sconto = f(Ricavi, Margine EBITDA, Tipo Investitore)
```

Range tipico: 10-40%

### Premio di Controllo

```text
Premio = (Valore Ottimale - Valore Status Quo) / Valore Status Quo
```

Range tipico: 10-40%

## 6. M&A e Sinergie

### Valore Acquisizione

```text
V_acquisizione = V_standalone + V_sinergie - Costi_integrazione
```

### Tipi di Sinergie

- **Costo** (piu' prevedibili): 3-7% dei costi combinati
- **Ricavo** (meno prevedibili): 1-3% dei ricavi
- **Finanziarie**: tax shields, capacita' debito

## 7. Risk Analysis

### Sensitivity 2D

Coppia primaria: WACC vs Terminal Growth Rate
Coppia secondaria: Crescita Ricavi vs Margine Operativo

### Scenari

Best (20%) / Base (55%) / Worst (25%)
Valore atteso = media ponderata

### Monte Carlo

- 10.000 simulazioni (default)
- Distribuzioni: normale, triangolare, uniforme
- Output: media, mediana, percentili, intervalli di confidenza

## 8. Sintesi Multi-Metodo

Il report finale pondera i risultati di tutti i metodi:

| Metodo | Peso |
| --- | --- |
| DCF FCFF (3-stage) | 40% |
| Valutazione Relativa | 25% |
| Monte Carlo (mediana) | 20% |
| Valore Atteso Scenari | 15% |

La raccomandazione e' basata sull'upside/downside del valore ponderato:

| Upside | Raccomandazione |
| --- | --- |
| > +15% | BUY |
| +5% a +15% | MODERATE BUY |
| -5% a +5% | HOLD |
| -15% a -5% | MODERATE SELL |
| -30% a -15% | SELL |
| < -30% | STRONG SELL |
