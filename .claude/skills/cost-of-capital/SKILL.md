---
name: cost-of-capital
description: Calcola il costo del capitale (WACC, CAPM, beta) per un'azienda seguendo la metodologia Damodaran
user_invocable: true
---

# Skill: Calcolo Costo del Capitale (Damodaran)

Calcola WACC, costo equity (CAPM) e costo debito per un'azienda, utilizzando il metodo
bottom-up per il beta e gli spread per rating per il costo del debito, secondo la
metodologia di Aswath Damodaran.

## Utilizzo

```
/cost-of-capital AAPL
/cost-of-capital ENEL.MI
/cost-of-capital AAPL --paese IT --settore "Utilities"
```

---

## Vincoli Critici

Leggere PRIMA di iniziare qualsiasi calcolo:

1. **Beta bottom-up preferito a regressione** — la regressione ha errore standard elevato ed e' backward-looking
2. **Pesi D/E a valori di MERCATO, non contabili** — book value distorce sistematicamente il WACC
3. **Risk-free nella stessa valuta dei cash flow** — US Treasury per USD, BTP/Bund per EUR
4. **MAI doppio conteggio del CRP** — se il CRP e' gia' incluso nell'ERP (es. ERP Italia 7%), non aggiungerlo separatamente
5. **Tax rate effettivo, non marginale** — per lo scudo fiscale del debito usare l'aliquota effettivamente pagata
6. **Beta negativo richiede giustificazione** — verificare che non sia un artefatto statistico
7. **WACC deve essere ragionevole** — tipicamente 6-12% per large cap mercati sviluppati; fuori range, ricontrollare

---

## Processo di Calcolo

### Step 1: Risk-Free Rate (Rf)

Il risk-free rate e' il rendimento di un investimento a rischio zero nella valuta dell'analisi.

**Regole di selezione:**

| Valuta | Strumento | Fonte |
|--------|-----------|-------|
| USD | US Treasury 10Y | Massive.com API / Fed |
| EUR (Italia) | BTP 10Y | Massive.com API / Banca d'Italia |
| EUR (Germania) | Bund 10Y | Massive.com API / Bundesbank |
| GBP | UK Gilt 10Y | Massive.com API / BoE |

**Principi:**
- Usare il titolo governativo a 10 anni nella valuta dei cash flow
- Per l'Italia: BTP 10Y (include il rischio sovrano italiano)
- Se si usa il Bund come base, aggiungere il CRP separatamente
- Il Rf deve essere coerente con l'ERP utilizzato (stesso mercato di riferimento)

> **CHECKPOINT**: Mostrare Rf selezionato, fonte, e data di riferimento.

---

### Step 2: Beta

**Metodo Bottom-Up (preferito da Damodaran):**

1. Identificare il settore/industria dell'azienda
2. Ottenere il beta unlevered di settore dal dataset Damodaran (`betas.xlsx`)
3. Relevare per il D/E target dell'azienda:

```
Beta_Levered = Beta_Unlevered * (1 + (1 - t) * D/E)
```

Per deleverare un beta osservato:
```
Beta_Unlevered = Beta_Levered / (1 + (1 - t) * D/E)
```

**Metodo di Regressione (alternativa — solo come sanity check):**
- Regressione rendimenti azione vs rendimenti indice di mercato
- Periodo: 5 anni, frequenza mensile (60 osservazioni)
- R² tipicamente basso (0.2-0.4) — alta incertezza
- Usare solo per confronto, non come input primario

**Beta per aziende multi-settore:**
```
Beta_U_azienda = Σ (peso_settore_i * Beta_U_settore_i)
```
Pesare per ricavi o asset di ciascun segmento.

**Valori tipici per settore (Damodaran):**

| Settore | Beta Unlevered | Beta Levered tipico |
|---------|---------------|-------------------|
| Technology | 1.10-1.30 | 1.20-1.50 |
| Utilities | 0.30-0.50 | 0.50-0.70 |
| Healthcare | 0.80-1.00 | 0.90-1.10 |
| Financials | 0.50-0.70 | 0.80-1.20 |
| Consumer Staples | 0.60-0.80 | 0.70-0.90 |
| Energy | 0.80-1.00 | 1.00-1.30 |
| Industrials | 0.80-1.00 | 0.90-1.20 |

> **CHECKPOINT**: Mostrare Beta unlevered di settore, D/E utilizzato, e Beta levered calcolato.
> Se il beta differisce significativamente da quello di regressione, segnalare.

---

### Step 3: Equity Risk Premium (ERP) e Country Risk Premium (CRP)

**ERP — Equity Risk Premium:**
- ERP base mercato maturo (USA): ~5.5% (stima Damodaran, aggiornata annualmente)
- Fonte: Dataset Damodaran `ctryprem.xlsx`

**CRP — Country Risk Premium:**
```
CRP = Default Spread Paese * (Sigma_equity / Sigma_bond)
```
Approssimazione Damodaran: `CRP ≈ Default Spread * 1.5`

**Approccio combinato per paese:**

