# Report di Valutazione - Microsoft Corp (MSFT)
**Data:** 2026-02-19
**Analista:** Valuation Analyst Multi-Agent System
**Metodologia:** Damodaran (NYU Stern)

---

## 1. Panoramica Aziendale

| Indicatore             | Valore                        |
| :--------------------- | :---------------------------- |
| Ticker                 | MSFT                          |
| Settore                | SERVICES-PREPACKAGED SOFTWARE |
| Paese                  | US                            |
| Prezzo Corrente        | $399.60                       |
| Market Cap             | $2,967.28B                    |
| Enterprise Value       | $2,946.27B                    |
| Azioni in Circolazione | 7,426M                        |
| Ricavi (TTM)           | $261.80B                      |
| EBITDA (TTM)           | $135.25B                      |
| EBIT (TTM)             | $118.55B                      |
| Utile Netto (TTM)      | $97.17B                       |
| EPS                    | $13.09                        |
| Book Value/Share       | $36.16                        |
| Debito Totale          | $59.03B                       |
| Cassa e Investimenti   | $80.04B                       |
| Debito Netto           | -$21.01B                      |
| Rating                 | AAA                           |
| Beta                   | 0.95                          |

## 2. Costo del Capitale (WACC)

### 2.1 Costo dell'Equity (CAPM)

**Formula CAPM:** `Re = Rf + Beta * ERP + CRP`

| Componente                              | Valore    |
| :-------------------------------------- | :-------- |
| Risk-Free Rate (US 10Y)                 | 4.05%     |
| Beta Levered                            | 0.95      |
| Beta Unlevered                          | 0.935     |
| Equity Risk Premium                     | 5.50%     |
| Premio Rischio Sistematico (Beta x ERP) | 5.22%     |
| Country Risk Premium                    | 0.00%     |
| **Costo Equity (Re)**                   | **9.28%** |

### 2.2 Costo del Debito

| Componente                | Valore    |
| :------------------------ | :-------- |
| Rating Creditizio         | AAA       |
| Default Spread            | 0.75%     |
| Costo Debito Pre-Tax (Kd) | 4.80%     |
| Tax Rate Effettivo        | 18.00%    |
| **Costo Debito Post-Tax** | **3.94%** |

### 2.3 WACC

**Formula:** `WACC = (E/V) * Re + (D/V) * Rd * (1-t)`

| Componente            | Valore    |
| :-------------------- | :-------- |
| Peso Equity (E/V)     | 98.05%    |
| Peso Debito (D/V)     | 1.95%     |
| Costo Equity (Re)     | 9.28%     |
| Costo Debito Post-Tax | 3.94%     |
| **WACC**              | **9.17%** |

## 3. Valutazione DCF (FCFF)

### 3.1 FCFF Base

**Formula:** `FCFF = EBIT*(1-t) + Deprezzamento - CapEx - Delta WC`

| Componente      | Valore (M USD) |
| :-------------- | :------------- |
| EBIT            | 118,548.00     |
| EBIT * (1-t)    | 97,209.36      |
| + Deprezzamento | 16,700.00      |
| - CapEx         | 44,477.00      |
| - Delta WC      | 3,200.00       |
| **FCFF Base**   | **66,232.36**  |

### 3.2 Proiezione Multi-Stage (3 fasi)

- **Fase 1 (Alta crescita):** 12% per 5 anni
- **Fase 2 (Transizione):** convergenza lineare per 5 anni
- **Fase 3 (Stabile):** 2.5% in perpetuita'
- **Tasso di sconto (WACC):** 9.17%

| Anno | Tasso Crescita | FCFF (M)   | Valore Attuale (M) |
| :--- | :------------- | :--------- | :----------------- |
| 1    | 12.00%         | 74,180.24  | 67,948.76          |
| 2    | 12.00%         | 83,081.87  | 69,709.63          |
| 3    | 12.00%         | 93,051.70  | 71,516.14          |
| 4    | 12.00%         | 104,217.90 | 73,369.46          |
| 5    | 12.00%         | 116,724.05 | 75,270.82          |
| 6    | 10.10%         | 128,513.18 | 75,911.43          |
| 7    | 8.20%          | 139,051.26 | 75,236.35          |
| 8    | 6.30%          | 147,811.49 | 73,257.86          |
| 9    | 4.40%          | 154,315.19 | 70,056.43          |
| 10   | 2.50%          | 158,173.07 | 65,775.64          |

### 3.3 Riepilogo Valutazione DCF

