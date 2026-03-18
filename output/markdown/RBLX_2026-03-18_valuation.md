# Report di Valutazione - Roblox Corporation (RBLX)
**Data:** 2026-03-18
**Analista:** Valuation Analyst Multi-Agent System
**Metodologia:** Damodaran (NYU Stern)

---

## 1. Executive Summary

| Metrica | Valore |
|---------|--------|
| **Valore Intrinseco Stimato** | **-$7.79** |
| Prezzo Corrente | $57.79 |
| Upside/Downside | -113.5% |
| Raccomandazione | **STRONG SELL** |
| IC 90% Monte Carlo | -$18.53 - -$5.98 |
| WACC | 12.52% |

> Il titolo appare fortemente sopravvalutato rispetto ai fondamentali.

## 2. Panoramica Aziendale

| Indicatore             | Valore                                       |
| :--------------------- | :------------------------------------------- |
| Ticker                 | RBLX                                         |
| Settore                | SERVICES-PREPACKAGED SOFTWARE                |
| Paese                  | US                                           |
| Prezzo Corrente        | $57.79                                       |
| Market Cap             | $41.93B                                      |
| Enterprise Value       | $41.33B                                      |
| Azioni in Circolazione | 709M                                         |
| Ricavi (TTM)           | $3.60B                                       |
| EBITDA (TTM)           | -$0.84B                                      |
| EBIT (TTM)             | -$1.04B                                      |
| Utile Netto (TTM)      | -$0.94B                                      |
| EPS                    | -$1.32 (negativo)                            |
| Book Value/Share       | $0.29                                        |
| Debito Totale          | $1.80B                                       |
| Cassa e Investimenti   | $2.41B                                       |
| Debito Netto           | -$0.60B                                      |
| Rating                 | BB                                           |
| Beta                   | 1.56                                         |
| **Nota**               | **Azienda attualmente in perdita operativa** |

## 3. Costo del Capitale (WACC)

### 2.1 Costo dell'Equity (CAPM)

**Formula CAPM:** `Re = Rf + Beta * ERP + CRP`

| Componente                              | Valore     |
| :-------------------------------------- | :--------- |
| Risk-Free Rate (US 10Y)                 | 4.23%      |
| Beta Levered                            | 1.56       |
| Beta Unlevered                          | 1.509      |
| Equity Risk Premium                     | 5.50%      |
| Premio Rischio Sistematico (Beta x ERP) | 8.58%      |
| Country Risk Premium                    | 0.00%      |
| **Costo Equity (Re)**                   | **12.81%** |

### 2.2 Costo del Debito

| Componente                | Valore    |
| :------------------------ | :-------- |
| Rating Creditizio         | BB        |
| Default Spread            | 3.00%     |
| Costo Debito Pre-Tax (Kd) | 7.23%     |
| Tax Rate Effettivo        | 21.00%    |
| **Costo Debito Post-Tax** | **5.71%** |

### 2.3 WACC

**Formula:** `WACC = (E/V) * Re + (D/V) * Rd * (1-t)`

| Componente            | Valore     |
| :-------------------- | :--------- |
| Peso Equity (E/V)     | 95.87%     |
| Peso Debito (D/V)     | 4.13%      |
| Costo Equity (Re)     | 12.81%     |
| Costo Debito Post-Tax | 5.71%      |
| **WACC**              | **12.52%** |

## 4. Valutazione DCF (FCFF)

> **Nota:** L'azienda ha EBIT negativo. Il FCFF calcolato potrebbe essere negativo. Il DCF proietta la convergenza verso la profittabilita' secondo le assunzioni dell'analista.

### 3.1 FCFF Base

**Formula:** `FCFF = EBIT*(1-t) + Deprezzamento - CapEx - Delta WC`

| Componente      | Valore (M USD) |
| :-------------- | :------------- |
| EBIT            | -1,045.00      |
| EBIT * (1-t)    | -825.55        |
| + Deprezzamento | 209.00         |
| - CapEx         | 180.00         |
| - Delta WC      | -481.00        |
| **FCFF Base**   | **-315.55**    |

