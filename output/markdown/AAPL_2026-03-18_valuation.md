# Report di Valutazione - Apple Inc. (AAPL)
**Data:** 2026-03-18
**Analista:** Valuation Analyst Multi-Agent System
**Metodologia:** Damodaran (NYU Stern)

---

## 1. Executive Summary

| Metrica | Valore |
|---------|--------|
| **Valore Intrinseco Stimato** | **$120.68** |
| Prezzo Corrente | $254.23 |
| Upside/Downside | -52.5% |
| Raccomandazione | **STRONG SELL** |
| IC 90% Monte Carlo | $79.37 - $161.18 |
| WACC | 10.88% |

> Il titolo appare fortemente sopravvalutato rispetto ai fondamentali.

## 2. Panoramica Aziendale

| Indicatore             | Valore               |
| :--------------------- | :------------------- |
| Ticker                 | AAPL                 |
| Settore                | ELECTRONIC COMPUTERS |
| Paese                  | US                   |
| Prezzo Corrente        | $254.23              |
| Market Cap             | $3,711.69B           |
| Enterprise Value       | $3,743.32B           |
| Azioni in Circolazione | 14,681M              |
| Ricavi (TTM)           | $391.04B             |
| EBITDA (TTM)           | $134.66B             |
| EBIT (TTM)             | $123.22B             |
| Utile Netto (TTM)      | $93.74B              |
| EPS                    | $6.38                |
| Book Value/Share       | $3.88                |
| Debito Totale          | $96.80B              |
| Cassa e Investimenti   | $65.17B              |
| Debito Netto           | $31.63B              |
| Rating                 | AA+                  |
| Beta                   | 1.24                 |

## 3. Costo del Capitale (WACC)

### 2.1 Costo dell'Equity (CAPM)

**Formula CAPM:** `Re = Rf + Beta * ERP + CRP`

| Componente                              | Valore     |
| :-------------------------------------- | :--------- |
| Risk-Free Rate (US 10Y)                 | 4.23%      |
| Beta Levered                            | 1.24       |
| Beta Unlevered                          | 1.213      |
| Equity Risk Premium                     | 5.50%      |
| Premio Rischio Sistematico (Beta x ERP) | 6.82%      |
| Country Risk Premium                    | 0.00%      |
| **Costo Equity (Re)**                   | **11.05%** |

### 2.2 Costo del Debito

| Componente                | Valore    |
| :------------------------ | :-------- |
| Rating Creditizio         | AA+       |
| Default Spread            | 0.85%     |
| Costo Debito Pre-Tax (Kd) | 5.08%     |
| Tax Rate Effettivo        | 16.20%    |
| **Costo Debito Post-Tax** | **4.26%** |

### 2.3 WACC

**Formula:** `WACC = (E/V) * Re + (D/V) * Rd * (1-t)`

| Componente            | Valore     |
| :-------------------- | :--------- |
| Peso Equity (E/V)     | 97.46%     |
| Peso Debito (D/V)     | 2.54%      |
| Costo Equity (Re)     | 11.05%     |
| Costo Debito Post-Tax | 4.26%      |
| **WACC**              | **10.88%** |

## 4. Valutazione DCF (FCFF)

### 3.1 FCFF Base

**Formula:** `FCFF = EBIT*(1-t) + Deprezzamento - CapEx - Delta WC`

| Componente      | Valore (M USD) |
| :-------------- | :------------- |
| EBIT            | 123,216.00     |
| EBIT * (1-t)    | 103,255.01     |
| + Deprezzamento | 11,445.00      |
| - CapEx         | 9,959.00       |
| - Delta WC      | 4,100.00       |
| **FCFF Base**   | **100,641.01** |

### 3.2 Proiezione Multi-Stage (3 fasi)

- **Fase 1 (Alta crescita):** 8% per 5 anni
- **Fase 2 (Transizione):** convergenza lineare per 5 anni
- **Fase 3 (Stabile):** 2.5% in perpetuita'
- **Tasso di sconto (WACC):** 10.88%

| Anno | Tasso Crescita | FCFF (M)   | Valore Attuale (M) |
| :--- | :------------- | :--------- | :----------------- |
| 1    | 8.00%          | 108,692.29 | 98,029.31          |
| 2    | 8.00%          | 117,387.67 | 95,485.38          |
| 3    | 8.00%          | 126,778.69 | 93,007.47          |
| 4    | 8.00%          | 136,920.98 | 90,593.87          |
| 5    | 8.00%          | 147,874.66 | 88,242.90          |
| 6    | 6.90%          | 158,078.01 | 85,077.49          |
| 7    | 5.80%          | 167,246.53 | 81,181.59          |
| 8    | 4.70%          | 175,107.12 | 76,658.69          |
| 9    | 3.60%          | 181,410.98 | 71,627.26          |
| 10   | 2.50%          | 185,946.25 | 66,215.46          |

### 3.3 Riepilogo Valutazione DCF

