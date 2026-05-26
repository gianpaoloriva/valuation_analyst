---
name: option-valuation
description: Valutazione tramite option pricing (Black-Scholes) - equity come call option sugli asset aziendali secondo Damodaran
user_invocable: true
---

# Skill: Valutazione con Option Pricing (Damodaran)

Valuta l'equity di un'azienda come una call option europea sugli asset aziendali
usando il modello Black-Scholes. Particolarmente utile per aziende in distress
o con alto leverage, dove il DCF tradizionale fallisce perche' i cash flow sono negativi.

## Utilizzo

```
/option-valuation TICKER
/option-valuation TICKER --volatilita 0.40 --scadenza-debito 5.0
```

---

## Vincoli Critici

1. **Usare come COMPLEMENTO, mai come unico metodo** — sempre affiancato da DCF o multipli
2. **Volatilita' asset e' il parametro piu' critico** — piccole variazioni cambiano molto il risultato
3. **Modello assume debito zero-coupon** — non considera coupon intermedi
4. **Distribuzione lognormale degli asset** — puo' sottostimare il rischio di coda
5. **NON usare per aziende con poco debito** — il valore opzione e' trascurabile se D/E < 0.5
6. **Ideale per distress**: quando V e' vicino a K, l'equity ha valore per il "tempo residuo"

---

## Quando Usare Questo Approccio

### Ideale per:
- Aziende con alto leverage (D/E > 2)
- Aziende in distress finanziario (V vicino a K)
- Aziende con utili negativi persistenti (DCF impossibile con FCFF negativi a lungo)
- Settori ciclici nei punti bassi del ciclo

