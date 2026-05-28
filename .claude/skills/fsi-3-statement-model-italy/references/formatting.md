# Standard di Formattazione — Contesto Italiano/IFRS

| Elemento | Formato |
|----------|---------|
| Input fissi | Font blu |
| Formule | Font nero |
| Link ad altri fogli | Font verde |
| Celle di controllo | Rosso se errore, verde se bilanciato |
| Valori negativi | Parentesi, non segno meno |
| Valuta | Nessun decimale per cifre grandi, 2 decimali per per-share. Simbolo € |
| Percentuali | 1 decimale |
| Intestazioni | Bold, bordo inferiore |
| Riga unità | Includere riga unità sotto intestazioni (€ milioni, %, x, ecc.) |

## Convenzioni Numeriche Italiane

| Elemento | Formato Italia | Formato US (da NON usare) |
|----------|---------------|--------------------------|
| Separatore migliaia | Punto (1.000.000) | Virgola (1,000,000) |
| Separatore decimali | Virgola (3,50%) | Punto (3.50%) |
| Valuta | €1.000.000 o EUR 1.000.000 | $1,000,000 |
| Percentuali | 3,9% | 3.9% |

**Nota:** In Excel, i formati numerici dipendono dalle impostazioni locali del sistema. Usare i formati numerici personalizzati appropriati per la localizzazione italiana quando si costruiscono modelli per utenti italiani.

## Linee Guida Separazione Visiva

- Bordo verticale sottile tra colonne storiche e proiettate
- Bordo inferiore spesso dopo totali di sezione (es. Totale Attivo)
- Bordo inferiore singolo per subtotali
- Bordo inferiore doppio per totali generali

## Formattazione Righe Totali e Subtotali

Tutte le righe di totale e subtotale devono usare **formattazione font bold** per i loro valori numerici, per distinguere chiaramente le cifre aggregate dalle singole voci.

### Tab Conto Economico
| Riga | Formattazione |
|------|--------------|
| Ricavi Netti | Bold |
| Totale Costo del Venduto | Bold |
| Utile Lordo | Bold |
| Totale Costi Operativi | Bold |
| EBITDA | Bold |
| EBIT (Risultato Operativo) | Bold |
| EBT (Risultato Prima delle Imposte) | Bold |
| Utile Netto | Bold |

### Tab Stato Patrimoniale
| Riga | Formattazione |
|------|--------------|
| Totale Attività Correnti | Bold |
| Totale Attività Non Correnti | Bold |
| Totale Attivo | Bold |
| Totale Passività Correnti | Bold |
| Totale Passività Non Correnti | Bold |
| Totale Passivo | Bold |
| Patrimonio Netto di Gruppo | Bold |
| Totale Patrimonio Netto | Bold |

### Tab Rendiconto Finanziario
| Riga | Formattazione |
|------|--------------|
| Flusso di Cassa da Attività Operativa prima di CCN | Bold |
| Totale Variazioni Capitale Circolante | Bold |
| Flusso Netto da Attività Operativa (CFO) | Bold |
| Flusso Netto da Attività di Investimento (CFI) | Bold |
| Flusso Netto da Attività di Finanziamento (CFF) | Bold |
| Cassa Finale | Bold |

## Formattazione Riga Check Stato Patrimoniale

La riga di check dello Stato Patrimoniale (sotto Totale Patrimonio Netto) usa formattazione numerica condizionale che mostra valori diversi da zero in rosso.

| Valore Check | Colore Font |
|-------------|------------|
| = 0 (bilanciato) | Nero (standard) |
| ≠ 0 (errore) | Rosso |

## Formattazione Righe Margini

| Elemento | Formato |
|----------|---------|
| Righe % margine | Rientro, corsivo, 1 decimale |
| Trend positivo | Nessuna formattazione speciale |
| Trend negativo | Segnalare per revisione |

## Formattazione Metriche Creditizie

| Elemento | Formato |
|----------|---------|
| Multipli di leva | 1 decimale con suffisso "x" (es. 2,5x) |
| Percentuali | 1 decimale con suffisso "%" |
| PFN negativa | Parentesi, indica posizione di cassa netta |
| Intestazione sezione | Bold, "METRICHE CREDITIZIE" |

## Soglie Colore Metriche Creditizie

| Metrica | Verde | Giallo | Rosso |
|---------|-------|--------|-------|
| Debito Totale / EBITDA | < 2,5x | 2,5x-4,0x | > 4,0x |
| PFN / EBITDA | < 2,0x | 2,0x-3,5x | > 3,5x |
| Interest Coverage | > 4,0x | 2,5x-4,0x | < 2,5x |
| Debito / Cap. Totale | < 40% | 40%-60% | > 60% |
| Current Ratio | > 1,5x | 1,0x-1,5x | < 1,0x |
| Quick Ratio | > 1,0x | 0,75x-1,0x | < 0,75x |

## Flag Ragionevolezza Margini

- Margine Lordo < 0% → ERRORE: Verificare Costo del Venduto
- Margine Lordo > 80% → ATTENZIONE: Verificare Ricavi/COGS
- Margine EBITDA < 0% → SEGNALAZIONE: Perdite operative
- Margine EBITDA > 50% → ATTENZIONE: Insolitamente alto
- Margine Utile Netto < 0% → SEGNALAZIONE: Perdite nette (può essere accettabile in fase di crescita)
- Margine Utile Netto > Margine Lordo → ERRORE: Problema nelle formule
