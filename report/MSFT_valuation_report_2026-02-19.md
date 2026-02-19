# Report di Valutazione - Microsoft Corporation (MSFT)
**Data:** 2026-02-19
**Analista:** Valuation Analyst Multi-Agent System
**Metodologia:** Damodaran (NYU Stern)

---

## 1. Panoramica Aziendale

| Indicatore             | Valore                |
| :--------------------- | :-------------------- |
| Ticker                 | MSFT                  |
| Settore                | Technology - Software |
| Paese                  | US                    |
| Prezzo Corrente        | $415.00               |
| Market Cap             | $3,083.45B            |
| Enterprise Value       | $3,062.45B            |
| Azioni in Circolazione | 7,430M                |
| Ricavi (TTM)           | $261.80B              |
| EBITDA (TTM)           | $135.20B              |
| EBIT (TTM)             | $118.50B              |
| Utile Netto (TTM)      | $97.20B               |
| EPS                    | $13.08                |
| Book Value/Share       | $36.14                |
| Debito Totale          | $59.00B               |
| Cassa                  | $80.00B               |
| Debito Netto           | -$21.00B              |
| Rating                 | AAA                   |
| Beta                   | 0.95                  |

## 2. Costo del Capitale (WACC)

### 2.1 Costo dell'Equity (CAPM)

**Formula CAPM:** `Re = Rf + Beta * ERP + CRP`

| Componente                              | Valore    |
| :-------------------------------------- | :-------- |
| Risk-Free Rate (US 10Y)                 | 4.30%     |
| Beta Levered                            | 0.95      |
| Beta Unlevered                          | 0.935     |
| Equity Risk Premium                     | 5.50%     |
| Premio Rischio Sistematico (Beta x ERP) | 5.22%     |
| Country Risk Premium                    | 0.00%     |
| **Costo Equity (Re)**                   | **9.53%** |

### 2.2 Costo del Debito

| Componente                | Valore    |
| :------------------------ | :-------- |
| Rating Creditizio         | AAA       |
| Default Spread            | 0.75%     |
| Costo Debito Pre-Tax (Kd) | 5.05%     |
| Tax Rate Effettivo        | 18.00%    |
| **Costo Debito Post-Tax** | **4.14%** |

### 2.3 WACC

**Formula:** `WACC = (E/V) * Re + (D/V) * Rd * (1-t)`

| Componente            | Valore    |
| :-------------------- | :-------- |
| Peso Equity (E/V)     | 98.12%    |
| Peso Debito (D/V)     | 1.88%     |
| Costo Equity (Re)     | 9.53%     |
| Costo Debito Post-Tax | 4.14%     |
| **WACC**              | **9.42%** |

## 3. Valutazione DCF (FCFF)

### 3.1 FCFF Base

**Formula:** `FCFF = EBIT*(1-t) + Deprezzamento - CapEx - Delta WC`

| Componente      | Valore (M USD) |
| :-------------- | :------------- |
| EBIT            | 118,500.00     |
| EBIT * (1-t)    | 97,170.00      |
| + Deprezzamento | 16,700.00      |
| - CapEx         | 44,500.00      |
| - Delta WC      | 3,200.00       |
| **FCFF Base**   | **66,170.00**  |

### 3.2 Proiezione Multi-Stage (3 fasi)

- **Fase 1 (Alta crescita):** 12% per 5 anni
- **Fase 2 (Transizione):** convergenza lineare per 5 anni
- **Fase 3 (Stabile):** 2.5% in perpetuita'
- **Tasso di sconto (WACC):** 9.42%

| Anno | Tasso Crescita | FCFF (M)   | Valore Attuale (M) |
| :--- | :------------- | :--------- | :----------------- |
| 1    | 12.00%         | 74,110.40  | 67,727.79          |
| 2    | 12.00%         | 83,003.65  | 69,322.26          |
| 3    | 12.00%         | 92,964.09  | 70,954.26          |
| 4    | 12.00%         | 104,119.78 | 72,624.68          |
| 5    | 12.00%         | 116,614.15 | 74,334.43          |
| 6    | 10.10%         | 128,392.18 | 74,793.71          |
| 7    | 8.20%          | 138,920.34 | 73,957.14          |
| 8    | 6.30%          | 147,672.32 | 71,845.76          |
| 9    | 4.40%          | 154,169.90 | 68,547.14          |
| 10   | 2.50%          | 158,024.15 | 64,209.75          |

