# Contesto Italiano — Adattamenti per Coverage Initiation

Questo documento contiene tutte le modifiche necessarie per adattare il workflow di coverage initiation al contesto italiano/europeo. Applicare queste sovrascritture quando si eseguono i 5 task dello skill.

---

## Sovrascritture Globali (Si Applicano a Tutti i Task)

### Fonti Dati

| Fonte US (da NON usare) | Fonte Italiana/Europea (da usare) |
|--------------------------|-----------------------------------|
| SEC EDGAR | CONSOB (consob.it → Emittenti) |
| 10-K (annuale) | Bilancio consolidato IFRS / Relazione annuale |
| 10-Q (trimestrale) | Relazione semestrale (IAS 34) / Resoconto intermedio |
| S&P Kensho MCP | Refinitiv/LSEG MCP (se disponibile) |
| Daloopa MCP | Bureau van Dijk/AIDA MCP (se disponibile) |
| Bloomberg (US) | Bloomberg / Refinitiv / FactSet (copertura EU) |
| Yahoo Finance | Borsa Italiana / Investing.com / Refinitiv |

### Principi Contabili

| GAAP US (da NON usare) | IFRS (da usare) | Impatto |
|-------------------------|------------------|---------|
| Goodwill ammortizzato | Goodwill con impairment test annuale (IAS 36) | No D&A su goodwill, rischio svalutazione |
| Operating lease off-balance | IFRS 16: tutti i leasing capitalizzati | Aumento debito, D&A, riduzione OpEx |
| R&D interamente a costo | IAS 38: sviluppo capitalizzabile se criteri soddisfatti | Possibile capitalizzazione R&D |
| Revenue recognition ASC 606 | IFRS 15: per performance obligation | Simile ma differenze in contratti complessi |
| Stock compensation ASC 718 | IFRS 2: share-based payment | Trattamento simile, alcune differenze |

### Valuta e Formato

- **Valuta**: EUR (€), non USD ($)
- **Separatore migliaia**: punto (1.000.000), non virgola
- **Separatore decimali**: virgola (3,50%), non punto
- **Formato prezzo target**: €XX,XX (non $XX.XX)
- **Unità standard**: EUR Milioni (€M), non USD Millions

### Fiscalità

- **Aliquota corporate**: ~27,9% (IRES 24% + IRAP 3,9%), non 21% US
- **IRAP**: base imponibile diversa (non deducibili interessi passivi e costo del lavoro)
- **Perdite fiscali**: art. 84 TUIR — riporto illimitato, limite utilizzo 80% (primi 3 esercizi 100%)
- **Dividendi**: ritenuta 26% per persone fisiche, participation exemption per società (95% esente)

---

## Task 1: Company Research — Adattamenti Italia

### Fonti per la Ricerca Qualitativa

| Sezione | Fonte US | Fonte Italiana |
|---------|----------|---------------|
| Company overview | SEC EDGAR, company website | CONSOB, Borsa Italiana scheda società, sito aziendale |
| Management bios | DEF 14A proxy statement | Relazione sul governo societario, sito aziendale |
| Governance | Proxy statement | Relazione sul governo societario e gli assetti proprietari (TUF art. 123-bis) |
| Azionariato | Schedule 13D/13G | CONSOB — partecipazioni rilevanti (soglia 3% per quotate) |
| Remunerazione | DEF 14A | Relazione sulla remunerazione (voto consultivo assemblea) |

### Struttura Governance Italiana

Includere nella sezione management/governance:
- **Modello di governance**: tradizionale (CdA + Collegio Sindacale) vs monistico vs dualistico
- **Collegio Sindacale**: organo di controllo obbligatorio, 3-5 membri effettivi
- **Società di revisione**: nome e durata incarico (max 9 anni, rotazione obbligatoria)
- **Azionista di controllo**: molto frequente in Italia (famiglie, fondazioni bancarie, Stato)
- **Patti parasociali**: accordi tra azionisti depositati in CONSOB
- **Amministratori indipendenti**: requisiti TUF + Codice di Corporate Governance

### Contesto Regolatorio Italiano

Nella sezione risk assessment, includere rischi regolatori specifici:
- **CONSOB**: regolatore mercati (equivalente SEC)
- **Banca d'Italia**: vigilanza bancaria e stabilità finanziaria
- **AGCM**: Autorità Garante Concorrenza e Mercato (antitrust)
- **ARERA**: regolatore energia/acqua/rifiuti (per utilities)
- **AGCOM**: regolatore comunicazioni (per telco/media)
- **Golden Power**: rischio per settori strategici (vedi skill golden-power-check)

### Competitori

Per l'analisi competitiva (5-10 competitor):
- Includere sia competitor italiani che europei
- Specificare se quotati e su quale borsa
- Per settori italiani dominanti (banche, utilities, lusso): includere i campioni nazionali europei

---

## Task 2: Financial Modeling — Adattamenti Italia

