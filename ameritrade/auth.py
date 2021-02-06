import dotenv
from urllib.parse import urlencode, urlparse

from .settings import AUTH_URL


class Authenticate:
    def __init__(self, redirect_uri: str = None, consumer_key: str = None):
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

    @staticmethod
    def parse_code(url: str):
        return urlparse(url)

    def manual_connect(self):
        if self.redirect_uri is None:
            self.redirect_uri = input("Enter your Redirect URI/Callback URL here\n")
        if self.consumer_key is None:
            self.consumer_key = input("Enter your Consumer Key here\n")

        custom_auth_url = self.auth_url


test_callback_url = None
