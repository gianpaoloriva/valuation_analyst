# Report di Valutazione - Alphabet Inc. (GOOGL)
**Data:** 2026-02-19
**Analista:** Valuation Analyst Multi-Agent System
**Metodologia:** Damodaran (NYU Stern)

---

## 1. Panoramica Aziendale

| Indicatore             | Valore                                      |
| :--------------------- | :------------------------------------------ |
| Ticker                 | GOOGL                                       |
| Settore                | Technology - Internet Content & Information |
| Paese                  | US                                          |
| Prezzo Corrente        | $178.00                                     |
| Market Cap             | $2,171.60B                                  |
| Enterprise Value       | $2,092.10B                                  |
| Azioni in Circolazione | 12,200M                                     |
| Ricavi (TTM)           | $350.00B                                    |
| EBITDA (TTM)           | $130.00B                                    |
| EBIT (TTM)             | $112.00B                                    |
| Utile Netto (TTM)      | $94.00B                                     |
| EPS                    | $7.70                                       |
| Book Value/Share       | $25.82                                      |
| Debito Totale          | $28.50B                                     |
| Cassa e Investimenti   | $108.00B                                    |
| Debito Netto           | -$79.50B                                    |
| Rating                 | AA+                                         |
| Beta                   | 1.05                                        |

## 2. Costo del Capitale (WACC)

### 2.1 Costo dell'Equity (CAPM)

**Formula CAPM:** `Re = Rf + Beta * ERP + CRP`

| Componente                              | Valore     |
| :-------------------------------------- | :--------- |
| Risk-Free Rate (US 10Y)                 | 4.30%      |
| Beta Levered                            | 1.05       |
| Beta Unlevered                          | 1.038      |
| Equity Risk Premium                     | 5.50%      |
| Premio Rischio Sistematico (Beta x ERP) | 5.78%      |
| Country Risk Premium                    | 0.00%      |
| **Costo Equity (Re)**                   | **10.08%** |

### 2.2 Costo del Debito

| Componente                | Valore    |
| :------------------------ | :-------- |
| Rating Creditizio         | AA+       |
| Default Spread            | 0.85%     |
| Costo Debito Pre-Tax (Kd) | 5.15%     |
| Tax Rate Effettivo        | 14.00%    |
| **Costo Debito Post-Tax** | **4.43%** |

### 2.3 WACC

**Formula:** `WACC = (E/V) * Re + (D/V) * Rd * (1-t)`

| Componente            | Valore     |
| :-------------------- | :--------- |
| Peso Equity (E/V)     | 98.70%     |
| Peso Debito (D/V)     | 1.30%      |
| Costo Equity (Re)     | 10.08%     |
| Costo Debito Post-Tax | 4.43%      |
| **WACC**              | **10.00%** |

> **Nota:** Alphabet ha una posizione di cassa netta di $79.50B (cassa > debito). Il peso del debito nella struttura del capitale e' minimo (1.30%), rendendo il WACC molto vicino al costo dell'equity.

## 3. Valutazione DCF (FCFF)

### 3.1 FCFF Base

**Formula:** `FCFF = EBIT*(1-t) + Deprezzamento - CapEx - Delta WC`

| Componente      | Valore (M USD) |
| :-------------- | :------------- |
| EBIT            | 112,000.00     |
| EBIT * (1-t)    | 96,320.00      |
| + Deprezzamento | 18,000.00      |
| - CapEx         | 52,000.00      |
| - Delta WC      | 2,500.00       |
| **FCFF Base**   | **59,820.00**  |

> **Nota:** Il CapEx di Alphabet ($52.00B) e' molto elevato rispetto ai ricavi (14.9%), riflettendo gli ingenti investimenti in data center e infrastruttura AI. Questo deprime il FCFF attuale ma dovrebbe generare ritorni futuri.

### 3.2 Proiezione Multi-Stage (3 fasi)

- **Fase 1 (Alta crescita):** 14% per 5 anni
- **Fase 2 (Transizione):** convergenza lineare per 5 anni
- **Fase 3 (Stabile):** 2.5% in perpetuita'
- **Tasso di sconto (WACC):** 10.00%

| Anno | Tasso Crescita | FCFF (M)   | Valore Attuale (M) |
| :--- | :------------- | :--------- | :----------------- |
| 1    | 14.00%         | 68,194.80  | 61,994.22          |
| 2    | 14.00%         | 77,742.07  | 64,247.47          |
| 3    | 14.00%         | 88,625.96  | 66,582.62          |
| 4    | 14.00%         | 101,033.60 | 69,002.63          |
| 5    | 14.00%         | 115,178.30 | 71,510.61          |
| 6    | 11.70%         | 128,654.16 | 72,614.54          |
| 7    | 9.40%          | 140,747.65 | 72,217.24          |
| 8    | 7.10%          | 150,740.74 | 70,312.14          |
| 9    | 4.80%          | 157,976.29 | 66,987.16          |
| 10   | 2.50%          | 161,925.70 | 62,418.80          |

