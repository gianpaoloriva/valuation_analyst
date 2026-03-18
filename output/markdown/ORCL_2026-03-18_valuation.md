# Report di Valutazione - Oracle Corp (ORCL)
**Data:** 2026-03-18
**Analista:** Valuation Analyst Multi-Agent System
**Metodologia:** Damodaran (NYU Stern)

---

## 1. Executive Summary

| Metrica | Valore |
|---------|--------|
| **Valore Intrinseco Stimato** | **$87.95** |
| Prezzo Corrente | $154.69 |
| Upside/Downside | -43.1% |
| Raccomandazione | **STRONG SELL** |
| IC 90% Monte Carlo | $31.79 - $102.31 |
| WACC | 9.28% |

> Il titolo appare fortemente sopravvalutato rispetto ai fondamentali.

## 2. Panoramica Aziendale

| Indicatore             | Valore                        |
| :--------------------- | :---------------------------- |
| Ticker                 | ORCL                          |
| Settore                | SERVICES-PREPACKAGED SOFTWARE |
| Paese                  | US                            |
| Prezzo Corrente        | $154.69                       |
| Market Cap             | $448.58B                      |
| Enterprise Value       | $524.97B                      |
| Azioni in Circolazione | 2,876M                        |
| Ricavi (TTM)           | $56.07B                       |
| EBITDA (TTM)           | $23.50B                       |
| EBIT (TTM)             | $17.63B                       |
| Utile Netto (TTM)      | $11.33B                       |
| EPS                    | $3.94                         |
| Book Value/Share       | $4.46                         |
| Debito Totale          | $88.44B                       |
| Cassa e Investimenti   | $12.04B                       |
| Debito Netto           | $76.40B                       |
| Rating                 | BBB+                          |
| Beta                   | 1.08                          |

## 3. Costo del Capitale (WACC)

### 3.1 Costo dell'Equity (CAPM)

**Formula CAPM:** `Re = Rf + Beta * ERP + CRP`

| Componente                              | Valore     |
| :-------------------------------------- | :--------- |
| Risk-Free Rate (US 10Y)                 | 4.23%      |
| Beta Levered                            | 1.08       |
| Beta Unlevered                          | 0.931      |
| Equity Risk Premium                     | 5.50%      |
| Premio Rischio Sistematico (Beta x ERP) | 5.94%      |
| Country Risk Premium                    | 0.00%      |
| **Costo Equity (Re)**                   | **10.17%** |

### 3.2 Costo del Debito

| Componente                | Valore    |
| :------------------------ | :-------- |
| Rating Creditizio         | BBB+      |
| Default Spread            | 1.65%     |
| Costo Debito Pre-Tax (Kd) | 5.88%     |
| Tax Rate Effettivo        | 19.00%    |
| **Costo Debito Post-Tax** | **4.76%** |

### 3.3 WACC

**Formula:** `WACC = (E/V) * Re + (D/V) * Rd * (1-t)`

| Componente            | Valore    |
| :-------------------- | :-------- |
| Peso Equity (E/V)     | 83.53%    |
| Peso Debito (D/V)     | 16.47%    |
| Costo Equity (Re)     | 10.17%    |
| Costo Debito Post-Tax | 4.76%     |
| **WACC**              | **9.28%** |

## 4. Valutazione DCF (FCFF)

### 4.1 FCFF Base

**Formula:** `FCFF = EBIT*(1-t) + Deprezzamento - CapEx - Delta WC`

| Componente      | Valore (M USD) |
| :-------------- | :------------- |
| EBIT            | 17,631.00      |
| EBIT * (1-t)    | 14,281.11      |
| + Deprezzamento | 5,869.00       |
| - CapEx         | 9,272.00       |
| - Delta WC      | 1,500.00       |
| **FCFF Base**   | **9,378.11**   |

### 4.2 Proiezione Multi-Stage (3 fasi)

- **Fase 1 (Alta crescita):** 12% per 5 anni
- **Fase 2 (Transizione):** convergenza lineare per 5 anni
- **Fase 3 (Stabile):** 2.5% in perpetuita'
- **Tasso di sconto (WACC):** 9.28%

| Anno | Tasso Crescita | FCFF (M)  | Valore Attuale (M) |
| :--- | :------------- | :-------- | :----------------- |
| 1    | 12.00%         | 10,503.48 | 9,611.57           |
| 2    | 12.00%         | 11,763.90 | 9,850.85           |
| 3    | 12.00%         | 13,175.57 | 10,096.08          |
| 4    | 12.00%         | 14,756.64 | 10,347.42          |
| 5    | 12.00%         | 16,527.43 | 10,605.02          |
| 6    | 10.10%         | 18,196.71 | 10,684.64          |
| 7    | 8.20%          | 19,688.83 | 10,579.09          |
| 8    | 6.30%          | 20,929.23 | 10,290.65          |
| 9    | 4.40%          | 21,850.12 | 9,831.15           |
| 10   | 2.50%          | 22,396.37 | 9,221.25           |

### 4.3 Riepilogo Valutazione DCF

