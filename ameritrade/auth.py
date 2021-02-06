from urllib.parse import urlencode

from ameritrade.constants import AUTH_URL


class Authenticate:
    def __init__(self, redirect_uri: str = None, consumer_key: int = None):
        self.redirect_uri = redirect_uri
        self.consumer_key = consumer_key

    @property
    def auth_url(self):
        params = {
            "redirect_uri": self.redirect_uri,
            "client_id": f"{self.consumer_key}@AMER.OAUTHAP",
            "response_type": "code"
            }
        return f"{AUTH_URL}?{urlencode(params)}"

    def manual_connect(self):
        pass
