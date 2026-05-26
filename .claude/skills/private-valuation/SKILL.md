---
name: private-valuation
description: Valutazione di societa' private con sconti di illiquidita', premi di controllo e total beta secondo Damodaran
user_invocable: true
---

# Skill: Valutazione Societa' Private (Damodaran)

Applica aggiustamenti specifici per societa' non quotate alla valutazione base (DCF o multipli),
includendo sconto di illiquidita', premio di controllo, e total beta per investitori
non diversificati, secondo la metodologia di Aswath Damodaran.

## Utilizzo

```
/private-valuation --ricavi 50000000 --ebitda 8000000 --settore "Manufacturing"
/private-valuation --valutazione-base 100000000 --tipo-partecipazione maggioranza
```

---

## Vincoli Critici

1. **Ordine di applicazione**: prima premio controllo, poi sconto illiquidita' — MAI invertire
2. **Total beta per investitori non diversificati** — il CAPM standard assume diversificazione
3. **Sconto illiquidita' non e' opzionale** — una societa' privata non e' liquida come una quotata
4. **Premio controllo solo per partecipazioni di maggioranza** — per quote di minoranza si applica ulteriore DLOM
5. **Valutazione base "come se quotata"** — partire dal DCF/multipli standard, poi aggiustare
6. **Floor 5%, cap 50%** sullo sconto illiquidita' — valori fuori range richiedono giustificazione

---

## Processo di Valutazione

### Step 1: Valutazione Base ("Come Se Quotata")

Eseguire la valutazione standard (DCF o multipli) ignorando lo status privato:
- Usare la skill `dcf-valuation` per il DCF
- Usare la skill `comparable-analysis` per i multipli (peer quotati)
- Il WACC usa il beta standard di settore (non il total beta — quello viene dopo)

Il risultato e' il **Valore Quotata Equivalente**.

> **CHECKPOINT**: Mostrare il valore base "come se quotata". Confermare prima di applicare aggiustamenti.

---

### Step 2: Total Beta (Investitore Non Diversificato)

**Concetto**: Un investitore in una societa' privata tipicamente non e' diversificato.
Il rischio rilevante e' il rischio TOTALE, non solo quello sistematico.

**Formula:**
```
Total Beta = Beta_mercato / Correlazione_con_mercato
```

Tipicamente: Total Beta = 2x-3x il Beta di mercato.

**Costo equity con total beta:**
```
Re_privato = Rf + Total_Beta * ERP
```

Questo e' significativamente piu' alto del Re per societa' quotata.

**Esempio:**

| Parametro | Quotata | Privata |
|-----------|---------|---------|
| Beta | 1.0 | 2.5 (total beta) |
| Rf | 4.2% | 4.2% |
| ERP | 5.5% | 5.5% |
| **Re** | **9.7%** | **17.95%** |

**Quando usare il total beta:**
- Sempre per fondatori e imprenditori con patrimonio concentrato
- Per fondi PE con portafoglio limitato
- NON per acquirenti strategici diversificati (usano beta standard)

> **CHECKPOINT**: Se si usa total beta, mostrare confronto Re quotata vs Re privata.
> Chiedere se l'investitore e' diversificato o meno.

---

### Step 3: Premio di Controllo

**Concetto**: Una partecipazione di maggioranza conferisce il controllo sulle decisioni
aziendali (management, dividendi, strategia). Questo ha un valore economico.

**Componenti del valore di controllo (Damodaran):**
1. Cambio management (se sottoperformante)
2. Cambio politica dividendi (se payout subottimale)
3. Cambio struttura capitale (se leverage non ottimale)
4. Decisioni strategiche (M&A, disinvestimenti, ristrutturazioni)

**Formula (Damodaran):**
```
Premio Controllo = (Valore Ottimale - Valore Status Quo) / Valore Status Quo
```

Il premio non e' un numero fisso: dipende da quanto l'azienda e' gestita sotto il suo potenziale.

**Range tipici:**

| Contesto | Premio Controllo |
|---------|-----------------|
| Azienda ben gestita, margini al top | 5-10% |
| Azienda gestita ragionevolmente | 10-20% |
| Azienda sotto potenziale significativo | 20-30% |
| Azienda con inefficienze gravi | 30-50% |

**Per minoranza**: il premio di controllo non si applica. Si applica invece un
**Discount for Lack of Control (DLOC)** rispetto al valore pro-rata:
```
DLOC = 1 - 1/(1 + Premio_Controllo)
```

> **CHECKPOINT**: Mostrare premio di controllo scelto e giustificazione.

---

### Step 4: Sconto di Illiquidita'

**Concetto**: Le azioni di societa' private non possono essere vendute facilmente.
Lo sconto compensa per il costo di liquidazione e il tempo necessario per vendere.

**Formula Damodaran:**
```
Sconto = 0.35 - 0.15 * ln(Ricavi_milioni) - 0.10 * Margine_EBITDA
```
Con floor = 5% e cap = 50%.

**Fattori che influenzano lo sconto:**

