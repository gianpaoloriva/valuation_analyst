---
name: fsi-dd-checklist-italy
description: >
  Checklist di due diligence per acquisizioni in Italia: workstream finanziari
  (IFRS, TFR, IRAP), legali (diritto societario italiano, Collegio Sindacale),
  fiscali (IRES+IRAP, transfer pricing), giuslavoristici (CCNL, TFR, art. 2112 c.c.),
  regolatori (GDPR, D.Lgs. 231, Golden Power).
  Triggers on "dd checklist", "due diligence", "checklist diligence",
  "cosa manca nella DD", "data room review", "diligence tracker".
---

# Due Diligence Checklist — Contesto Italiano

Adapt dello skill US `dd-checklist`. La struttura (scope → workstreams → tracking → red flags → output) è universale. Adattati i workstream con specifiche italiane.

**Per la struttura completa del workflow e il tracking**: riferirsi allo skill US `dd-checklist`. Qui si documentano gli adattamenti per workstream.

## Adattamenti per Workstream

### Financial Due Diligence — Integrazioni Italia

Voci aggiuntive specifiche per target italiane:
- **TFR**: fondo accantonato, flussi annui, quota conferita a fondi pensione vs in azienda. TFR è un debt-like item
- **IFRS 16**: passività per leasing on-balance, impatto su EBITDA e PFN
- **IRAP**: base imponibile separata, aliquota effettiva (variabile per regione: 3,9% base, fino a 4,97%)
- **Fondi rischi e oneri (IAS 37)**: contenziosi in corso, accantonamenti
- **Avviamento (IAS 36)**: no ammortamento, impairment test — verificare i test effettuati e le assunzioni
- **PFN (Posizione Finanziaria Netta)**: riconciliazione dettagliata, definizione condivisa tra le parti
- **Working capital**: DSO e DPO italiani tipicamente più lunghi (DSO 60-90 gg). Normalizzazione vs stagionalità
- **Perdite fiscali**: plafond art. 84 TUIR, limite 80% utilizzo, trasferibilità in caso di M&A (limitazioni art. 84 c. 3)

### Legal Due Diligence — Integrazioni Italia

- **Struttura societaria**: SPA / SRL / SAPA, statuto, patti parasociali
- **Organi di controllo**: Collegio Sindacale (composizione, verbali, rilievi), società di revisione (durata incarico, rotazione obbligatoria)
- **Contratti materiali**: verificare clausole di change of control (frequenti in contratti italiani)
- **Contenzioso**: verificare sia cause attive che passive, incluse cause di lavoro (frequenti in Italia)
- **Proprietà intellettuale**: brevetti, marchi registrati presso UIBM (Ufficio Italiano Brevetti e Marchi)
- **Immobili**: titoli di proprietà, catasto, conformità urbanistica, eventuali vincoli (paesaggistici, culturali)
- **D.Lgs. 231/2001**: Modello di Organizzazione e Gestione (MOG) — responsabilità amministrativa degli enti. Verificare se adottato, se aggiornato, Organismo di Vigilanza (OdV)

### Tax Due Diligence — Specifico Italia

- **IRES + IRAP**: aliquote, base imponibile IRAP, deducibilità costi
- **Transfer pricing**: documentazione (Master File, Local File) se parte di gruppo, rischi di rettifica
- **Accertamenti in corso**: verificare se ci sono accertamenti aperti con Agenzia delle Entrate
- **Consolidato fiscale**: se il target è in un consolidato, impatto della fuoriuscita
- **IVA**: gruppo IVA, crediti IVA, eventuali contestazioni
- **Agevolazioni fiscali**: Patent Box, credito d'imposta R&S (art. 1 c. 198-209 L. 160/2019), ZES
- **Perdite fiscali riportabili**: quantità, scadenza, limitazioni in caso di cambio di controllo (art. 84 c. 3 TUIR)
- **Imposta di registro**: se asset deal, stima dell'imposta proporzionale

### HR / People Due Diligence — Specifico Italia

- **CCNL**: contratto collettivo nazionale applicato, livello di inquadramento
- **TFR**: per dipendente, fondo vs fondi pensione
- **Art. 2112 c.c.**: in caso di cessione d'azienda, i rapporti di lavoro proseguono automaticamente con l'acquirente (nessun licenziamento per il solo trasferimento)
- **Accordi sindacali**: verificare accordi aziendali, RSU/RSA, eventuali procedure di licenziamento collettivo in corso
- **Contenziosi di lavoro**: particolarmente frequenti in Italia — verificare cause pendenti e rischio
- **Dirigenti**: contratto individuale, patti di non concorrenza, trattamento di fine mandato
- **Welfare aziendale**: benefit, polizze sanitarie integrative, fondi pensione aziendali

### IT / Technology Due Diligence — Integrazione

- **GDPR**: compliance al Reg. UE 2016/679 e al D.Lgs. 196/2003 (Codice Privacy), DPO nominato, DPIA effettuate
- **DORA** (Reg. UE 2022/2554): se target è operatore finanziario — resilienza operativa digitale
- **Perimetro di sicurezza nazionale cibernetica**: se target in settori strategici (D.L. 105/2019)
- ~~CCPA~~: non applicabile in Italia (sostituito da GDPR)

### Environmental / ESG — Integrazione

- **D.Lgs. 152/2006** (Testo Unico Ambiente): autorizzazioni ambientali (AIA, AUA), scarichi, rifiuti
- **Bonifica siti contaminati**: verificare se il sito è nel SIN (Siti di Interesse Nazionale) o nel catasto siti contaminati regionale
- **SFDR / Tassonomia UE**: classificazione ESG se rilevante per l'investitore
- **ETS (Emission Trading System)**: se il target è soggetto, verificare quote CO₂

### Regolatorio — Sezione Aggiuntiva (non presente nello skill US)

- **Golden Power**: verificare se il target opera in settori strategici (D.L. 21/2012). Se sì, obbligo di notifica per acquirenti esteri
- **Autorizzazioni settoriali**: licenze, concessioni, autorizzazioni specifiche per il settore del target
- **Antitrust AGCM**: verificare se l'operazione supera le soglie di notifica
- **D.Lgs. 231/2007 (AML)**: se il target è soggetto obbligato, verificare compliance antiriciclaggio

## Errori Comuni da Evitare

### ❌ Usare CCPA come riferimento privacy
In Italia/UE il riferimento è il GDPR (Reg. UE 2016/679). Il CCPA è la normativa privacy californiana e non si applica.

### ❌ Ignorare l'art. 2112 c.c.
In una cessione d'azienda, i rapporti di lavoro proseguono automaticamente. Non è possibile licenziare dipendenti per il solo fatto del trasferimento. Questo ha impatto significativo sulla struttura del deal e sui costi.

### ❌ Non verificare il D.Lgs. 231/2001
Il Modello 231 (responsabilità amministrativa degli enti per reati commessi nell'interesse della società) è un elemento critico della DD legale italiana. L'assenza di un MOG aggiornato è un red flag.
