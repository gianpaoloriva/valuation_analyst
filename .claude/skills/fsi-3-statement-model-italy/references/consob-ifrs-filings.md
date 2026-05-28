# Estrazione Dati da Bilanci IFRS — Contesto Italiano

**Quando usare:** Referenziare questo file quando un template di modello richiede l'estrazione di dati da bilanci di società italiane quotate (IFRS) o non quotate (OIC). Per template che forniscono dati direttamente o usano altre fonti dati, questo riferimento non è necessario.

---

## Fonti Dati per Società Italiane

### Società Quotate (IFRS obbligatorio)

| Fonte | Contenuto | Accesso |
|-------|-----------|---------|
| **CONSOB** | Comunicazioni price sensitive, prospetti, OPA, partecipazioni rilevanti | consob.it → Emittenti |
| **Borsa Italiana** | Bilanci, relazioni, prezzi, scheda società | borsaitaliana.it → Scheda società |
| **Bureau van Dijk / AIDA** | Bilanci strutturati, indici, confronti settoriali | Accesso su abbonamento |
| **Refinitiv / LSEG** | Consensus, stime analisti, dati di mercato | Accesso su abbonamento |
| **InfoCamere / Registro Imprese** | Visure camerali, bilanci depositati | registroimprese.it |

### Società Non Quotate (OIC)

| Fonte | Contenuto |
|-------|-----------|
| **Registro Imprese** | Bilanci depositati (obbligatorio per tutte le società di capitali) |
| **AIDA / Bureau van Dijk** | Bilanci strutturati con indici |
| **CERVED** | Report aziendali, scoring, analisi settoriali |

## Struttura del Bilancio IFRS Italiano

### Documenti Obbligatori

1. **Relazione sulla gestione** — Analisi della situazione patrimoniale, economica e finanziaria
2. **Bilancio consolidato IFRS** (se gruppo):
   - Situazione patrimoniale-finanziaria consolidata (Stato Patrimoniale)
   - Conto economico consolidato
   - Conto economico complessivo (OCI)
   - Prospetto delle variazioni del patrimonio netto
   - Rendiconto finanziario consolidato
   - Note al bilancio consolidato
3. **Bilancio d'esercizio** (capogruppo, può essere OIC o IFRS)
4. **Relazione della società di revisione**
5. **Relazione del Collegio Sindacale**

### Calendario di Pubblicazione

| Documento | Scadenza | Contenuto |
|-----------|----------|-----------|
| **Relazione annuale** | Entro 120 gg dalla chiusura esercizio (aprile per FY dic) | Bilancio completo, 2 anni comparativi |
| **Relazione semestrale** | Entro 60 gg dalla chiusura semestre (settembre per H1) | Bilancio semestrale abbreviato IFRS (IAS 34) |
| **Resoconto intermedio di gestione** | Facoltativo dal 2014 (molte large cap lo pubblicano ancora) | Q1/Q3 aggiornamento |

## Mappatura Voci di Bilancio IFRS → Modello

### Conto Economico (da Conto Economico Consolidato)

| Voce Bilancio IFRS | Voce Modello | Note |
|---------------------|-------------|------|
| Ricavi / Ricavi netti | Revenue / Ricavi | IFRS 15 — per performance obligation |
| Costo del venduto | COGS | Può includere D&A di produzione |
| Costi commerciali e di distribuzione | S&M / Selling Expenses | |
| Costi generali e amministrativi | G&A | Può includere compensi amministratori |
| Costi di ricerca e sviluppo | R&D | IAS 38: sviluppo capitalizzabile se criteri soddisfatti |
| Ammortamenti e svalutazioni | D&A | Separare ammortamento (D) da svalutazione (impairment) |
| Accantonamenti | Provisions | Fondi rischi e oneri (IAS 37) |
| Proventi / (Oneri) finanziari netti | Net Interest Expense | Include interessi su leasing IFRS 16 |
| Quota risultato società collegate | Equity Income | Metodo del patrimonio netto (IAS 28) |
| Imposte sul reddito | Taxes | IRES + IRAP (basi imponibili diverse) |
| Utile / (Perdita) del periodo | Net Income | |
| Utile / (Perdita) di pertinenza di terzi | Minority Interest | Da detrarre per NI di gruppo |

### Stato Patrimoniale (da Situazione Patrimoniale-Finanziaria)

**Struttura IFRS — Corrente / Non Corrente:**