### 3.3 Riepilogo Valutazione DCF

| Componente                   | Valore         |
| :--------------------------- | :------------- |
| VA Flussi di Cassa Espliciti | $708.32B       |
| Terminal Value (nominale)    | $2,339.35B     |
| VA Terminal Value            | $950.55B       |
| TV come % del Totale         | 0.57%          |
| **Enterprise Value**         | **$1,658.86B** |
| - Debito Netto               | -$21.00B       |
| **Equity Value**             | **$1,679.86B** |
| Azioni in Circolazione       | 7,430M         |
| **Valore per Azione (DCF)**  | **$226.09**    |
| Prezzo Corrente              | $415.00        |
| **Upside/Downside**          | **-45.5%**     |

## 4. Valutazione Relativa (Multipli)

### 4.1 Campione Comparabili

| Ticker   | Nome                      | Market Cap (B) | P/E      | EV/EBITDA | P/B      | EV/Sales |
| :------- | :------------------------ | :------------- | :------- | :-------- | :------- | :------- |
| AAPL     | Apple Inc.                | $3,450B        | 33.5     | 26.8      | 62.0     | 9.0      |
| GOOGL    | Alphabet Inc.             | $2,150B        | 24.0     | 17.5      | 7.8      | 7.2      |
| AMZN     | Amazon.com Inc.           | $2,300B        | 42.0     | 18.5      | 9.5      | 4.0      |
| META     | Meta Platforms Inc.       | $1,600B        | 27.5     | 16.0      | 9.0      | 11.5     |
| NVDA     | NVIDIA Corporation        | $3,200B        | 55.0     | 45.0      | 52.0     | 38.0     |
| ORCL     | Oracle Corporation        | $480B          | 38.0     | 22.0      | 28.0     | 9.5      |
| CRM      | Salesforce Inc.           | $310B          | 48.0     | 26.0      | 4.8      | 9.2      |
| **MSFT** | **Microsoft Corporation** | **$3,083B**    | **31.7** | **22.7**  | **11.5** | **11.7** |

### 4.2 Statistiche Multipli Comparabili

**P/E:** Media=38.3, Mediana=38.0, Min=24.0, Max=55.0 (n=7)
**EV/EBITDA:** Media=24.5, Mediana=22.0, Min=16.0, Max=45.0 (n=7)
**P/B:** Media=24.7, Mediana=9.5, Min=4.8, Max=62.0 (n=7)
**EV/Sales:** Media=12.6, Mediana=9.2, Min=4.0, Max=38.0 (n=7)

### 4.3 Valori Impliciti

| Multiplo  | Valore Implicito/Azione |
| :-------- | :---------------------- |
| PE/RATIO  | $497.12                 |
| EV/EBITDA | $403.15                 |
| PB/RATIO  | $343.30                 |
| EV/SALES  | $326.99                 |
| EV/EBIT   | $461.38                 |

**Valore Mediano Multipli:** $403.15
**Upside/Downside:** -2.9%

## 5. Analisi di Sensitivita'

### 5.1 WACC vs Tasso di Crescita Terminale

Valore per azione al variare di WACC e crescita terminale:

| WACC \ Terminal Growth | 1.5%    | 2.0%    | 2.5%    | 3.0%    | 3.5%    |
| :--------------------- | :------ | :------ | :------ | :------ | :------ |
| 7.0%                   | $247.79 | $269.25 | $295.44 | $328.15 | $370.17 |
| 8.0%                   | $208.42 | $223.10 | $240.42 | $261.17 | $286.51 |
| 8.5%                   | $192.98 | $205.37 | $219.81 | $236.85 | $257.27 |
| 9.0%                   | $179.62 | $190.20 | $202.39 | $216.60 | $233.36 |
| 9.5%                   | $167.94 | $177.07 | $187.48 | $199.48 | $213.45 |
| 10.0%                  | $157.65 | $165.59 | $174.57 | $184.82 | $196.63 |
| 11.0%                  | $140.36 | $146.50 | $153.35 | $161.04 | $169.74 |

### 5.2 Crescita Ricavi vs Margine Operativo