| Componente                   | Valore         |
| :--------------------------- | :------------- |
| VA Flussi di Cassa Espliciti | $846.12B       |
| Terminal Value (nominale)    | $2,275.12B     |
| VA Terminal Value            | $810.17B       |
| TV come % del Totale         | 0.49%          |
| **Enterprise Value**         | **$1,656.29B** |
| - Debito Netto               | $31.63B        |
| **Equity Value**             | **$1,624.66B** |
| Azioni in Circolazione       | 14,681M        |
| **Valore per Azione (DCF)**  | **$110.66**    |
| Prezzo Corrente              | $254.23        |
| **Upside/Downside**          | **-56.5%**     |

## 5. Valutazione Relativa (Multipli)

### 4.1 Campione Comparabili

| Ticker   | Nome                   | Market Cap (B) | P/E      | EV/EBITDA | P/B      | EV/Sales |
| :------- | :--------------------- | :------------- | :------- | :-------- | :------- | :------- |
| MSFT     | Microsoft Corporation  | $3,083B        | 31.7     | 22.7      | 11.5     | 11.7     |
| GOOGL    | Alphabet Inc.          | $2,150B        | 24.0     | 17.5      | 7.8      | 7.2      |
| AMZN     | Amazon.com Inc.        | $2,300B        | 42.0     | 18.5      | 9.5      | 4.0      |
| META     | Meta Platforms Inc.    | $1,600B        | 27.5     | 16.0      | 9.0      | 11.5     |
| SAMSUNG  | Samsung Electronics    | $350B          | 15.0     | 5.5       | 1.3      | 1.5      |
| SONY     | Sony Group Corporation | $130B          | 18.0     | 9.5       | 2.8      | 1.5      |
| **AAPL** | **Apple Inc.**         | **$3,712B**    | **39.8** | **27.8**  | **65.5** | **9.6**  |

### 4.2 Statistiche Multipli Comparabili

**P/E:** Media=26.4, Mediana=25.8, Min=15.0, Max=42.0 (n=6)
**EV/EBITDA:** Media=14.9, Mediana=16.8, Min=5.5, Max=22.7 (n=6)
**P/B:** Media=7.0, Mediana=8.4, Min=1.3, Max=11.5 (n=6)
**EV/Sales:** Media=6.2, Mediana=5.6, Min=1.5, Max=11.7 (n=6)

### 4.3 Valori Impliciti

| Multiplo  | Valore Implicito/Azione |
| :-------- | :---------------------- |
| PE/RATIO  | $164.41                 |
| EV/EBITDA | $151.48                 |
| PB/RATIO  | $32.58                  |
| EV/SALES  | $147.00                 |
| EV/EBIT   | $150.11                 |

**Valore Mediano Multipli:** $150.11
**Upside/Downside:** -41.0%

## 6. Analisi di Sensitivita'

### 5.1 WACC vs Tasso di Crescita Terminale

Valore per azione al variare di WACC e crescita terminale:

| WACC \ Terminal Growth | 1.5%    | 2.0%    | 2.5%    | 3.0%    | 3.5%    |
| :--------------------- | :------ | :------ | :------ | :------ | :------ |
| 7.0%                   | $160.11 | $174.12 | $191.22 | $212.57 | $239.99 |
| 8.0%                   | $134.43 | $144.02 | $155.34 | $168.89 | $185.45 |
| 8.5%                   | $124.36 | $132.46 | $141.89 | $153.02 | $166.37 |
| 9.0%                   | $115.63 | $122.55 | $130.52 | $139.81 | $150.76 |
| 9.5%                   | $108.00 | $113.97 | $120.78 | $128.63 | $137.77 |
| 10.0%                  | $101.28 | $106.47 | $112.35 | $119.05 | $126.78 |
| 11.0%                  | $89.97  | $93.99  | $98.47  | $103.51 | $109.20 |

### 5.2 Crescita Ricavi vs Margine Operativo

| Crescita Ricavi \ Margine Operativo | 28.0%   | 30.0%   | 33.0%   | 35.0%   | 38.0%   |
| :---------------------------------- | :------ | :------ | :------ | :------ | :------ |
| 3.0%                                | $69.33  | $74.39  | $81.97  | $87.03  | $94.61  |
| 5.0%                                | $79.65  | $85.44  | $94.13  | $99.92  | $108.60 |
| 8.0%                                | $98.24  | $105.34 | $116.01 | $123.11 | $133.78 |
| 10.0%                               | $113.05 | $121.21 | $133.45 | $141.61 | $153.85 |
| 12.0%                               | $130.14 | $139.51 | $153.57 | $162.94 | $177.00 |

## 7. Analisi per Scenari

**Scenari:**
- **Best Case** (20%): successo Apple Intelligence, ciclo iPhone forte, espansione Services (+25%)
- **Base Case** (55%): crescita moderata trainata da Services e wearables, iPhone stabile
- **Worst Case** (25%): saturazione iPhone, rallentamento Cina, pressione regolamentare (-20%)

