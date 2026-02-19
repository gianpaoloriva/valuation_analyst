"""Parser per fogli di calcolo Excel di Damodaran.

Fornisce funzioni per leggere, analizzare e estrarre dati dai
dataset di Aswath Damodaran (beta settoriali, premi per il rischio
paese, ecc.) distribuiti in formato Excel (.xls / .xlsx).
"""

from __future__ import annotations

import difflib
import re
from pathlib import Path
from typing import Any

import pandas as pd


# ---------------------------------------------------------------------------
# Lettura e pulizia del file Excel
# ---------------------------------------------------------------------------

def parse_damodaran_excel(
    filepath: Path,
    sheet_name: str | int = 0,
) -> pd.DataFrame:
    """Legge un file Excel di Damodaran e restituisce un DataFrame pulito.

    Gestisce le peculiarita' comuni dei file Damodaran: righe di
    intestazione da saltare, nomi di colonna sporchi, celle unite e
    righe vuote.

    Parametri
    ---------
    filepath : Path
        Percorso del file Excel (``.xls`` o ``.xlsx``).
    sheet_name : str | int, opzionale
        Nome o indice del foglio da leggere (default: ``0``).

    Restituisce
    -----------
    pd.DataFrame
        DataFrame con i dati puliti e le colonne rinominate.

    Solleva
    -------
    FileNotFoundError
        Se il file non esiste.
    ValueError
        Se il file non ha un'estensione supportata o non contiene
        dati validi.
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File non trovato: {filepath}")

    suffisso = filepath.suffix.lower()
    if suffisso not in (".xls", ".xlsx"):
        raise ValueError(
            f"Formato file non supportato: '{suffisso}'. "
            "Sono accettati solo file .xls e .xlsx."
        )

    # Determina il motore di lettura in base all'estensione
    engine = "xlrd" if suffisso == ".xls" else "openpyxl"

    # Prima lettura: individua la riga di intestazione
    df_raw = pd.read_excel(
        filepath,
        sheet_name=sheet_name,
        header=None,
        engine=engine,
    )

    # Cerca la prima riga con almeno 3 celle non vuote come intestazione
    riga_intestazione = _trova_riga_intestazione(df_raw)

    # Rilettura con l'intestazione corretta
    df = pd.read_excel(
        filepath,
        sheet_name=sheet_name,
        header=riga_intestazione,
        engine=engine,
    )

    # Pulizia dei nomi delle colonne
    df.columns = [_pulisci_nome_colonna(str(c)) for c in df.columns]

    # Rimuovi righe completamente vuote
    df = df.dropna(how="all").reset_index(drop=True)

    # Rimuovi colonne senza nome significativo (es. "Unnamed: 0")
    colonne_da_tenere = [
        c for c in df.columns if not c.startswith("unnamed")
    ]
    df = df[colonne_da_tenere]

    # Propagazione in avanti per gestire celle unite (forward fill
    # sulla prima colonna, se e' testuale)
    if len(df.columns) > 0:
        prima_col = df.columns[0]
        if df[prima_col].dtype == object:
            df[prima_col] = df[prima_col].ffill()

    return df


# ---------------------------------------------------------------------------
# Ricerca settore (fuzzy matching)
# ---------------------------------------------------------------------------

def cerca_settore(
    df: pd.DataFrame,
    settore: str,
) -> pd.Series | None:
    """Cerca un settore/industria nel DataFrame tramite corrispondenza fuzzy.

    Confronta il nome fornito con i valori della prima colonna del
    DataFrame utilizzando ``difflib.get_close_matches``.

    Parametri
    ---------
    df : pd.DataFrame
        DataFrame con i dati di settore (la prima colonna contiene i
        nomi dei settori).
    settore : str
        Nome del settore da cercare.

    Restituisce
    -----------
    pd.Series | None
        La riga corrispondente al settore trovato, oppure ``None`` se
        nessuna corrispondenza raggiunge la soglia minima.
    """
    if df.empty:
        return None

    prima_col = df.columns[0]
    nomi_settori = df[prima_col].dropna().astype(str).tolist()

    # Normalizzazione per il confronto
    settore_normalizzato = settore.strip().lower()
    mappa_nomi: dict[str, str] = {
        n.strip().lower(): n for n in nomi_settori
    }

    # Corrispondenza esatta (case-insensitive)
    if settore_normalizzato in mappa_nomi:
        nome_originale = mappa_nomi[settore_normalizzato]
        riga = df[df[prima_col].astype(str).str.strip() == nome_originale]
        if not riga.empty:
            return riga.iloc[0]

    # Corrispondenza fuzzy
    corrispondenze = difflib.get_close_matches(
        settore_normalizzato,
        list(mappa_nomi.keys()),
        n=1,
        cutoff=0.6,
    )

    if corrispondenze:
        nome_originale = mappa_nomi[corrispondenze[0]]
        riga = df[df[prima_col].astype(str).str.strip() == nome_originale]
        if not riga.empty:
            return riga.iloc[0]

    return None


# ---------------------------------------------------------------------------
# Estrazione beta settoriali
# ---------------------------------------------------------------------------

def estrai_beta_settore(
    filepath: Path,
    settore: str,
) -> dict[str, Any] | None:
    """Estrae i dati di beta per un settore dal file Damodaran dei beta.

    Cerca le colonne tipiche del dataset di Damodaran sui beta
    settoriali e restituisce un dizionario con i valori estratti.

    Parametri
    ---------
    filepath : Path
        Percorso del file Excel dei beta settoriali.
    settore : str
        Nome del settore/industria da cercare.

    Restituisce
    -----------
    dict[str, Any] | None
        Dizionario con le chiavi:
        - ``unlevered_beta`` (float)
        - ``levered_beta`` (float)
        - ``d_e_ratio`` (float)
        - ``effective_tax_rate`` (float)
        - ``num_firms`` (int)
        Restituisce ``None`` se il settore non viene trovato.
    """
    df = parse_damodaran_excel(filepath)
    riga = cerca_settore(df, settore)

    if riga is None:
        return None

    # Mappa i nomi colonna ai campi attesi (i nomi nei file Damodaran
    # variano nel tempo, quindi usiamo una ricerca flessibile)
    risultato: dict[str, Any] = {}

    risultato["unlevered_beta"] = _estrai_valore_colonna(
        riga, df.columns, ["unlevered_beta", "unlevered beta", "asset beta"]
    )
    risultato["levered_beta"] = _estrai_valore_colonna(
        riga, df.columns, ["levered_beta", "levered beta", "equity beta", "average beta"]
    )
    risultato["d_e_ratio"] = _estrai_valore_colonna(
        riga, df.columns, ["d/e_ratio", "d/e ratio", "de_ratio", "debt/equity"]
    )
    risultato["effective_tax_rate"] = _estrai_valore_colonna(
        riga, df.columns, ["effective_tax_rate", "tax_rate", "effective tax rate", "tax rate"]
    )
    risultato["num_firms"] = _estrai_valore_colonna(
        riga, df.columns, ["number_of_firms", "num_firms", "number of firms", "# of firms"]
    )

    # Converte num_firms a intero se possibile
    if risultato["num_firms"] is not None:
        try:
            risultato["num_firms"] = int(risultato["num_firms"])
        except (ValueError, TypeError):
            pass

    # Se nessun campo beta e' stato trovato, restituisci None
    if risultato["unlevered_beta"] is None and risultato["levered_beta"] is None:
        return None

    return risultato


# ---------------------------------------------------------------------------
# Estrazione ERP (Equity Risk Premium) per paese
# ---------------------------------------------------------------------------

def estrai_erp_paese(
    filepath: Path,
    paese: str,
) -> dict[str, Any] | None:
    """Estrae i dati di ERP (Equity Risk Premium) per un paese.

    Parametri
    ---------
    filepath : Path
        Percorso del file Excel con i dati ERP per paese.
    paese : str
        Nome del paese da cercare.

    Restituisce
    -----------
    dict[str, Any] | None
        Dizionario con le chiavi:
        - ``country_risk_premium`` (float)
        - ``equity_risk_premium`` (float)
        - ``default_spread`` (float)
        Restituisce ``None`` se il paese non viene trovato.
    """
    df = parse_damodaran_excel(filepath)
    riga = cerca_settore(df, paese)

    if riga is None:
        return None

    risultato: dict[str, Any] = {}

    risultato["country_risk_premium"] = _estrai_valore_colonna(
        riga, df.columns, [
            "country_risk_premium", "country risk premium",
            "country_premium", "additional_country_risk_premium",
        ]
    )
    risultato["equity_risk_premium"] = _estrai_valore_colonna(
        riga, df.columns, [
            "equity_risk_premium", "equity risk premium",
            "total_equity_risk_premium", "total equity risk premium",
            "erp",
        ]
    )
    risultato["default_spread"] = _estrai_valore_colonna(
        riga, df.columns, [
            "default_spread", "country default spread",
            "country_default_spread", "default spread",
        ]
    )

    # Se nessun campo ERP e' stato trovato, restituisci None
    if all(v is None for v in risultato.values()):
        return None

    return risultato


# ===========================================================================
# Funzioni interne (helper)
# ===========================================================================

def _trova_riga_intestazione(df: pd.DataFrame, soglia_colonne: int = 3) -> int:
    """Individua la riga di intestazione in un DataFrame grezzo.

    Scorre le prime righe del DataFrame e restituisce l'indice della
    prima riga con almeno ``soglia_colonne`` celle non vuote e
    contenenti testo.

    Parametri
    ---------
    df : pd.DataFrame
        DataFrame letto senza intestazione (``header=None``).
    soglia_colonne : int
        Numero minimo di celle non vuote richieste.

    Restituisce
    -----------
    int
        Indice della riga di intestazione (zero-based).
    """
    # Controlla al massimo le prime 20 righe
    limite = min(20, len(df))
    for i in range(limite):
        riga = df.iloc[i]
        celle_testo = sum(
            1 for val in riga
            if pd.notna(val) and isinstance(val, str) and len(val.strip()) > 0
        )
        if celle_testo >= soglia_colonne:
            return i

    # Se non trovata, assume la riga 0
    return 0


def _pulisci_nome_colonna(nome: str) -> str:
    """Pulisce il nome di una colonna.

    Rimuove spazi in eccesso, converte in minuscolo, sostituisce
    spazi e caratteri speciali con underscore.

    Parametri
    ---------
    nome : str
        Il nome originale della colonna.

    Restituisce
    -----------
    str
        Il nome pulito.
    """
    nome = nome.strip().lower()
    # Sostituisci spazi e caratteri speciali con underscore
    nome = re.sub(r"[^\w]+", "_", nome)
    # Rimuovi underscore iniziali/finali e doppi
    nome = re.sub(r"_+", "_", nome).strip("_")
    return nome


def _estrai_valore_colonna(
    riga: pd.Series,
    colonne: pd.Index,
    nomi_possibili: list[str],
) -> Any | None:
    """Cerca un valore in una riga provando diversi nomi di colonna.

    Confronta i ``nomi_possibili`` con i nomi effettivi delle colonne
    utilizzando una ricerca fuzzy.

    Parametri
    ---------
    riga : pd.Series
        La riga del DataFrame da cui estrarre il valore.
    colonne : pd.Index
        I nomi delle colonne del DataFrame.
    nomi_possibili : list[str]
        Lista di possibili nomi per la colonna cercata.

    Restituisce
    -----------
    Any | None
        Il valore trovato, oppure ``None``.
    """
    colonne_lower = [str(c).lower().strip() for c in colonne]

    for nome in nomi_possibili:
        nome_lower = nome.lower().strip()

        # Corrispondenza esatta
        if nome_lower in colonne_lower:
            idx = colonne_lower.index(nome_lower)
            valore = riga.iloc[idx]
            if pd.notna(valore):
                return _converti_valore(valore)

        # Corrispondenza parziale (la colonna contiene il nome cercato)
        for j, col in enumerate(colonne_lower):
            if nome_lower in col or col in nome_lower:
                valore = riga.iloc[j]
                if pd.notna(valore):
                    return _converti_valore(valore)

    # Tentativo fuzzy come ultima risorsa
    for nome in nomi_possibili:
        corrispondenze = difflib.get_close_matches(
            nome.lower(), colonne_lower, n=1, cutoff=0.7
        )
        if corrispondenze:
            idx = colonne_lower.index(corrispondenze[0])
            valore = riga.iloc[idx]
            if pd.notna(valore):
                return _converti_valore(valore)

    return None


def _converti_valore(valore: Any) -> Any:
    """Converte un valore letto da Excel in un tipo Python appropriato.

    Gestisce stringhe con percentuale (es. ``"12.5%"``), stringhe
    numeriche e valori gia' numerici.

    Parametri
    ---------
    valore : Any
        Il valore da convertire.

    Restituisce
    -----------
    Any
        Il valore convertito (float, int o stringa originale).
    """
    if isinstance(valore, (int, float)):
        return float(valore)

    if isinstance(valore, str):
        testo = valore.strip()

        # Gestione percentuali (es. "12.5%")
        if testo.endswith("%"):
            try:
                return float(testo.rstrip("%").strip()) / 100.0
            except ValueError:
                pass

        # Tentativo di conversione numerica
        try:
            return float(testo.replace(",", ""))
        except ValueError:
            pass

    return valore