| Componente                   | Valore         |
| :--------------------------- | :------------- |
| VA Flussi di Cassa Espliciti | $718.05B       |
| Terminal Value (nominale)    | $2,430.38B     |
| VA Terminal Value            | $1,010.66B     |
| TV come % del Totale         | 0.58%          |
| **Enterprise Value**         | **$1,728.72B** |
| - Debito Netto               | -$21.01B       |
| **Equity Value**             | **$1,749.72B** |
| Azioni in Circolazione       | 7,426M         |
| **Valore per Azione (DCF)**  | **$235.63**    |
| Prezzo Corrente              | $399.60        |
| **Upside/Downside**          | **-41.0%**     |

## 4. Valutazione Relativa (Multipli)

### 4.1 Campione Comparabili

| Ticker   | Nome                | Market Cap (B) | P/E      | EV/EBITDA | P/B      | EV/Sales |
| :------- | :------------------ | :------------- | :------- | :-------- | :------- | :------- |
| AAPL     | Apple Inc.          | $3,450B        | 33.5     | 26.8      | 62.0     | 9.0      |
| GOOGL    | Alphabet Inc.       | $2,150B        | 24.0     | 17.5      | 7.8      | 7.2      |
| AMZN     | Amazon.com Inc.     | $2,300B        | 42.0     | 18.5      | 9.5      | 4.0      |
| META     | Meta Platforms Inc. | $1,600B        | 27.5     | 16.0      | 9.0      | 11.5     |
| NVDA     | NVIDIA Corporation  | $3,200B        | 55.0     | 45.0      | 52.0     | 38.0     |
| ORCL     | Oracle Corporation  | $480B          | 38.0     | 22.0      | 28.0     | 9.5      |
| CRM      | Salesforce Inc.     | $310B          | 48.0     | 26.0      | 4.8      | 9.2      |
| **MSFT** | **Microsoft Corp**  | **$2,967B**    | **30.5** | **21.8**  | **11.1** | **11.3** |

### 4.2 Statistiche Multipli Comparabili

**P/E:** Media=38.3, Mediana=38.0, Min=24.0, Max=55.0 (n=7)
**EV/EBITDA:** Media=24.5, Mediana=22.0, Min=16.0, Max=45.0 (n=7)
**P/B:** Media=24.7, Mediana=9.5, Min=4.8, Max=62.0 (n=7)
**EV/Sales:** Media=12.6, Mediana=9.2, Min=4.0, Max=38.0 (n=7)

### 4.3 Valori Impliciti

| Multiplo  | Valore Implicito/Azione |
| :-------- | :---------------------- |
| PE/RATIO  | $497.25                 |
| EV/EBITDA | $403.53                 |
| PB/RATIO  | $343.48                 |
| EV/SALES  | $327.19                 |
| EV/EBIT   | $461.81                 |

**Valore Mediano Multipli:** $403.53
**Upside/Downside:** +1.0%

## 5. Analisi di Sensitivita'

### 5.1 WACC vs Tasso di Crescita Terminale

Valore per azione al variare di WACC e crescita terminale:

| WACC \ Terminal Growth | 1.5%    | 2.0%    | 2.5%    | 3.0%    | 3.5%    |
| :--------------------- | :------ | :------ | :------ | :------ | :------ |
| 7.0%                   | $248.17 | $269.66 | $295.90 | $328.65 | $370.73 |
| 8.0%                   | $208.74 | $223.44 | $240.78 | $261.57 | $286.95 |
| 8.5%                   | $193.28 | $205.69 | $220.15 | $237.21 | $257.66 |
| 9.0%                   | $179.89 | $190.49 | $202.70 | $216.93 | $233.72 |
| 9.5%                   | $168.20 | $177.34 | $187.77 | $199.78 | $213.78 |
| 10.0%                  | $157.89 | $165.85 | $174.84 | $185.10 | $196.93 |
| 11.0%                  | $140.58 | $146.73 | $153.59 | $161.29 | $170.00 |

### 5.2 Crescita Ricavi vs Margine Operativo

| Crescita Ricavi \ Margine Operativo | 35.0%   | 40.0%   | 45.0%   | 50.0%   | 55.0%   |
| :---------------------------------- | :------ | :------ | :------ | :------ | :------ |
| 5.0%                                | $131.24 | $153.92 | $176.61 | $199.29 | $221.97 |
| 8.0%                                | $164.50 | $192.63 | $220.77 | $248.90 | $277.03 |
| 10.0%                               | $191.32 | $223.81 | $256.31 | $288.81 | $321.31 |
| 12.0%                               | $222.51 | $260.06 | $297.61 | $335.16 | $372.71 |
| 15.0%                               | $278.94 | $325.58 | $372.22 | $418.86 | $465.50 |

## 6. Analisi per Scenari

**Scenari:**
- **Best Case** (20%): crescita AI/Cloud superiore, margini in espansione (+30%)
- **Base Case** (55%): continuazione trend attuale
- **Worst Case** (25%): rallentamento macro, pressione competitiva (-25%)

