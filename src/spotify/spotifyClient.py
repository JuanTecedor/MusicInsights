from typing import Any, Dict, List

import requests

from library.album import Album
from library.artist import Artist
from library.json_library import JSONLibrary
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
    BASE_URL = "https://api.spotify.com/v1"
    SAVED_TRACKS_URL = BASE_URL + "/me/tracks"

    def __init__(self, token: str) -> None:
        self.token = token
        self.user_id = self._get_user_id()
        self.CREATE_PLAYLIST_URL = self.BASE_URL \
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

    def download_library_as_json(self) -> JSONLibrary:
        library = JSONLibrary()
        headers = self._get_common_headers()
        headers["limit"] = "50"
        response = requests.get(url=self.SAVED_TRACKS_URL, headers=headers)
        json_data = response.json()

        if response.status_code != 200:
            raise UnableToGetTracksException(
                f"The response status code was not 200\n{response.text}"
            )

        self._add_items(library, json_data["items"])
        while json_data["next"]:
            response = requests.get(url=json_data["next"], headers=headers)
            json_data = response.json()
            self._add_items(library, json_data["items"])
        return library

    @staticmethod
    def _add_items(library: JSONLibrary, items: List[Dict[str, Any]]) -> None:
        for item in items:
            track_data = item["track"]
            song_id = track_data["id"]
            artists = \
                [artist_data["id"] for artist_data in track_data["artists"]]
            album_id = track_data["album"]["id"]

            if song_id not in library.songs:
                song = Song(
                    added_at=item["added_at"],
                    artists=artists,
                    duration_ms=track_data["duration_ms"],
                    explicit=track_data["explicit"],
                    song_id=song_id,
                    name=track_data["name"],
                    popularity=track_data["popularity"],
                    track_number=track_data["track_number"],
                    is_local=track_data["is_local"],
                    album_id=album_id,
                    disc_number=track_data["disc_number"],
                    song_type=track_data["type"]
                )
                library.songs[song_id] = song

            if album_id not in library.albums:
                album_data = track_data["album"]
                album = Album(
                    album_type=album_data["album_type"],
                    artists=artists,
                    album_id=album_id,
                    name=album_data["name"],
                    release_date=album_data["release_date"],
                    release_date_precision=album_data[
                        "release_date_precision"
                    ],
                    songs=[song_id],
                    total_tracks=album_data["total_tracks"]
                )
                library.albums[album_id] = album
            else:
                library.albums[album_id].songs.append(song_id)

            for artist_data in track_data["artists"]:
                artist_id = artist_data["id"]
                if artist_id not in library.artists:
                    artist = Artist(
                        name=artist_data["name"],
                        artist_id=artist_id,
                        artist_type=artist_data["type"]
                    )
                    library.artists[artist_id] = artist

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
                self.BASE_URL + f"/playlists/{playlist_id}/tracks",
                headers=self._get_common_headers(),
                json=data)

            if response.status_code != 201:
                raise UnableToAddSongsToPlaylistException(
                    f"The response status code was not 200\n{response.text}"
                )
