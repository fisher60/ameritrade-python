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
    def __init__(self):
        raise NotImplementedError(f"{type(self).__name__} class is currently only a placeholder.")
