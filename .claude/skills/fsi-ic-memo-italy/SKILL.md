---
name: fsi-ic-memo-italy
description: >
  Memo per Investment Committee su deal PE in Italia: sintesi DD, analisi
  finanziaria IFRS, deal terms con fiscalità italiana (PEX, IRES+IRAP),
  rendimenti con WACC italiano, raccomandazione strutturata.
  Triggers on "IC memo", "memo investment committee", "write-up del deal",
  "materiali IC", "memo di raccomandazione", "memo comitato investimenti".
---

# Investment Committee Memo — Contesto Italiano

Adapt dello skill US `ic-memo`. La struttura del memo è universale. Adattamenti su sezioni finanziarie, fiscali, e deal structure per il contesto italiano.

**Per la struttura completa del memo**: riferirsi allo skill US `ic-memo`. Qui si documentano gli adattamenti.

## Adattamenti al Contesto Italiano

### Sezione IV — Financial Analysis: Integrazioni

- Bilanci in IFRS (non US GAAP)
- QoE adjustments specifici: TFR, IFRS 16, fondi rischi IAS 37, avviamento IAS 36
- PFN (Posizione Finanziaria Netta) come metrica standard per il debito
- NWC con DSO/DPO italiani (più lunghi che US)
- Aliquota fiscale effettiva: IRES 24% + IRAP ~3,9% = ~27,9%
- Nota su deducibilità interessi (art. 96 TUIR — limite 30% ROL)

### Sezione VI — Deal Terms & Structure: Integrazioni

- **Struttura**: cessione partecipazioni (share deal) vs cessione azienda (asset deal)
- **PEX**: se share deal da veicolo societario con requisiti art. 87 TUIR → aliquota effettiva ~1,2% sulla plusvalenza
- **Imposta di registro**: se asset deal → proporzionale (3% avviamento, 2% immobili)
- **Affrancamento**: opzione step-up ex art. 176 c. 2-ter TUIR (imposta sostitutiva 12-16%)
- **Leva**: financing su Euribor + spread (non SOFR), leva tipica 3,0-4,5x EBITDA (mercato italiano)
- **Governance post-deal**: composizione CdA, Collegio Sindacale, diritti di minoranza per management/famiglia
- **Clausole tipiche italiane**: tag-along, drag-along, put/call, earn-out, escrow per reps & warranties

### Sezione VII — Returns Analysis: Integrazioni

- IRR e MOIC con parametri italiani (vedi skill `returns-analysis-italy`)
- Scenario fiscale: confronto PEX vs regime ordinario
- Impatto art. 96 TUIR su tax shield effettivo
- Carried interest: condizioni art. 60 D.L. 50/2017

### Sezione VIII — Risk Factors: Rischi Specifici Italia

Includere nel risk assessment:
- **Rischio regolatorio**: Golden Power, AGCM, regolatori settoriali
- **Rischio paese**: spread BTP-Bund, rating sovrano, instabilità politica
- **Rischio giuslavoristico**: rigidità art. 2112 c.c. (trasferimento d'azienda), CCNL, contenzioso lavoro
- **Rischio fiscale**: accertamenti in corso, transfer pricing, perdita agevolazioni
- **Rischio governance**: gestione della transizione da proprietà familiare a PE

### Valuta e Formato

- Tutti gli importi in EUR (€)
- S&U (Sources & Uses) in €M
- Multipli confrontati con transazioni italiane/europee comparabili

## Errori Comuni da Evitare

### ❌ Presentare returns senza scenario fiscale
La differenza tra PEX (~1,2% effettiva) e regime ordinario (~24% IRES) è enorme. Sempre mostrare i rendimenti netti con indicazione del regime fiscale applicabile.

### ❌ Usare SOFR o Treasury nel financing
Il debito è prezzato su Euribor 3M/6M + spread. Usare sempre parametri di mercato europei.

### ❌ Ignorare la governance post-deal
Nel PE italiano, la struttura post-deal (CdA, Collegio Sindacale, patti parasociali, diritti di co-vendita) è un elemento critico che va dettagliato nel memo, non solo accennato.