| Componente                   | Valore       |
| :--------------------------- | :----------- |
| VA Flussi di Cassa Espliciti | $101.12B     |
| Terminal Value (nominale)    | $338.61B     |
| VA Terminal Value            | $139.42B     |
| TV come % del Totale         | 0.58%        |
| **Enterprise Value**         | **$240.53B** |
| - Debito Netto               | $76.40B      |
| **Equity Value**             | **$164.14B** |
| Azioni in Circolazione       | 2,876M       |
| **Valore per Azione (DCF)**  | **$57.07**   |
| Prezzo Corrente              | $154.69      |
| **Upside/Downside**          | **-63.1%**   |

## 5. Valutazione Relativa (Multipli)

### 5.1 Campione Comparabili

| Ticker   | Nome                            | Market Cap (B) | P/E      | EV/EBITDA | P/B      | EV/Sales |
| :------- | :------------------------------ | :------------- | :------- | :-------- | :------- | :------- |
| MSFT     | Microsoft Corporation           | $3,083B        | 31.7     | 22.7      | 11.5     | 11.7     |
| SAP      | SAP SE                          | $310B          | 42.0     | 28.0      | 6.5      | 9.5      |
| CRM      | Salesforce Inc.                 | $310B          | 48.0     | 26.0      | 4.8      | 9.2      |
| IBM      | International Business Machines | $230B          | 28.0     | 15.5      | 8.2      | 4.0      |
| INTU     | Intuit Inc.                     | $180B          | 55.0     | 35.0      | 12.0     | 12.5     |
| NOW      | ServiceNow Inc.                 | $210B          | 65.0     | 45.0      | 20.0     | 18.0     |
| **ORCL** | **Oracle Corp**                 | **$449B**      | **39.3** | **22.3**  | **34.7** | **9.4**  |

### 5.2 Statistiche Multipli Comparabili

**P/E:** Media=45.0, Mediana=45.0, Min=28.0, Max=65.0 (n=6)
**EV/EBITDA:** Media=28.7, Mediana=27.0, Min=15.5, Max=45.0 (n=6)
**P/B:** Media=10.5, Mediana=9.8, Min=4.8, Max=20.0 (n=6)
**EV/Sales:** Media=10.8, Mediana=10.6, Min=4.0, Max=18.0 (n=6)

### 5.3 Valori Impliciti

| Multiplo  | Valore Implicito/Azione |
| :-------- | :---------------------- |
| PE/RATIO  | $177.23                 |
| EV/EBITDA | $194.05                 |
| PB/RATIO  | $43.93                  |
| EV/SALES  | $180.09                 |
| EV/EBIT   | $192.42                 |

**Valore Mediano Multipli:** $180.09
**Upside/Downside:** +16.4%

## 6. Analisi di Sensitivita'

### 6.1 WACC vs Tasso di Crescita Terminale

Valore per azione al variare di WACC e crescita terminale:

| WACC \ Terminal Growth | 1.5%   | 2.0%   | 2.5%   | 3.0%   | 3.5%    |
| :--------------------- | :----- | :----- | :----- | :----- | :------ |
| 7.0%                   | $63.13 | $70.98 | $80.58 | $92.55 | $107.93 |
| 8.0%                   | $48.71 | $54.09 | $60.43 | $68.03 | $77.31  |
| 8.5%                   | $43.06 | $47.60 | $52.88 | $59.12 | $66.60  |
| 9.0%                   | $38.17 | $42.04 | $46.51 | $51.71 | $57.84  |
| 9.5%                   | $33.89 | $37.23 | $41.05 | $45.44 | $50.56  |
| 10.0%                  | $30.13 | $33.03 | $36.32 | $40.07 | $44.39  |
| 11.0%                  | $23.79 | $26.04 | $28.55 | $31.37 | $34.55  |

### 6.2 Crescita Ricavi vs Margine Operativo

| Crescita Ricavi \ Margine Operativo | 25.0%  | 28.0%  | 30.0%   | 33.0%   | 36.0%   |
| :---------------------------------- | :----- | :----- | :------ | :------ | :------ |
| 5.0%                                | $25.02 | $32.36 | $37.25  | $44.59  | $51.92  |
| 8.0%                                | $38.12 | $47.22 | $53.28  | $62.38  | $71.47  |
| 10.0%                               | $48.67 | $59.17 | $66.17  | $76.67  | $87.18  |
| 12.0%                               | $60.93 | $73.06 | $81.14  | $93.27  | $105.40 |
| 15.0%                               | $83.07 | $98.12 | $108.16 | $123.21 | $138.27 |

## 7. Analisi per Scenari

**Scenari:**
- **Best Case** (20%): Cloud (OCI) supera il 20% di quota IaaS, AI su database autonomo accelera, margini in espansione (+25%)
- **Base Case** (55%): Crescita cloud 12-15%, margini stabili, integrazione Cerner completata
- **Worst Case** (25%): Rallentamento spesa IT enterprise, perdita quote cloud vs AWS/Azure/GCP, debito elevato (-20%)

