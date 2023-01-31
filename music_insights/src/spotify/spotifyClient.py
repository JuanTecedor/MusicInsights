from typing import Any, Dict, List, Optional

import requests

from library.song import Song
from utils import split_list_in_chunks


class UnableToGetUserIDException(Exception):
    pass


class UnableToGetTracksException(Exception):
    pass


class UnableToCreatePlaylistException(Exception):
    pass


class UnableToAddSongsToPlaylistException(Exception):
    pass


class SpotifyClient:
    _BASE_URL = "https://api.spotify.com/v1"
    _SAVED_TRACKS_URL = _BASE_URL + "/me/tracks"

    def __init__(self, token: str) -> None:
        self.token = token
        self.user_id = self._get_user_id()
        self.CREATE_PLAYLIST_URL = self._BASE_URL \
            + f"/users/{self.user_id}/playlists"

    def _get_user_id(self) -> None:
        response = requests.get(
            "https://api.spotify.com/v1/me",
            headers=self._get_common_headers()
        )
        if response.status_code != 200:
            raise UnableToGetUserIDException(
                f"The response status code was not 200\n{response.text}"
            )
        return response.json()["id"]

    def _get_common_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _parse_songs(json_response_items: List[Dict[str, Any]]) \
            -> Dict[Song.SongId_Type, Song]:
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

    def _request_songs(self, alternate_url: Optional[str] = None) \
            -> requests.Response:
        response = requests.get(
            url=alternate_url or self._SAVED_TRACKS_URL,
            headers=self._get_common_headers(),
            params={
                "limit": 50
            }
        )
        if response.status_code != 200:
            raise UnableToGetTracksException(
                f"The response status code was {response.status_code}"
            )
        return response

    def get_liked_songs(self) -> Dict[Song.SongId_Type, Song]:
        songs = {}
        next_url = None
        while True:
            response = self._request_songs(next_url)
            json_response = response.json()
            songs = songs | self._parse_songs(json_response["items"])
            next_url = json_response["next"]
            if next_url is None:
                break
        return songs

    # TODO update
    def create_playlist(
        self, playlist_name: str, song_list: List[Song.SongId_Type]
            ) -> None:
        data = {
            "name": playlist_name,
            "public": False,
            "collaborative": False,
            "description": ""
        }

        response = requests.post(
            self.CREATE_PLAYLIST_URL,
            headers=self._get_common_headers(),
            json=data
        )
        if response.status_code != 201:
            raise UnableToCreatePlaylistException(
                f"The response status code was not 200\n{response.text}"
            )

        playlist_id = response.json()["id"]
        self._add_songs_to_playlist(playlist_id, song_list)

    def _add_songs_to_playlist(
        self, playlist_id: str, song_list: List[Song.SongId_Type]
    ) -> None:
        max_size = 100
        splitted_song_list = split_list_in_chunks(song_list, max_size)
        for splitted in splitted_song_list:
            data = {
                "uris": [f"spotify:track:{x}" for x in splitted]
            }
            response = requests.post(
                self._BASE_URL + f"/playlists/{playlist_id}/tracks",
                headers=self._get_common_headers(),
                json=data)

            if response.status_code != 201:
                raise UnableToAddSongsToPlaylistException(
                    f"The response status code was not 200\n{response.text}"
                )
