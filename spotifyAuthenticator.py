import re

import requests

from credentials import client_id


class AccessTokenNotFoundException(Exception):
    pass


class SpotifyAuthenticator:
    @staticmethod
    def authenticate() -> str:
        # Implicit grant https://developer.spotify.com/documentation/general/guides/authorization/implicit-grant/
        url = "https://accounts.spotify.com/authorize"
        payload = {
            "client_id": client_id,
            "response_type": "token",
            "redirect_uri": "http://localhost/",
            "scope": "user-library-read"
        }
        response = requests.get(url=url, params=payload)
        print(response.url)
        url_string_response = input("Please enter the full URL:")
        search = re.search("access_token=([^&]+)", url_string_response)
        if search is None:
            raise AccessTokenNotFoundException("Unable to extract token from the URL")

        token = search.group(1)
        return token