| Voce Bilancio IFRS | Voce Modello | Note |
|---------------------|-------------|------|
| Disponibilità liquide e mezzi equivalenti | Cash | |
| Crediti commerciali | AR (Accounts Receivable) | Verificare DSO (60-90 gg Italia) |
| Rimanenze | Inventory | |
| Crediti tributari | Tax Receivables | Crediti IRES/IRAP/IVA |
| Altre attività correnti | Other Current Assets | |
| **Totale attività correnti** | **Total Current Assets** | |
| Immobili, impianti e macchinari | PP&E | IAS 16, include diritti d'uso IFRS 16 |
| Avviamento | Goodwill | IAS 36: no ammortamento, impairment test annuale |
| Altre attività immateriali | Intangible Assets | IAS 38: brevetti, concessioni, software |
| Partecipazioni | Equity Investments | Metodo equity (IAS 28) o FVTOCI |
| Attività per imposte anticipate | DTA (Deferred Tax Asset) | Include beneficio perdite fiscali |
| **Totale attività non correnti** | **Total Non-Current Assets** | |
| **TOTALE ATTIVO** | **Total Assets** | |
| Debiti commerciali | AP (Accounts Payable) | Verificare DPO (60-75 gg Italia) |
| Debiti finanziari correnti | Current Debt | Quota corrente mutui + linee di credito |
| Passività per leasing correnti | Current Lease Liabilities | IFRS 16 |
| Debiti tributari | Tax Payables | IRES/IRAP/IVA a debito |
| Fondo TFR (quota corrente) | Current TFR | Parte esigibile entro 12 mesi |
| Altre passività correnti | Other Current Liabilities | |
| **Totale passività correnti** | **Total Current Liabilities** | |
| Debiti finanziari non correnti | LT Debt | Obbligazioni, mutui, prestiti sindacati |
| Passività per leasing non correnti | Non-Current Lease Liabilities | IFRS 16 |
| Fondo TFR | TFR (Employee Severance) | IAS 19 — passività per benefici ai dipendenti |
| Fondi rischi e oneri | Provisions | IAS 37 — contenziosi, garanzie, ristrutturazioni |
| Passività per imposte differite | DTL (Deferred Tax Liability) | |
| **Totale passività non correnti** | **Total Non-Current Liabilities** | |
| **TOTALE PASSIVO** | **Total Liabilities** | |
| Capitale sociale | Share Capital | |
| Riserva sovrapprezzo azioni | Share Premium | |
| Altre riserve | Other Reserves | Riserva legale, OCI, riserve di conversione |
| Utili portati a nuovo | Retained Earnings | |
| **Patrimonio netto di gruppo** | **Total Equity (Group)** | |
| Patrimonio netto di terzi | Minority Interest (Equity) | |
| **TOTALE PATRIMONIO NETTO** | **Total Equity** | |

### Rendiconto Finanziario (da Rendiconto Finanziario Consolidato)

Le società IFRS possono usare metodo diretto o indiretto. La maggior parte usa il **metodo indiretto**.

| Voce Bilancio IFRS | Voce Modello | Note |
|---------------------|-------------|------|
| Utile del periodo | Net Income | Punto di partenza (metodo indiretto) |
| Ammortamenti | D&A | Add-back non monetario |
| Accantonamento TFR | TFR Provision | Add-back non monetario |
| Variazione crediti commerciali | ΔAR | Aumento = uso di cassa |
| Variazione rimanenze | ΔInventory | Aumento = uso di cassa |
| Variazione debiti commerciali | ΔAP | Aumento = fonte di cassa |
| Pagamento TFR | TFR Payments | Uso di cassa |
| Imposte pagate | Taxes Paid | Può differire da imposte da CE |
| Investimenti in immobilizzazioni | CapEx | |
| Acquisizioni di partecipazioni | Acquisitions | Al netto della cassa acquisita |
| Accensione debiti finanziari | Debt Issuance | |
| Rimborso debiti finanziari | Debt Repayment | |
| Pagamento canoni leasing | Lease Payments | IFRS 16: quota capitale in CFF |
| Dividendi pagati | Dividends | |
| Aumento di capitale | Equity Issuance | |

## Note Specifiche per l'Italia

### TFR (Trattamento di Fine Rapporto)

Il TFR è una passività specifica italiana per benefici ai dipendenti:
- **Post riforma 2007**: per aziende >50 dipendenti, il TFR matura verso INPS o fondi pensione (non più in azienda)
- **In bilancio**: il TFR residuo in azienda è valutato con metodo attuariale (IAS 19)
- **Nel modello**: trattare come passività a lungo termine, simile a un fondo pensione
- **Cash flow**: accantonamento TFR (add-back in CFO), pagamenti TFR (uso di cassa in CFO)

### IRAP e IRES — Due Imposte Separate

- **IRES** (24%): base imponibile = utile ante imposte con aggiustamenti fiscali
- **IRAP** (3.9% base): base imponibile = valore della produzione netta (NON deducibili interessi passivi e costo del lavoro dipendente)
- Nel modello semplificato: usare aliquota combinata ~27.9% su EBIT
- Nel modello dettagliato: calcolare IRES e IRAP separatamente su basi imponibili diverse

### Perdite Fiscali (Art. 84 TUIR) — Equivalente NOL

- **Riporto illimitato nel tempo** (no scadenza, a differenza di alcuni regimi pre-2011)
- **Limite utilizzo**: max 80% del reddito imponibile IRES di ciascun esercizio
- **Eccezione primi 3 esercizi**: perdite dei primi 3 periodi d'imposta utilizzabili al 100% (no limite 80%)
- **IRAP**: le perdite IRAP seguono regole proprie (riportabili con limite 80% dal 2012)
- **Fusioni/scissioni**: limiti all'utilizzo delle perdite della società incorporata (art. 172 TUIR — test vitalità)

### Dati Storici Richiesti

Estrarre minimo 3 anni di dati storici:
- La relazione annuale IFRS fornisce 2 anni comparativi per CE/CF, 2 per SP
- Per il 3° anno SP, estrarre dalla relazione annuale dell'anno precedente
- Le relazioni semestrali (IAS 34) forniscono dati comparativi del semestre precedente

### Checklist Estrazione Dati

- Identificare valuta e scala di reporting (migliaia, milioni di euro)
- 3 anni storici Conto Economico
- 3 anni storici Rendiconto Finanziario
- 3 anni storici Stato Patrimoniale
- Verificare NI dal CE = NI iniziale del Rendiconto Finanziario (ogni anno)
- Verificare Cassa SP = Cassa finale Rendiconto Finanziario (ogni anno)
- Estrarre scadenziario debito dalle note
- Estrarre dettaglio D&A o assunzioni vita utile
- Estrarre dettaglio TFR (accantonamento, utilizzi, utili/perdite attuariali)
- Notare voci non ricorrenti / one-time da normalizzare
- Verificare se la società riporta per segmento (IFRS 8)
