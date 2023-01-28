from enum import Enum
from typing import List
import requests

from credentials import client_id
from utils import extract_token_from_response


class SpotifyAuthenticator:
    class AvailableScopes(Enum):
        USER_LIBRARY_READ = "user-library-read"
        USER_TOP_READ = "user-top-read"
        PLAYLIST_READ_PRIVATE = "playlist-read-private"
        PLAYLIST_MODIFY_PRIVATE = "playlist-modify-private"

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
            breakpoint()
            pass  # TODO
        print(response.url)
        url_string_response = input("Please enter the full URL:")
        return extract_token_from_response(url_string_response)
