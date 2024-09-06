from typing import Final
from unittest.mock import patch

import responses

from music_insights.spotify.spotify_authenticator import SpotifyAuthenticator
from music_insights.spotify.spotify_client import SpotifyClient


class TestSpotifyClient:
    BASE_PATCH_PATH: Final[str] = \
        "music_insights.spotify.spotify_authenticator.SpotifyAuthenticator"

    @responses.activate()
    @patch(BASE_PATCH_PATH + "._get_url_from_input")
    @patch(BASE_PATCH_PATH + "._SpotifyAuthenticator__check_client_id")
    def test_client(self, _, get_url_mock):
        user_id = "id12345"
        get_url_mock.return_value = "access_token=abc"
        response_auth = responses.Response(
            method="GET",
            url=SpotifyAuthenticator._AUTH_ENDPOINT,
            json={
                "access_token": "invalid"
            },
            status=200
        )
        response_me = responses.Response(
            method="GET",
            url=SpotifyClient._ME_ENDPOINT,
            json={"id": user_id},
            status=200
        )
        responses.add(response_auth)
        responses.add(response_me)
        client = SpotifyClient.read_only_client()
        assert client.user_id == user_id
