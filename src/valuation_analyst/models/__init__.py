"""Pacchetto dei modelli dati per valuation_analyst.

Esporta tutte le dataclass utilizzate nel progetto per
rappresentare aziende, risultati di valutazione, flussi
di cassa, costo del capitale, comparabili, opzioni e scenari.
"""

from valuation_analyst.models.company import Company
from valuation_analyst.models.valuation_result import ValuationResult
from valuation_analyst.models.cash_flows import (
    ProiezioneCashFlow,
    CashFlowProjection,
)
from valuation_analyst.models.cost_of_capital import CostoCapitale
from valuation_analyst.models.comparable import (
    Comparabile,
    StatisticheMultiplo,
    AnalisiComparabili,
)
from valuation_analyst.models.option_inputs import InputBlackScholes
from valuation_analyst.models.scenario import (
    Scenario,
    AnalisiScenari,
    RisultatoSensitivity,
)

__all__ = [
    # Azienda
    "Company",
    # Risultato valutazione
    "ValuationResult",
    # Flussi di cassa
    "ProiezioneCashFlow",
    "CashFlowProjection",
    # Costo del capitale
    "CostoCapitale",
    # Comparabili
    "Comparabile",
    "StatisticheMultiplo",
    "AnalisiComparabili",
    # Opzioni
    "InputBlackScholes",
    # Scenari e sensitivity
    "Scenario",
    "AnalisiScenari",
    "RisultatoSensitivity",
]
