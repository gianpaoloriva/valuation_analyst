# Fonti Dati - Valuation Analyst

## 1. Massive.com (Dati Aziendali)

**URL**: https://massive.com
**Tipo**: API REST con autenticazione Bearer token
**Configurazione**: `MASSIVE_API_KEY` in `.env`

### Dati Disponibili

| Categoria | Endpoint | Descrizione |
|-----------|----------|-------------|
| Profilo | `/profile/{ticker}` | Info azienda, settore, market cap |
| Conto Economico | `/income-statement/{ticker}` | Ricavi, EBIT, utile netto |
| Stato Patrimoniale | `/balance-sheet/{ticker}` | Attivo, passivo, equity |
| Cash Flow | `/cash-flow-statement/{ticker}` | CapEx, D&A, variazione WC |
| Ratios | `/ratios/{ticker}` | P/E, P/B, ROE, margini |
| Quotazioni | `/quote/{ticker}` | Prezzo corrente, volume |
| Storico Prezzi | `/historical-price/{ticker}` | OHLC giornaliero |
| Treasury | `/treasury` | Yield titoli di stato |

### Uso nel Progetto
- `tools/massive_client.py`: Client wrapper
- `tools/market_data.py`: Dati di mercato
- `tools/fundamentals.py`: Dati fondamentali

## 2. Dataset Damodaran (Parametri di Settore)

**URL**: https://pages.stern.nyu.edu/~adamodar/
**Tipo**: File Excel (.xls/.xlsx) scaricabili
**Cache**: `data/cache/` (TTL 7 giorni)

### Dataset Disponibili

| Dataset | File | Contenuto |
|---------|------|-----------|
| Beta per Settore | Betas.xls | Beta unlevered/levered, D/E, tax rate |
| ERP e CRP | ctryprem.xlsx | Risk premium per paese |
| WACC per Settore | wacc.xlsx | WACC e componenti |
| P/E per Settore | pedata.xlsx | P/E trailing e forward |
| EV/EBITDA | vebitda.xlsx | EV/EBITDA per settore |
| P/B per Settore | pbvdata.xlsx | Price-to-Book |
| Price/Sales | psdata.xlsx | Revenue multiples |
| Margini | margin.xlsx | Margini operativi e netti |
| ROE | roe.xlsx | Return on Equity |
| CapEx | capex.xlsx | CapEx e D&A per settore |
| Dividendi | divfund.xlsx | Payout e dividend yield |
| Tax Rate | taxrate.xlsx | Aliquote effettive |

### Uso nel Progetto
- `tools/damodaran_data.py`: Download e parsing
- `tools/data_cache.py`: Gestione cache
- `utils/excel_parser.py`: Parsing Excel

### Aggiornamento
I dataset Damodaran vengono aggiornati tipicamente a gennaio di ogni anno.
Lo skill `/fetch-damodaran-data` scarica e aggiorna i dataset.

## 3. Dati Sample (per Demo)

**Percorso**: `data/samples/`

| File | Contenuto |
|------|-----------|
| `apple_financials.json` | Dati finanziari Apple (3 anni) |
| `sample_comparables.json` | Comparabili settore Tech (7 aziende) |

Questi file sono committati nel repo e usati dai demo scripts.

## Flusso Dati Completo

```
┌───────────┐     ┌─────────────────┐     ┌──────────────┐
│Massive.com│────▶│ massive_client  │────▶│   Company    │
│  (API)    │     │ market_data     │     │  dataclass   │
│           │     │ fundamentals    │     │              │
└───────────┘     └─────────────────┘     └──────┬───────┘
                                                  │
┌───────────┐     ┌─────────────────┐            │
│ Damodaran │────▶│ damodaran_data  │────▶ Tools ◀┘
│ (Excel)   │     │ excel_parser    │     (calcoli)
│           │     │ data_cache      │        │
└───────────┘     └─────────────────┘        │
                                              ▼
                                     ValuationResult
```