### Estrazione Dati Storici

**Fonti da usare (al posto di 10-K/10-Q):**

| Documento US | Documento Italiano IFRS | Dove trovarlo |
|-------------|-------------------------|---------------|
| 10-K | Bilancio consolidato IFRS (Relazione annuale) | CONSOB, Borsa Italiana, sito società |
| 10-Q | Relazione semestrale IAS 34 | Idem |
| 8-K | Comunicazione price sensitive | CONSOB |
| Earnings call transcript | Trascrizione conference call | Refinitiv, sito società |
| Proxy statement | Relazione governo societario + Relazione remunerazione | Sito società |

**Struttura bilancio IFRS da estrarre:**
- Conto economico consolidato → Income Statement
- Situazione patrimoniale-finanziaria → Balance Sheet
- Rendiconto finanziario consolidato → Cash Flow Statement
- Note al bilancio → Supporting details (debito, D&A, TFR, segmenti)

### Modello a 6 Tab — Adattamenti

**Tab 1 — Revenue Model:**
- Breakdown per area geografica: Italia, Europa, Nord America, Asia, Resto del Mondo
- Per società con ricavi prevalentemente italiani: breakdown regionale o per canale
- IFRS 8: usare i segmenti operativi come riportati dalla società

**Tab 2 — Income Statement:**
- Voci specifiche IFRS: accantonamento TFR, svalutazione goodwill (IAS 36), ammortamento RoU (IFRS 16)
- Separare IRES e IRAP se il modello lo richiede
- Quota risultato società collegate (equity method, IAS 28)
- Utile di pertinenza di terzi (minoranze)

**Tab 3 — Cash Flow Statement:**
- Pagamenti TFR in CFO (non CFF)
- Pagamenti leasing IFRS 16: quota capitale in CFF, interessi in CFO
- Imposte pagate (può differire da imposte da CE per timing)

**Tab 4 — Balance Sheet:**
- Attività per diritti d'uso (IFRS 16)
- Fondo TFR (passività non corrente)
- Fondi rischi e oneri (IAS 37)
- Passività per leasing (correnti + non correnti)
- Avviamento (no ammortamento, impairment test)

**Tab 5 — Scenarios:**
- Range di crescita più contenuti vs US (PIL Italia ~0,5-1,5% reale)
- Margini: considerare la struttura costi italiana (cuneo fiscale, TFR)

**Tab 6 — DCF Inputs:**
- **WACC con parametri italiani** (vedi sezione dedicata sotto)
- **Terminal growth**: 1,0-2,0% (non 2,5-3,5% US)
- **Aliquota fiscale**: ~27,9% (IRES+IRAP)
- **Working capital**: DSO 60-90 gg, DPO 60-75 gg

---

## Task 3: Valuation Analysis — Adattamenti Italia

### WACC — Parametri Italiani

```
Costo dell'Equity = BTP 10Y + Beta × ERP Italia

Dove:
- Risk-Free Rate = Rendimento BTP 10 anni (~3,5-4,5%)
  Alternativa: Bund 10Y + spread BTP-Bund
- Beta = 5 anni mensile vs FTSE MIB (società italiane) o EURO STOXX 50 (pan-europee)
- ERP Italia = 6,0-8,0% (include Country Risk Premium)
  Composto da: ERP maturo (~5,0-5,5%) + CRP Italia (~1,5-2,0%)

Costo del Debito Pre-Tax = Euribor 6M + spread creditizio
  NON usare SOFR, LIBOR, o Treasury

Aliquota Fiscale = ~27,9% (IRES 24% + IRAP 3,9%)

Range WACC tipici (Italia):
- Large cap stabile (FTSE MIB): 8-10%
- Mid cap crescita (STAR): 10-13%
- Small cap / alta crescita: 13-16%
```

### Terminal Growth

- **Conservativo**: 1,0-1,5% (crescita PIL reale Italia a lungo termine)
- **Moderato**: 1,5-2,0% (PIL nominale Eurozona, target inflazione BCE 2%)
- **Aggressivo**: 2,0-2,5% (solo leader di mercato con pricing power)
- **NON superare 2,5%** senza giustificazione forte

### Comparable Companies

**Costruzione peer group:**
- 5-10 peer, mix italiano + europeo dello stesso settore
- Fonti: Refinitiv, FactSet, Bloomberg (non solo S&P Kensho)
- Multipli da includere: EV/Ricavi, EV/EBITDA, P/E, P/BV, Dividend Yield
- Statistiche: Max, 75°, Mediana, 25°, Min

**Range multipli tipici Italia/EU:**
- EV/EBITDA: 6-15x (più basso che US)
- P/E: 8-25x (più basso che US)
- P/BV: 0,3-3,0x (banche italiane spesso <1x)
- Nota "discount italiano": 10-20% vs peer europei