| Scenario          | Probabilita' | Valore/Azione | Contributo Ponderato |
| :---------------- | :----------- | :------------ | :------------------- |
| Best Case         | 20%          | $138.33       | $27.67               |
| Base Case         | 55%          | $110.66       | $60.86               |
| Worst Case        | 25%          | $88.53        | $22.13               |
| **Valore Atteso** | 100%         |               | **$110.66**          |

**Valore Atteso Ponderato:** $110.66

## 8. Simulazione Monte Carlo

**Parametri della simulazione:**
- Iterazioni: 10.000
- WACC: Distribuzione Normale (media=10.88%, std=1.0%)
- Crescita Alta: Distribuzione Normale (media=8%, std=3%)
- Crescita Stabile: Distribuzione Triangolare (1.5%, 2.5%, 3.5%)

## Risultati Simulazione Monte Carlo
**Simulazioni eseguite:** 10,000

| Statistica | Valore |
|-----------|--------|
| Media | $114.77 |
| Mediana | $111.45 |
| Dev. Standard | $25.55 |
| Minimo | $52.80 |
| 5° Percentile | $79.37 |
| 25° Percentile | $96.81 |
| 75° Percentile | $128.92 |
| 95° Percentile | $161.18 |
| Massimo | $261.48 |

**IC 90%:** $79.37 - $161.18
**IC 50%:** $96.81 - $128.92

### Distribuzione dei Valori Simulati

```
    52.8 -     61.1 |  (17)
    61.1 -     69.5 | ███ (94)
    69.5 -     77.8 | ██████████ (307)
    77.8 -     86.2 | █████████████████████ (633)
    86.2 -     94.5 | ██████████████████████████████████████ (1111)
    94.5 -    102.9 | ██████████████████████████████████████████████ (1357)
   102.9 -    111.2 | ██████████████████████████████████████████████████ (1444)
   111.2 -    119.6 | █████████████████████████████████████████████ (1314)
   119.6 -    127.9 | ██████████████████████████████████████ (1105)
   127.9 -    136.3 | ████████████████████████████ (818)
   136.3 -    144.6 | ████████████████████ (606)
   144.6 -    153.0 | ██████████████ (417)
   153.0 -    161.3 | █████████ (281)
   161.3 -    169.7 | █████ (161)
   169.7 -    178.0 | ████ (125)
   178.0 -    186.4 | ██ (79)
   186.4 -    194.7 | █ (52)
   194.7 -    203.0 | █ (31)
   203.0 -    211.4 |  (21)
   211.4 -    219.7 |  (10)
   219.7 -    228.1 |  (3)
   228.1 -    236.4 |  (7)
   236.4 -    244.8 |  (4)
   244.8 -    253.1 |  (0)
   253.1 -    261.5 |  (3)
```

## 9. Sintesi Multi-Metodo e Raccomandazione

| Metodo                          | Valore/Azione | Upside/Downside | Peso |
| :------------------------------ | :------------ | :-------------- | :--- |
| DCF FCFF (3-stage)              | $110.66       | -56.5%          | 40%  |
| Valutazione Relativa (Multipli) | $150.11       | -41.0%          | 25%  |
| Valore Atteso Scenari           | $110.66       | -56.5%          | 15%  |
| Monte Carlo (Mediana)           | $111.45       | -56.2%          | 20%  |

### Valore Intrinseco Stimato

| | |
|---|---|
| **Valore Medio Ponderato** | **$120.68** |
| Prezzo Corrente | $254.23 |
| **Upside/Downside** | **-52.5%** |
| IC 90% Monte Carlo | $79.37 - $161.18 |

### Raccomandazione: **STRONG SELL**

> Il titolo appare fortemente sopravvalutato rispetto ai fondamentali.

## 10. Fattori di Rischio e Considerazioni

### Rischi al Rialzo

- Apple Intelligence genera un super-ciclo di aggiornamento iPhone
- Services raggiunge margini superiori al 75% e accelera la crescita
- Ingresso nel mercato AR/VR con Vision Pro di seconda generazione
- Espansione significativa in India e mercati emergenti
- Buyback aggressivi continuano a ridurre le azioni in circolazione

### Rischi al Ribasso

- Saturazione del mercato smartphone nei mercati sviluppati
- Rallentamento della domanda in Cina (concorrenza Huawei)
- Pressione regolatoria su App Store (DMA in Europa, antitrust US)
- Margini hardware in compressione per costi componenti
- Ritardo nell'adozione AI rispetto a Google e Microsoft
- Dipendenza eccessiva da iPhone (~50% dei ricavi)

---

### Disclaimer

*Questa analisi e' stata generata dal sistema multi-agente Valuation Analyst a scopo educativo e dimostrativo. Non costituisce consulenza finanziaria o raccomandazione di investimento. I dati finanziari utilizzati sono approssimativi e basati su informazioni pubblicamente disponibili. Consultare un consulente finanziario qualificato prima di prendere decisioni di investimento.*

---
*Report generato il 2026-03-18 dal Valuation Analyst Multi-Agent System*