### 3.2 Proiezione Multi-Stage (3 fasi)

- **Fase 1 (Alta crescita):** 20% per 5 anni
- **Fase 2 (Transizione):** convergenza lineare per 5 anni
- **Fase 3 (Stabile):** 3.0% in perpetuita'
- **Tasso di sconto (WACC):** 12.52%

| Anno | Tasso Crescita | FCFF (M)  | Valore Attuale (M) |
| :--- | :------------- | :-------- | :----------------- |
| 1    | 20.00%         | -378.66   | -336.54            |
| 2    | 20.00%         | -454.39   | -358.92            |
| 3    | 20.00%         | -545.27   | -382.79            |
| 4    | 20.00%         | -654.32   | -408.24            |
| 5    | 20.00%         | -785.19   | -435.39            |
| 6    | 16.60%         | -915.53   | -451.19            |
| 7    | 13.20%         | -1,036.38 | -453.93            |
| 8    | 9.80%          | -1,137.95 | -442.97            |
| 9    | 6.40%          | -1,210.77 | -418.89            |
| 10   | 3.00%          | -1,247.10 | -383.46            |

### 3.3 Riepilogo Valutazione DCF

| Componente                   | Valore      |
| :--------------------------- | :---------- |
| VA Flussi di Cassa Espliciti | -$4.07B     |
| Terminal Value (nominale)    | -$13.50B    |
| VA Terminal Value            | -$4.15B     |
| TV come % del Totale         | 0.50%       |
| **Enterprise Value**         | **-$8.22B** |
| - Debito Netto               | -$0.60B     |
| **Equity Value**             | **-$7.62B** |
| Azioni in Circolazione       | 709M        |
| **Valore per Azione (DCF)**  | **-$10.75** |
| Prezzo Corrente              | $57.79      |
| **Upside/Downside**          | **-118.6%** |

## 5. Valutazione Relativa (Multipli)

> **Nota:** L'azienda ha EPS e/o EBITDA negativi. I multipli P/E e EV/EBITDA non sono applicabili e sono riportati come N/A.

### 4.1 Campione Comparabili

| Ticker   | Nome                          | Market Cap (B) | P/E     | EV/EBITDA | P/B       | EV/Sales |
| :------- | :---------------------------- | :------------- | :------ | :-------- | :-------- | :------- |
| EA       | Electronic Arts Inc.          | $50B           | 75.2    | 36.8      | 8.2       | 6.8      |
| TTWO     | Take-Two Interactive Software | $39B           | N/A     | 48.7      | 11.3      | 6.1      |
| U        | Unity Software Inc.           | $8B            | N/A     | N/A       | 2.6       | 4.7      |
| APP      | AppLovin Corporation          | $145B          | 44.0    | 35.4      | 70.5      | 27.6     |
| SNAP     | Snap Inc.                     | $9B            | N/A     | N/A       | 4.0       | 1.7      |
| NFLX     | Netflix Inc.                  | $450B          | 52.0    | 35.0      | 18.0      | 11.5     |
| **RBLX** | **Roblox Corporation**        | **$42B**       | **N/A** | **N/A**   | **196.0** | **11.5** |

### 4.2 Statistiche Multipli Comparabili

**P/E:** Media=57.1, Mediana=52.0, Min=44.0, Max=75.2 (n=3)
**EV/EBITDA:** Media=39.0, Mediana=36.1, Min=35.0, Max=48.7 (n=4)
**P/B:** Media=19.1, Mediana=9.7, Min=2.6, Max=70.5 (n=6)
**EV/Sales:** Media=9.7, Mediana=6.5, Min=1.7, Max=27.6 (n=6)

### 4.3 Valori Impliciti

