from typing import List, Dict, Any

import requests

from library.album import Album
from library.artist import Artist
from library.library import Library
from library.song import Song


class SpotifyClientWrongResponseStatusCode(Exception):
    pass


class SpotifyClient:
    url = "https://api.spotify.com/v1/me/tracks"

    def __init__(self, token: str):
        self.token = token

    def download_library(self) -> Library:
        library = Library()
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "limit": "1"
        }
        response = requests.get(url=self.url, headers=headers)
        json_data = response.json()

        if response.status_code != 200:
            raise SpotifyClientWrongResponseStatusCode(
                "The response status code was not 200"
            )

        self._add_items(library, json_data["items"])
        while json_data["next"]:
            response = requests.get(url=json_data["next"], headers=headers)
            json_data = response.json()
            self._add_items(library, json_data["items"])
        return library

    @staticmethod
    def _add_items(library: Library, items: List[Dict[str, Any]]):
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
