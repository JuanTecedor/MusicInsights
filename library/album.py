from datetime import datetime
from typing import List

from library.artist import Artist
from library.song import Song


class Album:
    album_id_type = str

    def __init__(self, album_type: str, artists: List[Artist.artist_id_type],
                 album_id: album_id_type, name: str, release_date: datetime, release_date_precision: str,
                 songs: List[Song.song_id_type], total_tracks: int):
        self.album_type = album_type
        self.artists = artists
        self.album_id = album_id
        self.name = name
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.songs = songs
        self.total_tracks = total_tracks
