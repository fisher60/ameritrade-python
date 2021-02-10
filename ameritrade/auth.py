import aiohttp

from urllib.parse import unquote, urlencode, urlparse
from typing import Optional, Tuple

from .settings import AUTH_URL, OAUTH_URL


class Token:
    """Generic token class for storing refresh or access token data."""
    def __init__(self, token: str, token_type: str, expiration: int) -> None:
        self.token = token
        self.token_type = token_type
        self.expiration = expiration

    def __str__(self) -> str:
        return f"{self.token_type}: {self.token}"


class Authenticate:
    """Handles all API authentication."""
    def __init__(self, redirect_uri: str = None, consumer_key: str = None, refresh_token: Optional[str] = None) -> None:
        self.redirect_uri = redirect_uri
        self.consumer_key = consumer_key

        self.refresh_token = refresh_token
        self.access_token = None

    @property
    def auth_url(self) -> str:
        """Generates and encodes an auth url given the redirect_uri and consumer_key."""
        params = {
            "redirect_uri": self.redirect_uri,
            "client_id": f"{self.consumer_key}@AMER.OAUTHAP",
            "response_type": "code"
            }
        return f"{AUTH_URL}?{urlencode(params)}"

    @staticmethod
    def parse_code(url: str) -> str:
        """Parses the authorization code from the callback url."""
        parsed_url = urlparse(url)
        code = unquote(parsed_url.query.strip("code="))
        return code

    async def refresh_token_auth(self) -> Tuple[Token, Token]:
        """Authenticates using an existing refresh token."""
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.consumer_key,
        }

        return await self.auth_request(data=data)

    async def get_tokens(self, code: str) -> Tuple[Token, Token]:
        """Retrieves both access and refresh tokens using authentication code."""
        data = {
            "grant_type": "authorization_code",
            "access_type": "offline",
            "code": code,
            "client_id": self.consumer_key,
            "redirect_uri": self.redirect_uri
        }
        return await self.auth_request(data=data)

    async def get_tokens_from_refresh(self, old_refresh_token: Optional[str]) -> Tuple[Token, Token]:
        """Gets new refresh and access tokens from an existing refresh token."""

        data = {
            "grant_type": "refresh_token",
            "refresh_token": old_refresh_token,
            "access_type": "offline",
            "client_id": self.consumer_key,
        }

        return await self.auth_request(data=data)

    async def auth_request(self, data: dict) -> Tuple[Token, Token]:
        """Sends the request for authentication given either the authorization code or a refresh token in data."""
        async with aiohttp.ClientSession() as session:
            async with session.post(OAUTH_URL, data=data) as response:
                if response.status == 200:
                    data_response = await response.json()
                else:
                    raise AttributeError(
                        f"Auth POST request replied with a status of {response.status}. "
                        f"If using a refresh token you may need to use the manual auth to get a new one."
                    )

        self.access_token = Token(
            data_response.get("access_token"),
            "access",
            data_response.get("expires_in")
        )

        temp_refresh_token = Token(
            data_response.get("refresh_token"),
            "refresh",
            data_response.get("refresh_token_expires_in")
        )

        if temp_refresh_token.token is not None:
            self.refresh_token = temp_refresh_token

        return self.access_token, self.refresh_token

    async def authenticate(self) -> Tuple[Token, Token]:
        """Attempts to run automatic authentication with a refresh token, otherwise directs the user to manual auth."""
        if all([self.redirect_uri, self.consumer_key, self.refresh_token]):
            return await self.refresh_token_auth()
        else:
            should_manual_authenticate = input("Your configuration is incomplete, "
                                               "would you like to run the manual authentication? Y/n\n")
            if should_manual_authenticate.lower() in ["y", "yes"]:
                return await self.manual_auth()
            else:
                raise AttributeError("Your client is not fully configured, either complete configuration or "
                                     "run the manual authorization")

    async def manual_auth(self) -> Tuple[Token, Token]:
        """Guides the user through browser authentication for first-time setup."""
        if self.redirect_uri is None:
            self.redirect_uri = input("Enter your Redirect URI/Callback URL here\n")
        if self.consumer_key is None:
            self.consumer_key = input("Enter your Consumer Key here\n")

        custom_auth_url = self.auth_url

        print(custom_auth_url)
        auth_code = self.parse_code(input("Paste the above URL in your browser, follow the onscreen instructions, "
                                          "then paste the new (redirected url) here\n"))

        return await self.get_tokens(auth_code)
