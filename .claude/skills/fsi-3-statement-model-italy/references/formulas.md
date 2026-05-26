# Formula Reference — Contesto Italiano/IFRS

**IMPORTANTE:** Usare le formule indicate in questo documento di riferimento salvo diversa indicazione dell'utente.

---

## Linkage Fondamentali

```
Stato Patrimoniale:   Attivo = Passivo + Patrimonio Netto
Utile Netto:          CE Utile Netto → Rendiconto Finanziario (punto di partenza)
Cash Flow:            ΔCassa = CFO + CFI + CFF
Cash Tie-Out:         Cassa Finale (RF) = Cassa (SP Attivo)
Utili Portati a Nuovo: UPN precedente + Utile Netto - Dividendi = UPN finale
Aumento di Capitale:  ΔCapitale Sociale/Sovrapprezzo (SP) = Emissione Equity (CFF)
```

## Calcolo Utile Lordo

**IMPORTANTE:** L'Utile Lordo deve essere calcolato dai Ricavi Netti, non dai Ricavi Lordi.

```
Ricavi Netti - Costo del Venduto = Utile Lordo
```

| Termine | Definizione |
|---------|------------|
| Ricavi Lordi | Ricavi totali prima di deduzioni |
| Ricavi Netti | Ricavi Lordi - Resi - Abbuoni - Sconti |
| Costo del Venduto | Costi diretti attribuibili alla produzione dei beni/servizi venduti |
| Utile Lordo | Ricavi Netti - Costo del Venduto |

## Formule Margini

```
Margine Lordo %       = Utile Lordo / Ricavi Netti
EBITDA                = EBIT + D&A  (oppure = Utile Lordo - OpEx)
Margine EBITDA %      = EBITDA / Ricavi Netti
Margine EBIT %        = EBIT / Ricavi Netti
Margine Utile Netto % = Utile Netto / Ricavi Netti
```

## Formule Metriche Creditizie

```
Debito Totale           = Debiti Finanziari Correnti + Debiti Finanziari Non Correnti
PFN (Posiz. Fin. Netta) = Debito Totale - Cassa (+ Passività Leasing IFRS 16 se incluse)
Debito Totale / EBITDA  = Debito Totale / EBITDA (da CE)
PFN / EBITDA            = PFN / EBITDA (da CE)
Interest Coverage       = EBITDA / Oneri Finanziari (da CE)
Debito / Cap. Totale    = Debito Totale / (Debito Totale + Patrimonio Netto)
Debito / PN             = Debito Totale / Patrimonio Netto
Current Ratio           = Totale Attività Correnti / Totale Passività Correnti
Quick Ratio             = (Attività Correnti - Rimanenze) / Passività Correnti
```

## Formule di Previsione (Metodo % dei Ricavi Netti)

```
Costo del Venduto (Prev.)  = Ricavi Netti × % Costo del Venduto (da Assunzioni)
Costi Commerciali (Prev.)  = Ricavi Netti × % S&M (da Assunzioni)
Costi G&A (Prev.)          = Ricavi Netti × % G&A (da Assunzioni)
Costi R&D (Prev.)          = Ricavi Netti × % R&D (da Assunzioni)
SBC (Prev.)                = Ricavi Netti × % SBC (da Assunzioni)
```

## Formule Capitale Circolante

```
Crediti Commerciali (AR)
  AR Precedente
  + Ricavi (da CE)
  - Incassi (plug)
  = AR Finale
  DSO = (AR / Ricavi) × 365
  Range tipico Italia: 60-90 giorni (vs 30-45 US)

Rimanenze
  Rimanenze Precedenti
  + Acquisti (plug)
  - Costo del Venduto (da CE)
  = Rimanenze Finali
  DIO = (Rimanenze / Costo del Venduto) × 365

Debiti Commerciali (AP)
  AP Precedente
  + Acquisti (da calcolo Rimanenze)
  - Pagamenti (plug)
  = AP Finale
  DPO = (AP / Costo del Venduto) × 365
  Range tipico Italia: 60-75 giorni (vs 30-45 US)

Capitale Circolante Netto = AR + Rimanenze - AP
ΔCCN = CCN Corrente - CCN Precedente
```

## Formule Schedule D&A

```
PP&E Lordo Iniziale
+ CapEx
= PP&E Lordo Finale

Fondo Ammortamento Iniziale
+ Quota Ammortamento
= Fondo Ammortamento Finale

PP&E Netto = PP&E Lordo - Fondo Ammortamento

Nota IFRS 16: Diritti d'Uso (Right-of-Use Assets)
  RoU Iniziale
  + Nuovi Leasing
  - Ammortamento RoU
  = RoU Finale
  (L'ammortamento RoU va in D&A; gli interessi su leasing in Oneri Finanziari)
```

## Formule Schedule Debito