### 3.3 Riepilogo Valutazione DCF

| Componente                   | Valore         |
| :--------------------------- | :------------- |
| VA Flussi di Cassa Espliciti | $677.89B       |
| Terminal Value (nominale)    | $2,212.44B     |
| VA Terminal Value            | $852.85B       |
| TV come % del Totale         | 0.56%          |
| **Enterprise Value**         | **$1,530.73B** |
| - Debito Netto               | -$79.50B       |
| **Equity Value**             | **$1,610.23B** |
| Azioni in Circolazione       | 12,200M        |
| **Valore per Azione (DCF)**  | **$131.99**    |
| Prezzo Corrente              | $178.00        |
| **Upside/Downside**          | **-25.9%**     |

## 4. Valutazione Relativa (Multipli)

### 4.1 Campione Comparabili

| Ticker    | Nome                  | Market Cap (B) | P/E      | EV/EBITDA | P/B     | EV/Sales |
| :-------- | :-------------------- | :------------- | :------- | :-------- | :------ | :------- |
| MSFT      | Microsoft Corporation | $3,083B        | 31.7     | 22.7      | 11.5    | 11.7     |
| META      | Meta Platforms Inc.   | $1,600B        | 27.5     | 16.0      | 9.0     | 11.5     |
| AMZN      | Amazon.com Inc.       | $2,300B        | 42.0     | 18.5      | 9.5     | 4.0      |
| AAPL      | Apple Inc.            | $3,450B        | 33.5     | 26.8      | 62.0    | 9.0      |
| SNAP      | Snap Inc.             | $25B           | N/D      | 85.0      | 12.0    | 4.5      |
| TTD       | The Trade Desk Inc.   | $55B           | 140.0    | 75.0      | 35.0    | 26.0     |
| BIDU      | Baidu Inc.            | $38B           | 11.0     | 5.5       | 0.9     | 2.0      |
| **GOOGL** | **Alphabet Inc.**     | **$2,172B**    | **23.1** | **16.1**  | **6.9** | **6.0**  |

### 4.2 Statistiche Multipli Comparabili

**P/E:** Media=47.6, Mediana=32.6, Min=11.0, Max=140.0 (n=6)
**EV/EBITDA:** Media=35.6, Mediana=22.7, Min=5.5, Max=85.0 (n=7)
**P/B:** Media=20.0, Mediana=11.5, Min=0.9, Max=62.0 (n=7)
**EV/Sales:** Media=9.8, Mediana=9.0, Min=2.0, Max=26.0 (n=7)

### 4.3 Valori Impliciti

| Multiplo  | Valore Implicito/Azione |
| :-------- | :---------------------- |
| PE/RATIO  | $251.18                 |
| EV/EBITDA | $248.40                 |
| PB/RATIO  | $296.93                 |
| EV/SALES  | $264.71                 |
| EV/EBIT   | $251.60                 |

**Valore Mediano Multipli:** $251.60
**Upside/Downside:** +41.3%

## 5. Analisi di Sensitivita'

### 5.1 WACC vs Tasso di Crescita Terminale

Valore per azione al variare di WACC e crescita terminale:

| WACC \ Terminal Growth | 1.5%    | 2.0%    | 2.5%    | 3.0%    | 3.5%    |
| :--------------------- | :------ | :------ | :------ | :------ | :------ |
| 8.0%                   | $128.26 | $137.02 | $147.36 | $159.75 | $174.87 |
| 9.0%                   | $111.07 | $117.38 | $124.65 | $133.13 | $143.13 |
| 9.5%                   | $104.10 | $109.54 | $115.75 | $122.91 | $131.25 |
| 10.0%                  | $97.96  | $102.69 | $108.05 | $114.16 | $121.20 |
| 10.5%                  | $92.51  | $96.66  | $101.32 | $106.59 | $112.60 |
| 11.0%                  | $87.65  | $91.31  | $95.39  | $99.97  | $105.16 |
| 12.0%                  | $79.33  | $82.23  | $85.42  | $88.97  | $92.92  |

### 5.2 Crescita Ricavi vs Margine Operativo

| Crescita Ricavi \ Margine Operativo | 25.0%   | 30.0%   | 32.0%   | 35.0%   | 40.0%   |
| :---------------------------------- | :------ | :------ | :------ | :------ | :------ |
| 5.0%                                | $72.62  | $90.19  | $97.22  | $107.76 | $125.34 |
| 8.0%                                | $89.73  | $111.41 | $120.09 | $133.10 | $154.79 |
| 10.0%                               | $103.52 | $128.50 | $138.49 | $153.47 | $178.45 |
| 14.0%                               | $138.21 | $171.37 | $184.63 | $204.53 | $237.68 |
| 18.0%                               | $184.80 | $228.83 | $246.44 | $272.85 | $316.88 |

## 6. Analisi per Scenari

**Scenari:**
- **Best Case** (25%): accelerazione AI (Gemini), crescita Cloud > 30%, margini in espansione (+35%)
- **Base Case** (50%): continuazione trend attuale, crescita ricavi ~14%
- **Worst Case** (25%): rallentamento ads, perdita quote ricerca, pressione regolatoria (-30%)

