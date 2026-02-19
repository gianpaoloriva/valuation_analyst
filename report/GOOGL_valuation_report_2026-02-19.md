# Report di Valutazione - Alphabet Inc. Class A Common Stock (GOOGL)
**Data:** 2026-02-19
**Analista:** Valuation Analyst Multi-Agent System
**Metodologia:** Damodaran (NYU Stern)

---

## 1. Panoramica Aziendale

| Indicatore             | Valore                                               |
| :--------------------- | :--------------------------------------------------- |
| Ticker                 | GOOGL                                                |
| Settore                | SERVICES-COMPUTER PROGRAMMING, DATA PROCESSING, ETC. |
| Paese                  | US                                                   |
| Prezzo Corrente        | $303.33                                              |
| Market Cap             | $3,669.38B                                           |
| Enterprise Value       | $3,604.66B                                           |
| Azioni in Circolazione | 12,097M                                              |
| Ricavi (TTM)           | $350.02B                                             |
| EBITDA (TTM)           | $130.64B                                             |
| EBIT (TTM)             | $112.39B                                             |
| Utile Netto (TTM)      | $100.68B                                             |
| EPS                    | $8.32                                                |
| Book Value/Share       | $26.87                                               |
| Debito Totale          | $28.50B                                              |
| Cassa e Investimenti   | $93.23B                                              |
| Debito Netto           | -$64.72B                                             |
| Rating                 | AA+                                                  |
| Beta                   | 1.05                                                 |

## 2. Costo del Capitale (WACC)

### 2.1 Costo dell'Equity (CAPM)

**Formula CAPM:** `Re = Rf + Beta * ERP + CRP`

| Componente                              | Valore    |
| :-------------------------------------- | :-------- |
| Risk-Free Rate (US 10Y)                 | 4.05%     |
| Beta Levered                            | 1.05      |
| Beta Unlevered                          | 1.043     |
| Equity Risk Premium                     | 5.50%     |
| Premio Rischio Sistematico (Beta x ERP) | 5.78%     |
| Country Risk Premium                    | 0.00%     |
| **Costo Equity (Re)**                   | **9.83%** |

### 2.2 Costo del Debito

| Componente                | Valore    |
| :------------------------ | :-------- |
| Rating Creditizio         | AA+       |
| Default Spread            | 0.85%     |
| Costo Debito Pre-Tax (Kd) | 4.90%     |
| Tax Rate Effettivo        | 14.00%    |
| **Costo Debito Post-Tax** | **4.21%** |

### 2.3 WACC

**Formula:** `WACC = (E/V) * Re + (D/V) * Rd * (1-t)`

| Componente            | Valore    |
| :-------------------- | :-------- |
| Peso Equity (E/V)     | 99.23%    |
| Peso Debito (D/V)     | 0.77%     |
| Costo Equity (Re)     | 9.83%     |
| Costo Debito Post-Tax | 4.21%     |
| **WACC**              | **9.78%** |

## 3. Valutazione DCF (FCFF)

### 3.1 FCFF Base

**Formula:** `FCFF = EBIT*(1-t) + Deprezzamento - CapEx - Delta WC`

| Componente      | Valore (M USD) |
| :-------------- | :------------- |
| EBIT            | 112,387.00     |
| EBIT * (1-t)    | 96,652.82      |
| + Deprezzamento | 18,256.00      |
| - CapEx         | 52,549.00      |
| - Delta WC      | 2,500.00       |
| **FCFF Base**   | **59,859.82**  |

### 3.2 Proiezione Multi-Stage (3 fasi)

- **Fase 1 (Alta crescita):** 14% per 5 anni
- **Fase 2 (Transizione):** convergenza lineare per 5 anni
- **Fase 3 (Stabile):** 2.5% in perpetuita'
- **Tasso di sconto (WACC):** 9.78%

| Anno | Tasso Crescita | FCFF (M)   | Valore Attuale (M) |
| :--- | :------------- | :--------- | :----------------- |
| 1    | 14.00%         | 68,240.19  | 62,159.87          |
| 2    | 14.00%         | 77,793.82  | 64,548.30          |
| 3    | 14.00%         | 88,684.96  | 67,028.50          |
| 4    | 14.00%         | 101,100.85 | 69,604.00          |
| 5    | 14.00%         | 115,254.97 | 72,278.47          |
| 6    | 11.70%         | 128,739.80 | 73,541.41          |
| 7    | 9.40%          | 140,841.34 | 73,285.68          |
| 8    | 7.10%          | 150,841.08 | 71,495.46          |
| 9    | 4.80%          | 158,081.45 | 68,251.09          |
| 10   | 2.50%          | 162,033.49 | 63,724.04          |

