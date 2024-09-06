import logging
from typing import Any, Optional

import requests
from typing_extensions import Self

from music_insights.library.album import Album
from music_insights.library.artist import Artist
from music_insights.library.library import Library
from music_insights.library.song import Song
from music_insights.spotify.spotify_authenticator import SpotifyAuthenticator
from music_insights.utils.utils import split_list_in_chunks


class InvalidStatusCodeException(Exception):
    pass


class SpotifyClient:
    _BASE_URL = "https://api.spotify.com/v1"
    _ME_ENDPOINT = _BASE_URL + "/me"
    _SAVED_TRACKS_URL = _ME_ENDPOINT + "/tracks"
    _ARTISTS_URL = _BASE_URL + "/artists"
    _ALBUMS_URL = _BASE_URL + "/albums"
    _PLAYLISTS_URL = _BASE_URL + "/playlists"

    _GET_EXPECTED_STATUS_CODE = 200
    _POST_EXPECTED_STATUS_CODE = 201

    def __init__(self, token: str) -> None:
        self._token = token
        self.user_id = self._get_user_id()
        self.CREATE_PLAYLIST_URL = self._BASE_URL \
            + f"/users/{self.user_id}/playlists"

    @classmethod
    def read_only_client(cls) -> Self:
        return cls(
            SpotifyAuthenticator().authenticate(
                [SpotifyAuthenticator.AvailableScopes.USER_LIBRARY_READ]
            )
        )

    @classmethod
    def read_write_playlist_client(cls) -> Self:
        return cls(
            SpotifyAuthenticator().authenticate([
                SpotifyAuthenticator.AvailableScopes.PLAYLIST_READ_PRIVATE,
                SpotifyAuthenticator.AvailableScopes.PLAYLIST_MODIFY_PRIVATE
            ])
        )

    @staticmethod
    def _check_status_code(response: requests.Response, expected_status_code):
        if response.status_code != expected_status_code:
            raise InvalidStatusCodeException(
                f"The status code was {response.status_code}, "
                f"expected {expected_status_code}."
            )

    def _get_user_id(self) -> str:
        response = requests.get(
            self._ME_ENDPOINT,
            headers=self._get_common_headers()
        )
        self._check_status_code(response, self._GET_EXPECTED_STATUS_CODE)
        return response.json()["id"]

    def _get_common_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }

    def _request_songs(self, alternate_url: Optional[str] = None) \
            -> requests.Response:
        response = requests.get(
            url=alternate_url or self._SAVED_TRACKS_URL,
            headers=self._get_common_headers(),
            params={
                "limit": 50
            }
        )
        self._check_status_code(response, self._GET_EXPECTED_STATUS_CODE)
        return response

    @staticmethod
    def _parse_songs(json_response_items: list[dict[str, Any]]) \
            -> dict[Song.IDType, Song]:
        songs = {}
        for song_data in json_response_items:
            track_data = song_data["track"]
            song_id = track_data["id"]
            songs[song_id] = Song(
                added_at=song_data["added_at"],
                song_id=song_id,
                album_id=track_data["album"]["id"],
                popularity=track_data["popularity"],
                track_number=track_data["track_number"],
                duration_ms=track_data["duration_ms"],
                explicit=track_data["explicit"],
                name=track_data["name"],
                is_local=track_data["is_local"],
                disc_number=track_data["disc_number"],
                artists=[
                    album_data["id"]
                    for album_data
                    in track_data["album"]["artists"]
                ]
            )
        return songs

    def get_liked_songs(self) -> Library.SongsContainerType:
        logging.info("Requesting liked songs")
        songs: dict[Song.IDType, Song] = {}
        next_url = None
        while True:
            response = self._request_songs(next_url)
            json_response = response.json()
            songs = songs | self._parse_songs(json_response["items"])
            next_url = json_response["next"]
            if next_url is None:
                break
        logging.info(f"Found {len(songs)} songs")
        return songs

    @staticmethod
    def _parse_artists(json_response_items: list[dict[str, Any]]) \
            -> dict[Artist.IDType, Artist]:
        artists = {}
        for artist_data in json_response_items:
            artist_id = artist_data["id"]
            artists[artist_id] = Artist(
                artist_data["name"],
                artist_data["id"],
                artist_data["followers"]["total"],
                artist_data["genres"],
                artist_data["popularity"]
            )
        return artists

    def get_artists(self, ids: list[Artist.IDType]) \
            -> Library.ArtistsContainerType:
        logging.info("Requesting artists")
        artists: dict[Artist.IDType, Artist] = {}
        id_chunks = split_list_in_chunks(ids, 50)
        for id_chunk in id_chunks:
            response = requests.get(
                url=self._ARTISTS_URL,
                headers=self._get_common_headers(),
                params={"ids": ",".join(id_chunk)}
            )
            self._check_status_code(response, self._GET_EXPECTED_STATUS_CODE)
            artists = artists | self._parse_artists(response.json()["artists"])
        logging.info(f"Found {len(artists)} artists")
        return artists

    @staticmethod
    def _parse_albums(json_response_items: list[dict[str, Any]]) \
            -> dict[Album.IDType, Album]:
        albums = {}
        for album_data in json_response_items:
            album_id = album_data["id"]
            albums[album_id] = Album(
                [artist_data["id"] for artist_data in album_data["artists"]],
                album_data["id"],
                album_data["name"],
                album_data["release_date"],
                album_data["release_date_precision"],
                [
                    song_data["id"]
                    for song_data
                    in album_data["tracks"]["items"]
                ],
                album_data["total_tracks"],
                album_data["genres"],
                album_data["label"],
                album_data["popularity"]
            )
        return albums

    def get_albums(self, ids: list[Album.IDType]) \
            -> Library.AlbumsContainerType:
        logging.info("Requesting albums")
        albums: dict[Album.IDType, Album] = {}
        id_chunks = split_list_in_chunks(ids, 20)
        for id_chunk in id_chunks:
            response = requests.get(
                url=self._ALBUMS_URL,
                headers=self._get_common_headers(),
                params={"ids": ",".join(id_chunk)}
            )
            self._check_status_code(response, self._GET_EXPECTED_STATUS_CODE)
            albums = albums | self._parse_albums(response.json()["albums"])
        logging.info(f"Found {len(albums)} albums")
        return albums

    def create_playlist(
        self, playlist_name: str, song_list: list[Song.IDType]
    ) -> None:
        data = {
            "name": playlist_name,
            "public": False,
            "collaborative": False
        }
        response = requests.post(
            self.CREATE_PLAYLIST_URL,
            headers=self._get_common_headers(),
            json=data
        )
        self._check_status_code(response, self._POST_EXPECTED_STATUS_CODE)
        playlist_id = response.json()["id"]
        self._add_songs_to_playlist(playlist_id, song_list)
        logging.info(
            f"Added playlist with name {playlist_name} "
            f"containing {len(song_list)} songs"
        )

    def _add_songs_to_playlist(
        self, playlist_id: str, song_list: list[Song.IDType]
    ) -> None:
        max_size = 100
        splitted_song_list = split_list_in_chunks(song_list, max_size)
        for splitted in splitted_song_list:
            data = {
                "uris": [f"spotify:track:{x}" for x in splitted]
            }
            response = requests.post(
                self._PLAYLISTS_URL + f"/{playlist_id}/tracks",
                headers=self._get_common_headers(),
                json=data
            )
            self._check_status_code(response, self._POST_EXPECTED_STATUS_CODE)
