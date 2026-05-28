---
name: fsi-thesis-tracker-italy
description: >
  Tracker tesi di investimento per posizioni su società quotate italiane/europee.
  Monitora dati chiave, catalizzatori, e milestones nel tempo. Aggiorna convinzione
  e scorecard con nuovi sviluppi.
  Triggers on "aggiorna tesi", "update thesis", "la tesi è ancora valida",
  "thesis check", "verifica posizioni", "review tesi [società]".
---

# Thesis Tracker — Contesto Italiano

Adapt dello skill US `thesis-tracker`. Il workflow è quasi interamente universale. Adattamenti minimi su catalizzatori e contesto di mercato.

## Workflow

### Step 1: Definire o Caricare la Tesi

Se nuova tesi:
- **Società**: nome e ticker Borsa Italiana
- **Posizione**: Long o Short
- **Tesi** (1-2 frasi): es. "Long Enel — re-rating da riduzione debito + crescita rinnovabili + dividend yield >6%"
- **Pilastri chiave**: 3-5 argomenti a supporto
- **Rischi chiave**: 3-5 rischi che invaliderebbero la tesi
- **Catalizzatori**: eventi prossimi che possono provare/smentire la tesi
- **Prezzo target / valutazione**: fair value in € se la tesi si realizza
- **Trigger di uscita**: cosa farebbe chiudere la posizione

**Catalizzatori specifici per il mercato italiano:**
- Risultati semestrali/annuali (molte società non pubblicano trimestrali)
- Assemblea azionisti (aprile-giugno) — dividendo, rinnovo CdA
- Decisioni regolatori: ARERA (utilities), AGCM (antitrust), Banca d'Italia (banche), CONSOB
- Politica monetaria BCE e impatto su spread BTP-Bund
- PNRR — bandi, milestone, erogazioni
- Golden Power per settori strategici
- Revisione rating creditizio (Moody's, S&P, Fitch) sull'Italia o sulla società

### Step 2: Log Aggiornamenti

Per ogni nuovo dato o sviluppo:

| Data | Sviluppo | Impatto sulla tesi | Azione | Convinzione aggiornata |
|------|---------|-------------------|--------|----------------------|
| | | Rafforza / Indebolisce / Neutro su pilastro X | Nessuna / Aumentare / Ridurre / Uscire | Alta / Media / Bassa |

### Step 3: Scorecard Tesi

| Pilastro | Aspettativa originale | Stato attuale | Trend |
|----------|----------------------|---------------|-------|
| Crescita ricavi >5% | In linea | H1 +6% organico | Stabile |
| Espansione margini | In ritardo | EBITDA margin flat YoY | Attenzione |
| Riduzione PFN | In anticipo | PFN −15% vs FY precedente | Positivo |

### Step 4: Calendario Catalizzatori

| Data | Evento | Impatto atteso | Note |
|------|--------|---------------|------|
| | | | |

### Step 5: Output

Sintesi tesi per: morning meeting, portfolio review, comitato rischi.
Formato: markdown o Word con scorecard, aggiornamenti recenti, livello di convinzione.

## Errori Comuni da Evitare

### ❌ Ignorare il rischio paese Italia
Lo spread BTP-Bund, il rating sovrano, e le decisioni politiche (Legge di Bilancio, Golden Power) possono impattare la tesi indipendentemente dai fondamentali della società. Includere sempre un pilastro/rischio macro.
