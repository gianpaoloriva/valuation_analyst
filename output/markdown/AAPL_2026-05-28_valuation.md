# Report di Valutazione - Apple Inc. (AAPL)
**Data:** 2026-05-28
**Analista:** Valuation Analyst Multi-Agent System
**Metodologia:** Damodaran (NYU Stern)

---

## 1. Executive Summary

| Metrica | Valore |
|---------|--------|
| **Valore Intrinseco Stimato** | **$117.53** |
| Prezzo Corrente | $310.85 |
| Upside/Downside | -62.2% |
| Raccomandazione | **STRONG SELL** |
| IC 90% Monte Carlo | $76.71 - $154.03 |
| WACC | 11.18% |

> Il titolo appare fortemente sopravvalutato rispetto ai fondamentali.

## 2. Panoramica Aziendale

| Indicatore             | Valore               |
| :--------------------- | :------------------- |
| Ticker                 | AAPL                 |
| Settore                | ELECTRONIC COMPUTERS |
| Paese                  | US                   |
| Prezzo Corrente        | $310.85              |
| Market Cap             | $4,565.56B           |
| Enterprise Value       | $4,597.20B           |
| Azioni in Circolazione | 14,687M              |
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

### 3.1 Costo dell'Equity (CAPM)

**Formula CAPM:** `Re = Rf + Beta * ERP + CRP`

| Componente                              | Valore     |
| :-------------------------------------- | :--------- |
| Risk-Free Rate (US 10Y)                 | 4.50%      |
| Beta Levered                            | 1.24       |
| Beta Unlevered                          | 1.218      |
| Equity Risk Premium                     | 5.50%      |
| Premio Rischio Sistematico (Beta x ERP) | 6.82%      |
| Country Risk Premium                    | 0.00%      |
| **Costo Equity (Re)**                   | **11.32%** |

### 3.2 Costo del Debito

| Componente                | Valore    |
| :------------------------ | :-------- |
| Rating Creditizio         | AA+       |
| Default Spread            | 0.85%     |
| Costo Debito Pre-Tax (Kd) | 5.35%     |
| Tax Rate Effettivo        | 16.20%    |
| **Costo Debito Post-Tax** | **4.48%** |

### 3.3 WACC

**Formula:** `WACC = (E/V) * Re + (D/V) * Rd * (1-t)`

| Componente            | Valore     |
| :-------------------- | :--------- |
| Peso Equity (E/V)     | 97.92%     |
| Peso Debito (D/V)     | 2.08%      |
| Costo Equity (Re)     | 11.32%     |
| Costo Debito Post-Tax | 4.48%      |
| **WACC**              | **11.18%** |

## 4. Valutazione DCF (FCFF)

### 4.1 FCFF Base

**Formula:** `FCFF = EBIT*(1-t) + Deprezzamento - CapEx - Delta WC`

| Componente      | Valore (M USD) |
| :-------------- | :------------- |
| EBIT            | 123,216.00     |
| EBIT * (1-t)    | 103,255.01     |
| + Deprezzamento | 11,445.00      |
| - CapEx         | 9,959.00       |
| - Delta WC      | 4,100.00       |
| **FCFF Base**   | **100,641.01** |

### 4.2 Proiezione Multi-Stage (3 fasi)

- **Fase 1 (Alta crescita):** 8% per 5 anni
- **Fase 2 (Transizione):** convergenza lineare per 5 anni
- **Fase 3 (Stabile):** 2.5% in perpetuita'
- **Tasso di sconto (WACC):** 11.18%

| Anno | Tasso Crescita | FCFF (M)   | Valore Attuale (M) |
| :--- | :------------- | :--------- | :----------------- |
| 1    | 8.00%          | 108,692.29 | 97,764.16          |
| 2    | 8.00%          | 117,387.67 | 94,969.54          |
| 3    | 8.00%          | 126,778.69 | 92,254.82          |
| 4    | 8.00%          | 136,920.98 | 89,617.69          |
| 5    | 8.00%          | 147,874.66 | 87,055.94          |
| 6    | 6.90%          | 158,078.01 | 83,706.09          |
| 7    | 5.80%          | 167,246.53 | 79,656.95          |
| 8    | 4.70%          | 175,107.12 | 75,015.55          |
| 9    | 3.60%          | 181,410.98 | 69,902.38          |
| 10   | 2.50%          | 185,946.25 | 64,446.12          |

