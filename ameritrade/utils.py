from aiohttp.web import HTTPException


async def get_data_response(response) -> dict:
    data_response = await response.json()
    if response.status != 200:
        raise HTTPException(reason=data_response["error"])

    return data_response
