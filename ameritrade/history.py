from aiohttp import ClientSession

from dataclasses import dataclass
from dataclass_factory import Factory

from typing import List, Optional

from .auth import Auth
from .settings import GET_PRICE_HISTORY_URL
from .utils import get_data_response


@dataclass
class Candle:
    close: int
    datetime: int
    high: int
    low: int
    open: int
    volume: int


class History:
    _factory = Factory()

    def __init__(self, symbol: str, auth_class: Auth, candles: Optional[List[dict]] = None) -> None:
        self.symbol = symbol.upper()
        self.auth_class = auth_class

        if candles is not None:
            self.candles = candles
            self.data = self.load_history(candles)
        else:
            self.candles = None
            self.data = None

    def load_history(self, _candles):
        return [self._factory.load(x, Candle) for x in _candles]

    async def get_price_history(
            self,
            period: Optional[int] = None,
            frequency: Optional[int] = None,
            period_type: Optional[str] = None,
            frequency_type: Optional[str] = None,
            end_date: Optional[int] = None,
            start_date: Optional[int] = None,
    ) -> List[Candle]:
        """
        :param period: The number of periods to show.

        :param frequency: The number of the frequencyType to be included in each candle.

        :param period_type: The type of period to show.
            Valid values are day, month, year, or ytd (year to date). Default is day.

        :param frequency_type: The type of frequency with which a new candle is formed.
            Options are: minute, daily, weekly, monthly.

        :param end_date: End date as milliseconds since epoch. If startDate and endDate are provided,
            period should not be provided. Default is previous trading day.

        :param start_date: Start date as milliseconds since epoch.
            If startDate and endDate are provided, period should not be provided.

        :return: The JSON response of the request
        """
        url = f"{GET_PRICE_HISTORY_URL}{self.symbol}/pricehistory"
        headers = {"Authorization": f"Bearer {self.auth_class.access_token.token}"}
        params = {}

        if period is not None:
            params["period"] = period
        if frequency is not None:
            params["frequency"] = frequency
        if period_type is not None:
            params["periodType"] = period_type
        if frequency_type is not None:
            params["frequencyType"] = frequency_type
        if end_date is not None:
            params["endDate"] = end_date
        if start_date is not None:
            params["startDate"] = start_date

        async with ClientSession(headers=headers) as session:
            async with session.get(url=url, params=params) as response:
                data_response = await get_data_response(response)
                self.candles = data_response.get("candles")
                self.data = self.load_history(self.candles)
                return self.data