**PFN per Enterprise Value:**
```
PFN = Debiti Finanziari (correnti + non correnti)
    + Passività Leasing IFRS 16 (se incluse)
    - Disponibilità Liquide
    - Investimenti Finanziari a Breve
EV = Market Cap + PFN
```

### Precedent Transactions

Per transazioni M&A italiane:
- Fonti: Mergermarket, Bureau van Dijk Zephyr, Bloomberg M&A
- Includere premio OPA (tipicamente 20-40% in Italia)
- Considerare operazioni di delisting (frequenti negli ultimi anni)

### Output Valutazione

- **Prezzo target**: €XX,XX (non $XX.XX)
- **Raccomandazione**: COMPRARE / MANTENERE / VENDERE (o BUY/HOLD/SELL se report in inglese)
- **Upside**: XX%
- **Catalizzatori**: 3-5, includere catalizzatori specifici italiani (es. PNRR, politica industriale, regolamentazione settoriale)

---

## Task 4: Chart Generation — Adattamenti Italia

### Modifiche ai Grafici

La maggior parte dei grafici è universale. Adattamenti necessari:

| Chart | Adattamento |
|-------|-------------|
| chart_01 (Stock price) | Prezzo in EUR, benchmark FTSE MIB (non S&P 500) |
| chart_03 (Revenue by product) | Etichette in EUR |
| chart_04 (Revenue by geography) | Focus su Italia/Europa/Global |
| chart_28 (DCF sensitivity) | WACC 8-13% range, terminal growth 0,5-2,5% |
| chart_30 (Comps) | Peer europei, multipli in range italiano |
| chart_32 (Football field) | Prezzo target in EUR |
| chart_34 (Historical multiples) | Multipli vs FTSE MIB / settore italiano |

### Fonti Dati per Grafici

- **Prezzo storico**: Borsa Italiana, Refinitiv, Bloomberg (non Yahoo Finance US)
- **Benchmark**: FTSE MIB, EURO STOXX 50 (non S&P 500, Nasdaq)
- **Multipli storici**: Refinitiv, Bloomberg consensus

---

## Task 5: Report Assembly — Adattamenti Italia

### Formato Report

Il formato report è largamente universale. Adattamenti:

- **Standard di riferimento**: JPMorgan, Goldman Sachs, Morgan Stanley, + **Mediobanca, Intesa Sanpaolo IMI, Equita**
- **Lingua**: italiano o inglese (confermare con l'utente)
- **Valuta**: tutti i valori in EUR
- **Disclaimer**: conformità CONSOB (non SEC) per report di ricerca equity
- **Conflitti di interesse**: disclosure secondo Regolamento MAR e direttiva MiFID II

### Sezioni Aggiuntive per il Contesto Italiano

Nella sezione Company 101, aggiungere:
- **Governance**: modello di governance, Collegio Sindacale, azionista di controllo
- **Contesto regolatorio**: regolatori settoriali italiani/EU rilevanti
- **ESG/Sostenibilità**: rating ESG, classificazione SFDR, Tassonomia UE

Nella sezione Valuation:
- **WACC**: mostrare il calcolo completo con parametri italiani
- **Comparabili**: tabella con peer europei
- **Football field**: tutti i range in EUR

### Disclaimer CONSOB

Includere nel report finale:
```
DISCLAIMER
Questo report è stato redatto a scopo informativo e non costituisce
sollecitazione all'investimento ai sensi del D.Lgs. 58/1998 (TUF).
Le informazioni contenute sono basate su fonti ritenute attendibili,
ma non se ne garantisce l'accuratezza o la completezza. Le opinioni
espresse possono essere modificate senza preavviso. Si raccomanda
di consultare un consulente finanziario autorizzato prima di effettuare
qualsiasi investimento.
```

---

## Metriche Settoriali Specifiche per l'Italia

### Banche (settore dominante Borsa Italiana)
NON usare DCF standard. Usare:
- **DDM** (Dividend Discount Model)
- **Excess Return Model**
- Metriche: ROE, ROTE, CET1, Cost/Income, NIM, NPL Ratio, Coverage, P/BV, P/TE

### Utilities (Enel, Terna, Snam, Italgas, A2A, Hera)
- **RAB-based valuation** per utilities regolate
- EV/RAB, Dividend Yield, FFO/Net Debt
- Considerare i periodi regolatori ARERA

### Lusso (Ferrari, Moncler, Brunello Cucinelli)
- Crescita organica, like-for-like, breakdown per area geografica
- Margine lordo >65%, EV/EBITDA premium
- Confronto con LVMH, Kering, Hermès

### Industriali (Leonardo, Prysmian, Interpump)
- ROIC, book-to-bill, backlog
- Esposizione geografica (molte hanno >50% ricavi fuori Italia)
- CapEx intensity, cash conversion

### Infrastrutture/Concessioni
- Durata concessione residua → DCF su durata concessione
- Traffico/volumi come driver di ricavo
- EV/EBITDA + premio per visibilità cash flow