| Multiplo  | Valore Implicito/Azione |
| :-------- | :---------------------- |
| PE/RATIO  | $0.52                   |
| EV/EBITDA | $0.85                   |
| PB/RATIO  | $2.87                   |
| EV/SALES  | $33.69                  |
| EV/EBIT   | $0.85                   |

**Valore Mediano Multipli:** $0.85
**Upside/Downside:** -98.5%

## 6. Analisi di Sensitivita'

### 5.1 WACC vs Tasso di Crescita Terminale

Valore per azione al variare di WACC e crescita terminale:

| WACC \ Terminal Growth | 2.0%    | 2.5%    | 3.0%    | 3.5%    | 4.0%    |
| :--------------------- | :------ | :------ | :------ | :------ | :------ |
| 9.0%                   | -$11.60 | -$12.44 | -$13.41 | -$14.56 | -$15.94 |
| 10.0%                  | -$9.91  | -$10.53 | -$11.23 | -$12.04 | -$12.98 |
| 11.0%                  | -$8.60  | -$9.07  | -$9.60  | -$10.19 | -$10.87 |
| 12.0%                  | -$7.56  | -$7.93  | -$8.33  | -$8.79  | -$9.30  |
| 13.0%                  | -$6.71  | -$7.01  | -$7.33  | -$7.68  | -$8.08  |
| 14.0%                  | -$6.01  | -$6.25  | -$6.51  | -$6.79  | -$7.10  |
| 15.0%                  | -$5.42  | -$5.62  | -$5.83  | -$6.06  | -$6.31  |

### 5.2 Crescita Ricavi vs Margine Operativo

| Crescita Ricavi \ Margine Operativo | 5.0%   | 10.0%  | 15.0%  | 20.0%  | 25.0%  |
| :---------------------------------- | :----- | :----- | :----- | :----- | :----- |
| 10.0%                               | $4.30  | $7.39  | $10.48 | $13.57 | $16.65 |
| 15.0%                               | $5.63  | $9.94  | $14.26 | $18.57 | $22.88 |
| 20.0%                               | $7.49  | $13.53 | $19.57 | $25.61 | $31.65 |
| 25.0%                               | $10.07 | $18.53 | $26.98 | $35.43 | $43.89 |
| 30.0%                               | $13.64 | $25.45 | $37.25 | $49.05 | $60.86 |

## 7. Analisi per Scenari

**Scenari:**
- **Best Case** (20%): DAU supera 100M, monetizzazione ARPDAU in forte crescita, margini operativi positivi (+35%)
- **Base Case** (55%): crescita ricavi 20%, graduale miglioramento margini, path to profitability entro 2027
- **Worst Case** (25%): rallentamento DAU, pressione regolamentare child safety, margini restano negativi (-30%)

| Scenario          | Probabilita' | Valore/Azione | Contributo Ponderato |
| :---------------- | :----------- | :------------ | :------------------- |
| Best Case         | 20%          | -$14.51       | -$2.90               |
| Base Case         | 55%          | -$10.75       | -$5.91               |
| Worst Case        | 25%          | -$7.52        | -$1.88               |
| **Valore Atteso** | 100%         |               | **-$10.69**          |

**Valore Atteso Ponderato:** -$10.69

## 8. Simulazione Monte Carlo

**Parametri della simulazione:**
- Iterazioni: 10.000
- WACC: Distribuzione Normale (media=12.52%, std=1.5%)
- Crescita Alta: Distribuzione Normale (media=20%, std=5%)
- Crescita Stabile: Distribuzione Triangolare (1.5%, 2.5%, 3.5%)

## Risultati Simulazione Monte Carlo
**Simulazioni eseguite:** 10,000

| Statistica | Valore |
|-----------|--------|
| Media | -$11.14 |
| Mediana | -$10.48 |
| Dev. Standard | $3.99 |
| Minimo | -$39.52 |
| 5° Percentile | -$18.53 |
| 25° Percentile | -$13.15 |
| 75° Percentile | -$8.36 |
| 95° Percentile | -$5.98 |
| Massimo | -$2.94 |

