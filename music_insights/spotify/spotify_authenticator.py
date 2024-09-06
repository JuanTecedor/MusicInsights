import re
from enum import Enum

import requests

from music_insights.spotify.credentials import (InvalidClientIdException,
                                                client_id)


class BadStatusCodeException(Exception):
    pass


class AccessTokenNotFoundException(Exception):
    pass


class SpotifyAuthenticator:
    _AUTH_ENDPOINT = "https://accounts.spotify.com/authorize"

    class AvailableScopes(Enum):
        USER_LIBRARY_READ = "user-library-read"
        USER_TOP_READ = "user-top-read"
        PLAYLIST_READ_PRIVATE = "playlist-read-private"
        PLAYLIST_MODIFY_PRIVATE = "playlist-modify-private"

    @staticmethod
    def _extract_token_from_response(url_string_response: str) -> str:
        search = re.search("access_token=([^&]+)", url_string_response)
        if search is None:
            raise AccessTokenNotFoundException(
                "Unable to extract token from the URL. "
                "Did you paste the complete URL? "
                "Is the client ID valid?"
            )
        return search.group(1)

    @staticmethod
    def _get_url_from_input() -> str:
        return input(
            "Please go to the URL, accept the permissions and paste the "
            "complete redirected URL after the authorization is done:\n"
        )

    @staticmethod
    def __check_client_id() -> None:
        if client_id is None:
            raise InvalidClientIdException("The client ID is invalid.")

    @staticmethod
    def authenticate(scope: list[AvailableScopes]) -> str:
        SpotifyAuthenticator.__check_client_id()
        # Implicit grant
        # https://developer.spotify.com/documentation/general/guides/authorization/implicit-grant/
        scope_str_list = [scope.value for scope in scope]
        url = SpotifyAuthenticator._AUTH_ENDPOINT
        payload = {
            "client_id": client_id,
            "response_type": "token",
            "redirect_uri": "http://localhost/",
            "scope": " ".join(scope_str_list)
        }
        response = requests.get(url=url, params=payload)
        if response.status_code != 200:
            raise BadStatusCodeException(
                f"The status code was {response.status_code}"
            )
        print(response.url)
        return SpotifyAuthenticator._extract_token_from_response(
            SpotifyAuthenticator._get_url_from_input()
        )
