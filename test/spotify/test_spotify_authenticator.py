from typing import Final
from unittest.mock import patch

import pytest
import responses

from music_insights.spotify.spotify_authenticator import (
    AccessTokenNotFoundException, BadStatusCodeException, SpotifyAuthenticator)


class TestAuthenticator:
    BASE_PATCH_PATH: Final[str] = \
        "music_insights.spotify.spotify_authenticator.SpotifyAuthenticator"

    @responses.activate()
    @patch(BASE_PATCH_PATH + "._get_url_from_input")
    @patch(BASE_PATCH_PATH + "._SpotifyAuthenticator__check_client_id")
    def test_authenticator(self, _, get_url_mock):
        access_token = "abnmghjk"
        url = "access_token=" + access_token
        get_url_mock.return_value = url
        response = responses.Response(
            method="GET",
            url=SpotifyAuthenticator._AUTH_ENDPOINT,
            json={
                "access_token": access_token
            },
            status=200
        )
        responses.add(response)
        authenticator = SpotifyAuthenticator()
        token = authenticator.authenticate([
            SpotifyAuthenticator.AvailableScopes.USER_LIBRARY_READ,
            SpotifyAuthenticator.AvailableScopes.PLAYLIST_MODIFY_PRIVATE,
            SpotifyAuthenticator.AvailableScopes.PLAYLIST_READ_PRIVATE
        ])
        assert token == access_token

    @responses.activate()
    @patch(BASE_PATCH_PATH + "._get_url_from_input")
    @patch(BASE_PATCH_PATH + "._SpotifyAuthenticator__check_client_id")
    def test_authenticator_invalid_url(self, _, get_url_mock):
        url = "invalid"
        get_url_mock.return_value = url
        response = responses.Response(
            method="GET",
            url=SpotifyAuthenticator._AUTH_ENDPOINT,
            json={
                "access_token": "invalid"
            },
            status=200
        )
        responses.add(response)
        authenticator = SpotifyAuthenticator()
        with pytest.raises(AccessTokenNotFoundException):
            authenticator.authenticate([
                SpotifyAuthenticator.AvailableScopes.PLAYLIST_READ_PRIVATE
            ])

    @responses.activate()
    @patch(BASE_PATCH_PATH + "._SpotifyAuthenticator__check_client_id")
    def test_authenticator_invalid_response_code(self, _):
        response = responses.Response(
            method="GET",
            url=SpotifyAuthenticator._AUTH_ENDPOINT,
            status=400
        )
        responses.add(response)
        authenticator = SpotifyAuthenticator()
        with pytest.raises(BadStatusCodeException):
            authenticator.authenticate([
                SpotifyAuthenticator.AvailableScopes.PLAYLIST_READ_PRIVATE
            ])