```
Debito Finanziario Iniziale
+ Nuove Accensioni
- Rimborsi
= Debito Finanziario Finale

Oneri Finanziari = Debito Medio × Tasso di Interesse
  (Usare saldo iniziale per evitare circolarità, o iterare se riferimenti circolari abilitati)

Nota IFRS 16: Passività per Leasing
  Passività Leasing Iniziale
  + Nuovi Leasing
  - Pagamenti Canoni (quota capitale)
  = Passività Leasing Finale
  Interessi su Leasing = Passività Leasing Iniziale × Tasso Implicito
```

## Formule TFR (Trattamento di Fine Rapporto)

```
SCHEDULE TFR (IAS 19)

Fondo TFR Iniziale
+ Costo del Servizio Corrente (service cost)
+ Oneri Finanziari su TFR (interest cost = TFR iniziale × tasso di attualizzazione)
+/- Utili/Perdite Attuariali (remeasurement — in OCI, non in CE)
- Pagamenti TFR (liquidazioni, anticipi, trasferimenti a INPS/fondi pensione)
= Fondo TFR Finale

Nel Cash Flow (metodo indiretto):
  Accantonamento TFR (service cost + interest cost): add-back in CFO
  Pagamenti TFR: uso di cassa in CFO
  Utili/Perdite Attuariali: non transitano per il CE, vanno in OCI

Per aziende >50 dipendenti (post riforma 2007):
  La quota TFR maturanda va a INPS o fondi pensione complementare
  In azienda resta solo il TFR pregresso (in graduale esaurimento)
```

## Formule Utili Portati a Nuovo

```
Utili Portati a Nuovo Iniziali
+ Utile Netto (da CE)
+/- Altre Variazioni (OCI riclassificato, SBC se applicabile)
- Dividendi
= Utili Portati a Nuovo Finali
```

## Perdite Fiscali (Art. 84 TUIR) — Equivalente NOL

```
SCHEDULE PERDITE FISCALI RIPORTABILI

Perdite Fiscali Iniziali (Anno 1 / Costituzione = 0)
+ Perdite Generate (se Reddito Imponibile IRES < 0, allora ABS(RI), altrimenti 0)
- Perdite Utilizzate (limitato da reddito imponibile e cap di utilizzo)
= Perdite Fiscali Finali

REGOLA SALDO INIZIALE

Per nuova società o primo periodo modellato:
  Saldo Perdite Iniziale = 0
  Le perdite possono aumentare solo attraverso perdite realizzate (RI < 0)

CALCOLO UTILIZZO PERDITE (Art. 84 TUIR)

Reddito Imponibile IRES (EBT con aggiustamenti fiscali)
  Se RI > 0:
    Perdite Disponibili = Saldo Perdite Iniziale
    Limite Utilizzo = RI × 80% (limite generale)
    ECCEZIONE: Perdite dei primi 3 esercizi → utilizzabili al 100% (no limite 80%)
    Perdite Utilizzate = MIN(Perdite Disponibili, Limite Utilizzo)
    Reddito Tassabile = RI - Perdite Utilizzate
  Se RI ≤ 0:
    Perdite Utilizzate = 0
    Reddito Tassabile = 0
    Perdite Generate = ABS(RI)

CALCOLO IMPOSTE CON PERDITE

IRES = MAX(0, Reddito Tassabile IRES × 24%)
IRAP = MAX(0, Valore Produzione Netta × aliquota IRAP)
  ATTENZIONE: perdite IRES NON riducono base IRAP
  Perdite IRAP hanno regole proprie (riportabili con limite 80% dal 2012)

Imposte Totali = IRES + IRAP

IMPOSTE ANTICIPATE (DTA) PER PERDITE FISCALI

DTA - Perdite Riportabili = Saldo Perdite × 24% (solo aliquota IRES)
ΔDTA = DTA Corrente - DTA Precedente
  (Aumento DTA = beneficio non monetario in CF)
  (Riduzione DTA = costo non monetario in CF)

NOTE IMPORTANTI:
- Riporto illimitato nel tempo (no scadenza)
- In caso di fusione/scissione: test di vitalità art. 172 TUIR
  (patrimonio netto e ricavi della società con perdite devono superare soglie)
- Consolidato fiscale: perdite utilizzabili solo all'interno del gruppo
```

## Struttura Stato Patrimoniale (IFRS)