### 3.3 Riepilogo Valutazione DCF

| Componente                   | Valore         |
| :--------------------------- | :------------- |
| VA Flussi di Cassa Espliciti | $685.92B       |
| Terminal Value (nominale)    | $2,280.83B     |
| VA Terminal Value            | $897.00B       |
| TV come % del Totale         | 0.57%          |
| **Enterprise Value**         | **$1,582.91B** |
| - Debito Netto               | -$64.72B       |
| **Equity Value**             | **$1,647.64B** |
| Azioni in Circolazione       | 12,097M        |
| **Valore per Azione (DCF)**  | **$136.20**    |
| Prezzo Corrente              | $303.33        |
| **Upside/Downside**          | **-55.1%**     |

## 4. Valutazione Relativa (Multipli)

### 4.1 Campione Comparabili

| Ticker    | Nome                                   | Market Cap (B) | P/E      | EV/EBITDA | P/B      | EV/Sales |
| :-------- | :------------------------------------- | :------------- | :------- | :-------- | :------- | :------- |
| MSFT      | Microsoft Corporation                  | $3,083B        | 31.7     | 22.7      | 11.5     | 11.7     |
| META      | Meta Platforms Inc.                    | $1,600B        | 27.5     | 16.0      | 9.0      | 11.5     |
| AMZN      | Amazon.com Inc.                        | $2,300B        | 42.0     | 18.5      | 9.5      | 4.0      |
| AAPL      | Apple Inc.                             | $3,450B        | 33.5     | 26.8      | 62.0     | 9.0      |
| SNAP      | Snap Inc.                              | $25B           | N/D      | 85.0      | 12.0     | 4.5      |
| TTD       | The Trade Desk Inc.                    | $55B           | 140.0    | 75.0      | 35.0     | 26.0     |
| BIDU      | Baidu Inc.                             | $38B           | 11.0     | 5.5       | 0.9      | 2.0      |
| **GOOGL** | **Alphabet Inc. Class A Common Stock** | **$3,669B**    | **36.4** | **27.6**  | **11.3** | **10.3** |

### 4.2 Statistiche Multipli Comparabili

**P/E:** Media=47.6, Mediana=32.6, Min=11.0, Max=140.0 (n=6)
**EV/EBITDA:** Media=35.6, Mediana=22.7, Min=5.5, Max=85.0 (n=7)
**P/B:** Media=20.0, Mediana=11.5, Min=0.9, Max=62.0 (n=7)
**EV/Sales:** Media=9.8, Mediana=9.0, Min=2.0, Max=26.0 (n=7)

### 4.3 Valori Impliciti

| Multiplo  | Valore Implicito/Azione |
| :-------- | :---------------------- |
| PE/RATIO  | $271.32                 |
| EV/EBITDA | $250.50                 |
| PB/RATIO  | $309.04                 |
| EV/SALES  | $265.76                 |
| EV/EBIT   | $253.74                 |

**Valore Mediano Multipli:** $265.76
**Upside/Downside:** -12.4%

## 5. Analisi di Sensitivita'

### 5.1 WACC vs Tasso di Crescita Terminale

Valore per azione al variare di WACC e crescita terminale:

| WACC \ Terminal Growth | 1.5%    | 2.0%    | 2.5%    | 3.0%    | 3.5%    |
| :--------------------- | :------ | :------ | :------ | :------ | :------ |
| 8.0%                   | $128.22 | $137.05 | $147.48 | $159.99 | $175.25 |
| 9.0%                   | $110.86 | $117.23 | $124.57 | $133.13 | $143.22 |
| 9.5%                   | $103.83 | $109.32 | $115.59 | $122.81 | $131.23 |
| 10.0%                  | $97.63  | $102.41 | $107.82 | $113.98 | $121.09 |
| 10.5%                  | $92.14  | $96.32  | $101.02 | $106.34 | $112.41 |
| 11.0%                  | $87.23  | $90.92  | $95.04  | $99.67  | $104.90 |
| 12.0%                  | $78.83  | $81.76  | $84.98  | $88.56  | $92.55  |

### 5.2 Crescita Ricavi vs Margine Operativo