| Fattore | Sconto minore | Sconto maggiore |
|---------|--------------|-----------------|
| Ricavi | Elevati (> €100M) | Bassi (< €10M) |
| Profittabilita' | Alta (EBITDA margin > 20%) | Bassa o negativa |
| Asset tangibili | Elevati | Pochi (asset-light) |
| Settore | Attrattivo per acquirenti | Di nicchia |
| Complessita' | Semplice | Complessa |
| Informazione | Bilanci auditati | Contabilita' limitata |

**Range tipici:**

| Profilo | Sconto Illiquidita' |
|---------|-------------------|
| Grande, profittevole, auditata | 10-15% |
| Media, profittevole | 15-25% |
| Piccola, profittevole | 20-30% |
| Piccola, in perdita | 30-40% |
| Micro, early-stage | 40-50% |

> **CHECKPOINT**: Mostrare sconto calcolato con formula e componenti. Verificare ragionevolezza.

---

### Step 5: Calcolo Valore Finale

**Ordine di applicazione (CRITICO — non invertire):**

```
1. Valore "come se quotata"           = V_base
2. + Premio di controllo (se magg.)    = V_base * (1 + premio_controllo)
3. - Sconto illiquidita'               = V_2 * (1 - sconto_illiquidita)
4. = Valore Privata Finale             = V_finale
```

**Formula combinata:**
```
V_privata = V_quotata * (1 + premio_controllo) * (1 - sconto_illiquidita)
```

**Tabella ponte:**

| Step | Componente | Valore |
|------|-----------|--------|
| 1 | Valore "come se quotata" | €X.XX |
| 2 | + Premio controllo (XX%) | +€X.XX |
| 3 | = Valore post-controllo | €X.XX |
| 4 | - Sconto illiquidita' (XX%) | -€X.XX |
| 5 | **= Valore Societa' Privata** | **€X.XX** |

> **CHECKPOINT FINALE**: Mostrare tabella ponte completa. Il valore finale deve essere
> plausibile rispetto ai multipli di transazione per aziende simili nel settore.

---

## Errori Comuni

| Errore | Perche' e' grave | Come evitarlo |
|--------|-----------------|---------------|
| Invertire ordine sconto/premio | Risultato diverso: (1+p)*(1-s) ≠ (1-s)*(1+p) in valore assoluto | Sempre controllo prima, illiquidita' dopo |
| Usare beta standard per investitore non diversificato | Sottostima il rischio percepito | Chiedere il profilo dell'investitore |
| Sconto illiquidita' fisso (es. sempre 25%) | Ignora le caratteristiche dell'azienda | Usare la formula Damodaran |
| Premio controllo per minoranza | Minoranza non ha controllo | Usare DLOC per minoranza |
| Ignorare la dimensione | Le micro-imprese hanno sconto molto maggiore | Ricavi sono il driver principale |
| Non documentare le assunzioni | Non riproducibile, non difendibile | Esplicitare ogni scelta |

---

## Parametri per Paese

| Parametro | US | Italia |
|-----------|-----|--------|
| Sconto illiquidita' medio | 20-25% | 25-30% (mercato meno liquido) |
| Premio controllo medio | 20-30% | 25-35% (concentrazione proprietaria) |
| Fonti transazioni private | PitchBook, PrivCo | AIDA (Bureau van Dijk), Zephyr |
| Normativa vendita quote | State law | Art. 2469 c.c. (diritto prelazione) |
| Perizia per contenzio | Appraisal rights | Art. 2437 c.c. (recesso) |
| Tax su capital gain | Federal + State | 26% (capital gain qualificato) |
| PEX (partecipation exemption) | N/A | 95% esenzione (art. 87 TUIR) |

**Nota Italia**: In Italia, la concentrazione proprietaria e' molto alta (famiglie, holding)
e il mercato delle transazioni private e' meno liquido. Gli sconti tendono a essere piu' alti.
La PEX (Participation Exemption) riduce significativamente il carico fiscale su cessioni qualificate.

---

## Metodologia — Riferimento (Damodaran)

### Tre Dimensioni dello Sconto Privata

Damodaran identifica tre dimensioni separate:
1. **Illiquidita'**: costo di vendita elevato, tempo necessario
2. **Controllo vs minoranza**: differenza di valore tra chi controlla e chi no
3. **Diversificazione investitore**: total beta vs market beta

Queste tre dimensioni sono indipendenti e possono combinarsi.

### Quando NON Applicare Sconti

- **Acquirente strategico quotato**: e' diversificato, non paga sconto illiquidita'
  (l'asset diventa liquido post-acquisizione)
- **IPO imminente**: lo sconto si riduce progressivamente
- **Settore con molti acquirenti**: il mercato privato e' piu' liquido

---

## Note Operative

- **MAI creare script .py ad-hoc**. Usare SEMPRE `run_analysis.py`
- La valutazione base deve essere completata prima di questa skill
- Per aziende italiane: considerare PEX e normativa art. 2469 c.c.
- Output: sezione aggiuntiva nel report (dopo le 10 sezioni standard)
- Loggare in `data/logs/prompt_log.md` tramite `utils/logging_utils.py`
