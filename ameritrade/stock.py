from typing import Optional

from .history import History
from .quotes import Quote, QuoteData
from .auth import Auth


class Stock:

    def __init__(
            self,
            auth_class: Auth,
            symbol: Optional[str] = None,
            quote: Optional[Quote] = None,
            history: Optional[History] = None
    ):
        self.auth_class: Auth = auth_class
        self.quote: Optional[QuoteData] = None

        self.history: Optional[History] = None

        self._quote_object: Quote = Quote(auth_class=auth_class, symbol=symbol)
        self._history_object: History = History(auth_class=auth_class, symbol=symbol)

        if quote is not None:
            self.quote = quote.data
            self.symbol = self.quote.symbol
        else:
            self.quote = None
            self.symbol = symbol

        if history:
            self.history = history.data
        else:
            self.history = None

    def __str__(self) -> str:
        return self.quote.symbol

    def __float__(self) -> float:
        return float(self.quote.bid_price)

    def __int__(self) -> int:
        return int(self.quote.bid_price)

    async def get_quote(self) -> QuoteData:
        """This is an alias for Quote.get_quote()."""
        self.quote = await self._quote_object.get_quote()
        return self.quote

    async def get_price_history(
            self,
            period: Optional[int] = None,
            frequency: Optional[int] = None,
            period_type: Optional[str] = None,
            frequency_type: Optional[str] = None,
            end_date: Optional[int] = None,
            start_date: Optional[int] = None,
    ) -> list:
        """This is an alias for History.get_price_history."""
        self.history = await self._history_object.get_price_history(
            period=period,
            frequency=frequency,
            period_type=period_type,
            frequency_type=frequency_type,
            end_date=end_date,
            start_date=start_date
        )
        return self.history
