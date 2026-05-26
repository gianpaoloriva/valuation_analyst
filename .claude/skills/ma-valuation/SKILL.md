---
name: ma-valuation
description: Valutazione M&A con stima sinergie, accretion/dilution e calcolo del valore di acquisizione secondo Damodaran
user_invocable: true
---

# Skill: Valutazione M&A e Sinergie (Damodaran)

Calcola il valore di un'acquisizione includendo sinergie operative e finanziarie,
analisi accretion/dilution, e il prezzo massimo d'offerta. Segue il framework
Damodaran dove il valore creato dal deal e' la differenza tra valore delle sinergie
e premio pagato.

## Utilizzo

```
/ma-valuation --acquirente MSFT --target ATVI
/ma-valuation --acquirente MSFT --target ATVI --sinergie-costo 0.05 --sinergie-ricavo 0.03
```

---

## Vincoli Critici

1. **Valore creato = Sinergie - Premio pagato** — se il premio supera le sinergie, l'acquirente distrugge valore
2. **Sinergie di costo piu' prevedibili dei ricavi** — pesare di conseguenza (70/30)
3. **Probabilita' realizzazione < 100%** — tipicamente 50-70% delle sinergie stimate si materializzano
4. **Tempo di realizzazione 2-3 anni** — le sinergie non si realizzano al Day 1
5. **Costi di integrazione significativi** — IT, ristrutturazione, retention bonus, consulenti
6. **Accretion/dilution non e' un criterio di valore** — un deal dilutivo puo' comunque creare valore

---

## Processo di Valutazione M&A

### Step 1: Valutazione Standalone

Valutare acquirente e target separatamente, ciascuno "as is":
- Usare skill `dcf-valuation` e/o `comparable-analysis`
- Il valore standalone del target e' il **floor** del prezzo d'offerta

**Output:**

| Entita' | EV Standalone | Equity Value | Per Azione |
|---------|--------------|-------------|------------|
| Acquirente | €X.XX M | €X.XX M | €X.XX |
| Target | €X.XX M | €X.XX M | €X.XX |

> **CHECKPOINT**: Mostrare valutazioni standalone. Confermare prima di procedere alle sinergie.

---

### Step 2: Stima Sinergie Operative

