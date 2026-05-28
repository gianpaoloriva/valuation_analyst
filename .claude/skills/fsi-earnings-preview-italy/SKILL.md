---
name: fsi-earnings-preview-italy
description: >
  Analisi pre-earnings per società quotate su Borsa Italiana: stime consensus,
  scenari bull/base/bear, metriche chiave da monitorare, catalizzatori.
  Fonti consensus Refinitiv IBES / Bloomberg con copertura EU.
  Triggers on "earnings preview", "anteprima utili", "cosa aspettarsi dai risultati",
  "pre-earnings", "preview risultati", "cosa monitorare per [società]".
---

# Earnings Preview — Contesto Italiano

Adapt dello skill US `earnings-preview`. Il framework scenari e la struttura "what to watch" sono universali. Adattati timing, fonti consensus, metriche settoriali, e contesto mercato.

## Workflow

### Step 1: Raccolta Contesto

- Identificare la società e il periodo di reporting (trimestre o semestre)
- Verificare se la società pubblica trimestrali o solo semestrali (dal 2014 i resoconti intermedi Q1/Q3 non sono obbligatori per le quotate italiane — molte mid/small cap non li pubblicano)
- Cercare stime consensus via Refinitiv IBES o Bloomberg (ricavi, EBITDA, EBIT, utile netto, EPS)
- Trovare la data di pubblicazione risultati — in Italia i risultati escono tipicamente **prima dell'apertura** (ore 7:00-8:30) o **dopo la chiusura** (ore 17:30+) del mercato. Conference call solitamente in mattinata (ore 9:00-11:00) o primo pomeriggio (ore 14:00-15:00)
- Verificare il calendario Borsa Italiana per festività / chiusure
- Rileggere il comunicato stampa e la conference call del periodo precedente per guidance e commento del management

### Step 2: Framework Metriche Chiave

Costruire il "cosa monitorare" specifico per la società:

**Metriche finanziarie (IFRS):**
- Ricavi vs consensus (totale e per segmento IFRS 8)
- EBITDA / EBITDA adjusted vs consensus — verificare la definizione MAP della società
- EBIT vs consensus
- Utile netto e EPS vs consensus
- Free Cash Flow
- PFN (Posizione Finanziaria Netta) — variazione vs trimestre/semestre precedente
- Guidance aggiornata vs consensus forward

**Metriche operative per settore (adattate al mercato italiano):**

| Settore | Metriche chiave | Società esempio |
|---------|----------------|----------------|
| Banche | Margine d'interesse (NII), commissioni nette, cost/income, CET1 ratio, NPL ratio, costo del rischio, Texas ratio | Intesa, UniCredit, Mediobanca |
| Utilities | RAB, EBITDA regolato, FFO/Net Debt, investimenti regolati vs non regolati, volumi (GWh, Smc) | Enel, Terna, Snam, Italgas, A2A |
| Lusso | Crescita organica, like-for-like, breakdown per area geografica e canale, margine lordo | Ferrari, Moncler, Brunello Cucinelli |
| Industriali | Book-to-bill, backlog, ROIC, cash conversion, breakdown geografico (molte hanno >50% ricavi extra-Italia) | Leonardo, Prysmian, Interpump |
| Telco/Media | ARPU, churn, net adds, EBITDA after lease (EBITDAaL), CapEx/Revenue | TIM, Inwit |
| Infrastrutture/Concessioni | Traffico (veicoli/giorno), ricavo per veicolo-km, durata residua concessione | Atlantia (delisted), ASTM |
| Assicurazioni | Combined ratio, premi raccolti, Solvency II ratio, risultato investimenti | Generali, Unipol |
| Oil & Gas | Produzione (boe/d), prezzo realizzato, reserve replacement, upstream vs downstream | Eni, Saipem, Tenaris |

### Step 3: Analisi Scenari

3 scenari con implicazioni sul prezzo:

| Scenario | Ricavi | EBITDA | EPS | Driver chiave | Reazione attesa |
|----------|--------|--------|-----|--------------|----------------|
| Bull | | | | | |
| Base | | | | | |
| Bear | | | | | |

Per ciascuno scenario:
- Cosa dovrebbe succedere operativamente
- Quale commento del management segnalerebbe questo scenario
- Contesto storico: come ha reagito il titolo a risultati simili in passato?
- Considerare il contesto macro: decisioni BCE, spread BTP-Bund, dati macro Italia/Eurozona

### Step 4: Checklist Catalizzatori

Identificare i 3-5 elementi che determineranno la reazione del titolo:

1. [Metrica] vs [consensus / whisper number] — perché è importante
2. [Guidance] — cosa si aspetta il buy-side di sentire
3. [Cambiamento narrativo] — cambi strategici, M&A, ristrutturazioni, spin-off
4. [Contesto regolatorio] — decisioni ARERA (utilities), Banca d'Italia (banche), AGCM (antitrust), Golden Power
5. [Dividendo / buyback] — politica di remunerazione, DPS atteso vs consensus

**Catalizzatori specifici per il mercato italiano:**
- Impatto PNRR su società infrastrutturali/industriali
- Decisioni BCE su tassi (impatto su banche e utilities)
- Evoluzione spread BTP-Bund (impatto su tutto il mercato)
- Politica industriale / Golden Power per settori strategici
- Calendario assemblee azionisti (tipicamente aprile-giugno) per dividend

### Step 5: Output

One-pager earnings preview con:
- Società, periodo, data pubblicazione risultati
- Tabella stime consensus (fonte e data: Refinitiv IBES / Bloomberg)
- Metriche chiave da monitorare (ordinate per importanza)
- Tabella scenari Bull/Base/Bear
- Checklist catalizzatori
- Trading setup: performance recente del titolo vs FTSE MIB, implied move da opzioni IDEM (se disponibili), volumi recenti

**Formato**: valori in EUR (€), separatori europei

## Errori Comuni da Evitare

### ❌ Aspettarsi trimestrali da tutte le società
Molte mid/small cap italiane pubblicano solo H1 e FY. Verificare sempre il calendario IR della società prima di preparare il preview.

### ❌ Usare solo consensus Bloomberg US-centric
Per società italiane, Refinitiv IBES ha tipicamente la migliore copertura di analisti europei. Bloomberg è valido ma verificare il numero di stime nel consensus — per small cap italiane potrebbe esserci un solo analista.

### ❌ Ignorare il contesto macro europeo
Le earnings delle società italiane sono fortemente influenzate da: tassi BCE, spread BTP-Bund, PIL Eurozona, cambio EUR/USD. Includere sempre nel framing degli scenari.

### ❌ Trascurare la guidance qualitativa
Le società italiane danno spesso guidance meno granulare delle US — frasi come "crescita a singola cifra" o "margini stabili". Anche queste indicazioni qualitative vanno monitorate e confrontate con il consensus numerico.
