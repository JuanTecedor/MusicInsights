import json
from datetime import datetime

from library.album import Album
from library.artist import Artist
from library.song import Song


class UnknownDatePrecisionError(Exception):
    pass


class Library:
    songs_path = "out/songs.json"
    albums_path = "out/albums.json"
    artists_path = "out/artists.json"

    def __init__(self):
        self.artists = {}
        self.songs = {}
        self.albums = {}

    @staticmethod
    def _date_precision_to_date_format(precision):
        if precision == "year":
            return "%Y"
        elif precision == "month":
            return "%Y-%m"
        elif precision == "day":
            return "%Y-%m-%d"
        else:
            raise UnknownDatePrecisionError(f"The precision of the date is not known {precision}.")

    def load_from_files(self):
        with open(self.songs_path, "r") as file:
            songs_dict = json.load(file)
            for song_id, song_data in songs_dict.items():
                song_data["added_at"] = datetime.fromisoformat(song_data["added_at"][:-1])
                self.songs[song_id] = Song(**song_data)

        with open(self.albums_path, "r") as file:
            albums_dict = json.load(file)
            for album_id, album_data in albums_dict.items():
                date_format = self._date_precision_to_date_format(album_data["release_date_precision"])
                album_data["release_date"] = datetime.strptime(album_data["release_date"], date_format)
                self.albums[album_id] = Album(**album_data)

        with open(self.artists_path, "r") as file:
            artists_dict = json.load(file)
            for artist_id, artist_data in artists_dict.items():
                self.artists[artist_id] = Artist(**artist_data)

    def save_to_file(self):
        with open(self.songs_path, "w") as file:
            json.dump(self.songs, file, default=vars, indent=4)

        with open(self.albums_path, "w") as file:
            json.dump(self.albums, file, default=vars, indent=4)

        with open(self.artists_path, "w") as file:
            json.dump(self.artists, file, default=vars, indent=4)
