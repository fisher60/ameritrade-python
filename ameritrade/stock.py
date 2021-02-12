from dataclass_factory import Factory, Schema, NameStyle

from .quotes import Quote


class Stock:
    _factory = Factory(default_schema=Schema(name_style=NameStyle.camel_lower))

    def __init__(self, data):
        clean_data = self.clean_data(data)
        self.quote: Quote = self._factory.load(clean_data, Quote)

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