| Scenario          | Probabilita' | Valore/Azione | Contributo Ponderato |
| :---------------- | :----------- | :------------ | :------------------- |
| Best Case         | 25%          | $178.18       | $44.55               |
| Base Case         | 50%          | $131.99       | $65.99               |
| Worst Case        | 25%          | $92.39        | $23.10               |
| **Valore Atteso** | 100%         |               | **$133.64**          |

**Valore Atteso Ponderato:** $133.64

## 7. Simulazione Monte Carlo

**Parametri della simulazione:**
- Iterazioni: 10.000
- WACC: Distribuzione Normale (media=10.00%, std=1.2%)
- Crescita Alta: Distribuzione Normale (media=14%, std=4%)
- Crescita Stabile: Distribuzione Triangolare (1.5%, 2.5%, 3.5%)

## Risultati Simulazione Monte Carlo
**Simulazioni eseguite:** 10,000

| Statistica | Valore |
|-----------|--------|
| Media | $140.20 |
| Mediana | $133.26 |
| Dev. Standard | $41.01 |
| Minimo | $54.28 |
| 5° Percentile | $87.50 |
| 25° Percentile | $111.69 |
| 75° Percentile | $160.60 |
| 95° Percentile | $214.97 |
| Massimo | $463.87 |

**IC 90%:** $87.50 - $214.97
**IC 50%:** $111.69 - $160.60

### Distribuzione dei Valori Simulati

```
    54.3 -     70.7 | █ (57)
    70.7 -     87.1 | ███████████ (423)
    87.1 -    103.4 | ██████████████████████████████ (1158)
   103.4 -    119.8 | ███████████████████████████████████████████████ (1793)
   119.8 -    136.2 | ██████████████████████████████████████████████████ (1895)
   136.2 -    152.6 | █████████████████████████████████████████ (1589)
   152.6 -    169.0 | █████████████████████████████ (1104)
   169.0 -    185.4 | ███████████████████ (738)
   185.4 -    201.7 | ████████████ (473)
   201.7 -    218.1 | ███████ (303)
   218.1 -    234.5 | ████ (164)
   234.5 -    250.9 | ███ (118)
   250.9 -    267.3 | █ (68)
   267.3 -    283.7 | █ (44)
   283.7 -    300.0 |  (29)
   300.0 -    316.4 |  (18)
   316.4 -    332.8 |  (7)
   332.8 -    349.2 |  (6)
   349.2 -    365.6 |  (5)
   365.6 -    382.0 |  (2)
   382.0 -    398.3 |  (1)
   398.3 -    414.7 |  (2)
   414.7 -    431.1 |  (2)
   431.1 -    447.5 |  (0)
   447.5 -    463.9 |  (1)
```

## 8. Sintesi Multi-Metodo e Raccomandazione

| Metodo                          | Valore/Azione | Upside/Downside | Peso |
| :------------------------------ | :------------ | :-------------- | :--- |
| DCF FCFF (3-stage)              | $131.99       | -25.9%          | 40%  |
| Valutazione Relativa (Multipli) | $251.60       | +41.3%          | 25%  |
| Valore Atteso Scenari           | $133.64       | -24.9%          | 15%  |
| Monte Carlo (Mediana)           | $133.26       | -25.1%          | 20%  |

### Valore Intrinseco Stimato

| | |
|---|---|
| **Valore Medio Ponderato** | **$162.39** |
| Prezzo Corrente | $178.00 |
| **Upside/Downside** | **-8.8%** |
| IC 90% Monte Carlo | $87.50 - $214.97 |

### Raccomandazione: **MODERATE SELL**

> Il titolo appare moderatamente sopravvalutato rispetto al valore intrinseco.

## 9. Fattori di Rischio e Considerazioni

### Rischi al Rialzo
- Accelerazione dell'adozione di Gemini e AI products
- Google Cloud supera il 15% di quota mercato cloud globale
- YouTube diventa piattaforma dominante per streaming/TV
- Miglioramento dei margini operativi tramite efficienza AI interna
- Buyback aggressivi che riducono le azioni in circolazione

### Rischi al Ribasso
- Perdita di quote nel mercato della ricerca (AI competitors)
- Pressione regolatoria antitrust (DOJ, UE)
- Rallentamento del mercato pubblicitario digitale
- CapEx AI superiore alle attese senza ritorni proporzionali
- Competizione nel cloud da AWS e Azure
- Rischio di disruption tecnologica nel core business Search

---

### Disclaimer

*Questa analisi e' stata generata dal sistema multi-agente Valuation Analyst a scopo educativo e dimostrativo. Non costituisce consulenza finanziaria o raccomandazione di investimento. I dati finanziari utilizzati sono approssimativi e basati su informazioni pubblicamente disponibili. Consultare un consulente finanziario qualificato prima di prendere decisioni di investimento.*

---
*Report generato il 2026-02-19 dal Valuation Analyst Multi-Agent System*