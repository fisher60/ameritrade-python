from aiohttp import ClientSession
from aiohttp.web import HTTPException

from .auth import Auth
from .settings import GET_QUOTES_URL


async def get_quotes(*symbols: str, auth_class: Auth) -> dict:
    params = {
        "symbol": ",".join(symbols)
    }
    headers = {"Authorization": f"Bearer {auth_class.access_token.token}"}

    async with ClientSession(headers=headers) as session:
        async with session.get(url=GET_QUOTES_URL, params=params) as response:
            data_response = await response.json()
            if response.status != 200:
                raise HTTPException(reason=data_response["error"])

        return data_response


class Quote:
    def __init__(self, stock_data: dict):
        self.asset_type = stock_data.get("assetType")
        self.asset_main_type = stock_data.get("assetMainType")
        self.cusip = stock_data.get("cusip")
        self.symbol = stock_data.get("symbol")
        self.description = stock_data.get("description")
        self.bid_price = stock_data.get("bidPrice")
        self.bid_size = stock_data.get("bidSize")
        self.bid_id = stock_data.get("bidId")
        self.ask_price = stock_data.get("askPrice")
        self.ask_size = stock_data.get("askSize")
        self.ask_id = stock_data.get("askId")
        self.last_price = stock_data.get("lastPrice")
        self.last_size = stock_data.get("lastSize")
        self.last_id = stock_data.get("lastId")
        self.open_price = stock_data.get("openPrice")
        self.high_price = stock_data.get("highPrice")
        self.low_price = stock_data.get("lowPrice")
        self.bid_tick = stock_data.get("bidTick")
        self.close_price = stock_data.get("closePrice")
        self.net_change = stock_data.get("netChange")
        self.total_volume = stock_data.get("totalVolume")
        self.quote_time_in_long = stock_data.get("quoteTimeInLong")
        self.trade_time_in_long = stock_data.get("tradeTimeInLong")
        self.mark = stock_data.get("mark")
        self.exchange = stock_data.get("exchange")
        self.exchange_name = stock_data.get("exchangeName")
        self.marginable = stock_data.get("marginable")
        self.shortable = stock_data.get("shortable")
        self.volatility = stock_data.get("volatility")
        self.digits = stock_data.get("digits")
        self.fifty_two_week_high = stock_data.get("52WkHigh")
        self.fifty_two_week_low = stock_data.get("52WkLow")
        self.net_asset_value = stock_data.get("nAV")
        self.pe_ratio = stock_data.get("peRatio")
        self.div_amount = stock_data.get("divAmount")
        self.div_yield = stock_data.get("divYield")
        self.div_date = stock_data.get("divDate")
        self.security_status = stock_data.get("securityStatus")
        self.regular_market_last_price = stock_data.get("regularMarketLastPrice")
        self.regular_market_last_size = stock_data.get("regularMarketLastSize")
        self.regular_market_net_change = stock_data.get("regularMarketNetChange")
        self.regular_market_trade_time_in_long = stock_data.get("regularMarketTradeTimeInLong")
        self.net_percent_change_in_double = stock_data.get("netPercentChangeInDouble")
        self.mark_change_in_double = stock_data.get("markChangeInDouble")
        self.mark_percent_change_in_double = stock_data.get("markPercentChangeInDouble")
        self.regular_market_percent_change_in_double = stock_data.get("regularMarketPercentChangeInDouble")
        self.delayed = stock_data.get("delayed")
