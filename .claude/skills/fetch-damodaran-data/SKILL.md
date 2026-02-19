---
name: fetch-damodaran-data
description: Scarica e aggiorna i dataset Damodaran (beta, ERP, WACC, multipli per settore e paese)
user_invocable: true
---

# Skill: Download Dataset Damodaran

Scarica i dataset di Aswath Damodaran dal sito NYU Stern e li salva nella cache locale.

## Utilizzo
```
/fetch-damodaran-data                    # Scarica tutti i dataset
/fetch-damodaran-data --dataset betas    # Solo beta di settore
/fetch-damodaran-data --forza            # Forza re-download anche se in cache
/fetch-damodaran-data --lista            # Lista dataset disponibili
```

## Dataset Disponibili
- **betas** - Beta unlevered/levered per settore
- **erp** - Equity Risk Premium e Country Risk Premium
- **wacc** - WACC e componenti per settore
- **pe** - P/E ratio per settore
- **ev_ebitda** - EV/EBITDA per settore
- **pb** - P/B per settore
- **ps** - Price/Sales per settore
- **margins** - Margini operativi per settore
- **capex** - CapEx e D&A per settore
- **roe** - ROE per settore
- **dividends** - Payout e dividend yield per settore
- **country_risk** - Risk premium per paese

## Workflow

### 1. Download
```python
from valuation_analyst.tools.damodaran_data import scarica_dataset, lista_settori
path = scarica_dataset("betas", forza_download=True)
```

### 2. Verifica
Conferma il download e mostra statistiche (dimensione file, data download, numero righe).

### 3. Logging
Logga in prompt_log.md.

## Fonte
Tutti i dataset provengono da: https://pages.stern.nyu.edu/~adamodar/
Aggiornati tipicamente a gennaio di ogni anno.