### 4.3 Riepilogo Valutazione DCF

| Componente                   | Valore         |
| :--------------------------- | :------------- |
| VA Flussi di Cassa Espliciti | $834.39B       |
| Terminal Value (nominale)    | $2,196.29B     |
| VA Terminal Value            | $761.20B       |
| TV come % del Totale         | 0.48%          |
| **Enterprise Value**         | **$1,595.59B** |
| - Debito Netto               | $31.63B        |
| **Equity Value**             | **$1,563.96B** |
| Azioni in Circolazione       | 14,687M        |
| **Valore per Azione (DCF)**  | **$106.48**    |
| Prezzo Corrente              | $310.85        |
| **Upside/Downside**          | **-65.7%**     |

## 5. Valutazione Relativa (Multipli)

### 5.1 Campione Comparabili

| Ticker   | Nome                   | Market Cap (B) | P/E      | EV/EBITDA | P/B      | EV/Sales |
| :------- | :--------------------- | :------------- | :------- | :-------- | :------- | :------- |
| MSFT     | Microsoft Corporation  | $3,083B        | 31.7     | 22.7      | 11.5     | 11.7     |
| GOOGL    | Alphabet Inc.          | $2,150B        | 24.0     | 17.5      | 7.8      | 7.2      |
| AMZN     | Amazon.com Inc.        | $2,300B        | 42.0     | 18.5      | 9.5      | 4.0      |
| META     | Meta Platforms Inc.    | $1,600B        | 27.5     | 16.0      | 9.0      | 11.5     |
| SAMSUNG  | Samsung Electronics    | $350B          | 15.0     | 5.5       | 1.3      | 1.5      |
| SONY     | Sony Group Corporation | $130B          | 18.0     | 9.5       | 2.8      | 1.5      |
| **AAPL** | **Apple Inc.**         | **$4,566B**    | **48.7** | **34.1**  | **80.2** | **11.8** |

### 5.2 Statistiche Multipli Comparabili

**P/E:** Media=26.4, Mediana=25.8, Min=15.0, Max=42.0 (n=6)
**EV/EBITDA:** Media=14.9, Mediana=16.8, Min=5.5, Max=22.7 (n=6)
**P/B:** Media=7.0, Mediana=8.4, Min=1.3, Max=11.5 (n=6)
**EV/Sales:** Media=6.2, Mediana=5.6, Min=1.5, Max=11.7 (n=6)

### 5.3 Valori Impliciti

| Multiplo  | Valore Implicito/Azione |
| :-------- | :---------------------- |
| PE/RATIO  | $164.34                 |
| EV/EBITDA | $151.42                 |
| PB/RATIO  | $32.57                  |
| EV/SALES  | $146.94                 |
| EV/EBIT   | $150.04                 |

**Valore Mediano Multipli:** $150.04
**Upside/Downside:** -51.7%

## 6. Analisi di Sensitivita'

### 6.1 WACC vs Tasso di Crescita Terminale

Valore per azione al variare di WACC e crescita terminale:

| WACC \ Terminal Growth | 1.5%    | 2.0%    | 2.5%    | 3.0%    | 3.5%    |
| :--------------------- | :------ | :------ | :------ | :------ | :------ |
| 7.0%                   | $160.05 | $174.05 | $191.14 | $212.48 | $239.89 |
| 8.0%                   | $134.38 | $143.96 | $155.27 | $168.82 | $185.37 |
| 8.5%                   | $124.30 | $132.40 | $141.83 | $152.96 | $166.30 |
| 9.0%                   | $115.58 | $122.50 | $130.47 | $139.75 | $150.70 |
| 9.5%                   | $107.96 | $113.92 | $120.73 | $128.57 | $137.71 |
| 10.0%                  | $101.23 | $106.43 | $112.30 | $119.00 | $126.72 |
| 11.0%                  | $89.93  | $93.95  | $98.43  | $103.46 | $109.16 |

### 6.2 Crescita Ricavi vs Margine Operativo

| Crescita Ricavi \ Margine Operativo | 28.0%   | 30.0%   | 33.0%   | 35.0%   | 38.0%   |
| :---------------------------------- | :------ | :------ | :------ | :------ | :------ |
| 3.0%                                | $67.24  | $72.15  | $79.51  | $84.42  | $91.78  |
| 5.0%                                | $77.17  | $82.78  | $91.20  | $96.81  | $105.23 |
| 8.0%                                | $95.02  | $101.90 | $112.22 | $119.10 | $129.41 |
| 10.0%                               | $109.24 | $117.13 | $128.96 | $136.85 | $148.68 |
| 12.0%                               | $125.63 | $134.68 | $148.26 | $157.31 | $170.89 |