### NON usare per:
- Aziende con poco debito (il valore opzione e' trascurabile)
- Aziende con utili stabili e positivi (DCF e' piu' appropriato e preciso)
- Come unico metodo di valutazione

---

## Processo di Valutazione

### Step 1: Stima dei Parametri

**I 5 parametri Black-Scholes:**

| Parametro | Simbolo | Come stimarlo |
|-----------|---------|--------------|
| Valore asset | V | Market Cap + Valore di mercato debito |
| Debito nominale (strike) | K | Face value totale del debito |
| Scadenza | T | Maturity media ponderata del debito |
| Risk-free rate | r | Treasury/BTP nella valuta dei cash flow |
| Volatilita' asset | σ | Da equity volatility o comparabili |

**Valore Asset (V):**
```
V = Market Cap + Valore di Mercato Debito
```
Se debito non quotato, approssimare con book value.

**Strike Price (K):**
```
K = Short-Term Debt + Long-Term Debt (face value)
```
Alcuni analisti: K = ST Debt + 0.5 * LT Debt (per approssimare maturity media).

**Scadenza (T):**
```
T = Maturity media ponderata del debito (in anni)
```
Se non disponibile, usare 5-7 anni come approssimazione.

**Volatilita' Asset (σ) — il parametro piu' difficile:**

Tre approcci:

1. **Da volatilita' equity (metodo iterativo):**
   ```
   σ_V = σ_E * (E/V) / N(d1)
   ```
   Richiede soluzione iterativa perche' E dipende da σ_V.

2. **Da volatilita' equity + leverage (approssimazione):**
   ```
   σ_V ≈ σ_E * E / (E + D)
   ```

3. **Da comparabili:** volatilita' media asset di aziende simili nel settore.

**Volatilita' tipica per settore:**

| Settore | σ Asset tipica |
|---------|--------------|
| Technology | 30-50% |
| Healthcare/Pharma | 25-40% |
| Utilities | 15-25% |
| Financials | 20-35% |
| Aziende in distress | 40-60%+ |

> **CHECKPOINT**: Mostrare tabella con tutti e 5 i parametri, fonte e metodo di stima.
> La volatilita' e' il punto piu' critico — giustificare la scelta.

---

### Step 2: Calcolo Black-Scholes

**Formula:**
```
E = V * N(d1) - K * e^(-rT) * N(d2)
```

dove:
```
d1 = [ln(V/K) + (r + σ²/2) * T] / (σ * √T)
d2 = d1 - σ * √T
```

- **E** = Valore equity
- **V** = Valore totale asset (firm value)
- **K** = Valore nominale del debito (strike)
- **r** = Risk-free rate
- **T** = Scadenza media debito (anni)
- **σ** = Volatilita' asset
- **N(.)** = Funzione distribuzione cumulativa normale standard

**Calcolo passo per passo:**
1. Calcolare d1
2. Calcolare d2 = d1 - σ√T
3. Calcolare N(d1) e N(d2) dalla distribuzione normale
4. E = V * N(d1) - K * e^(-rT) * N(d2)

> **CHECKPOINT**: Mostrare d1, d2, N(d1), N(d2), e valore equity risultante.

---

### Step 3: Output Derivati

**Valore Debito (residuale):**
```
D_mercato = V - E
```

**Yield to Maturity implicito:**
```
YTM = -ln(D_mercato / K) / T
```

**Default Spread implicito:**
```
Default Spread = YTM - r
```

**Probabilita' di Default:**
```
P(default) = N(-d2)
```

Questa e' la probabilita' risk-neutral che V < K alla scadenza.

**Tabella output:**

| Metrica | Valore |
|---------|--------|
| Valore Asset (V) | €X.XX M |
| Debito Nominale (K) | €X.XX M |
| **Valore Equity (E)** | **€X.XX M** |
| Valore Equity / Azione | €X.XX |
| Valore Debito (D = V - E) | €X.XX M |
| YTM Implicito | X.XX% |
| Default Spread | X.XX bps |
| **Probabilita' Default** | **X.X%** |

> **CHECKPOINT**: Mostrare tabella completa. La probabilita' di default e' coerente
> con il rating dell'azienda? Se diverge, spiegare.

---

### Step 4: Sensitivity sulla Volatilita'

La volatilita' e' il parametro piu' incerto — eseguire sempre la sensitivity.

**Tabella sensitivity:**

| σ Asset | Valore Equity | Equity/Azione | P(Default) |
|---------|--------------|--------------|------------|
| 20% | €X.XX M | €X.XX | X.X% |
| 30% | €X.XX M | €X.XX | X.X% |
| 40% | €X.XX M | €X.XX | X.X% |
| 50% | €X.XX M | €X.XX | X.X% |
| 60% | €X.XX M | €X.XX | X.X% |

Paradosso dell'opzione: maggiore volatilita' → maggiore valore equity (per aziende in distress).
Questo e' corretto: piu' incertezza = piu' probabilita' che V superi K.

> **CHECKPOINT FINALE**: Mostrare sensitivity su σ. Confrontare valore equity B-S
> con valore DCF (se disponibile). Se divergono, spiegare le implicazioni.

---

## Errori Comuni

| Errore | Perche' e' grave | Come evitarlo |
|--------|-----------------|---------------|
| Usare volatilita' equity come proxy per volatilita' asset | σ_E > σ_V per il leverage; sovrastima il valore opzione | Usare la formula di de-leveraging |
| Ignorare i coupon del debito | Il modello assume zero-coupon; con coupon il debito scade "prima" | Usare K aggiustato o maturity piu' breve |
| Applicare a aziende con poco debito | Il valore opzione ≈ V - K se V >> K; non aggiunge nulla | Usare solo se D/E > 1 |
| Non fare sensitivity su σ | Il risultato e' molto sensibile a σ | Sempre presentare una tabella σ |
| Confondere P(default) risk-neutral e reale | N(-d2) e' risk-neutral; la probabilita' reale e' diversa | Specificare che e' risk-neutral |
| Usare come unico metodo | Non sufficientemente robusto da solo | Sempre complementare con DCF/multipli |

---

## Parametri per Paese

| Parametro | US | Italia |
|-----------|-----|--------|
| Risk-free rate | US 10Y Treasury | BTP 10Y |
| Volatilita' indice | VIX (S&P 500) | VSTOXX (Euro Stoxx 50) |
| Ristrutturazione debito | Chapter 11 (debtor-friendly) | L.F. / Composizione con creditori |
| Soglia distress | Market-based | Meno trasparenza su crediti deteriorati |
| Procedura insolvenza | 12-18 mesi | 3-7 anni (piu' lunga) |

**Nota Italia**: Le procedure concorsuali italiane sono piu' lunghe. Questo impatta T
(scadenza effettiva) e puo' aumentare il valore dell'opzione — piu' tempo = piu' valore temporale.

---

## Limitazioni del Modello

1. Assume distribuzione lognormale del valore asset — sottostima i fat tails
2. Assume volatilita' costante — in realta' σ varia con leverage e ciclo
3. Non considera coupon intermedi del debito — il debito reale paga cedole
4. Non considera covenant o opzioni di ristrutturazione
5. La stima della volatilita' asset e' il punto piu' debole e soggettivo

---

## Note Operative

- **MAI creare script .py ad-hoc**. Usare SEMPRE `run_analysis.py`
- Questa skill produce una sezione aggiuntiva nel report (se rilevante)
- Prerequisiti: dati su debito (face value, maturity), market cap, volatilita' equity
- Per il risk-free rate, usare lo stesso della skill `cost-of-capital`
- Loggare in `data/logs/prompt_log.md` tramite `utils/logging_utils.py`
