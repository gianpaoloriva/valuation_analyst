---
name: dcf-valuation
description: Esegue una valutazione DCF (Discounted Cash Flow) completa con modelli FCFF/FCFE multi-stage secondo Damodaran
user_invocable: true
---

# Skill: Valutazione DCF (Damodaran)

Calcola il valore intrinseco di un'azienda tramite Discounted Cash Flow, utilizzando modelli
FCFF (Free Cash Flow to Firm) o FCFE (Free Cash Flow to Equity) multi-stage secondo la
metodologia di Aswath Damodaran.

## Utilizzo

```
/dcf-valuation AAPL
/dcf-valuation ENEL.MI
/dcf-valuation AAPL --metodo FCFE
```

---

## Vincoli Critici

Leggere PRIMA di iniziare qualsiasi calcolo:

1. **FCFF si sconta al WACC, FCFE al costo equity (Re)** — MAI confondere i due tassi
2. **Terminal growth <= crescita PIL nominale** del paese (2-3% US, 1-2% Italia)
3. **Terminal Value non dovrebbe superare il 75% del valore totale** — se accade, rivedere le assunzioni di crescita o il periodo esplicito
4. **Reinvestment rate coerente**: in fase stabile g = RIR * ROIC, non un valore arbitrario
5. **ROIC in fase stabile converge verso WACC** — un'azienda matura non genera extra-rendimenti in perpetuita'
6. **Aziende in perdita**: FCFF puo' essere negativo; procedere comunque con convergenza verso margini positivi in fase stabile
7. **Valori di mercato, non contabili**: debito netto e pesi D/E devono usare valori di mercato

---

## Processo DCF

### Step 1: Raccolta e Validazione Dati

**Input richiesti:**
- Configurazione in `configs/{TICKER}.json`
- Dati finanziari da Massive.com API (o fallback da config `fondamentali_fallback`)
- WACC dalla skill `cost-of-capital` (o da parametro esplicito)

**Dati fondamentali necessari:**

| Dato | Fonte primaria | Fallback |
|------|---------------|----------|
| Ricavi | API | `fondamentali_fallback.ricavi` |
| EBIT | API | `fondamentali_fallback.ebit` |
| EBITDA | API | `fondamentali_fallback.ebitda` |
| Utile Netto | API | `fondamentali_fallback.utile_netto` |
| Debito Totale | API | `fondamentali_fallback.total_debt` |
| Cassa | API | `fondamentali_fallback.cash` |
| CapEx | API | `fondamentali_fallback.capex` |
| Deprezzamento | API | `fondamentali_fallback.deprezzamento` |
| Delta WC | API | `fondamentali_fallback.delta_wc` |
| Tax Rate | API | `fondamentali_fallback.tax_rate` |
| Beta Levered | API | `fondamentali_fallback.beta_levered` |

**Parametri per paese:**
- Se `paese == "IT"`: risk-free = BTP 10Y, ERP = 7%, tax = 27.9% (IRES + IRAP)
- Se `paese == "US"`: risk-free = US 10Y Treasury, ERP = 5.5%, tax = 25%

> **CHECKPOINT**: Mostrare all'utente la tabella dati input. Confermare prima di procedere.
> Segnalare eventuali anomalie (EBIT negativo, margini fuori range settoriale, delta WC anomalo).

---

### Step 2: Calcolo FCFF Base

**Formula FCFF (Free Cash Flow to Firm):**
```
FCFF = EBIT * (1 - t) + Deprezzamento - CapEx - Delta Working Capital
```

Equivalentemente:
```
FCFF = EBIT * (1 - t) - Reinvestimento Netto
```
dove Reinvestimento Netto = CapEx - Deprezzamento + Delta WC

**Formula FCFE (Free Cash Flow to Equity):**
```
FCFE = Utile Netto + Deprezzamento - CapEx - Delta WC - Rimborso Debito Netto
```

Oppure partendo da FCFF:
```
FCFE = FCFF - Interessi * (1 - t) + Nuovo Debito Netto
```

