from dataclass_factory import Factory, Schema, NameStyle

from typing import Optional

from .history import History
from .quotes import Quote
from .auth import Auth


class Stock:
    _factory = Factory(default_schema=Schema(name_style=NameStyle.camel_lower))

    def __init__(
            self,
            auth_class: Auth,
            symbol: Optional[str] = None,
            data: Optional[dict] = None,
            history: Optional[History] = None
    ):
        if data:
            clean_data = self.clean_data(data)
            self.quote: Quote = self._factory.load(clean_data, Quote)
            self.symbol: str = self.quote.symbol
        else:
            self.symbol: str = symbol

        if history:
            self.history: History = history
        else:
            self.history: History = History(self.symbol, auth_class)

    @staticmethod
    def clean_data(data) -> dict:
        data["fiftyTwoWeekHigh"] = data["52WkHigh"]
        data["fiftyTwoWeekLow"] = data["52WkLow"]
        data["netAssetValue"] = data["nAV"]
        return data

    def __str__(self) -> str:
        return self.quote.symbol

    def __float__(self) -> float:
        return float(self.quote.bid_price)

    def __int__(self) -> int:
        return int(self.quote.bid_price)