| Crescita Ricavi \ Margine Operativo | 25.0%   | 30.0%   | 32.0%   | 35.0%   | 40.0%   |
| :---------------------------------- | :------ | :------ | :------ | :------ | :------ |
| 5.0%                                | $73.83  | $92.00  | $99.27  | $110.17 | $128.34 |
| 8.0%                                | $91.68  | $114.13 | $123.11 | $136.58 | $159.04 |
| 10.0%                               | $106.08 | $131.95 | $142.31 | $157.83 | $183.71 |
| 14.0%                               | $142.30 | $176.70 | $190.47 | $211.11 | $245.52 |
| 18.0%                               | $190.98 | $236.72 | $255.02 | $282.47 | $328.21 |

## 6. Analisi per Scenari

**Scenari:**
- **Best Case** (25%): accelerazione AI (Gemini), crescita Cloud > 30%, margini in espansione (+35%)
- **Base Case** (50%): continuazione trend attuale, crescita ricavi ~14%
- **Worst Case** (25%): rallentamento ads, perdita quote ricerca, pressione regolatoria (-30%)

| Scenario          | Probabilita' | Valore/Azione | Contributo Ponderato |
| :---------------- | :----------- | :------------ | :------------------- |
| Best Case         | 25%          | $183.87       | $45.97               |
| Base Case         | 50%          | $136.20       | $68.10               |
| Worst Case        | 25%          | $95.34        | $23.84               |
| **Valore Atteso** | 100%         |               | **$137.90**          |

**Valore Atteso Ponderato:** $137.90

## 7. Simulazione Monte Carlo

**Parametri della simulazione:**
- Iterazioni: 10.000
- WACC: Distribuzione Normale (media=9.78%, std=1.2%)
- Crescita Alta: Distribuzione Normale (media=14%, std=4%)
- Crescita Stabile: Distribuzione Triangolare (1.5%, 2.5%, 3.5%)

## Risultati Simulazione Monte Carlo
**Simulazioni eseguite:** 10,000

| Statistica | Valore |
|-----------|--------|
| Media | $145.13 |
| Mediana | $137.64 |
| Dev. Standard | $43.78 |
| Minimo | $54.54 |
| 5° Percentile | $89.35 |
| 25° Percentile | $114.80 |
| 75° Percentile | $166.57 |
| 95° Percentile | $224.55 |
| Massimo | $518.59 |

**IC 90%:** $89.35 - $224.55
**IC 50%:** $114.80 - $166.57

### Distribuzione dei Valori Simulati

```
    54.5 -     73.1 | █ (71)
    73.1 -     91.7 | █████████████ (530)
    91.7 -    110.2 | ████████████████████████████████████ (1450)
   110.2 -    128.8 | ██████████████████████████████████████████████████ (1996)
   128.8 -    147.3 | ███████████████████████████████████████████████ (1906)
   147.3 -    165.9 | █████████████████████████████████████ (1512)
   165.9 -    184.5 | ████████████████████████ (962)
   184.5 -    203.0 | ███████████████ (612)
   203.0 -    221.6 | ██████████ (402)
   221.6 -    240.2 | █████ (212)
   240.2 -    258.7 | ███ (134)
   258.7 -    277.3 | ██ (86)
   277.3 -    295.8 | █ (46)
   295.8 -    314.4 |  (34)
   314.4 -    333.0 |  (19)
   333.0 -    351.5 |  (8)
   351.5 -    370.1 |  (5)
   370.1 -    388.7 |  (6)
   388.7 -    407.2 |  (2)
   407.2 -    425.8 |  (2)
   425.8 -    444.3 |  (3)
   444.3 -    462.9 |  (1)
   462.9 -    481.5 |  (0)
   481.5 -    500.0 |  (0)
   500.0 -    518.6 |  (1)
```

## 8. Sintesi Multi-Metodo e Raccomandazione

| Metodo                          | Valore/Azione | Upside/Downside | Peso |
| :------------------------------ | :------------ | :-------------- | :--- |
| DCF FCFF (3-stage)              | $136.20       | -55.1%          | 40%  |
| Valutazione Relativa (Multipli) | $265.76       | -12.4%          | 25%  |
| Valore Atteso Scenari           | $137.90       | -54.5%          | 15%  |
| Monte Carlo (Mediana)           | $137.64       | -54.6%          | 20%  |

### Valore Intrinseco Stimato

| | |
|---|---|
| **Valore Medio Ponderato** | **$169.13** |
| Prezzo Corrente | $303.33 |
| **Upside/Downside** | **-44.2%** |
| IC 90% Monte Carlo | $89.35 - $224.55 |

### Raccomandazione: **STRONG SELL**

> Il titolo appare fortemente sopravvalutato rispetto ai fondamentali.

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