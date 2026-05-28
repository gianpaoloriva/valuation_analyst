---
name: fsi-competitive-analysis-italy
description: >
  Framework per deck di analisi competitiva nel contesto italiano/europeo:
  posizionamento di mercato, deep-dive competitor, analisi comparativa,
  sintesi strategica. Fonti IFRS, valuta EUR, peer Borsa Italiana/europei.
  Triggers on "analisi competitiva", "competitive analysis", "landscape competitivo",
  "competitor analysis", "peer comparison", "mappa di mercato", "benchmark [società]".
---

# Analisi Competitiva — Contesto Italiano

Adapt dello skill US `competitive-analysis`. Il framework a 9 step e le regole di design/prompt fidelity sono interamente universali. Adattati fonti dati, gerarchia fonti, valuta, e metriche settoriali.

**Per la struttura completa del workflow, le regole di design, e la quality checklist**: riferirsi allo skill US `competitive-analysis` che contiene il framework dettagliato (280 righe). Qui si documentano solo gli adattamenti.

## Adattamenti al Contesto Italiano

### Gerarchia Fonti (sostituisce la sezione US)

1. Bilanci consolidati IFRS / Relazioni annuali (revisionati) — da CONSOB o sito IR
2. Conference call / presentazioni investitori (commento management)
3. Ricerca sell-side (stime analisti — Mediobanca, Equita, Intesa IMI, broker internazionali)
4. Report di settore (McKinsey, BCG, associazioni di categoria italiane: Confindustria, ABI, ANIE, ANIA)
5. News (solo sviluppi recenti; verificare vs fonti primarie)

### Valuta e Formato

- Tutti i dati in EUR (€), non USD
- Separatori europei (punto migliaia, virgola decimali)
- Se confronto con competitor extra-EU: convertire in EUR, notare tasso di cambio e data
- Dati mancanti: "−" o "N/D" con flag "[S]" per stime

### Metriche Settoriali Italiane (integra Step 0)

| Settore | Metriche chiave |
|---------|----------------|
| Banche | NII, commissioni nette, cost/income, CET1, NPL ratio, ROTE, P/BV |
| Utilities | RAB, EBITDA regolato, FFO/Net Debt, dividend yield, periodo regolatorio ARERA |
| Lusso | Crescita organica, like-for-like, margine lordo, breakdown geografico |
| Industriali | Book-to-bill, backlog, ROIC, cash conversion, % ricavi export |
| Infrastrutture | Traffico/volumi, durata concessione, EV/EBITDA + premio visibilità |
| Assicurazioni | Combined ratio, premi lordi, Solvency II, investment yield |
| Oil & Gas | Produzione (boe/d), breakeven, reserve replacement, upstream EBITDA |

### Contesto Regolatorio (integra Step 8)

Nella sezione M&A e contesto strategico, includere:
- **AGCM**: soglie antitrust (fatturato Italia >€532M / fatturato imprese interessate >€32M)
- **Golden Power**: settori strategici soggetti a D.L. 21/2012 (5G, AI, semiconduttori, energia, difesa, agroalimentare, finanza)
- **Regolatori settoriali**: ARERA (utilities), AGCOM (telco/media), Banca d'Italia (banche), IVASS (assicurazioni)
- **Tassonomia UE / SFDR**: rilevante per ESG assessment
- **Ruolo dello Stato**: in Italia lo Stato è azionista rilevante in molti settori (Eni, Enel, Leonardo, Poste, MPS)

### Posizionamento e Comparazione

- Step 5 (visualization): per il mercato italiano, considerare anche il clustering per dimensione (FTSE MIB vs Mid Cap vs STAR) e per proprietà (familiare vs PE-backed vs statale vs public)
- Step 7 (comparative): includere "discount italiano" se rilevante (10-20% vs peer europei)
- Step 9 (synthesis): nei bull/base/bear, includere scenari macro Italia (spread BTP-Bund, rating sovrano, BCE)

## Errori Comuni da Evitare

### ❌ Usare fonti 10-K / SEC EDGAR
Le società italiane/europee pubblicano bilanci consolidati IFRS depositati su CONSOB o sul sito IR. Non esistono 10-K o 10-Q.

### ❌ Convertire in USD
Il confronto deve essere in EUR. Solo per competitor US/non-EU, convertire il loro dato in EUR (non viceversa).

### ❌ Ignorare la struttura proprietaria nei competitive dynamics
In Italia la struttura proprietaria (familiare, statale, PE-backed) è un competitive factor. Influenza decisioni strategiche, M&A, governance, e velocità di esecuzione.
