---
name: fsi-ib-check-deck-italy
description: >
  Quality check per presentazioni investment banking in contesto italiano:
  coerenza numeri (€, IFRS), allineamento dati-narrativa, language polish
  (italiano professionale o inglese IB), formattazione, disclaimer CONSOB.
  Triggers on "check deck", "controlla presentazione", "QC deck", "revisione pitch",
  "verifica materiali", "final pass presentazione", "controlla i numeri".
---

# IB Deck Checker — Contesto Italiano

Adapt dello skill US `ib-check-deck`. La metodologia QC a 4 dimensioni è universale. Adattati: valuta, terminologia, fonti, compliance.

**Per il workflow completo** (environment check, estrazione testo, script `extract_numbers.py`, output report): riferirsi allo skill US `ib-check-deck`. Qui si documentano gli adattamenti.

## Adattamenti al Contesto Italiano

### 1. Number Consistency — Parametri Italiani

**Formati valuta:**
- Unità standard: **€M** (milioni di euro) — non $M, $MM, €MM
- Separatore migliaia: `.` (punto) — non `,`
- Separatore decimale: `,` (virgola) — non `.`
- Verificare coerenza: €500M vs €500 milioni vs €500.000.000 → stesso numero

**Metriche IFRS da verificare:**
- EBITDA, EBIT, Utile netto (non Net Income)
- PFN (Posizione Finanziaria Netta) — non Net Debt
- Patrimonio netto (non Shareholders' Equity)
- Ricavi (non Revenue, se deck in italiano)
- Capitale circolante netto (non Net Working Capital, se in italiano)

**Controlli specifici:**
- Aliquota fiscale: verificare ~27,9% (IRES 24% + IRAP ~3,9%), non 21% US
- Multipli: confrontare con range italiani/europei (EV/EBITDA mid-market IT: 6-10x, non 10-15x US)
- Tassi: Euribor (non SOFR/Treasury)
- Se presenti proiezioni: crescita PIL Italia (~0,5-1,5%) coerente con proiezioni aziendali

### 2. Data-Narrative Alignment — Contesto Italiano

Stessi controlli dello skill US, più:

- **Posizionamento di mercato**: "#1 in Italia" → verificare con dati di mercato italiano (non globale)
- **Quote di mercato**: mercato Italia è più piccolo — percentuali più alte sono plausibili
- **Riferimenti regolatori**: se il deck cita normativa, verificare che sia quella corretta e vigente (es. non citare normativa abrogata)
- **PNRR / fondi UE**: se citati come driver di crescita, verificare che i fondi siano effettivamente allocati al settore
- **Trend macro**: riferimenti a BCE (non Fed), spread BTP-Bund, inflazione Eurozona

### 3. Language Polish — Doppio Registro

I deck IB italiani possono essere in italiano, inglese, o misti. Verificare:

**Se in italiano:**
- Registro professionale finanziario (vedi `references/ib-terminology-italy.md`)
- No anglicismi inutili quando esiste il termine italiano corretto
- Anglicismi accettati nel gergo IB: EBITDA, deal, due diligence, cash flow, leverage, multiple
- No contrazioni, esclamativi, linguaggio colloquiale
- Coerenza: se si usa "ricavi" in una slide, non usare "fatturato" in un'altra (a meno che non siano metriche diverse)

**Se in inglese:**
- Stesse regole dello skill US (vedi `references/ib-terminology.md` US)
- Attenzione a italianismi tradotti letteralmente ("the society" per "la società" → "the company")

**Se misto (italiano con sezioni finanziarie in inglese):**
- Coerenza nella scelta: le slide finanziarie possono essere in inglese, ma non alternare a caso
- Glossario implicito coerente (se "Enterprise Value" su una slide, non "Valore d'Impresa" su un'altra)

### 4. Visual & Formatting QC — Integrazioni

Stessi controlli dello skill US (fonti grafici, assi, tipografia, formattazione numeri), più:

- **Disclaimer CONSOB**: se il materiale è destinato a clienti, deve includere disclaimer appropriato
- **Logo e branding**: verificare che il logo dell'intermediario sia presente e corretto
- **Fonte dati**: se dati di mercato, citare la fonte (Borsa Italiana, ISTAT, Banca d'Italia, Refinitiv, S&P Capital IQ)
- **Date**: formato italiano GG/MM/AAAA o GG mese AAAA — non MM/DD/YYYY
- **Nota IFRS**: se bilancio presentato, specificare "Principi contabili IFRS" (non GAAP)

## Output

Usare `references/report-format-italy.md` come struttura. Stessa classificazione di severity dello skill US (Critical / Important / Minor), con l'aggiunta:

- **Critical**: anche disclaimer CONSOB mancante (se materiale per clienti), errori su normativa citata
- **Important**: anche inconsistenza lingua (italiano/inglese), metriche US anziché italiane/IFRS
- **Minor**: anche formato date non italiano, anglicismi evitabili

## Errori Comuni da Evitare

### ❌ Applicare standard US ai numeri
$M, US GAAP, aliquota 21%, multipli S&P 500 non sono appropriati per deck su società italiane.

### ❌ Non verificare il registro linguistico
Un deck in italiano con anglicismi casuali o un deck in inglese con italianismi tradotti male è un segnale di scarsa professionalità.

### ❌ Ignorare il disclaimer
Materiali IB destinati a clienti o controparti devono includere disclaimer appropriati. L'assenza è un problema di compliance, non solo di formattazione.
