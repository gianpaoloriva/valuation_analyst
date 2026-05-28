# Formato Report Deck Check — Italia

## Template Report

```markdown
# Report QC Presentazione: [Nome Presentazione]

## Sintesi
- Problemi totali: X
- Critici: X (incongruenze numeriche, errori fattuali, disclaimer mancante)
- Importanti: X (allineamento dati-narrativa, linguaggio, metriche)
- Minori: X (formattazione)

## Problemi Critici

### Coerenza Numeri
1. **[Nome problema]** (Slide X, Y)
   - Slide X: [valore]
   - Slide Y: [valore]
   - Azione: [raccomandazione]

### Allineamento Dati-Narrativa
1. **[Nome problema]** (Slide X, Y)
   - Affermazione: "[testo citato]"
   - I dati mostrano: [contraddizione]
   - Azione: [raccomandazione]

### Compliance
1. **[Nome problema]** (Slide X)
   - [Descrizione — es. disclaimer CONSOB mancante, normativa errata]
   - Azione: [raccomandazione]

## Problemi Importanti

### Linguaggio
1. **[Tipo problema]** (Slide X)
   - Attuale: "[testo citato]"
   - Suggerito: "[sostituzione]"

### Metriche e Riferimenti
1. **[Tipo problema]** (Slide X)
   - [Descrizione — es. metrica US anziché IFRS, tasso SOFR anziché Euribor]
   - Azione: [raccomandazione]

## Problemi Minori

### Formattazione
1. **[Tipo problema]** (Slide X)
   - [Descrizione e correzione]

## Checklist Finale
- [ ] Numeri riconciliati tra slide
- [ ] Narrativa coerente con dati
- [ ] Linguaggio professionale IB (italiano o inglese coerente)
- [ ] Grafici con fonte dati citata
- [ ] Formattazione coerente (€, separatori, date GG/MM/AAAA)
- [ ] Disclaimer CONSOB / nota legale presente
- [ ] Metriche IFRS (non US GAAP)
- [ ] Riferimenti a tassi/indici europei (Euribor, FTSE MIB, non SOFR/S&P 500)
```

## Classificazione Severity

**Critico** (blocca la consegna al cliente):
- Incongruenze numeriche tra slide
- Errori di calcolo
- Errori fattuali (nomi, titoli, date)
- Dati che contraddicono la narrativa
- Disclaimer CONSOB mancante (se materiale per clienti)
- Normativa citata errata o abrogata

**Importante** (da correggere):
- Linguaggio colloquiale o registro inappropriato
- Affermazioni vaghe senza quantificazione
- Inconsistenza terminologica (italiano/inglese misto casuale)
- Fonti grafici mancanti
- Metriche US anziché IFRS/italiane

**Minore** (rifinitura):
- Inconsistenze font/colore
- Variazioni formato date
- Spaziatura/allineamento
- Formato numeri non italiano (virgola vs punto)
