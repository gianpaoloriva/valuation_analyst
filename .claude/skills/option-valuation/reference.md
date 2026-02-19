# Riferimento Metodologico: Option Pricing per Equity (Damodaran)

## Concetto Chiave

L'equity di un'azienda puo' essere vista come una **call option europea**
sugli asset aziendali, con strike price uguale al valore nominale del debito.

- Se V (valore asset) > K (debito): equity ha valore positivo
- Se V < K: l'azienda e' tecnicamente insolvente, ma l'equity puo' ancora avere valore
  (per il "valore temporale" dell'opzione - la possibilita' che V superi K prima di T)

## Formula Black-Scholes per Equity

```
E = V * N(d1) - K * e^(-rT) * N(d2)
```

Dove:
```
d1 = [ln(V/K) + (r + sigma^2/2) * T] / (sigma * sqrt(T))
d2 = d1 - sigma * sqrt(T)
```

- **E** = Valore equity
- **V** = Valore totale asset (firm value)
- **K** = Valore nominale del debito
- **r** = Risk-free rate
- **T** = Scadenza media ponderata del debito (anni)
- **sigma** = Volatilita' del valore degli asset
- **N(.)** = Funzione distribuzione cumulativa normale standard

## Parametri

### Valore Asset (V)
```
V = Market Cap + Valore di mercato debito
```
Se il debito non e' quotato, approssimare con valore contabile.

### Strike Price (K)
```
K = Valore nominale totale del debito (short-term + long-term)
```
Alcuni analisti usano: K = ST Debt + 0.5 * LT Debt (per approx maturity media).

### Scadenza (T)
```
T = Maturity media ponderata del debito
```
Se non disponibile, usare 5-7 anni come approssimazione.

### Volatilita' Asset (sigma)
Piu' difficile da stimare. Approcci:

1. **Da volatilita' equity**: sigma_V = sigma_E * (E/V) / N(d1)
   (richiede soluzione iterativa perche' E dipende da sigma_V)

2. **Da volatilita' equity + leverage**:
   ```
   sigma_V ≈ sigma_E * E / (E + D)
   ```

3. **Da comparabili**: volatilita' media asset di aziende simili

### Volatilita' tipica per settore
- Technology: 30-50%
- Healthcare/Pharma: 25-40%
- Utilities: 15-25%
- Financials: 20-35%
- Aziende in distress: 40-60%+

## Output Derivati

### Valore Debito
```
D = V - E
```

### Yield to Maturity Implicito
```
YTM = -ln(D/K) / T
```

### Default Spread
```
Default Spread = YTM - Risk-free rate
```

### Probabilita' di Default
```
P(default) = N(-d2)
```

## Quando Usare Questo Approccio

### Ideale per:
- Aziende con alto leverage (D/E > 2)
- Aziende in distress finanziario (V vicino a K)
- Aziende con utili negativi (DCF impossibile)
- Settori ciclici nei punti bassi del ciclo

### NON usare per:
- Aziende con poco debito (il valore opzione e' trascurabile)
- Aziende con utili stabili e positivi (DCF e' piu' appropriato)
- Come unico metodo di valutazione (sempre come complemento)

## Limitazioni del Modello
1. Assume distribuzione lognormale del valore asset
2. Assume volatilita' costante
3. Non considera coupon intermedi del debito
4. Non considera covenant o opzioni di ristrutturazione
5. La stima della volatilita' asset e' il punto piu' debole
