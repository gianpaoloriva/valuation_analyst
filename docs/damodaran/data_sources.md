# Fonti Dati - Valuation Analyst

## 1. Massive.com (Dati Aziendali)

**URL**: [https://massive.com](https://massive.com)
**Tipo**: API REST con autenticazione Bearer token
**Configurazione**: `MASSIVE_API_KEY` in `.env`

### Endpoint Utilizzati

| Categoria | Endpoint | Descrizione |
| --- | --- | --- |
| Profilo | `/v3/reference/tickers/{ticker}` | Info azienda, market cap, shares |
| Prezzo | `/v2/aggs/ticker/{ticker}/prev` | Prezzo di chiusura |
| Treasury | `/fed/v1/treasury-yields` | Rendimento US 10Y (risk-free rate) |
| Fondamentali | `/stocks/financials/v1/*` | Income, balance, cash flow (piano premium) |

### Uso nel Progetto

- `tools/fetch_dati.py`: modulo principale per il recupero dati
  - Dati di mercato (prezzo, market cap, shares): sempre live
  - Fondamentali: live se piano premium, altrimenti fallback da `configs/{TICKER}.json`

### Fallback

Se l'API non fornisce i fondamentali (piano free), il sistema usa i valori
nella sezione `fondamentali_fallback` del config JSON del ticker. I valori
sono in milioni USD e vanno aggiornati manualmente dall'analista.

## 2. Dataset Damodaran (Parametri di Settore)

**URL**: [https://pages.stern.nyu.edu/~adamodar/](https://pages.stern.nyu.edu/~adamodar/)
**Tipo**: File Excel (.xls/.xlsx) scaricabili
**Cache**: `data/cache/` (TTL configurabile, default 24 ore)

### Dataset Disponibili

| Dataset | File | Contenuto |
| --- | --- | --- |
| Beta per Settore | Betas.xls | Beta unlevered/levered, D/E, tax rate |
| ERP e CRP | ctryprem.xlsx | Risk premium per paese |
| WACC per Settore | wacc.xlsx | WACC e componenti |
| P/E per Settore | pedata.xlsx | P/E trailing e forward |
| EV/EBITDA | vebitda.xlsx | EV/EBITDA per settore |
| P/B per Settore | pbvdata.xlsx | Price-to-Book |
| Price/Sales | psdata.xlsx | Revenue multiples |
| Margini | margin.xlsx | Margini operativi e netti |

### Uso nel Progetto

- `tools/damodaran_data.py`: download e parsing dei dataset
- `tools/data_cache.py`: gestione cache con TTL
- `utils/excel_parser.py`: parsing file Excel

### Aggiornamento

I dataset Damodaran vengono aggiornati tipicamente a gennaio di ogni anno.
La skill `/fetch-damodaran-data` scarica e aggiorna i dataset nella cache.

## 3. Configurazione Analista (configs/)

**Percorso**: `configs/{TICKER}.json`

Ogni file contiene i parametri decisi dall'analista che non sono
recuperabili automaticamente da API:

- Crescita attesa (alta e stabile)
- Rating creditizio
- Comparabili con i loro multipli
- Parametri sensitivity e scenari
- Rischi qualitativi
- Fondamentali di fallback

Vedere `configs/_template.json` per la struttura completa documentata.

## Flusso Dati Completo

```text
+------------+     +------------------+
| Massive.com| --> | tools/fetch_dati |--+
|  (API)     |     | (live + fallback)|  |
+------------+     +------------------+  |
                                         v
+------------+     +------------------+  TOOLS
| Damodaran  | --> | damodaran_data   |-->(calcoli)
| (Excel)    |     | data_cache       |  |
+------------+     +------------------+  |
                                         v
+------------+                     Report .md
|  configs/  | --> run_analysis.py --> output/markdown/
| {TICKER}.  |                     --> output/pdf/
|   json     |
+------------+
```
