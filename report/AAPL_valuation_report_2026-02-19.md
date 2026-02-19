# Report di Valutazione - Apple Inc. (AAPL)
**Data:** 2026-02-19
**Analista:** Valuation Analyst Multi-Agent System
**Metodologia:** Damodaran (NYU Stern)

---

## 1. Panoramica Aziendale

| Indicatore             | Valore               |
| :--------------------- | :------------------- |
| Ticker                 | AAPL                 |
| Settore                | ELECTRONIC COMPUTERS |
| Paese                  | US                   |
| Prezzo Corrente        | $264.35              |
| Market Cap             | $3,880.96B           |
| Enterprise Value       | $3,912.59B           |
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

## 2. Costo del Capitale (WACC)

### 2.1 Costo dell'Equity (CAPM)

**Formula CAPM:** `Re = Rf + Beta * ERP + CRP`

| Componente                              | Valore     |
| :-------------------------------------- | :--------- |
| Risk-Free Rate (US 10Y)                 | 4.05%      |
| Beta Levered                            | 1.24       |
| Beta Unlevered                          | 1.215      |
| Equity Risk Premium                     | 5.50%      |
| Premio Rischio Sistematico (Beta x ERP) | 6.82%      |
| Country Risk Premium                    | 0.00%      |
| **Costo Equity (Re)**                   | **10.87%** |

### 2.2 Costo del Debito

| Componente                | Valore    |
| :------------------------ | :-------- |
| Rating Creditizio         | AA+       |
| Default Spread            | 0.85%     |
| Costo Debito Pre-Tax (Kd) | 4.90%     |
| Tax Rate Effettivo        | 16.20%    |
| **Costo Debito Post-Tax** | **4.11%** |

### 2.3 WACC

**Formula:** `WACC = (E/V) * Re + (D/V) * Rd * (1-t)`

| Componente            | Valore     |
| :-------------------- | :--------- |
| Peso Equity (E/V)     | 97.57%     |
| Peso Debito (D/V)     | 2.43%      |
| Costo Equity (Re)     | 10.87%     |
| Costo Debito Post-Tax | 4.11%      |
| **WACC**              | **10.71%** |

## 3. Valutazione DCF (FCFF)

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
- **Tasso di sconto (WACC):** 10.71%

| Anno | Tasso Crescita | FCFF (M)   | Valore Attuale (M) |
| :--- | :------------- | :--------- | :----------------- |
| 1    | 8.00%          | 108,692.29 | 98,181.56          |
| 2    | 8.00%          | 117,387.67 | 95,782.22          |
| 3    | 8.00%          | 126,778.69 | 93,441.51          |
| 4    | 8.00%          | 136,920.98 | 91,158.01          |
| 5    | 8.00%          | 147,874.66 | 88,930.30          |
| 6    | 6.90%          | 158,078.01 | 85,873.41          |
| 7    | 5.80%          | 167,246.53 | 82,068.32          |
| 8    | 4.70%          | 175,107.12 | 77,616.39          |
| 9    | 3.60%          | 181,410.98 | 72,634.74          |
| 10   | 2.50%          | 185,946.25 | 67,251.11          |

### 3.3 Riepilogo Valutazione DCF

| Componente                   | Valore         |
| :--------------------------- | :------------- |
| VA Flussi di Cassa Espliciti | $852.94B       |
| Terminal Value (nominale)    | $2,322.80B     |
| VA Terminal Value            | $840.09B       |
| TV come % del Totale         | 0.50%          |
| **Enterprise Value**         | **$1,693.02B** |
| - Debito Netto               | $31.63B        |
| **Equity Value**             | **$1,661.39B** |
| Azioni in Circolazione       | 14,681M        |
| **Valore per Azione (DCF)**  | **$113.17**    |
| Prezzo Corrente              | $264.35        |
| **Upside/Downside**          | **-57.2%**     |

## 4. Valutazione Relativa (Multipli)

### 4.1 Campione Comparabili

| Ticker   | Nome                   | Market Cap (B) | P/E      | EV/EBITDA | P/B      | EV/Sales |
| :------- | :--------------------- | :------------- | :------- | :-------- | :------- | :------- |
| MSFT     | Microsoft Corporation  | $3,083B        | 31.7     | 22.7      | 11.5     | 11.7     |
| GOOGL    | Alphabet Inc.          | $2,150B        | 24.0     | 17.5      | 7.8      | 7.2      |
| AMZN     | Amazon.com Inc.        | $2,300B        | 42.0     | 18.5      | 9.5      | 4.0      |
| META     | Meta Platforms Inc.    | $1,600B        | 27.5     | 16.0      | 9.0      | 11.5     |
| SAMSUNG  | Samsung Electronics    | $350B          | 15.0     | 5.5       | 1.3      | 1.5      |
| SONY     | Sony Group Corporation | $130B          | 18.0     | 9.5       | 2.8      | 1.5      |
| **AAPL** | **Apple Inc.**         | **$3,881B**    | **41.4** | **29.1**  | **68.1** | **10.0** |

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
**Upside/Downside:** -43.2%

