---
name: sensitivity-analysis
description: Analisi di sensitivita' 2D, scenari best/base/worst e simulazione Monte Carlo secondo Damodaran
user_invocable: true
---

# Skill: Analisi di Sensitivita' e Rischio (Damodaran)

Esegue tre tipi di analisi del rischio sulla valutazione: sensitivity table 2D,
analisi per scenari (best/base/worst), e simulazione Monte Carlo. L'obiettivo e'
comunicare un **range di valori**, non un punto singolo.

## Utilizzo

```
/sensitivity-analysis AAPL
/sensitivity-analysis ENEL.MI --tipo montecarlo --iterazioni 10000
/sensitivity-analysis AAPL --tipo scenari
```

---

## Vincoli Critici

1. **Griglia sensitivity dispari** (5x5 o 7x5) — il caso base deve cadere al centro della matrice
2. **Range WACC ragionevole** — tipicamente ±200 bps dal caso base; range troppo stretto nasconde rischi
3. **Terminal growth non negativa** e mai superiore al PIL nominale del paese
4. **Probabilita' scenari = 100%** — la somma delle probabilita' deve essere esattamente 1.0
5. **Monte Carlo: minimo 10.000 iterazioni** — con meno la distribuzione non converge
6. **Il valore puntuale DCF deve cadere nel range** — se il DCF base e' fuori dal range di sensitivity, c'e' un errore
7. **Documentare tutte le distribuzioni** — ogni assunzione Monte Carlo deve essere esplicitata

---

## Workflow 1: Analisi di Sensitivita' 2D

### Step 1: Selezione Parametri e Range

**Coppie standard (eseguire entrambe):**

| Tabella | Asse X | Asse Y | Range tipico |
|---------|--------|--------|-------------|
| Tabella 1 | Terminal Growth | WACC | g ±100bps, WACC ±200bps |
| Tabella 2 | Crescita Ricavi | Margine Operativo | ±3pp ciascuno |

**Range da config:**
- `config.sensitivity.wacc_range` — valori WACC
- `config.sensitivity.growth_range` — valori terminal growth
- `config.sensitivity.crescita_range` — tassi crescita ricavi
- `config.sensitivity.margine_range` — margini operativi

Se non in config, usare range default centrati sul caso base.

### Step 2: Calcolo Matrice

Per ogni combinazione (parametro_x_i, parametro_y_j), ricalcolare il modello DCF completo
e ottenere il valore per azione.

**Formato output — Tabella 1 (WACC vs Terminal Growth):**

```
Valore/azione   g=1.0%   g=1.5%   g=2.0%   g=2.5%   g=3.0%
WACC 7.0%       €X.XX    €X.XX    €X.XX    €X.XX    €X.XX
WACC 7.5%       €X.XX    €X.XX    €X.XX    €X.XX    €X.XX
WACC 8.0%       €X.XX    [BASE]   €X.XX    €X.XX    €X.XX
WACC 8.5%       €X.XX    €X.XX    €X.XX    €X.XX    €X.XX
WACC 9.0%       €X.XX    €X.XX    €X.XX    €X.XX    €X.XX
```

Il caso base deve essere evidenziato (grassetto o [BASE]).

### Step 3: Interpretazione

- Identificare il range di valori plausibili
- Segnalare l'asimmetria: se il valore e' piu' sensibile al ribasso che al rialzo
- Confrontare con il prezzo di mercato: in quante celle il titolo risulta sottovalutato?

> **CHECKPOINT**: Mostrare le due tabelle di sensitivity. Commentare il range e la sensibilita'
> relativa ai parametri.

---

## Workflow 2: Analisi per Scenari

### Step 1: Definizione Scenari

Tre scenari con parametri e probabilita':

| Parametro | Best Case | Base Case | Worst Case |
|-----------|-----------|-----------|------------|
| Crescita ricavi | `config.scenari.upside_pct` | Caso base | `config.scenari.downside_pct` |
| Margine operativo | +2-3pp vs base | Caso base | -2-3pp vs base |
| WACC | -50bps | Caso base | +100bps |
| Terminal growth | +50bps | Caso base | -50bps |
| **Probabilita'** | `config.scenari.prob_best` | `config.scenari.prob_base` | `config.scenari.prob_worst` |

**Descrizioni da config:**
- Best: `config.scenari.desc_best`
- Base: `config.scenari.desc_base`
- Worst: `config.scenari.desc_worst`

### Step 2: Calcolo Valore per Scenario

Per ogni scenario, eseguire il DCF completo con i parametri dello scenario.

### Step 3: Valore Atteso Ponderato

```
E[V] = P(best) * V(best) + P(base) * V(base) + P(worst) * V(worst)
```

**Verifica**: P(best) + P(base) + P(worst) = 1.0

**Tabella output:**

| Scenario | Probabilita' | Valore/azione | Contributo |
|----------|-------------|--------------|------------|
| Best Case | XX% | €X.XX | €X.XX |
| Base Case | XX% | €X.XX | €X.XX |
| Worst Case | XX% | €X.XX | €X.XX |
| **Valore Atteso** | **100%** | **€X.XX** | |

> **CHECKPOINT**: Mostrare tabella scenari con descrizioni, parametri, valori e valore atteso.

---

## Workflow 3: Simulazione Monte Carlo

### Step 1: Definizione Distribuzioni

**Distribuzioni per parametro:**