```
ATTIVO
  Disponibilità liquide (da RF cassa finale)
  Crediti commerciali (da CCN)
  Rimanenze (da CCN)
  Crediti tributari
  Altre attività correnti
  Totale Attività Correnti

  Immobili, impianti e macchinari netti (da Schedule D&A)
  Diritti d'uso (IFRS 16)
  Avviamento (impairment test annuale, NO ammortamento)
  Altre attività immateriali
  Partecipazioni
  Attività per imposte anticipate (da Schedule Perdite Fiscali)
  Totale Attività Non Correnti
  TOTALE ATTIVO

PASSIVO
  Debiti commerciali (da CCN)
  Debiti finanziari correnti (da Schedule Debito)
  Passività per leasing correnti (IFRS 16)
  Debiti tributari
  Fondo TFR quota corrente
  Altre passività correnti
  Totale Passività Correnti

  Debiti finanziari non correnti (da Schedule Debito)
  Passività per leasing non correnti (IFRS 16)
  Fondo TFR (da Schedule TFR)
  Fondi rischi e oneri (IAS 37)
  Passività per imposte differite
  Totale Passività Non Correnti
  TOTALE PASSIVO

PATRIMONIO NETTO
  Capitale sociale
  Riserva sovrapprezzo azioni
  Altre riserve (riserva legale, OCI, conversione)
  Utili portati a nuovo (da Schedule UPN)
  Patrimonio Netto di Gruppo
  Patrimonio Netto di Terzi
  TOTALE PATRIMONIO NETTO

CHECK: Attivo - Passivo - Patrimonio Netto = 0
```

## Struttura Rendiconto Finanziario (Metodo Indiretto)

```
FLUSSI DA ATTIVITÀ OPERATIVA (CFO)
  Utile Netto (LINK: CE)
  + Ammortamenti (LINK: Schedule D&A, include RoU IFRS 16)
  + Accantonamento TFR (LINK: Schedule TFR)
  + SBC se applicabile
  - ΔDTA (Imposte Anticipate) (LINK: Schedule Perdite Fiscali)
  - ΔCrediti commerciali (LINK: CCN)
  - ΔRimanenze (LINK: CCN)
  + ΔDebiti commerciali (LINK: CCN)
  - Pagamenti TFR (LINK: Schedule TFR)
  = CFO

FLUSSI DA ATTIVITÀ DI INVESTIMENTO (CFI)
  - CapEx (LINK: Schedule D&A)
  - Acquisizioni partecipazioni
  = CFI

FLUSSI DA ATTIVITÀ DI FINANZIAMENTO (CFF)
  + Accensione debiti finanziari (LINK: Schedule Debito)
  - Rimborso debiti finanziari (LINK: Schedule Debito)
  - Pagamento canoni leasing quota capitale (LINK: IFRS 16)
  + Aumento di capitale (LINK: SP Capitale/Sovrapprezzo)
  - Dividendi (LINK: Schedule UPN)
  = CFF

Variazione Netta di Cassa = CFO + CFI + CFF
Cassa Iniziale
+ Variazione Netta di Cassa
= Cassa Finale (LINK A: SP Disponibilità Liquide)
```

## Struttura Conto Economico (IFRS)

```
Ricavi Netti
  Crescita %
(-) Costo del Venduto
  % dei Ricavi Netti
────────────────
Utile Lordo (= Ricavi Netti - Costo del Venduto)
  Margine Lordo %

(-) Costi Commerciali
  % dei Ricavi Netti
(-) Costi G&A
  % dei Ricavi Netti
(-) Costi R&D
  % dei Ricavi Netti
(-) Ammortamenti (se non inclusi sopra)
(-) SBC (se applicabile)
  % dei Ricavi Netti
────────────────
EBIT (Risultato Operativo)
  Margine EBIT %

EBITDA (= EBIT + D&A)
  Margine EBITDA %

(+/-) Proventi / (Oneri) finanziari netti
  (include interessi su leasing IFRS 16)
────────────────
EBT (Risultato Prima delle Imposte)
(-) Utilizzo Perdite Fiscali (da Schedule Perdite, riduce reddito tassabile IRES)
────────────────
Reddito Tassabile
(-) IRES (Reddito Tassabile × 24%)
(-) IRAP (Valore Produzione Netta × 3.9%)
  Nota: base imponibile IRAP ≠ base imponibile IRES
────────────────
Utile Netto
  Margine Utile Netto %

(-) Utile di pertinenza di terzi
= Utile Netto di Gruppo
```

## Formule di Controllo

```
Check SP:               = Attivo - Passivo - Patrimonio Netto  (deve = 0)
Cash Tie-Out:            = Cassa SP - Cassa Finale RF           (deve = 0)
Roll-Forward UPN:        = UPN prec. + UN - Dividendi - UPN SP  (deve = 0)
DTA Tie-Out:             = DTA Schedule Perdite - DTA SP         (deve = 0)
Aumento Capitale:        = ΔCapitale/Sovrapprezzo (SP) - Emissione (CFF)  (deve = 0)
Limite Utilizzo Perdite: = Perdite Utilizzate ≤ RI × 80%        (deve essere VERO, tranne primi 3 esercizi)
Saldo Perdite ≥ 0:       = Saldo Perdite Finali ≥ 0             (deve essere VERO)
TFR Tie-Out:             = TFR Schedule - TFR SP                 (deve = 0)
IFRS 16 Tie-Out:         = Passività Leasing Schedule - Passività Leasing SP  (deve = 0)
```