| Scenario          | Probabilita' | Valore/Azione | Contributo Ponderato |
| :---------------- | :----------- | :------------ | :------------------- |
| Best Case         | 20%          | $71.34        | $14.27               |
| Base Case         | 55%          | $57.07        | $31.39               |
| Worst Case        | 25%          | $45.66        | $11.41               |
| **Valore Atteso** | 100%         |               | **$57.07**           |

**Valore Atteso Ponderato:** $57.07

## 8. Simulazione Monte Carlo

**Parametri della simulazione:**
- Iterazioni: 10.000
- WACC: Distribuzione Normale (media=9.28%, std=1.0%)
- Crescita Alta: Distribuzione Normale (media=12%, std=3%)
- Crescita Stabile: Distribuzione Triangolare (1.5%, 2.5%, 3.5%)

## Risultati Simulazione Monte Carlo
**Simulazioni eseguite:** 10,000

| Statistica | Valore |
|-----------|--------|
| Media | $61.17 |
| Mediana | $57.70 |
| Dev. Standard | $22.27 |
| Minimo | $10.70 |
| 5° Percentile | $31.79 |
| 25° Percentile | $45.76 |
| 75° Percentile | $72.71 |
| 95° Percentile | $102.31 |
| Massimo | $224.62 |

**IC 90%:** $31.79 - $102.31
**IC 50%:** $45.76 - $72.71

### Distribuzione dei Valori Simulati

```
    10.7 -     19.3 |  (28)
    19.3 -     27.8 | ██████ (227)
    27.8 -     36.4 | ████████████████████ (716)
    36.4 -     44.9 | ███████████████████████████████████████ (1390)
    44.9 -     53.5 | ██████████████████████████████████████████████████ (1747)
    53.5 -     62.0 | ███████████████████████████████████████████████ (1669)
    62.0 -     70.6 | █████████████████████████████████████████ (1454)
    70.6 -     79.2 | ████████████████████████████ (982)
    79.2 -     87.7 | ██████████████████ (657)
    87.7 -     96.3 | ████████████ (425)
    96.3 -    104.8 | ████████ (283)
   104.8 -    113.4 | ████ (145)
   113.4 -    121.9 | ███ (111)
   121.9 -    130.5 | █ (65)
   130.5 -    139.1 | █ (37)
   139.1 -    147.6 |  (29)
   147.6 -    156.2 |  (10)
   156.2 -    164.7 |  (8)
   164.7 -    173.3 |  (4)
   173.3 -    181.8 |  (4)
   181.8 -    190.4 |  (5)
   190.4 -    199.0 |  (2)
   199.0 -    207.5 |  (0)
   207.5 -    216.1 |  (1)
   216.1 -    224.6 |  (1)
```

## 9. Sintesi Multi-Metodo e Raccomandazione

| Metodo                          | Valore/Azione | Upside/Downside | Peso |
| :------------------------------ | :------------ | :-------------- | :--- |
| DCF FCFF (3-stage)              | $57.07        | -63.1%          | 40%  |
| Valutazione Relativa (Multipli) | $180.09       | +16.4%          | 25%  |
| Valore Atteso Scenari           | $57.07        | -63.1%          | 15%  |
| Monte Carlo (Mediana)           | $57.70        | -62.7%          | 20%  |

### Valore Intrinseco Stimato

| | |
|---|---|
| **Valore Medio Ponderato** | **$87.95** |
| Prezzo Corrente | $154.69 |
| **Upside/Downside** | **-43.1%** |
| IC 90% Monte Carlo | $31.79 - $102.31 |

### Raccomandazione: **STRONG SELL**

> Il titolo appare fortemente sopravvalutato rispetto ai fondamentali.

## 10. Fattori di Rischio e Considerazioni

### Rischi al Rialzo

- Oracle Cloud Infrastructure (OCI) guadagna quota nel mercato IaaS
- Autonomous Database e AI generativa su cloud attraggono nuovi clienti
- Integrazione Cerner genera sinergie nel settore healthcare
- Transizione SaaS migliora la ricorrenza dei ricavi e i margini
- Buyback aggressivi continuano a ridurre le azioni in circolazione

### Rischi al Ribasso

- Debito elevato (~$88B) limita la flessibilita' finanziaria
- Concorrenza intensa nel cloud da AWS, Azure e GCP
- Rallentamento della spesa IT enterprise in scenario recessivo
- Rischio di esecuzione sull'integrazione Cerner ($28B acquisizione)
- Dipendenza dal database on-premise in declino strutturale
- CapEx crescente per data center senza garanzia di ritorni

---

### Disclaimer

*Questa analisi e' stata generata dal sistema multi-agente Valuation Analyst a scopo educativo e dimostrativo. Non costituisce consulenza finanziaria o raccomandazione di investimento. I dati finanziari utilizzati sono approssimativi e basati su informazioni pubblicamente disponibili. Consultare un consulente finanziario qualificato prima di prendere decisioni di investimento.*

---
*Report generato il 2026-03-18 dal Valuation Analyst Multi-Agent System*