| Paese | Rf | ERP | CRP | Note |
|-------|-----|-----|-----|------|
| USA | US 10Y (~4.2%) | 5.5% | 0% | Mercato maturo, nessun CRP |
| Italia (metodo BTP) | BTP 10Y (~3.8%) | 7% | Incluso | CRP gia' nel Rf e ERP |
| Italia (metodo Bund) | Bund 10Y (~2.5%) | 5.5% | ~1.5% | CRP separato |
| UK | Gilt 10Y | 5.5% | 0% | Mercato maturo |
| Brasile | Treasury BR 10Y | 5.5% | ~3.0% | Mercato emergente |

**ATTENZIONE doppio conteggio:**
- Se si usa BTP come Rf: il rischio Italia e' gia' nel tasso. Usare ERP ~7% che include il CRP.
  NON aggiungere un CRP separato.
- Se si usa Bund come Rf: il rischio Italia NON e' nel tasso. Usare ERP ~5.5% + CRP ~1.5%.
- I due approcci devono dare risultati simili. Se divergono > 0.5%, ricontrollare.

> **CHECKPOINT**: Mostrare ERP, CRP (se applicabile), e metodo utilizzato.
> Confermare che non c'e' doppio conteggio.

---

### Step 4: Costo Equity (Re) — CAPM

```
Re = Rf + Beta_Levered * ERP + CRP
```

Se si usa il metodo BTP per l'Italia (CRP incluso nell'ERP):
```
Re = Rf_BTP + Beta_Levered * ERP_Italia
```

**Verifica di ragionevolezza:**

| Tipo azienda | Re tipico |
|-------------|-----------|
| Large cap USA, basso rischio | 8-10% |
| Large cap USA, medio rischio | 10-12% |
| Mid cap USA | 11-14% |
| Large cap Italia | 10-13% |
| Mid cap Italia | 12-16% |
| Emergenti | 14-20% |

Se Re e' fuori dal range tipico per il profilo dell'azienda, ricontrollare gli input.

> **CHECKPOINT**: Mostrare calcolo Re passo per passo: Rf + Beta * ERP (+ CRP).

---

### Step 5: Costo del Debito (Rd)

**Metodo da rating creditizio (preferito):**
```
Rd_pre_tax = Rf + Default Spread (da rating)
Rd_post_tax = Rd_pre_tax * (1 - t)
```

**Tabella spread per rating (Damodaran):**

| Rating | Spread su Rf | Rd pre-tax indicativo (US) |
|--------|-------------|--------------------------|
| AAA | +0.75% | ~5.0% |
| AA+ | +0.85% | ~5.1% |
| AA | +1.00% | ~5.2% |
| AA- | +1.10% | ~5.3% |
| A+ | +1.15% | ~5.4% |
| A | +1.25% | ~5.5% |
| A- | +1.40% | ~5.6% |
| BBB+ | +1.75% | ~6.0% |
| BBB | +2.00% | ~6.2% |
| BBB- | +2.50% | ~6.7% |
| BB+ | +3.00% | ~7.2% |
| BB | +3.50% | ~7.7% |
| B+ | +4.00% | ~8.2% |
| B | +5.00% | ~9.2% |
| B- | +6.00% | ~10.2% |
| CCC+ | +7.00% | ~11.2% |
| CCC | +8.00% | ~12.2% |
| CC | +10.00% | ~14.2% |
| D | +12.00% | ~16.2% |

**Metodo da interest coverage (se rating non disponibile):**
```
Interest Coverage = EBIT / Interessi Passivi
```

| Interest Coverage | Rating Implicito |
|-------------------|-----------------|
| > 12.5 | AAA |
| 9.5 - 12.5 | AA |
| 7.5 - 9.5 | A+ |
| 6.0 - 7.5 | A |
| 4.5 - 6.0 | A- |
| 3.5 - 4.5 | BBB |
| 3.0 - 3.5 | BB+ |
| 2.5 - 3.0 | BB |
| 2.0 - 2.5 | B+ |
| 1.5 - 2.0 | B |
| 1.0 - 1.5 | B- |
| 0.5 - 1.0 | CCC |
| < 0.5 | D |

**Metodo effettivo (sanity check):**
```
Rd_effettivo = Interessi Pagati / Debito Totale Medio
```

**Scudo fiscale:**
- US: `t = 25%` (corporate tax rate)
- Italia: `t = 27.9%` (IRES 24% + IRAP 3.9%)
- IRAP: deducibilita' limitata degli interessi (art. 96 TUIR: max 30% ROL)

> **CHECKPOINT**: Mostrare rating utilizzato, spread, Rd pre e post-tax.

---

### Step 6: WACC — Weighted Average Cost of Capital

```
WACC = (E/V) * Re + (D/V) * Rd * (1 - t)
```

