from aiohttp import ClientSession

from dataclasses import dataclass
from dataclass_factory import Factory, Schema, NameStyle

from typing import Optional

from .auth import Auth
from .settings import GET_QUOTES_URL, GET_QUOTE_URL
from .utils import get_data_response


async def get_quotes(*symbols: str, auth_class: Auth) -> dict:
    params = {
        "symbol": ",".join(symbols)
    }
    headers = {"Authorization": f"Bearer {auth_class.access_token.token}"}
    async with ClientSession(headers=headers) as session:
        async with session.get(url=GET_QUOTES_URL, params=params) as response:
            return await get_data_response(response)


@dataclass
class QuoteData:
    asset_type: str
    asset_main_type: str
    cusip: str
    symbol: str
    description: str
    bid_price: float
    bid_size: float
    bid_id: str
    ask_price: float
    ask_size: float
    ask_id: str
    last_price: float
    last_size: float
    last_id: str
    open_price: float
    high_price: float
    low_price: float
    bid_tick: str
    close_price: float
    net_change: float
    total_volume: float
    quote_time_in_long: float
    trade_time_in_long: float
    mark: float
    exchange: str
    exchange_name: str
    marginable: bool
    shortable: bool
    volatility: float
    digits: float
    fifty_two_week_high: float
    fifty_two_week_low: float
    net_asset_value: float
    pe_ratio: float
    div_amount: float
    div_yield: float
    div_date: str
    security_status: str
    regular_market_last_price: float
    regular_market_last_size: float
    regular_market_net_change: float
    regular_market_trade_time_in_long: float
    net_percent_change_in_double: float
    mark_change_in_double: float
    mark_percent_change_in_double: float
    regular_market_percent_change_in_double: float
    delayed: bool


class Quote:
    _factory = Factory(default_schema=Schema(name_style=NameStyle.camel_lower))

    def __init__(self, auth_class: Auth, data: Optional[dict] = None, symbol: Optional[str] = None):
        self.data: Optional[QuoteData] = None
        self.auth_class = auth_class
        if data is not None:
            self.data = self._factory.load(self.clean_data(data), QuoteData)
            self.symbol: str = self.data.symbol.upper()
        else:
            self.data = None
            self.symbol: str = symbol.upper()

    async def get_quote(self, symbol: Optional[str] = None, auth_class: Optional[Auth] = None) -> QuoteData:
        """
        :param symbol: The stock symbol, will default to self.symbol if arg not passed.
        :param auth_class: The authorization class for the request, will default to self.auth_class if arg not passed.
        :return: QuoteData dataclass
        """
        symbol = symbol.upper() if symbol else self.symbol
        auth_class = auth_class if auth_class else self.auth_class

        url = f"{GET_QUOTE_URL}{symbol}/quotes"
        headers = {"Authorization": f"Bearer {auth_class.access_token.token}"}

        async with ClientSession(headers=headers) as session:
            async with session.get(url=url) as response:
                data_response = await get_data_response(response)
                self.data = self._factory.load(self.clean_data(data_response.get(symbol)), QuoteData)
                return self.data

    @staticmethod
    def clean_data(data) -> dict:
        data["fiftyTwoWeekHigh"] = data["52WkHigh"]
        data["fiftyTwoWeekLow"] = data["52WkLow"]
        data["netAssetValue"] = data["nAV"]
        return data
