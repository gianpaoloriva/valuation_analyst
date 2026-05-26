---
name: fsi-client-report-italy
description: >
  Report periodico per clienti italiani: performance portafoglio, allocazione,
  commento di mercato. Benchmark FTSE MIB / EURO STOXX 50, valuta EUR,
  disclaimer CONSOB, reportistica costi MiFID II. Per distribuzione trimestrale o annuale.
  Triggers on "report cliente", "client report", "report performance",
  "report trimestrale", "rendiconto portafoglio", "estratto conto clienti".
---

# Report Cliente — Contesto Italiano

Adapt dello skill US `client-report`. Struttura e workflow identici. Adattati account types, benchmark, valuta, disclaimer e compliance MiFID II.

## Workflow

### Step 1: Parametri Report

- **Nome cliente** e nucleo familiare
- **Periodo**: trimestre, YTD, annuale, personalizzato
- **Contenitori**: tutti o specifico (deposito titoli, fondo pensione, GPM, PIR)
- **Benchmark**: FTSE MIB, EURO STOXX 50, blend personalizzato coerente con IPS/profilo MiFID II
- **Branding**: logo, colori, disclaimer dello studio/intermediario
- **Lingua**: italiano (default) o inglese

### Step 2: Sintesi Performance

**Riepilogo Household:**

| | Trim. | YTD | 1 Anno | 3 Anni Ann. | 5 Anni Ann. | Dall'inizio |
|---|-------|-----|--------|-------------|-------------|-------------|
| Portafoglio | | | | | | |
| Benchmark | | | | | | |
| +/− | | | | | | |

**Per Contenitore:**

| Contenitore | Tipo | Valore (€) | Trim. | YTD | Benchmark |
|------------|------|-----------|-------|-----|-----------|
| Deposito Titoli | Amministrato | | | | |
| Fondo Pensione | Negoziale/Aperto | | | | |
| GPM | Gestione Patrimoniale | | | | |
| PIR | Piano Individuale Risparmio | | | | |
| Polizza Unit-linked | Ramo III | | | | |
| **Totale** | | | | | |

### Step 3: Panoramica Allocazione

Allocazione corrente con grafico (torta o barre):

| Asset Class | % Portafoglio | Valore (€) | Target IPS % | Drift |
|------------|--------------|-----------|-------------|-------|
| Azionario Europa | | | | |
| Azionario USA | | | | |
| Azionario Emergenti | | | | |
| Obbligazionario Gov. EUR | | | | |
| Obbligazionario Corporate | | | | |
| Alternativi | | | | |
| Liquidità | | | | |

### Step 4: Dettaglio Posizioni

| Titolo | ISIN | Asset Class | Quantità | Prezzo (€) | Valore (€) | % Portaf. | Rendimento Trim. |
|--------|------|-----------|----------|-----------|-----------|----------|-----------------|
| | | | | | | | |

### Step 5: Commento di Mercato

Sintesi mercati adattata al livello di sofisticazione del cliente:
- Cosa è successo sui mercati nel periodo (2-3 frasi) — focus su mercato italiano/europeo, BCE, spread BTP-Bund
- Come ha impattato il portafoglio
- Outlook e razionale del posizionamento (2-3 frasi)
- Per clienti retail: linguaggio semplice, no gergo tecnico
- Per clienti sofisticati: più tecnico, riferimenti a multipli, macro

### Step 6: Riepilogo Operatività

- Operazioni eseguite nel periodo
- Versamenti e prelievi
- Dividendi e cedole incassati (distinguere redditi di capitale e redditi diversi)
- Commissioni e costi addebitati
- Ribilanciamenti effettuati
- Contributi a fondo pensione

### Step 7: Note di Pianificazione

- Progresso verso obiettivi finanziari (pensione, istruzione, acquisto immobiliare)
- Eventuali variazioni al piano o raccomandazioni
- Situazione plafond minusvalenze (scadenze in arrivo)
- Prossime azioni e scadenze (dichiarazione redditi, rinnovo adeguatezza MiFID II)
- Data prossima revisione

### Step 8: Output

- Report PDF (8-12 pagine) con branding
- Documento Word per personalizzazione
- Excel dati di supporto (opzionale)

**Struttura report:**
1. Copertina (nome cliente, periodo, logo)
2. Sintesi esecutiva (1 pagina)
3. Performance (1-2 pagine)
4. Allocazione con grafici (1 pagina)
5. Dettaglio posizioni (1-2 pagine)
6. Commento di mercato (1 pagina)
7. Operatività (1 pagina)
8. Note di pianificazione (1 pagina)
9. **Reportistica costi MiFID II** — ex-post annuale obbligatoria (costi del servizio, costi del prodotto, incentivi, impatto costi su rendimento) → vedi skill `costi-mifid-exante-expost`
10. Disclaimer e avvertenze (1 pagina)

### Disclaimer

Includere nel report:
```
Il presente report ha finalità esclusivamente informativa e non costituisce
sollecitazione all'investimento ai sensi del D.Lgs. 58/1998 (TUF).
I rendimenti passati non sono indicativi di quelli futuri. Il valore degli
investimenti può variare e l'investitore potrebbe non recuperare l'importo
investito. Si raccomanda di consultare il proprio consulente finanziario
per valutazioni personalizzate.
```

## Errori Comuni da Evitare

### ❌ Usare S&P 500 come benchmark default
Il benchmark deve essere coerente con il profilo MiFID II del cliente. Per portafogli italiani/europei: FTSE MIB, EURO STOXX 50, o blend personalizzato. L'S&P 500 è appropriato solo come componente di un benchmark composito.

### ❌ Mostrare account types US
Non esistono IRA, Roth, 401k, 529 in Italia. I contenitori sono: deposito titoli (regime amministrato/dichiarativo), fondo pensione, GPM (gestione patrimoniale), PIR, polizze.

### ❌ Dimenticare la reportistica costi MiFID II
Il report annuale ex-post sui costi è obbligatorio per tutti gli intermediari. Deve mostrare: costi del servizio, costi del prodotto, incentivi ricevuti, impatto complessivo dei costi sul rendimento.

### ❌ Non segnalare le minusvalenze in scadenza
Il report è l'occasione per segnalare al cliente eventuali minusvalenze nel plafond in scadenza (4 anni). Includere sempre nella sezione "Note di pianificazione".