| Parametro | Distribuzione | Parametri | Fonte |
|-----------|--------------|-----------|-------|
| WACC | Normale | mu=WACC_base, sigma=`config.monte_carlo.wacc_std` (default 0.8%) | Incertezza su beta, ERP |
| Crescita alta | Normale | mu=g_alta, sigma=`config.monte_carlo.crescita_alta_std` (default 2%) | Incertezza fondamentale |
| Terminal growth | Uniforme | [1.0%, 3.0%] US; [0.5%, 2.0%] IT | Range PIL nominale |
| Margine operativo | Normale | mu=margine_base, sigma=2% | Incertezza settoriale |
| Tax rate | Triangolare | (min, moda, max) = (t-3%, t, t+3%) | Rischio fiscale |

### Step 2: Correlazioni tra Parametri

Parametri spesso correlati — documentare e implementare:
- Crescita ricavi e margine: **correlazione negativa** (-0.3) — crescita spesso costa margini
- WACC e terminal growth: **bassa correlazione** (~0)
- Margine e tax rate: **bassa correlazione** (~0)

### Step 3: Simulazione

- Numero iterazioni: **minimo 10.000** (default), raccomandato 50.000-100.000
- Per ogni iterazione: estrarre parametri dalle distribuzioni, calcolare DCF, salvare valore
- Verificare convergenza della media (variazione < 0.5% nelle ultime 1.000 iterazioni)

### Step 4: Statistiche e Output

**Tabella output:**

| Statistica | Valore |
|-----------|--------|
| Media | €X.XX |
| Mediana | €X.XX |
| Dev. Standard | €X.XX |
| 5° Percentile | €X.XX |
| 25° Percentile | €X.XX |
| 75° Percentile | €X.XX |
| 95° Percentile | €X.XX |
| Prob. sopra prezzo mercato | XX% |

**Intervalli di confidenza:**
```
IC 90% = [P5, P95]     — range ampio
IC 50% = [P25, P75]    — range centrale
```

**Descrizione distribuzione:**
- Forma (simmetrica, skewed left/right)
- Code (fat tails indicano rischio estremo)
- Moda vs media (se divergono, la distribuzione e' asimmetrica)

> **CHECKPOINT FINALE**: Mostrare tabella statistiche e descrizione distribuzione.
> Segnalare la probabilita' che il titolo sia sottovalutato al prezzo corrente.

---

## Errori Comuni

| Errore | Perche' e' grave | Come evitarlo |
|--------|-----------------|---------------|
| Range sensitivity troppo stretto | Nasconde rischi reali, falsa sicurezza | ±200bps WACC, ±100bps growth minimo |
| Scenari non indipendenti | Probabilita' non sommano a 100% | Verificare sempre la somma |
| Monte Carlo con poche iterazioni | Distribuzione non converge, risultati instabili | Minimo 10.000, ideale 50.000+ |
| Ignorare correlazioni | Sottostima la varianza, sovrastima la diversificazione | Modellare almeno crescita-margine |
| Terminal growth > PIL in ogni cella | Viola il vincolo fondamentale | Cap al PIL nominale del paese |
| Usare distribuzioni senza giustificazione | Risultati ininterpretabili | Documentare ogni scelta |
| Non evidenziare il caso base | Il lettore non sa dove e' il punto di partenza | Sempre evidenziare nella griglia |
| Range troppo ampio che include valori assurdi | Diluisce il segnale | WACC < 4% o > 15% raramente sensato |

---

## Parametri per Paese

| Parametro | US | Italia |
|-----------|-----|--------|
| Terminal growth range | 1.5%-3.5% | 0.5%-2.0% |
| WACC range tipico | 7%-11% | 6%-10% |
| Valuta output | USD ($) | EUR (€) |
| PIL nominale di riferimento | ~4-5% | ~2-3% |
| Rischio regolatorio | Basso | Medio (CONSOB, AGCM) |

---

## Metodologia — Riferimento (Damodaran)

### Perche' Tre Approcci al Rischio

- **Sensitivity 2D**: mostra la relazione meccanica tra parametri e valore. Utile per capire
  "quanto cambia il valore se il WACC sale di 50bps?"
- **Scenari**: incorpora narrativa e probabilita'. Utile per comunicare a non-tecnici:
  "nel caso peggiore il titolo vale X"
- **Monte Carlo**: cattura l'incertezza completa e le interazioni tra parametri.
  Produce un range probabilistico: "c'e' il 70% di probabilita' che il valore sia tra X e Y"

I tre sono complementari, non alternativi. Il report standard include tutti e tre.

### Best Practice

1. Eseguire SEMPRE sensitivity su WACC e terminal growth (Tabella 1 standard)
2. Per Monte Carlo, documentare tutte le distribuzioni assunte
3. Le correlazioni tra parametri possono avere impatto significativo — non ignorarle
4. Usare il risultato per comunicare un RANGE, non un valore puntuale
5. Il valore puntuale dal DCF base deve cadere entro il range ragionevole

---

## Note Operative

- **MAI creare script .py ad-hoc**. Usare SEMPRE `run_analysis.py`
- I range sensitivity sono in `configs/{TICKER}.json` sezione `sensitivity`
- Gli scenari sono in `configs/{TICKER}.json` sezione `scenari`
- I parametri Monte Carlo sono in `configs/{TICKER}.json` sezione `monte_carlo`
- Output: sezioni 6, 7, 8 del report standard
- Loggare in `data/logs/prompt_log.md` tramite `utils/logging_utils.py`