## 7. Analisi per Scenari

**Scenari:**
- **Best Case** (20%): successo Apple Intelligence, ciclo iPhone forte, espansione Services (+25%)
- **Base Case** (55%): crescita moderata trainata da Services e wearables, iPhone stabile
- **Worst Case** (25%): saturazione iPhone, rallentamento Cina, pressione regolamentare (-20%)

| Scenario          | Probabilita' | Valore/Azione | Contributo Ponderato |
| :---------------- | :----------- | :------------ | :------------------- |
| Best Case         | 20%          | $133.10       | $26.62               |
| Base Case         | 55%          | $106.48       | $58.57               |
| Worst Case        | 25%          | $85.19        | $21.30               |
| **Valore Atteso** | 100%         |               | **$106.48**          |

**Valore Atteso Ponderato:** $106.48

## 8. Simulazione Monte Carlo

**Parametri della simulazione:**
- Iterazioni: 10.000
- WACC: Distribuzione Normale (media=11.18%, std=1.0%)
- Crescita Alta: Distribuzione Normale (media=8%, std=3%)
- Crescita Stabile: Distribuzione Triangolare (1.5%, 2.5%, 3.5%)

## Risultati Simulazione Monte Carlo
**Simulazioni eseguite:** 10,000

| Statistica | Valore |
|-----------|--------|
| Media | $110.26 |
| Mediana | $107.27 |
| Dev. Standard | $24.05 |
| Minimo | $51.41 |
| 5° Percentile | $76.71 |
| 25° Percentile | $93.31 |
| 75° Percentile | $123.65 |
| 95° Percentile | $154.03 |
| Massimo | $247.47 |

**IC 90%:** $76.71 - $154.03
**IC 50%:** $93.31 - $123.65

### Distribuzione dei Valori Simulati

```
    51.4 -     59.3 |  (17)
    59.3 -     67.1 | ███ (89)
    67.1 -     74.9 | █████████ (285)
    74.9 -     82.8 | ████████████████████ (606)
    82.8 -     90.6 | █████████████████████████████████████ (1081)
    90.6 -     98.5 | █████████████████████████████████████████████ (1317)
    98.5 -    106.3 | ██████████████████████████████████████████████████ (1447)
   106.3 -    114.2 | █████████████████████████████████████████████ (1318)
   114.2 -    122.0 | ███████████████████████████████████████ (1136)
   122.0 -    129.8 | █████████████████████████████ (842)
   129.8 -    137.7 | █████████████████████ (612)
   137.7 -    145.5 | ███████████████ (435)
   145.5 -    153.4 | ██████████ (298)
   153.4 -    161.2 | █████ (168)
   161.2 -    169.0 | ████ (131)
   169.0 -    176.9 | ███ (87)
   176.9 -    184.7 | █ (51)
   184.7 -    192.6 | █ (29)
   192.6 -    200.4 |  (26)
   200.4 -    208.3 |  (7)
   208.3 -    216.1 |  (8)
   216.1 -    223.9 |  (2)
   223.9 -    231.8 |  (5)
   231.8 -    239.6 |  (0)
   239.6 -    247.5 |  (3)
```

## 9. Sintesi Multi-Metodo e Raccomandazione

| Metodo                          | Valore/Azione | Upside/Downside | Peso |
| :------------------------------ | :------------ | :-------------- | :--- |
| DCF FCFF (3-stage)              | $106.48       | -65.7%          | 40%  |
| Valutazione Relativa (Multipli) | $150.04       | -51.7%          | 25%  |
| Valore Atteso Scenari           | $106.48       | -65.7%          | 15%  |
| Monte Carlo (Mediana)           | $107.27       | -65.5%          | 20%  |

### Valore Intrinseco Stimato

| | |
|---|---|
| **Valore Medio Ponderato** | **$117.53** |
| Prezzo Corrente | $310.85 |
| **Upside/Downside** | **-62.2%** |
| IC 90% Monte Carlo | $76.71 - $154.03 |

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
*Report generato il 2026-05-28 dal Valuation Analyst Multi-Agent System*