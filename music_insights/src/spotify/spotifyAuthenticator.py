import re
from enum import Enum
from typing import List

import requests

from spotify.credentials import client_id


class BadStatusCodeException(Exception):
    pass


class AccessTokenNotFoundException(Exception):
    pass


class SpotifyAuthenticator:
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
                "Did you paste the complete URL?"
            )
        return search.group(1)

    @staticmethod
    def authenticate(scope: List[AvailableScopes]) -> str:
        # Implicit grant
        # https://developer.spotify.com/documentation/general/guides/authorization/implicit-grant/
        scope_str_list = [scope.value for scope in scope]
        url = "https://accounts.spotify.com/authorize"
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
        url_string_response = input(
            "Please go to the following URL and paste the complete URL after "
            "the authorization is done (when redirected to localhost):")
        return SpotifyAuthenticator._extract_token_from_response(
            url_string_response
        )