**Reinvestment Rate:**
```
RIR = (CapEx - Depr + Delta WC) / EBIT(1 - t)
```

**Scelta del metodo:**
- **FCFF** (default): preferito per aziende con struttura di capitale in evoluzione
- **FCFE**: indicato quando il leverage e' stabile e prevedibile

**Gestione aziende in perdita:**
- Se EBIT < 0, FCFF sara' negativo — procedere comunque
- Proiettare convergenza verso margini positivi nel periodo esplicito
- Usare margini target di settore come riferimento per la fase stabile

> **CHECKPOINT**: Mostrare FCFF calcolato e le sue componenti in tabella:
>
> | Componente | Valore |
> |-----------|--------|
> | EBIT(1-t) | ... |
> | + Deprezzamento | ... |
> | - CapEx | ... |
> | - Delta WC | ... |
> | **= FCFF** | **...** |
>
> Se FCFF negativo, spiegare il motivo e confermare le assunzioni.

---

### Step 3: Modello Multi-Stage (3 Fasi)

**Modello a 3 fasi (preferito da Damodaran):**

| Fase | Durata | Crescita | Caratteristiche |
|------|--------|----------|-----------------|
| 1 - Alta crescita | `config.anni_alta` (default 5) | `config.crescita_alta` | Reinvestimento elevato, margini in espansione |
| 2 - Transizione | `config.anni_transizione` (default 5) | Convergenza lineare | ROIC converge verso WACC, RIR si normalizza |
| 3 - Stabile | Perpetuita' | `config.crescita_stabile` | Crescita = PIL nominale, RIR = g/ROIC |

**Calcolo crescita per anno:**
```
Fase 1: g_t = crescita_alta                      (anni 1..n1)
Fase 2: g_t = crescita_alta - t * (alta - stabile) / n2   (anni n1+1..n1+n2)
Fase 3: g = crescita_stabile                      (perpetuita')
```

**Crescita fondamentale (check di coerenza):**
```
g = Reinvestment Rate * ROIC
```

La crescita implicita nei fondamentali deve essere ragionevolmente vicina alla crescita
assunta nel modello. Se divergono significativamente, segnalare.

**Stima della crescita — fonti:**
- Crescita fondamentale: g = RIR * ROIC
- Crescita storica: CAGR ricavi ultimi 3-5 anni
- Consenso analisti: crescita attesa prossimi 3-5 anni
- La crescita stabile NON deve MAI superare la crescita nominale del PIL

> **CHECKPOINT**: Mostrare tabella proiezione cash flow per tutti gli anni espliciti:
>
> | Anno | Crescita | FCFF | Fattore Sconto | PV(FCFF) |
> |------|----------|------|---------------|----------|
> | 1 | ... | ... | ... | ... |
> | ... | | | | |
> | n | ... | ... | ... | ... |

---

### Step 4: Terminal Value

