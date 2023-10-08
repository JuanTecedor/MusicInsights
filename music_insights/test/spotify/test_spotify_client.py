import responses
from unittest.mock import patch
from pytest import fixture

from music_insights.spotify.spotify_client import SpotifyClient
from music_insights.spotify.spotify_authenticator import SpotifyAuthenticator


class TestSpotifyClient:
    @responses.activate()
    @patch(
        "music_insights.spotify.spotify_authenticator"
        ".SpotifyAuthenticator._get_url_from_input"
    )
    def test_client(self, get_url_mock):
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