**Sinergie di Costo (piu' prevedibili, 3-7% dei costi combinati):**
- Eliminazione duplicati (sede, IT, admin, back-office)
- Economie di scala (procurement, produzione, logistica)
- Razionalizzazione forza vendita

**Sinergie di Ricavo (meno prevedibili, 1-3% dei ricavi combinati):**
- Cross-selling prodotti
- Accesso a nuovi mercati/canali
- Pricing power (riduzione concorrenza)

**Valutazione sinergie:**
```
PV(Sinergie) = Σ [Sinergia_annua_t * (1 - tax) / (1 + WACC)^t]
```

Parametri:
- **Tempo fase-in**: sinergie crescono linearmente da 0 a pieno regime in 2-3 anni
- **Probabilita' realizzazione**: 50-70% (haircut sulle stime)
- **WACC per sinergie**: WACC combinato (le sinergie appartengono all'entita' combinata)

**Tabella sinergie:**

| Tipo | Stima Annua | Prob. Realizz. | Sinergia Attesa | PV |
|------|------------|---------------|----------------|-----|
| Costo | €X.XX M | XX% | €X.XX M | €X.XX M |
| Ricavo | €X.XX M | XX% | €X.XX M | €X.XX M |
| **Totale** | | | | **€X.XX M** |

> **CHECKPOINT**: Mostrare tabella sinergie con probabilita' e PV. Le stime sono conservative?

---

### Step 3: Sinergie Finanziarie

**Tax benefits:**
- Utilizzo perdite fiscali (NOL) del target
- Incremento capacita' di debito (interest tax shield)
- Step-up del basis fiscale (se applicabile)

**Riduzione costo del capitale:**
- Diversificazione cash flow → minore beta combinato
- Rating combinato potenzialmente migliore → minore spread debito
- Maggiore capacita' di debito → struttura capitale piu' efficiente

**Formula:**
```
Sinergia_finanziaria = PV(Tax savings) + PV(Riduzione costo debito * Debito incrementale)
```

**Nota Italia:** Riporto perdite fiscali soggetto a limiti (art. 84 TUIR: 80% del reddito
imponibile). Fusione: art. 172 TUIR, test di vitalita' economica.

---

### Step 4: Costi di Integrazione

**Costi one-time tipici:**

| Voce | Range tipico |
|------|-------------|
| Ristrutturazione/severance | 1-3% dei ricavi target |
| Integrazione IT/sistemi | €5-50M (dipende da complessita') |
| Rebranding/marketing | 0.5-1% dei ricavi |
| Consulenti (legal, M&A, accounting) | 1-3% del deal value |
| Retention bonus key people | 0.5-2% del deal value |

**Formula costi netti:**
```
Costi_integrazione_netti = Costi_one_time * (1 - tax_rate)
```

---

### Step 5: Prezzo Massimo d'Offerta

**Formula fondamentale (Damodaran):**
```
Valore Acquisizione = Valore Standalone Target
                    + PV(Sinergie Operative)
                    + PV(Sinergie Finanziarie)
                    - Costi Integrazione Netti

Prezzo Massimo = Valore Acquisizione
```

Oltre questo prezzo, l'acquisizione distrugge valore per gli azionisti dell'acquirente.

**Premio implicito:**
```
Premio = (Prezzo Offerta - Prezzo Pre-Annuncio) / Prezzo Pre-Annuncio
```

**Benchmark premi M&A:**

| Contesto | Premio tipico |
|---------|--------------|
| Media storica M&A | 25-35% |
| Range tipico | 15-50% |
| Premi > 50% | Richiedono sinergie eccezionali |
| Hostile takeover | Spesso > 40% |

**Tabella ponte:**

| Componente | Valore |
|-----------|--------|
| Valore Standalone Target | €X.XX M |
| + PV Sinergie Operative | +€X.XX M |
| + PV Sinergie Finanziarie | +€X.XX M |
| - Costi Integrazione | -€X.XX M |
| **= Prezzo Massimo** | **€X.XX M** |
| Premio implicito su prezzo mercato | XX% |

> **CHECKPOINT**: Mostrare prezzo massimo e premio implicito.
> Il premio e' nel range 15-50%? Se no, spiegare.

---

### Step 6: Analisi Accretion/Dilution

**Concetto**: L'EPS dell'acquirente aumenta (accretive) o diminuisce (dilutive) post-deal?

**Formula:**
```
EPS_pro_forma = (Utile Acquirente + Utile Target + Sinergie nette) / Azioni totali
```

**Se pagato in cash:**
```
Azioni_totali = Azioni_acquirente (invariate)
Ma: costo finanziamento riduce l'utile
```

**Se pagato in azioni:**
```
Azioni_totali = Azioni_acquirente + Nuove_azioni_emesse
Nuove_azioni = Prezzo_offerta * Azioni_target / Prezzo_acquirente
```

**Se pagato in mix cash+azioni:** combinazione dei due effetti.

**Tabella accretion/dilution:**

| Metrica | Pre-Deal | Pro-Forma | Variazione |
|---------|----------|-----------|------------|
| Utile Netto | €X.XX M | €X.XX M | +/-XX% |
| Azioni Outstanding | X.XX M | X.XX M | +/-XX% |
| **EPS** | **€X.XX** | **€X.XX** | **+/-XX%** |
| P/E implicito | X.Xx | X.Xx | |

**ATTENZIONE**: Accretion/dilution NON e' un criterio di creazione di valore.
Un deal dilutivo puo' creare valore se le sinergie a lungo termine compensano.
Un deal accretive puo' distruggere valore se si e' overpaid.

> **CHECKPOINT FINALE**: Mostrare analisi completa: prezzo massimo, premio, accretion/dilution.
> Il deal crea valore per l'acquirente al prezzo proposto?

---

## Errori Comuni

| Errore | Perche' e' grave | Come evitarlo |
|--------|-----------------|---------------|
| Sovrastimare sinergie di ricavo | Cross-selling raramente raggiunge le stime | Haircut 50%+ su sinergie ricavo |
| Ignorare costi di integrazione | Possono erodere gran parte delle sinergie | Stimare 1-5% del deal value |
| Usare accretion come criterio di valore | Accretion ≠ creazione valore | Focusarsi su NPV delle sinergie |
| Sinergie al Day 1 | Ci vogliono 2-3 anni per pieno regime | Modellare il phase-in |
| Ignorare rischio di esecuzione | Non tutte le sinergie si materializzano | Probability-weight al 50-70% |
| Premio basato solo su precedenti | Ogni deal ha sinergie diverse | Premio = f(sinergie specifiche) |
| Non considerare alternative del target | Il target potrebbe rifiutare | Offrire almeno il valore standalone |

---

## Parametri per Paese

| Parametro | US | Italia |
|-----------|-----|--------|
| Normativa OPA | Williams Act | TUF art. 102-112, CONSOB |
| Soglia OPA obbligatoria | Nessuna (volontaria) | 30% (totalitaria), 25% (IPO) |
| Golden Power | CFIUS | D.L. 21/2012 (settori strategici) |
| Tax merger | IRC §368 (tax-free reorg) | Art. 172 TUIR (neutralita' fiscale) |
| Antitrust | FTC/DOJ | AGCM (soglie fatturato) |
| Squeeze-out | Varia per stato (90-95%) | 95% (TUF art. 111) |
| Riporto perdite post-merger | IRC §382 limits | Art. 84 TUIR (80% reddito, test vitalita') |
| Advisor fees tipici | 1-2% deal value | 1.5-3% deal value |

**Nota Italia**: OPA obbligatoria al superamento del 30% — impatto significativo
sulla strutturazione del deal. Golden Power puo' bloccare acquisizioni in settori
strategici (energia, telecom, difesa, finanza, sanita').

---

## Metodologia M&A — Riferimento (Damodaran)

### Framework Decisionale

```
Se Prezzo_offerta < Valore_standalone + Sinergie - Costi_integrazione:
    → Acquisizione crea valore per acquirente
Se Prezzo_offerta > Valore_standalone + Sinergie - Costi_integrazione:
    → Acquisizione distrugge valore (overpaying)
Se Prezzo_offerta = Valore_standalone (no premio):
    → Target non accettera' (nessun incentivo)
```

### Chi Cattura il Valore?

Il valore creato (sinergie) viene diviso tra acquirente e target:
- **Premio al target** = parte delle sinergie trasferite agli azionisti target
- **Valore residuo acquirente** = sinergie - premio
- In mercati competitivi, il target cattura gran parte delle sinergie (bidding war)

### Tipi di Acquisizione per Motivazione

| Tipo | Motivazione | Sinergie tipiche |
|------|------------|-----------------|
| Orizzontale | Scala, quota mercato | Costo (alte), Ricavo (medie) |
| Verticale | Integrazione filiera | Costo (medie), Ricavo (basse) |
| Conglomerale | Diversificazione | Finanziarie (basse) |
| Hostile | Cambio management | Efficienza operativa |

---

## Note Operative

- **MAI creare script .py ad-hoc**. Usare SEMPRE `run_analysis.py`
- Prerequisiti: valutazione standalone di acquirente e target (skill `dcf-valuation` e `comparable-analysis`)
- Per deal italiani: verificare soglie OPA (30%) e Golden Power
- Output: sezione aggiuntiva nel report (dopo le 10 sezioni standard)
- Loggare in `data/logs/prompt_log.md` tramite `utils/logging_utils.py`