**Metodo Gordon Growth (perpetuita') — preferito:**
```
TV = FCFF_{n+1} / (WACC - g)
   = FCFF_n * (1 + g_stabile) / (WACC - g_stabile)
```

**Vincoli obbligatori:**
- `g_stabile < WACC` — altrimenti TV diverge all'infinito
- `g_stabile <= PIL nominale` del paese (2-3% US, 1-2% Italia)
- Il reinvestment rate in fase stabile deve essere coerente: `RIR_stabile = g_stabile / ROIC_stabile`

**Metodo Exit Multiple (alternativo):**
```
TV = EBITDA_n * Multiplo_uscita
```
Il multiplo uscita dovrebbe riflettere un'azienda matura nel settore.

**Reinvestment rate in fase stabile:**
```
RIR_stabile = g_stabile / ROIC_stabile
```
Se ROIC_stabile converge a WACC (come dovrebbe):
```
RIR_stabile = g_stabile / WACC
```

**Verifica TV/EV ratio:**
- < 60%: modello robusto
- 60-75%: accettabile, ma segnalare la dipendenza dal terminal value
- > 75%: rivedere le assunzioni — periodo esplicito troppo corto o crescita di fase 1 troppo bassa

> **CHECKPOINT**: Mostrare Terminal Value, metodo utilizzato, e rapporto TV/EV.
> Se TV/EV > 75%, suggerire azioni correttive (allungare periodo esplicito, rivedere crescita).

---

### Step 5: Enterprise Value -> Equity Value -> Per Azione

**Ponte di valutazione:**
```
Enterprise Value  = PV(cash flow espliciti) + PV(terminal value)
                  = Σ [FCFF_t / (1+WACC)^t] + TV / (1+WACC)^n

Equity Value      = Enterprise Value - Debito Netto
                  = Enterprise Value - (Debito Totale - Cassa)

Valore Per Azione = Equity Value / Azioni Outstanding
```

**Se si usa FCFE:**
```
Equity Value      = Σ [FCFE_t / (1+Re)^t] + TV_equity / (1+Re)^n
Valore Per Azione = Equity Value / Azioni Outstanding
```
Con FCFE non si passa per Enterprise Value: il risultato e' direttamente Equity Value.

> **CHECKPOINT**: Mostrare il ponte completo EV -> Equity -> Per Azione:
>
> | Componente | Valore |
> |-----------|--------|
> | PV Cash Flow Espliciti | ... |
> | PV Terminal Value | ... |
> | **Enterprise Value** | **...** |
> | - Debito Totale | ... |
> | + Cassa | ... |
> | **Equity Value** | **...** |
> | / Azioni Outstanding | ... |
> | **Valore Per Azione** | **...** |

---

### Step 6: Validazione e Output

**Confronto con il mercato:**
```
Upside/Downside = (Valore Intrinseco - Prezzo Mercato) / Prezzo Mercato
```

**Scala raccomandazione:**

| Upside/Downside | Raccomandazione |
|-----------------|-----------------|
| > +25% | STRONG BUY |
| +15% a +25% | BUY |
| +5% a +15% | MODERATE BUY |
| -5% a +5% | HOLD |
| -15% a -5% | MODERATE SELL |
| -25% a -15% | SELL |
| < -25% | STRONG SELL |

**Check di coerenza finali:**
1. ROIC in fase stabile ~ WACC (non rendimenti abnormi in perpetuita')
2. RIR coerente con crescita: g = RIR * ROIC
3. Margini in fase stabile sostenibili (confrontare con mediana settore)
4. TV/EV ratio ragionevole (< 75%)
5. Se multiplo implicito (EV/EBITDA implicito) e' fuori range settore, indagare

**Output generato:**
- Sezione report markdown per il report completo (sezione 4: Valutazione DCF)
- Tabella proiezione cash flow
- Ponte EV -> Equity -> Per Azione
- Confronto con prezzo di mercato e raccomandazione

> **CHECKPOINT FINALE**: Mostrare riepilogo con valore per azione, prezzo mercato,
> upside/downside, raccomandazione. Chiedere conferma prima di includere nel report.

---

## Errori Comuni

| Errore | Perche' e' grave | Come evitarlo |
|--------|-----------------|---------------|
| Scontare FCFE al WACC | Sottovaluta il costo del capitale proprio | FCFE si sconta a Re (costo equity) |
| Terminal growth > PIL nominale | Implica che l'azienda cresca piu' dell'economia in perpetuita' | Cap a 2-3% (US) o 1-2% (IT) |
| Ignorare il reinvestimento stabile | Crescita senza reinvestimento e' incoerente | Calcolare sempre RIR = g/ROIC |
| CapEx = Deprezzamento in perpetuita' | Implica zero investimento netto, possibile solo se g = 0 | Lasciare CapEx > Depr se g > 0 |
| Dimenticare il cash nel ponte EV->Equity | Sottovaluta il valore per gli azionisti | Equity = EV - Debito + Cassa |
| Usare book value per D/E | I pesi devono riflettere il mercato, non la contabilita' | Usare market cap per equity, market value per debito |
| WACC diverso per ogni anno | Il WACC deve riflettere la struttura target, non quella attuale | Un solo WACC (o convergenza esplicita se struttura cambia) |
| Non normalizzare WC ciclico | Delta WC anomalo in un anno distorce FCFF base | Usare media 3 anni o normalizzare |

---

## Parametri per Paese

| Parametro | US | Italia |
|-----------|-----|--------|
| Risk-free rate | US 10Y Treasury (~4.2%) | BTP 10Y (~3.8%) |
| Equity Risk Premium | 5.5% | 7% (include CRP) |
| Country Risk Premium | 0% | ~1.5% (incluso in ERP) |
| Tax rate | 25% (corporate) | 27.9% (IRES 24% + IRAP 3.9%) |
| Terminal growth | 2-3% | 1-2% |
| Costo debito base | SOFR + spread | Euribor + spread |
| Valuta | USD | EUR |
| Indice riferimento | S&P 500 | FTSE MIB |
| Fonte crescita PIL | BEA / Fed | ISTAT / BCE |

---

## Metodologia DCF — Riferimento Completo (Damodaran)

### FCFF vs FCFE: Quando Usare Quale

| Criterio | FCFF + WACC | FCFE + Re |
|----------|-------------|-----------|
| Leverage in evoluzione | Preferito | Sconsigliato |
| Leverage stabile | Funziona | Preferito |
| Aziende in perdita | Preferito | Difficile (utile netto negativo) |
| Banche / Finanziarie | Non applicabile | Preferito (FCFE diretto) |
| Semplicita' | Piu' passaggi | Meno passaggi |

### Modelli di Crescita

**Modello 2 Fasi:**
1. Fase alta (5-10 anni): crescita superiore al mercato
2. Fase stabile (perpetuita'): crescita = economia

**Modello 3 Fasi (preferito):**
1. Fase alta (5 anni): crescita basata su fondamentali attuali
2. Fase transizione (5 anni): convergenza lineare da alta a stabile
3. Fase stabile (perpetuita'): crescita = risk-free reale + inflazione

### Terminal Value — Dettaglio

Il TV cattura il valore dell'azienda oltre il periodo esplicito di proiezione.
Due metodi:

1. **Gordon Growth**: `TV = FCF_{n+1} / (r - g)` — coerente con il framework DCF
2. **Exit Multiple**: `TV = Metrica_n * Multiplo` — utile come cross-check ma introduce circolarita'

Il Gordon Growth e' preferito perche' forza coerenza interna (crescita, reinvestimento, rischio).

### Reinvestment Rate — Ruolo Critico

Il tasso di reinvestimento collega crescita e rendimento:
```
g = RIR * ROIC
```

Implicazioni:
- Se ROIC > WACC e g > 0, l'azienda crea valore reinvestendo
- Se ROIC = WACC, il reinvestimento e' neutro (NPV = 0)
- Se ROIC < WACC, il reinvestimento distrugge valore
- In fase stabile, assumere ROIC → WACC (competitive equilibrium)

### Fonti Dati

| Dato | Fonte Primaria | Alternativa |
|------|---------------|-------------|
| Bilanci e cash flow | Massive.com API | Config fallback |
| WACC | Skill cost-of-capital | Parametro esplicito |
| Crescita settore | Dataset Damodaran | Consenso analisti |
| CapEx/Depr ratio settore | Dataset Damodaran `capex.xlsx` | Media storica azienda |
| Beta settoriale | Dataset Damodaran `betas.xlsx` | Regressione storica |

---

## Note Operative

- **MAI creare script .py ad-hoc** per l'analisi DCF. Usare SEMPRE `run_analysis.py`
- Il config `configs/{TICKER}.json` e' lo step zero — verificare che esista e sia completo
- Per il WACC, invocare prima la skill `cost-of-capital` se non gia' calcolato
- Per la sensitivity sul DCF, invocare la skill `sensitivity-analysis` dopo il calcolo base
- Loggare l'analisi in `data/logs/prompt_log.md` tramite `utils/logging_utils.py`