**Pesi del capitale:**
- **E** = Market Cap (valore di mercato dell'equity)
- **D** = Valore di mercato del debito (approssimabile con book value per investment grade)
- **V** = E + D

**MAI usare book value per l'equity** — market cap e' l'unica misura corretta.
Per il debito, il book value e' una buona approssimazione se il rating e' investment grade
e i tassi non sono cambiati drasticamente dall'emissione.

**Output finale — tabella riepilogativa:**

| Componente | Valore |
|-----------|--------|
| Risk-Free Rate (Rf) | X.XX% |
| Beta Unlevered (settore) | X.XX |
| D/E (market value) | X.XX |
| Beta Levered | X.XX |
| ERP | X.XX% |
| Country Risk Premium | X.XX% |
| **Costo Equity (Re)** | **X.XX%** |
| Rating credito | XXX |
| Default spread | X.XX% |
| Costo Debito pre-tax (Rd) | X.XX% |
| Tax rate | X.XX% |
| Costo Debito post-tax | X.XX% |
| Peso Equity (E/V) | X.XX% |
| Peso Debito (D/V) | X.XX% |
| **WACC** | **X.XX%** |

**Verifica di ragionevolezza:**

| Tipo azienda | WACC tipico |
|-------------|------------|
| Large cap USA | 8-10% |
| Large cap Europa | 7-9% |
| Mid cap | 9-12% |
| High yield / Distressed | 12-18% |
| Utilities regolate | 5-7% |

> **CHECKPOINT FINALE**: Mostrare tabella completa. Se WACC fuori range tipico, spiegare perche'.
> Chiedere conferma prima di passare il WACC al calcolo DCF.

---

## Errori Comuni

| Errore | Perche' e' grave | Come evitarlo |
|--------|-----------------|---------------|
| Usare book value per i pesi D/E | Distorce WACC, spesso sovrastima il peso del debito | Sempre market cap per equity |
| Doppio conteggio CRP | Re inflazionato, valore intrinseco sottostimato | Se Rf = BTP, CRP e' gia' incluso |
| Beta di regressione come unico input | Errore standard alto, R² basso | Usare bottom-up, regressione come check |
| Beta negativo senza verifica | Spesso artefatto di bassa liquidita' o periodo anomalo | Investigare, usare bottom-up |
| Risk-free in valuta diversa dai CF | Incoerenza valutaria che invalida il CAPM | Rf nella valuta dei cash flow |
| Tax rate marginale per scudo fiscale | Sovrastima il beneficio fiscale del debito | Usare tax rate effettivo |
| Ignorare le preferred shares | Distorce la struttura del capitale | Trattare come componente separata o come debito |
| WACC costante con leverage che cambia | Se l'azienda sta deleveraging, il WACC cala nel tempo | Usare WACC target o ricalibrare per fase |

---

## Parametri per Paese

| Parametro | US | Italia |
|-----------|-----|--------|
| Risk-free rate | US 10Y Treasury (~4.2%) | BTP 10Y (~3.8%) |
| ERP | 5.5% | 7% (include CRP ~1.5%) |
| CRP | 0% | Incluso nell'ERP se Rf=BTP |
| Tax rate (corporate) | 25% | 27.9% (IRES 24% + IRAP 3.9%) |
| Deducibilita' interessi | Limitata (§163(j): 30% EBITDA) | Art. 96 TUIR: 30% ROL |
| Costo debito base | SOFR + spread | Euribor + spread |
| Beta mercato | S&P 500 | FTSE MIB |
| Dataset Damodaran | Diretto (US-centric) | Con aggiustamento CRP |

---

## Metodologia CAPM e WACC — Riferimento Completo (Damodaran)

### CAPM — Assunzioni e Limiti

Il Capital Asset Pricing Model assume:
- Investitori diversificati (solo rischio sistematico prezzato)
- Mercati efficienti (prezzi riflettono informazione disponibile)
- Un unico fattore di rischio (il mercato)

Limiti noti: non cattura rischi di liquidita', dimensione, momentum. Per aziende private
o poco liquide, considerare il Total Beta (skill `private-valuation`).

### WACC — Quando Non Usarlo

- **Aziende finanziarie** (banche, assicurazioni): il debito e' materia prima, non finanziamento.
  Usare FCFE scontato al costo equity.
- **Leverage in rapido cambiamento**: il WACC assume struttura capitale stabile.
  Se l'azienda sta facendo deleveraging massiccio, usare APV (Adjusted Present Value).
- **Aziende in distress**: il costo del debito e' molto alto e instabile.
  Considerare la skill `option-valuation` (equity come opzione).

### Fonti Dati Damodaran

| Dataset | Contenuto |
|---------|-----------|
| `betas.xlsx` | Beta unlevered/levered per settore |
| `ctryprem.xlsx` | ERP e CRP per paese |
| `wacc.xlsx` | WACC e componenti per settore |
| `ratings.xlsx` | Spread per rating |

Tutti disponibili su: https://pages.stern.nyu.edu/~adamodar/

---

## Note Operative

- **MAI creare script .py ad-hoc**. Usare SEMPRE `run_analysis.py`
- Il WACC calcolato qui e' l'input per la skill `dcf-valuation`
- Per la sensitivity sul WACC, invocare la skill `sensitivity-analysis`
- Il rating credito va specificato in `configs/{TICKER}.json` campo `rating_credito`
- Loggare in `data/logs/prompt_log.md` tramite `utils/logging_utils.py`
