---
name: checklist
description: Gestisci la checklist di avanzamento del progetto
user_invocable: true
---

# Comando: /checklist

Visualizza e gestisci la checklist di avanzamento del progetto.

## Azioni
1. Leggi `checklist.md` dalla root del progetto
2. Mostra lo stato corrente
3. Se richiesto, aggiorna i task completati

## Sotto-comandi
```
/checklist              # Mostra checklist corrente
/checklist completa X   # Segna task X come completato
/checklist fase N       # Mostra solo la fase N
```

## Formato
Mostra la checklist con percentuale di completamento per fase e totale.
