# Riferimento Metodologico: Costo del Capitale (Damodaran)

## CAPM - Capital Asset Pricing Model

### Formula
```
Re = Rf + Beta * ERP + CRP
```

Dove:
- **Re** = Costo equity (rendimento richiesto dagli azionisti)
- **Rf** = Risk-free rate (Treasury 10Y nella valuta dell'azienda)
- **Beta** = Sensibilita' al rischio sistematico
- **ERP** = Equity Risk Premium (premio per rischio mercato azionario)
- **CRP** = Country Risk Premium (premio per rischio paese, se applicabile)

### Risk-Free Rate
- USA: US Treasury 10Y yield
- Europa: Bund tedesco 10Y (o equivalente nella valuta locale)
- Deve essere nella stessa valuta dei cash flow
- Fonte: Massive.com API o dati di mercato

### Equity Risk Premium (ERP)
- ERP base mercato maturo (USA): ~5.5% (stima Damodaran aggiornata)
- Fonte: Dataset Damodaran `ctryprem.xlsx`
- Aggiornato annualmente su: https://pages.stern.nyu.edu/~adamodar/

### Country Risk Premium (CRP)
- Basato su rating sovrano e default spread
- CRP = Default Spread Paese * (Sigma_equity / Sigma_bond)
- Tipicamente: CRP = Default Spread * 1.5
- Fonte: Dataset Damodaran `ctryprem.xlsx`

## Beta

### Beta Bottom-Up (metodo preferito da Damodaran)
1. **Identifica settore/industria** dell'azienda
2. **Beta unlevered settore**: Dal dataset Damodaran (media di settore)
3. **Relever per D/E target**:
   ```
   Beta_L = Beta_U * (1 + (1 - t) * D/E)
   ```

### Beta di Regressione (alternativa)
- Regressione rendimenti azione vs rendimenti mercato (5 anni, mensili)
- Meno affidabile: alto errore standard, backward-looking
- Usare solo come sanity check

### Unlevered Beta
```
Beta_U = Beta_L / (1 + (1 - t) * D/E)
```

## WACC - Weighted Average Cost of Capital

### Formula
```
WACC = (E/V) * Re + (D/V) * Rd * (1 - t)
```

Dove:
- **E/V** = Peso equity (valore mercato equity / valore totale)
- **D/V** = Peso debito (valore mercato debito / valore totale)
- **Re** = Costo equity (da CAPM)
- **Rd** = Costo debito pre-tax
- **t** = Aliquota fiscale effettiva

### Costo del Debito
- **Da rating**: Default spread + Risk-free rate
  - AAA: Rf + 0.75%
  - AA: Rf + 1.00%
  - A: Rf + 1.25%
  - BBB: Rf + 2.00%
  - BB: Rf + 3.00%
  - B: Rf + 4.00%
  - CCC: Rf + 8.00%
- **Da interest coverage**: Interest Coverage → Rating implicito → Default spread
- **Effettivo**: Interessi pagati / Debito totale

### Pesi Capitale
- Usare valori di **mercato**, non contabili
- E = Market Cap
- D = Valore di mercato del debito (approssimabile con valore contabile per investment grade)
- V = E + D

## Fonti Dati Damodaran
| Dataset | URL | Contenuto |
|---------|-----|-----------|
| Betas by Industry | Betas.xls | Beta unlevered/levered per settore |
| Country Risk Premium | ctryprem.xlsx | ERP e CRP per paese |
| WACC by Industry | wacc.xlsx | WACC e componenti per settore |
| Cost of Debt | wacc.xlsx | Costo debito per settore |

## Valori Tipici di Riferimento
- Risk-free rate (USA, 2024): ~4.2%
- ERP mercato maturo: 5.0-5.5%
- Beta settore Technology: 1.1-1.3
- Beta settore Utilities: 0.5-0.7
- Beta settore Healthcare: 0.9-1.1
- WACC tipico (USA, large cap): 8-10%