| Scenario          | Probabilita' | Valore/Azione | Contributo Ponderato |
| :---------------- | :----------- | :------------ | :------------------- |
| Best Case         | 20%          | $306.32       | $61.26               |
| Base Case         | 55%          | $235.63       | $129.60              |
| Worst Case        | 25%          | $176.72       | $44.18               |
| **Valore Atteso** | 100%         |               | **$235.04**          |

**Valore Atteso Ponderato:** $235.04

## 7. Simulazione Monte Carlo

**Parametri della simulazione:**
- Iterazioni: 10.000
- WACC: Distribuzione Normale (media=9.17%, std=1.0%)
- Crescita Alta: Distribuzione Normale (media=12%, std=3%)
- Crescita Stabile: Distribuzione Triangolare (1.5%, 2.5%, 3.5%)

## Risultati Simulazione Monte Carlo
**Simulazioni eseguite:** 10,000

| Statistica | Valore |
|-----------|--------|
| Media | $247.32 |
| Mediana | $237.38 |
| Dev. Standard | $62.82 |
| Minimo | $105.91 |
| 5° Percentile | $164.88 |
| 25° Percentile | $203.95 |
| 75° Percentile | $279.71 |
| 95° Percentile | $363.27 |
| Massimo | $723.39 |

**IC 90%:** $164.88 - $363.27
**IC 50%:** $203.95 - $279.71

### Distribuzione dei Valori Simulati

```
   105.9 -    130.6 |  (30)
   130.6 -    155.3 | ██████ (254)
   155.3 -    180.0 | █████████████████████ (800)
   180.0 -    204.7 | ███████████████████████████████████████ (1475)
   204.7 -    229.4 | ██████████████████████████████████████████████████ (1871)
   229.4 -    254.1 | ████████████████████████████████████████████ (1674)
   254.1 -    278.8 | ████████████████████████████████████ (1356)
   278.8 -    303.5 | ████████████████████████ (924)
   303.5 -    328.2 | ████████████████ (610)
   328.2 -    352.9 | ██████████ (385)
   352.9 -    377.6 | ██████ (248)
   377.6 -    402.3 | ███ (137)
   402.3 -    427.0 | ██ (91)
   427.0 -    451.7 | █ (55)
   451.7 -    476.4 |  (36)
   476.4 -    501.1 |  (25)
   501.1 -    525.8 |  (6)
   525.8 -    550.5 |  (7)
   550.5 -    575.2 |  (6)
   575.2 -    599.9 |  (4)
   599.9 -    624.6 |  (4)
   624.6 -    649.3 |  (0)
   649.3 -    674.0 |  (0)
   674.0 -    698.7 |  (1)
   698.7 -    723.4 |  (1)
```

## 8. Sintesi Multi-Metodo e Raccomandazione

| Metodo                          | Valore/Azione | Upside/Downside | Peso |
| :------------------------------ | :------------ | :-------------- | :--- |
| DCF FCFF (3-stage)              | $235.63       | -41.0%          | 40%  |
| Valutazione Relativa (Multipli) | $403.53       | +1.0%           | 25%  |
| Valore Atteso Scenari           | $235.04       | -41.2%          | 15%  |
| Monte Carlo (Mediana)           | $237.38       | -40.6%          | 20%  |

### Valore Intrinseco Stimato

| | |
|---|---|
| **Valore Medio Ponderato** | **$277.87** |
| Prezzo Corrente | $399.60 |
| **Upside/Downside** | **-30.5%** |
| IC 90% Monte Carlo | $164.88 - $363.27 |

### Raccomandazione: **STRONG SELL**

> Il titolo appare fortemente sopravvalutato rispetto ai fondamentali.

## 9. Fattori di Rischio e Considerazioni

### Rischi al Rialzo
- Accelerazione della crescita AI (Copilot, Azure OpenAI)
- Espansione dei margini da economie di scala nel cloud
- Successo nell'integrazione di Activision Blizzard
- Aumento della quota di mercato nel cloud vs AWS/GCP

### Rischi al Ribasso
- Rallentamento della spesa IT enterprise
- Pressione competitiva nel cloud (AWS, GCP)
- Rischi regolatori (antitrust, privacy)
- Compressione dei multipli del settore Technology
- CapEx elevato per infrastruttura AI senza ritorno proporzionale

---

### Disclaimer

*Questa analisi e' stata generata dal sistema multi-agente Valuation Analyst a scopo educativo e dimostrativo. Non costituisce consulenza finanziaria o raccomandazione di investimento. I dati finanziari utilizzati sono approssimativi e basati su informazioni pubblicamente disponibili. Consultare un consulente finanziario qualificato prima di prendere decisioni di investimento.*

---
*Report generato il 2026-02-19 dal Valuation Analyst Multi-Agent System*