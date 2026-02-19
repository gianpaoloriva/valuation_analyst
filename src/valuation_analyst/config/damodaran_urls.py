"""URL per i dataset di Aswath Damodaran (NYU Stern).

Contiene la mappatura completa dei nomi dei dataset
ai relativi URL sulla pagina di Damodaran, sia per
la versione HTML consultabile sia per il file
scaricabile in formato Excel (.xls/.xlsx).
"""

from dataclasses import dataclass

from valuation_analyst.config.settings import DAMODARAN_BASE_URL


@dataclass(frozen=True)
class DamodaranDataset:
    """Rappresenta un singolo dataset di Damodaran.

    Attributes:
        nome: Nome identificativo del dataset.
        descrizione: Descrizione in italiano del contenuto.
        percorso_html: Percorso relativo alla pagina HTML.
        percorso_excel: Percorso relativo al file Excel scaricabile.
    """

    nome: str
    descrizione: str
    percorso_html: str
    percorso_excel: str

    @property
    def url_html(self) -> str:
        """URL completo della pagina HTML del dataset."""
        return f"{DAMODARAN_BASE_URL}{self.percorso_html}"

    @property
    def url_excel(self) -> str:
        """URL completo del file Excel scaricabile."""
        return f"{DAMODARAN_BASE_URL}{self.percorso_excel}"


# --- Definizione di tutti i dataset disponibili ---

DAMODARAN_DATASETS: dict[str, DamodaranDataset] = {
    "betas_by_industry": DamodaranDataset(
        nome="betas_by_industry",
        descrizione="Beta per settore industriale (levered e unlevered)",
        percorso_html="New_Home_Page/datafile/Betas.html",
        percorso_excel="New_Home_Page/datafile/Betas.xls",
    ),
    "erp": DamodaranDataset(
        nome="erp",
        descrizione="Equity Risk Premium e premio per rischio paese",
        percorso_html="New_Home_Page/datafile/ctryprem.html",
        percorso_excel="New_Home_Page/datafile/ctryprem.xlsx",
    ),
    "wacc": DamodaranDataset(
        nome="wacc",
        descrizione="Costo medio ponderato del capitale per settore",
        percorso_html="New_Home_Page/datafile/wacc.html",
        percorso_excel="New_Home_Page/datafile/wacc.xls",
    ),
    "revenue_multiples": DamodaranDataset(
        nome="revenue_multiples",
        descrizione="Multipli prezzo/ricavi e EV/ricavi per settore",
        percorso_html="New_Home_Page/datafile/psdata.html",
        percorso_excel="New_Home_Page/datafile/psdata.xls",
    ),
    "pe_ratios": DamodaranDataset(
        nome="pe_ratios",
        descrizione="Rapporto prezzo/utili (P/E) per settore",
        percorso_html="New_Home_Page/datafile/pedata.html",
        percorso_excel="New_Home_Page/datafile/pedata.xls",
    ),
    "ev_ebitda": DamodaranDataset(
        nome="ev_ebitda",
        descrizione="Multiplo EV/EBITDA per settore",
        percorso_html="New_Home_Page/datafile/vebitda.html",
        percorso_excel="New_Home_Page/datafile/vebitda.xls",
    ),
    "pb_ratios": DamodaranDataset(
        nome="pb_ratios",
        descrizione="Rapporto prezzo/valore contabile (P/BV) per settore",
        percorso_html="New_Home_Page/datafile/pbvdata.html",
        percorso_excel="New_Home_Page/datafile/pbvdata.xls",
    ),
    "margins": DamodaranDataset(
        nome="margins",
        descrizione="Margini operativi e netti per settore",
        percorso_html="New_Home_Page/datafile/margin.html",
        percorso_excel="New_Home_Page/datafile/margin.xls",
    ),
    "roe": DamodaranDataset(
        nome="roe",
        descrizione="Return on Equity (ROE) per settore",
        percorso_html="New_Home_Page/datafile/roe.html",
        percorso_excel="New_Home_Page/datafile/roe.xls",
    ),
    "capex": DamodaranDataset(
        nome="capex",
        descrizione="Investimenti in conto capitale (CapEx) per settore",
        percorso_html="New_Home_Page/datafile/capex.html",
        percorso_excel="New_Home_Page/datafile/capex.xls",
    ),
    "dividends": DamodaranDataset(
        nome="dividends",
        descrizione="Dati sui dividendi e payout ratio per settore",
        percorso_html="New_Home_Page/datafile/divfund.html",
        percorso_excel="New_Home_Page/datafile/divfund.xls",
    ),
    "cost_of_debt": DamodaranDataset(
        nome="cost_of_debt",
        descrizione="Costo del debito e struttura del capitale per settore",
        percorso_html="New_Home_Page/datafile/wacc.html",
        percorso_excel="New_Home_Page/datafile/wacc.xls",
    ),
    "country_risk": DamodaranDataset(
        nome="country_risk",
        descrizione="Premio per il rischio paese e rating sovrani",
        percorso_html="New_Home_Page/datafile/ctryprem.html",
        percorso_excel="New_Home_Page/datafile/ctryprem.xlsx",
    ),
    "tax_rates": DamodaranDataset(
        nome="tax_rates",
        descrizione="Aliquote fiscali effettive e marginali per settore",
        percorso_html="New_Home_Page/datafile/taxrate.html",
        percorso_excel="New_Home_Page/datafile/taxrate.xls",
    ),
    "growth_rates": DamodaranDataset(
        nome="growth_rates",
        descrizione="Tassi di crescita storici e attesi per settore",
        percorso_html="New_Home_Page/datafile/histgr.html",
        percorso_excel="New_Home_Page/datafile/histgr.xls",
    ),
}
"""Dizionario di tutti i dataset Damodaran disponibili.

Chiave: nome identificativo del dataset.
Valore: oggetto DamodaranDataset con URL HTML e Excel.
"""


def ottieni_url_html(nome_dataset: str) -> str:
    """Restituisce l'URL della pagina HTML per un dataset.

    Args:
        nome_dataset: Nome identificativo del dataset.

    Returns:
        URL completo della pagina HTML.

    Raises:
        KeyError: Se il nome del dataset non e' presente nel dizionario.
    """
    return DAMODARAN_DATASETS[nome_dataset].url_html


def ottieni_url_excel(nome_dataset: str) -> str:
    """Restituisce l'URL del file Excel scaricabile per un dataset.

    Args:
        nome_dataset: Nome identificativo del dataset.

    Returns:
        URL completo del file Excel.

    Raises:
        KeyError: Se il nome del dataset non e' presente nel dizionario.
    """
    return DAMODARAN_DATASETS[nome_dataset].url_excel


def lista_dataset_disponibili() -> list[str]:
    """Restituisce la lista dei nomi di tutti i dataset disponibili.

    Returns:
        Lista ordinata dei nomi dei dataset.
    """
    return sorted(DAMODARAN_DATASETS.keys())
