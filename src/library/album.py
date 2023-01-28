from datetime import datetime
from typing import List

from library.artist import Artist
from library.song import Song


class Album:
    AlbumId_Type = str
    AlbumName_Type = str

    def __init__(self,
                 album_type: str,
                 artists: List[Artist.ArtistId_Type],
                 album_id: AlbumId_Type,
                 name: AlbumName_Type,
                 release_date: datetime,
                 release_date_precision: str,
                 songs: List[Song.SongId_Type],
                 total_tracks: int) -> None:
        self.album_type = album_type
        self.artists = artists
        self.album_id = album_id
        self.name = name
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.songs = songs
        self.total_tracks = total_tracks
