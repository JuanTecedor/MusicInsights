from datetime import datetime
from typing import List

from src.library.artist import Artist
from src.library.song import Song


class Album:
    AlbumId = str

    def __init__(self,
                 album_type: str,
                 artists: List[Artist.ArtistId],
                 album_id: AlbumId,
                 name: str,
                 release_date: datetime,
                 release_date_precision: str,
                 songs: List[Song.SongId],
                 total_tracks: int):
        self.album_type = album_type
        self.artists = artists
        self.album_id = album_id
        self.name = name
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.songs = songs
        self.total_tracks = total_tracks
