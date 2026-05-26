---
name: fsi-buyer-list-italy
description: >
  Costruzione lista buyer per processi M&A sell-side nel mercato italiano:
  buyer strategici e financial sponsor, con note su soglie AGCM, Golden Power,
  e sponsor attivi in Italia. Prioritizzazione e contact mapping.
  Triggers on "buyer list", "lista buyer", "potenziali acquirenti",
  "chi comprerebbe", "buyer strategici", "financial sponsor", "universo buyer".
---

# Buyer List — Contesto Italiano

Adapt dello skill US `buyer-list`. Il workflow è quasi interamente universale. Adattamenti minimi su antitrust, Golden Power, e financial sponsor attivi in Italia.

**Per la struttura completa del workflow**: riferirsi allo skill US `buyer-list`. Qui si documentano solo gli adattamenti.

## Adattamenti al Contesto Italiano

### Step 2 — Buyer Strategici: Note Aggiuntive

Per ciascun buyer strategico, valutare in aggiunta:
- **Rischio antitrust AGCM**: soglie di notifica (fatturato in Italia >€532M o fatturato imprese interessate >€32M). Se superata, l'operazione va notificata all'AGCM — tempi di autorizzazione ~45 giorni (Fase I), fino a 6 mesi se Fase II
- **Golden Power**: se il target opera in settori strategici (5G, AI, semiconduttori, energia, difesa, agroalimentare, finanza), l'acquirente estero (extra-UE ed extra-SEE) potrebbe dover notificare alla Presidenza del Consiglio. Anche investitori UE in alcuni casi
- **Antitrust UE**: se supera soglie EUMR (fatturato mondiale >€5Mld, fatturato UE >€250M per almeno 2 imprese), competenza Commissione EU

### Step 3 — Financial Sponsor: Contesto Italiano

| Categoria | Sponsor attivi in Italia (esempi) |
|-----------|----------------------------------|
| Large cap PE | Advent, CVC, KKR, BC Partners, Cinven, Permira, Bain Capital |
| Mid-market PE | Investindustrial, Ardian, PAI Partners, Tikehau, NB Renaissance, Triton |
| Italian-focused PE | Clessidra, Progressio, Xenon, DeA Capital, Quadrivio, Alcedo |
| Infrastrutture | Macquarie, Brookfield, Antin, F2i (italiano) |
| Growth equity | General Atlantic, Insight, TCV, Italian Angels for Growth |

Per ogni sponsor verificare:
- Fund vintage e deployment pace (come US)
- Track record specifico in Italia (le operazioni mid-market italiane richiedono spesso gestione della famiglia fondatrice)
- Capacità di operare con management italiano e governance italiana (Collegio Sindacale, assemblee)

### Step 4 — Prioritizzazione: Note Aggiuntive

- Verificare se il buyer è soggetto a Golden Power → aggiungere nella colonna "Note"
- Per buyer esteri: valutare la complessità regolatoria (AGCM + eventualmente Commissione EU + Golden Power) → impatto su timeline
- Per target familiari italiani: prioritizzare buyer che hanno track record nel gestire management continuity e transizioni generazionali

### Valuta

Tutti gli importi in EUR (€). Revenue e financial capacity in €M.

## Errori Comuni da Evitare

### ❌ Ignorare Golden Power
Per target in settori strategici, un buyer extra-UE potrebbe vedersi bloccare o condizionare l'operazione. Verificare sempre l'applicabilità prima di inserire nel Tier 1.

### ❌ Sottovalutare la componente familiare
Molte società target in Italia sono a proprietà familiare. Il seller spesso ha preferenze forti su management continuity, sede, brand, occupazione. Mappare queste preferenze nello Step 1.
