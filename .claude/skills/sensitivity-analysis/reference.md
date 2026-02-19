# Riferimento Metodologico: Risk & Sensitivity Analysis

## Analisi di Sensitivita' 2D

### Concetto
Varia due parametri chiave simultaneamente per creare una matrice di valori risultanti.

### Parametri Tipici
- **WACC** vs **Terminal Growth Rate** (coppia piu' comune)
- **Crescita ricavi** vs **Margine operativo**
- **P/E** vs **Crescita EPS**
- **Beta** vs **ERP**

### Formato Output
```
             Growth 1.5%  2.0%  2.5%  3.0%  3.5%
WACC  8.0%    $210     $225   $245   $270   $305
      8.5%    $195     $208   $225   $248   $278
      9.0%    $182     $193   $208   $228   $255
      9.5%    $170     $180   $193   $210   $233
     10.0%    $160     $168   $180   $195   $215
```

### Implementazione
Per ogni combinazione (r_i, g_j), ricalcola il modello DCF completo.

## Analisi per Scenari

### Definizione Scenari
| Scenario | Probabilita' | Descrizione |
|---------|-------------|-------------|
| **Best** | 15-25% | Crescita superiore alle attese, margini in espansione |
| **Base** | 50-60% | In linea con le stime degli analisti |
| **Worst** | 15-25% | Rallentamento, compressione margini |

### Parametri per Scenario
Per ogni scenario, specificare:
- Tasso crescita ricavi
- Margine operativo target
- WACC (puo' cambiare per rischio)
- Terminal growth rate
- Multiplo uscita (se usato)

### Valore Atteso
```
E[V] = Σ P(scenario_i) * V(scenario_i)
```

## Simulazione Monte Carlo

### Principio
Assegna distribuzioni di probabilita' ai parametri incerti,
poi simula migliaia di scenari casuali per ottenere una distribuzione del valore.

### Distribuzioni Tipiche per Parametro
| Parametro | Distribuzione | Parametri |
|-----------|--------------|-----------|
| Crescita ricavi | Normale | mu=g_base, sigma=2-3% |
| Margine operativo | Normale | mu=m_base, sigma=1-2% |
| WACC | Triangolare | (min, mode, max) |
| Terminal growth | Uniforme | [1.5%, 3.5%] |
| Tax rate | Triangolare | (20%, 25%, 30%) |

### Correlazioni
Parametri spesso correlati:
- Crescita ricavi e margine: correlazione negativa (crescita costa)
- WACC e terminal growth: poca correlazione diretta
- Margine e tax rate: poca correlazione

### Numero Iterazioni
- Minimo: 10,000
- Raccomandato: 50,000-100,000
- Verificare convergenza della media

### Output Statistiche
| Statistica | Valore |
|-----------|--------|
| Media | $XX.XX |
| Mediana | $XX.XX |
| Dev. Standard | $XX.XX |
| 5° Percentile | $XX.XX |
| 25° Percentile | $XX.XX |
| 75° Percentile | $XX.XX |
| 95° Percentile | $XX.XX |

### Intervallo di Confidenza
```
IC 90% = [P5, P95]
IC 50% = [P25, P75]
```

## Best Practice
1. Esegui SEMPRE sensitivity su WACC e terminal growth
2. Per Monte Carlo, documenta tutte le distribuzioni assunte
3. Le correlazioni tra parametri possono avere impatto significativo
4. Usa il risultato per comunicare un RANGE, non un valore puntuale
5. Il valore puntuale dal DCF base deve cadere entro il range ragionevole