## 5. Analisi di Sensitivita'

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
| 3.0%                                | $70.56  | $75.71  | $83.42  | $88.57  | $96.28  |
| 5.0%                                | $81.12  | $87.01  | $95.85  | $101.75 | $110.59 |
| 8.0%                                | $100.14 | $107.38 | $118.25 | $125.49 | $136.35 |
| 10.0%                               | $115.30 | $123.62 | $136.10 | $144.42 | $156.90 |
| 12.0%                               | $132.80 | $142.36 | $156.71 | $166.27 | $180.61 |

## 6. Analisi per Scenari

**Scenari:**
- **Best Case** (20%): successo Apple Intelligence, ciclo iPhone forte, espansione Services (+25%)
- **Base Case** (55%): crescita moderata trainata da Services e wearables, iPhone stabile
- **Worst Case** (25%): saturazione iPhone, rallentamento Cina, pressione regolamentare (-20%)

| Scenario          | Probabilita' | Valore/Azione | Contributo Ponderato |
| :---------------- | :----------- | :------------ | :------------------- |
| Best Case         | 20%          | $141.46       | $28.29               |
| Base Case         | 55%          | $113.17       | $62.24               |
| Worst Case        | 25%          | $90.53        | $22.63               |
| **Valore Atteso** | 100%         |               | **$113.17**          |

**Valore Atteso Ponderato:** $113.17

## 7. Simulazione Monte Carlo

**Parametri della simulazione:**
- Iterazioni: 10.000
- WACC: Distribuzione Normale (media=10.71%, std=1.0%)
- Crescita Alta: Distribuzione Normale (media=8%, std=3%)
- Crescita Stabile: Distribuzione Triangolare (1.5%, 2.5%, 3.5%)

## Risultati Simulazione Monte Carlo
**Simulazioni eseguite:** 10,000

| Statistica | Valore |
|-----------|--------|
| Media | $117.47 |
| Mediana | $113.95 |
| Dev. Standard | $26.47 |
| Minimo | $53.61 |
| 5° Percentile | $80.92 |
| 25° Percentile | $98.89 |
| 75° Percentile | $132.00 |
| 95° Percentile | $165.55 |
| Massimo | $270.09 |

**IC 90%:** $80.92 - $165.55
**IC 50%:** $98.89 - $132.00

### Distribuzione dei Valori Simulati

```
    53.6 -     62.3 |  (17)
    62.3 -     70.9 | ███ (96)
    70.9 -     79.6 | ███████████ (321)
    79.6 -     88.2 | ██████████████████████ (656)
    88.2 -     96.9 | ██████████████████████████████████████ (1126)
    96.9 -    105.6 | ███████████████████████████████████████████████ (1374)
   105.6 -    114.2 | ██████████████████████████████████████████████████ (1445)
   114.2 -    122.9 | █████████████████████████████████████████████ (1325)
   122.9 -    131.5 | █████████████████████████████████████ (1076)
   131.5 -    140.2 | ████████████████████████████ (817)
   140.2 -    148.9 | ████████████████████ (578)
   148.9 -    157.5 | ██████████████ (410)
   157.5 -    166.2 | █████████ (273)
   166.2 -    174.8 | █████ (156)
   174.8 -    183.5 | ████ (121)
   183.5 -    192.2 | ██ (81)
   192.2 -    200.8 | █ (47)
   200.8 -    209.5 | █ (34)
   209.5 -    218.1 |  (19)
   218.1 -    226.8 |  (9)
   226.8 -    235.5 |  (5)
   235.5 -    244.1 |  (7)
   244.1 -    252.8 |  (2)
   252.8 -    261.4 |  (2)
   261.4 -    270.1 |  (3)
```

## 8. Sintesi Multi-Metodo e Raccomandazione

| Metodo                          | Valore/Azione | Upside/Downside | Peso |
| :------------------------------ | :------------ | :-------------- | :--- |
| DCF FCFF (3-stage)              | $113.17       | -57.2%          | 40%  |
| Valutazione Relativa (Multipli) | $150.11       | -43.2%          | 25%  |
| Valore Atteso Scenari           | $113.17       | -57.2%          | 15%  |
| Monte Carlo (Mediana)           | $113.95       | -56.9%          | 20%  |

### Valore Intrinseco Stimato

| | |
|---|---|
| **Valore Medio Ponderato** | **$122.56** |
| Prezzo Corrente | $264.35 |
| **Upside/Downside** | **-53.6%** |
| IC 90% Monte Carlo | $80.92 - $165.55 |

### Raccomandazione: **STRONG SELL**

> Il titolo appare fortemente sopravvalutato rispetto ai fondamentali.

## 9. Fattori di Rischio e Considerazioni

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
*Report generato il 2026-02-19 dal Valuation Analyst Multi-Agent System*