| Crescita Ricavi \ Margine Operativo | 35.0%   | 40.0%   | 45.0%   | 50.0%   | 55.0%   |
| :---------------------------------- | :------ | :------ | :------ | :------ | :------ |
| 5.0%                                | $126.76 | $148.75 | $170.74 | $192.74 | $214.73 |
| 8.0%                                | $158.64 | $185.87 | $213.11 | $240.35 | $267.58 |
| 10.0%                               | $184.33 | $215.76 | $247.19 | $278.63 | $310.06 |
| 12.0%                               | $214.20 | $250.49 | $286.77 | $323.06 | $359.35 |
| 15.0%                               | $268.23 | $313.24 | $358.25 | $403.26 | $448.27 |

## 6. Analisi per Scenari

**Scenari:**
- **Best Case** (20%): crescita AI/Cloud superiore, margini in espansione (+30%)
- **Base Case** (55%): continuazione trend attuale
- **Worst Case** (25%): rallentamento macro, pressione competitiva (-25%)

| Scenario          | Probabilita' | Valore/Azione | Contributo Ponderato |
| :---------------- | :----------- | :------------ | :------------------- |
| Best Case         | 20%          | $293.92       | $58.78               |
| Base Case         | 55%          | $226.09       | $124.35              |
| Worst Case        | 25%          | $169.57       | $42.39               |
| **Valore Atteso** | 100%         |               | **$225.53**          |

**Valore Atteso Ponderato:** $225.53

## 7. Simulazione Monte Carlo

**Parametri della simulazione:**
- Iterazioni: 10.000
- WACC: Distribuzione Normale (media=WACC calcolato, std=1%)
- Crescita Alta: Distribuzione Normale (media=12%, std=3%)
- Crescita Stabile: Distribuzione Triangolare (1.5%, 2.5%, 3.5%)

## Risultati Simulazione Monte Carlo
**Simulazioni eseguite:** 10,000

| Statistica | Valore |
|-----------|--------|
| Media | $236.71 |
| Mediana | $227.75 |
| Dev. Standard | $58.45 |
| Minimo | $103.09 |
| 5° Percentile | $159.11 |
| 25° Percentile | $196.15 |
| 75° Percentile | $267.11 |
| 95° Percentile | $344.67 |
| Massimo | $648.84 |

**IC 90%:** $159.11 - $344.67
**IC 50%:** $196.15 - $267.11

### Distribuzione dei Valori Simulati

```
   103.1 -    124.9 |  (26)
   124.9 -    146.7 | █████ (195)
   146.7 -    168.6 | ██████████████████ (618)
   168.6 -    190.4 | █████████████████████████████████████ (1282)
   190.4 -    212.2 | ███████████████████████████████████████████████ (1636)
   212.2 -    234.1 | ██████████████████████████████████████████████████ (1707)
   234.1 -    255.9 | ███████████████████████████████████████████ (1482)
   255.9 -    277.7 | ██████████████████████████████ (1026)
   277.7 -    299.6 | ████████████████████ (716)
   299.6 -    321.4 | ██████████████ (487)
   321.4 -    343.2 | █████████ (312)
   343.2 -    365.1 | █████ (190)
   365.1 -    386.9 | ███ (115)
   386.9 -    408.7 | ██ (84)
   408.7 -    430.5 | █ (40)
   430.5 -    452.4 | █ (36)
   452.4 -    474.2 |  (22)
   474.2 -    496.0 |  (5)
   496.0 -    517.9 |  (6)
   517.9 -    539.7 |  (6)
   539.7 -    561.5 |  (4)
   561.5 -    583.4 |  (2)
   583.4 -    605.2 |  (1)
   605.2 -    627.0 |  (1)
   627.0 -    648.8 |  (1)
```

## 8. Sintesi Multi-Metodo e Raccomandazione

| Metodo                          | Valore/Azione | Upside/Downside | Peso |
| :------------------------------ | :------------ | :-------------- | :--- |
| DCF FCFF (3-stage)              | $226.09       | -45.5%          | 40%  |
| Valutazione Relativa (Multipli) | $403.15       | -2.9%           | 25%  |
| Valore Atteso Scenari           | $225.53       | -45.7%          | 15%  |
| Monte Carlo (Mediana)           | $227.75       | -45.1%          | 20%  |

### Valore Intrinseco Stimato

| | |
|---|---|
| **Valore Medio Ponderato** | **$270.60** |
| Prezzo Corrente | $415.00 |
| **Upside/Downside** | **-34.8%** |
| IC 90% Monte Carlo | $159.11 - $344.67 |

### Raccomandazione: **SELL**

> Il titolo appare significativamente sopravvalutato.

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