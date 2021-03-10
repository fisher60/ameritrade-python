# ameritrade-python
This is a simple and lightweight async api wrapper for Ameritrade's API.

The official docs for the Ameritrade API can be found [here](https://developer.tdameritrade.com/apis).

Simple usage using an existing refresh token:
```python
import asyncio
from os import environ
from ameritrade import auth, stock

test_redirect_uri = environ.get("callback_url")
consumer_key = environ.get("consumer_key")
refresh_token = environ.get("refresh_token")

test_auth = auth.Auth(redirect_uri=test_redirect_uri, consumer_key=consumer_key, refresh_token=refresh_token)

async def main():
    """Gets new tokens, then gets a single stock quote for 'KO'/coca-cola."""
    await test_auth.refresh_token_auth()  # Gets fresh tokens

    test_stock = stock.Stock(auth_class=test_auth, symbol="ko")  # creates stock object for KO
    await test_stock.get_quote()  # Makes the quote request
    print(test_stock.quote)


loop = asyncio.get_event_loop()  # Creates the event loop
loop.run_until_complete(main())  # Runs the event loop
```

### Environ
I suggest utilizing a .env file. \
If you are not providing a refresh token, it is recommended that you use auth.Auth.manual_auth() in order to use
Ameritrade's front end auth tools, you can follow the on-screen instructions for this.

You may choose to save your refresh token in a secure location/format, if using a previous refresh token, you only
need to provide these to your auth class:
- consumer_key
- refresh_token
