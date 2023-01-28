import json
import os
from datetime import datetime
from typing import Any, Dict, LiteralString

from library.album import Album
from library.artist import Artist
from library.song import Song


class UnknownDatePrecisionException(Exception):
    pass


class JSONLibrary:
    _BASE_PATH = os.path.join("out")
    _SONGS_PATH = os.path.join(_BASE_PATH, "songs.json")
    _ALBUMS_PATH = os.path.join(_BASE_PATH, "albums.json")
    _ARTISTS_PATH = os.path.join(_BASE_PATH, "artists.json")

    def __init__(self) -> None:
        self.artists = {}
        self.songs = {}
        self.albums = {}

    @staticmethod
    def _date_precision_to_date_format(precision: str) -> str:
        if precision == "year":
            return "%Y"
        elif precision == "month":
            return "%Y-%m"
        elif precision == "day":
            return "%Y-%m-%d"
        else:
            raise UnknownDatePrecisionException(
                f"The precision of the date is unknown {precision}."
            )

    @staticmethod
    def _load_from_file(path: LiteralString) -> Dict[Any, Any]:
        with open(path, "r") as file:
            return json.load(file)

    @staticmethod
    def _load_songs_from_file():
        songs = {}
        for song_id, song_data in \
                JSONLibrary._load_from_file(JSONLibrary._SONGS_PATH).items():
            song_data["added_at"] \
                = datetime.fromisoformat(song_data["added_at"][:-1])
            songs[song_id] = Song(**song_data)
        return songs

    @staticmethod
    def _load_artists_from_file():
        artists = {}
        for artist_id, artist_data in \
                JSONLibrary._load_from_file(JSONLibrary._ARTISTS_PATH).items():
            artists[artist_id] = Artist(**artist_data)
        return artists

    @staticmethod
    def _load_albums_from_file():
        albums = {}
        for album_id, album_data in \
                JSONLibrary._load_from_file(JSONLibrary._ALBUMS_PATH).items():
            date_format = JSONLibrary._date_precision_to_date_format(
                album_data["release_date_precision"]
            )
            album_data["release_date"] = datetime.strptime(
                album_data["release_date"], date_format
            )
            albums[album_id] = Album(**album_data)
        return albums

    def load_from_files(self) -> None:
        # TODO ERROR CHECKING
        self.songs = self._load_songs_from_file()
        self.artists = self._load_artists_from_file()
        self.albums = self._load_albums_from_file()

    def save_to_file(self) -> None:
        with open(self._SONGS_PATH, "w") as file:
            json.dump(self.songs, file, default=vars, indent=4)

        with open(self._ALBUMS_PATH, "w") as file:
            json.dump(self.albums, file, default=vars, indent=4)

        with open(self._ARTISTS_PATH, "w") as file:
            json.dump(self.artists, file, default=vars, indent=4)