**IC 90%:** -$18.53 - -$5.98
**IC 50%:** -$13.15 - -$8.36
**Prob. valore negativo:** 100.00%

### Distribuzione dei Valori Simulati

```
   -39.5 -    -38.1 |  (2)
   -38.1 -    -36.6 |  (1)
   -36.6 -    -35.1 |  (2)
   -35.1 -    -33.7 |  (3)
   -33.7 -    -32.2 |  (1)
   -32.2 -    -30.7 |  (3)
   -30.7 -    -29.3 |  (7)
   -29.3 -    -27.8 |  (10)
   -27.8 -    -26.3 |  (19)
   -26.3 -    -24.9 |  (25)
   -24.9 -    -23.4 | █ (46)
   -23.4 -    -22.0 | █ (65)
   -22.0 -    -20.5 | ███ (108)
   -20.5 -    -19.0 | ███ (138)
   -19.0 -    -17.6 | ███████ (249)
   -17.6 -    -16.1 | ██████████ (377)
   -16.1 -    -14.6 | ███████████████ (564)
   -14.6 -    -13.2 | ████████████████████████ (868)
   -13.2 -    -11.7 | █████████████████████████████████ (1185)
   -11.7 -    -10.3 | ███████████████████████████████████████████ (1556)
   -10.3 -     -8.8 | ██████████████████████████████████████████████████ (1777)
    -8.8 -     -7.3 | ███████████████████████████████████████████ (1562)
    -7.3 -     -5.9 | ███████████████████████████ (993)
    -5.9 -     -4.4 | ██████████ (389)
    -4.4 -     -2.9 | █ (50)
```

## 9. Sintesi Multi-Metodo e Raccomandazione

| Metodo                          | Valore/Azione | Upside/Downside | Peso |
| :------------------------------ | :------------ | :-------------- | :--- |
| DCF FCFF (3-stage)              | -$10.75       | -118.6%         | 40%  |
| Valutazione Relativa (Multipli) | $0.85         | -98.5%          | 25%  |
| Valore Atteso Scenari           | -$10.69       | -118.5%         | 15%  |
| Monte Carlo (Mediana)           | -$10.48       | -118.1%         | 20%  |

### Valore Intrinseco Stimato

| | |
|---|---|
| **Valore Medio Ponderato** | **-$7.79** |
| Prezzo Corrente | $57.79 |
| **Upside/Downside** | **-113.5%** |
| IC 90% Monte Carlo | -$18.53 - -$5.98 |

### Raccomandazione: **STRONG SELL**

> Il titolo appare fortemente sopravvalutato rispetto ai fondamentali.

## 10. Fattori di Rischio e Considerazioni

### Rischi al Rialzo

- DAU supera 100M con espansione in nuovi mercati (Asia, LatAm)
- Monetizzazione advertising in forte crescita (Roblox Ads)
- Espansione oltre il gaming: shopping, concerti, education
- Margini operativi raggiungono il positivo prima del previsto
- Partnership con brand globali per esperienze immersive

### Rischi al Ribasso

- Pressione regolamentare sulla sicurezza dei minori (child safety)
- Rallentamento della crescita DAU nei mercati maturi
- Stock-based compensation elevata ($1B+/anno) diluisce gli azionisti
- Concorrenza da Fortnite (Epic), Minecraft (MSFT), Meta Horizon
- Difficolta' nel monetizzare utenti piu' giovani (<13 anni)
- Convertible notes ($1.8B) con rischio di conversione diluente

---

### Disclaimer

*Questa analisi e' stata generata dal sistema multi-agente Valuation Analyst a scopo educativo e dimostrativo. Non costituisce consulenza finanziaria o raccomandazione di investimento. I dati finanziari utilizzati sono approssimativi e basati su informazioni pubblicamente disponibili. Consultare un consulente finanziario qualificato prima di prendere decisioni di investimento.*

---
*Report generato il 2026-03-18 dal Valuation Analyst Multi-Agent System*