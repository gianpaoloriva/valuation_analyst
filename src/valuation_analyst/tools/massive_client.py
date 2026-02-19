"""Client wrapper per l'API di Massive.com.

Fornisce un'interfaccia Python per accedere ai dati finanziari
disponibili tramite il servizio Massive.com (https://massive.com).
Supporta richieste sincrone tramite httpx, gestisce gli errori HTTP
con messaggi in italiano e rispetta i limiti di rate limiting.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import httpx

from valuation_analyst.config.settings import MASSIVE_API_KEY, MASSIVE_BASE_URL

logger = logging.getLogger(__name__)

# Limite conservativo: massimo 5 richieste al secondo
_MIN_INTERVALLO_RICHIESTE: float = 0.2


class MassiveClientError(Exception):
    """Errore generico del client Massive.com."""


class MassiveRateLimitError(MassiveClientError):
    """Errore di superamento del limite di richieste (rate limit)."""


class MassiveAuthError(MassiveClientError):
    """Errore di autenticazione con l'API Massive.com."""


class MassiveNotFoundError(MassiveClientError):
    """Errore: risorsa non trovata nell'API Massive.com."""


class MassiveClient:
    """Client per accedere ai dati finanziari tramite Massive.com API.

    Incapsula tutte le chiamate REST verso l'API di Massive.com,
    gestendo autenticazione, rate limiting, errori HTTP e parsing
    delle risposte JSON.

    Parametri
    ---------
    api_key : str | None, opzionale
        Chiave API. Se non specificata, viene letta dalla
        configurazione (``MASSIVE_API_KEY`` in ``.env``).
    base_url : str | None, opzionale
        URL base dell'API. Se non specificato, viene usato
        quello definito in ``settings.py``.
    timeout : float, opzionale
        Timeout in secondi per le richieste HTTP (default: 30.0).

    Solleva
    -------
    ValueError
        Se la chiave API non e' configurata.

    Esempi
    ------
    >>> with MassiveClient() as client:
    ...     profilo = client.get_company_profile("AAPL")
    ...     print(profilo["companyName"])
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key: str = api_key or MASSIVE_API_KEY
        self.base_url: str = base_url or MASSIVE_BASE_URL

        if not self.api_key:
            raise ValueError(
                "API key Massive.com non configurata. "
                "Imposta MASSIVE_API_KEY nel file .env nella radice del progetto."
            )

        self._client: httpx.Client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
                "User-Agent": "valuation-analyst/0.1.0",
            },
            timeout=timeout,
        )

        # Timestamp dell'ultima richiesta per il rate limiting
        self._ultimo_timestamp: float = 0.0
        logger.debug("MassiveClient inizializzato con base_url=%s", self.base_url)

    # ------------------------------------------------------------------
    # Gestione del ciclo di vita
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Chiude la connessione HTTP sottostante."""
        self._client.close()
        logger.debug("Connessione MassiveClient chiusa.")

    def __enter__(self) -> MassiveClient:
        """Supporto per context manager (with statement)."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Chiude la connessione all'uscita dal context manager."""
        self.close()

    # ------------------------------------------------------------------
    # Metodi pubblici per il recupero dati
    # ------------------------------------------------------------------

    def get_company_profile(self, ticker: str) -> dict[str, Any]:
        """Recupera il profilo aziendale completo.

        Restituisce informazioni anagrafiche dell'azienda: nome,
        settore, industria, paese, borsa, descrizione, numero di
        dipendenti, CEO e sito web.

        Parametri
        ---------
        ticker : str
            Simbolo azionario (es. ``"AAPL"``).

        Restituisce
        -----------
        dict[str, Any]
            Dizionario con i dati del profilo aziendale. Le chiavi
            principali includono: ``companyName``, ``sector``,
            ``industry``, ``country``, ``exchange``, ``description``,
            ``fullTimeEmployees``, ``ceo``, ``website``.
        """
        return self._get(f"/profile/{ticker}")

    def get_income_statement(
        self,
        ticker: str,
        period: str = "annual",
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Recupera il conto economico (income statement).

        Restituisce i dati del conto economico per gli ultimi
        esercizi, inclusi ricavi, costo del venduto, utile lordo,
        spese operative, EBIT, EBITDA, utile netto e EPS.

        Parametri
        ---------
        ticker : str
            Simbolo azionario.
        period : str, opzionale
            Periodicita': ``"annual"`` o ``"quarter"`` (default: ``"annual"``).
        limit : int, opzionale
            Numero massimo di periodi da restituire (default: 5).

        Restituisce
        -----------
        list[dict[str, Any]]
            Lista di dizionari, uno per ogni periodo. Chiavi principali:
            ``date``, ``revenue``, ``costOfRevenue``, ``grossProfit``,
            ``operatingExpenses``, ``operatingIncome``, ``ebitda``,
            ``netIncome``, ``eps``, ``epsDiluted``.
        """
        return self._get(
            f"/income-statement/{ticker}",
            params={"period": period, "limit": limit},
        )

    def get_balance_sheet(
        self,
        ticker: str,
        period: str = "annual",
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Recupera lo stato patrimoniale (balance sheet).

        Restituisce attivita', passivita' e patrimonio netto per
        gli ultimi esercizi.

        Parametri
        ---------
        ticker : str
            Simbolo azionario.
        period : str, opzionale
            Periodicita': ``"annual"`` o ``"quarter"`` (default: ``"annual"``).
        limit : int, opzionale
            Numero massimo di periodi (default: 5).

        Restituisce
        -----------
        list[dict[str, Any]]
            Lista di dizionari con chiavi: ``date``, ``totalAssets``,
            ``totalCurrentAssets``, ``cashAndCashEquivalents``,
            ``totalDebt``, ``longTermDebt``, ``shortTermDebt``,
            ``totalStockholdersEquity``, ``totalLiabilities``.
        """
        return self._get(
            f"/balance-sheet-statement/{ticker}",
            params={"period": period, "limit": limit},
        )

    def get_cash_flow_statement(
        self,
        ticker: str,
        period: str = "annual",
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Recupera il rendiconto finanziario (cash flow statement).

        Restituisce i flussi di cassa operativi, da investimento
        e da finanziamento per gli ultimi esercizi.

        Parametri
        ---------
        ticker : str
            Simbolo azionario.
        period : str, opzionale
            Periodicita': ``"annual"`` o ``"quarter"`` (default: ``"annual"``).
        limit : int, opzionale
            Numero massimo di periodi (default: 5).

        Restituisce
        -----------
        list[dict[str, Any]]
            Lista di dizionari con chiavi: ``date``, ``operatingCashFlow``,
            ``capitalExpenditure``, ``freeCashFlow``,
            ``depreciationAndAmortization``, ``changeInWorkingCapital``,
            ``dividendsPaid``, ``netCashFromFinancing``.
        """
        return self._get(
            f"/cash-flow-statement/{ticker}",
            params={"period": period, "limit": limit},
        )

    def get_financial_ratios(
        self,
        ticker: str,
        period: str = "annual",
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Recupera i principali indici finanziari (financial ratios).

        Restituisce margini, redditivita', leva finanziaria, liquidita'
        e multipli di valutazione per gli ultimi esercizi.

        Parametri
        ---------
        ticker : str
            Simbolo azionario.
        period : str, opzionale
            Periodicita': ``"annual"`` o ``"quarter"`` (default: ``"annual"``).
        limit : int, opzionale
            Numero massimo di periodi (default: 5).

        Restituisce
        -----------
        list[dict[str, Any]]
            Lista di dizionari con chiavi: ``date``, ``grossProfitMargin``,
            ``operatingProfitMargin``, ``netProfitMargin``, ``returnOnEquity``,
            ``returnOnAssets``, ``currentRatio``, ``debtEquityRatio``,
            ``priceEarningsRatio``, ``priceToBookRatio``,
            ``enterpriseValueOverEBITDA``.
        """
        return self._get(
            f"/ratios/{ticker}",
            params={"period": period, "limit": limit},
        )

    def get_quote(self, ticker: str) -> dict[str, Any]:
        """Recupera la quotazione corrente dell'azione.

        Restituisce prezzo, variazione, volume, market cap e altri
        dati di trading in tempo reale (o quasi).

        Parametri
        ---------
        ticker : str
            Simbolo azionario.

        Restituisce
        -----------
        dict[str, Any]
            Dizionario con chiavi: ``price``, ``change``,
            ``changesPercentage``, ``volume``, ``avgVolume``,
            ``marketCap``, ``sharesOutstanding``, ``dayLow``,
            ``dayHigh``, ``yearLow``, ``yearHigh``, ``pe``,
            ``eps``, ``open``, ``previousClose``.
        """
        risposta = self._get(f"/quote/{ticker}")
        # L'endpoint quote puo' restituire una lista con un solo elemento
        if isinstance(risposta, list) and len(risposta) > 0:
            return risposta[0]
        return risposta

    def get_historical_prices(
        self,
        ticker: str,
        from_date: str,
        to_date: str,
    ) -> list[dict[str, Any]]:
        """Recupera i prezzi storici giornalieri.

        Parametri
        ---------
        ticker : str
            Simbolo azionario.
        from_date : str
            Data di inizio nel formato ``"YYYY-MM-DD"``.
        to_date : str
            Data di fine nel formato ``"YYYY-MM-DD"``.

        Restituisce
        -----------
        list[dict[str, Any]]
            Lista di dizionari con chiavi: ``date``, ``open``,
            ``high``, ``low``, ``close``, ``adjClose``, ``volume``.
        """
        risposta = self._get(
            f"/historical-price-full/{ticker}",
            params={"from": from_date, "to": to_date},
        )
        # L'API restituisce un oggetto con chiave "historical"
        if isinstance(risposta, dict) and "historical" in risposta:
            return risposta["historical"]
        return risposta if isinstance(risposta, list) else []

    def get_market_cap(self, ticker: str) -> float | None:
        """Recupera la capitalizzazione di mercato corrente.

        Parametri
        ---------
        ticker : str
            Simbolo azionario.

        Restituisce
        -----------
        float | None
            Capitalizzazione di mercato, oppure ``None`` se non disponibile.
        """
        try:
            quote = self.get_quote(ticker)
            return float(quote.get("marketCap", 0)) or None
        except (MassiveClientError, ValueError, TypeError) as e:
            logger.warning("Impossibile ottenere la market cap per %s: %s", ticker, e)
            return None

    def get_shares_outstanding(self, ticker: str) -> float | None:
        """Recupera il numero di azioni in circolazione.

        Parametri
        ---------
        ticker : str
            Simbolo azionario.

        Restituisce
        -----------
        float | None
            Numero di azioni in circolazione, oppure ``None``.
        """
        try:
            quote = self.get_quote(ticker)
            return float(quote.get("sharesOutstanding", 0)) or None
        except (MassiveClientError, ValueError, TypeError) as e:
            logger.warning(
                "Impossibile ottenere le azioni in circolazione per %s: %s", ticker, e,
            )
            return None

    def get_key_metrics(
        self,
        ticker: str,
        period: str = "annual",
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Recupera le metriche chiave per l'azienda.

        Include enterprise value, beta, PE, PB, debt-to-equity e altre
        metriche aggregate.

        Parametri
        ---------
        ticker : str
            Simbolo azionario.
        period : str, opzionale
            Periodicita' (default: ``"annual"``).
        limit : int, opzionale
            Numero massimo di periodi (default: 5).

        Restituisce
        -----------
        list[dict[str, Any]]
            Lista di dizionari con metriche chiave per ogni periodo.
        """
        return self._get(
            f"/key-metrics/{ticker}",
            params={"period": period, "limit": limit},
        )

    def get_treasury_yield(self, maturity: str = "10Y") -> float | None:
        """Recupera il rendimento dei Treasury USA per una data scadenza.

        Parametri
        ---------
        maturity : str, opzionale
            Scadenza del Treasury: ``"3M"``, ``"2Y"``, ``"5Y"``,
            ``"10Y"``, ``"30Y"`` (default: ``"10Y"``).

        Restituisce
        -----------
        float | None
            Rendimento annuo come decimale (es. 0.042 per 4.2%),
            oppure ``None`` se non disponibile.
        """
        try:
            risposta = self._get(
                "/treasury",
                params={"maturity": maturity},
            )
            # Tenta di estrarre il rendimento dalla risposta
            if isinstance(risposta, list) and len(risposta) > 0:
                yield_val = risposta[0].get("yield") or risposta[0].get("close")
                if yield_val is not None:
                    # Se il valore e' in percentuale (es. 4.2), convertirlo in decimale
                    val = float(yield_val)
                    return val / 100.0 if val > 1.0 else val
            elif isinstance(risposta, dict):
                yield_val = risposta.get("yield") or risposta.get("close")
                if yield_val is not None:
                    val = float(yield_val)
                    return val / 100.0 if val > 1.0 else val
            return None
        except (MassiveClientError, ValueError, TypeError) as e:
            logger.warning(
                "Impossibile ottenere il rendimento Treasury %s: %s", maturity, e,
            )
            return None

    # ------------------------------------------------------------------
    # Metodi interni
    # ------------------------------------------------------------------

    def _rispetta_rate_limit(self) -> None:
        """Attende se necessario per rispettare il limite di richieste.

        Garantisce che tra due richieste consecutive passi almeno
        ``_MIN_INTERVALLO_RICHIESTE`` secondi.
        """
        adesso = time.monotonic()
        trascorso = adesso - self._ultimo_timestamp
        if trascorso < _MIN_INTERVALLO_RICHIESTE:
            attesa = _MIN_INTERVALLO_RICHIESTE - trascorso
            logger.debug("Rate limiting: attesa di %.3f secondi.", attesa)
            time.sleep(attesa)
        self._ultimo_timestamp = time.monotonic()

    def _get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Esegue una richiesta GET verso l'API.

        Gestisce il rate limiting, gli errori HTTP e il parsing
        della risposta JSON.

        Parametri
        ---------
        endpoint : str
            Percorso dell'endpoint (es. ``"/profile/AAPL"``).
        params : dict[str, Any] | None, opzionale
            Parametri di query string.

        Restituisce
        -----------
        Any
            Il corpo della risposta JSON (dict o list).

        Solleva
        -------
        MassiveAuthError
            Se la risposta e' 401 o 403.
        MassiveRateLimitError
            Se la risposta e' 429 (troppi richieste).
        MassiveNotFoundError
            Se la risposta e' 404.
        MassiveClientError
            Per qualsiasi altro errore HTTP o di connessione.
        """
        self._rispetta_rate_limit()

        url = endpoint
        logger.debug("GET %s params=%s", url, params)

        try:
            risposta = self._client.get(url, params=params)
        except httpx.TimeoutException as e:
            raise MassiveClientError(
                f"Timeout nella richiesta a {url}. "
                "Verifica la connessione di rete e riprova."
            ) from e
        except httpx.ConnectError as e:
            raise MassiveClientError(
                f"Impossibile connettersi a {self.base_url}. "
                "Verifica la connessione di rete."
            ) from e
        except httpx.HTTPError as e:
            raise MassiveClientError(
                f"Errore HTTP nella richiesta a {url}: {e}"
            ) from e

        # Gestione codici di errore specifici
        codice = risposta.status_code

        if codice == 401 or codice == 403:
            raise MassiveAuthError(
                f"Autenticazione fallita (codice {codice}). "
                "Verifica che la chiave API sia valida e attiva."
            )

        if codice == 404:
            raise MassiveNotFoundError(
                f"Risorsa non trovata: {url}. "
                "Verifica che il ticker o l'endpoint siano corretti."
            )

        if codice == 429:
            # Legge l'header Retry-After se presente
            retry_after = risposta.headers.get("Retry-After", "60")
            raise MassiveRateLimitError(
                f"Limite di richieste superato. "
                f"Riprova tra {retry_after} secondi."
            )

        if codice >= 500:
            raise MassiveClientError(
                f"Errore del server Massive.com (codice {codice}). "
                "Il servizio potrebbe essere temporaneamente non disponibile."
            )

        if codice >= 400:
            raise MassiveClientError(
                f"Errore nella richiesta (codice {codice}): "
                f"{risposta.text[:200]}"
            )

        # Parsing della risposta JSON
        try:
            dati = risposta.json()
        except ValueError as e:
            raise MassiveClientError(
                f"Risposta non valida dall'API (non e' JSON): {risposta.text[:200]}"
            ) from e

        # Alcune API restituiscono un messaggio di errore nel corpo JSON
        if isinstance(dati, dict) and "Error Message" in dati:
            raise MassiveClientError(
                f"Errore dall'API Massive.com: {dati['Error Message']}"
            )

        return dati
