# Riferimento Metodologico: Valutazione Societa' Private (Damodaran)

## Sconto di Illiquidita'

### Concetto
Le azioni di societa' non quotate non possono essere vendute facilmente sul mercato.
Questo sconto compensa l'investitore per la minore liquidita'.

### Metodo Damodaran
Lo sconto dipende da caratteristiche dell'azienda:

1. **Ricavi**: Aziende piu' grandi -> sconto minore
2. **Profittabilita'**: Aziende profittevoli -> sconto minore
3. **Dimensione attivo**: Asset tangibili -> sconto minore

### Range Tipici
| Caratteristica | Sconto Illiquidita' |
|---------------|-------------------|
| Grande, profittevole | 10-15% |
| Media, profittevole | 15-25% |
| Piccola, profittevole | 20-30% |
| Piccola, in perdita | 30-40% |

### Formula Approssimativa (Damodaran)
```
Sconto = 0.35 - 0.15 * ln(Ricavi in milioni) - 0.10 * (Margine EBITDA)
```
Soggetto a floor 5% e cap 50%.

## Premio di Controllo

### Concetto
Una partecipazione di maggioranza vale piu' della quota proporzionale
perche' conferisce il controllo sulle decisioni aziendali.

### Componenti del Valore di Controllo
1. Cambio management
2. Cambio politica dividendi
3. Cambio struttura capitale
4. Decisioni strategiche (M&A, disinvestimenti)

### Range Tipici
| Contesto | Premio Controllo |
|---------|-----------------|
| Azienda ben gestita | 10-15% |
| Azienda gestita sotto potenziale | 20-30% |
| Azienda con inefficienze significative | 30-50% |

### Formula (Damodaran)
```
Premio Controllo = (Valore ottimale - Valore status quo) / Valore status quo
```

## Total Beta

### Concetto
Per un investitore non diversificato (tipico di societa' private),
il rischio rilevante e' il rischio TOTALE, non solo quello sistematico.

### Formula
```
Total Beta = Beta_mercato / Correlazione_con_mercato
```

Tipicamente: Total Beta = 2-3x Beta mercato

### Impatto sul Costo Equity
```
Re_privato = Rf + Total_Beta * ERP
```
Questo e' significativamente piu' alto del costo equity per societa' quotata.

## Ordine di Applicazione Sconti/Premi
1. Partire dalla valutazione "come se quotata"
2. Applicare premio controllo (se maggioranza)
3. Applicare sconto illiquidita'

```
Valore_privato = Valore_quotata * (1 + premio_controllo) * (1 - sconto_illiquidita)
```
