from datetime import datetime
from typing import List

from attrs import define

from library.artist import Artist
from library.song import Song


@define
class Album():  # TODO
    AlbumId_Type = str
    AlbumName_Type = str

    artists: List[Artist.ArtistId_Type]
    album_id: AlbumId_Type
    name: AlbumName_Type
    release_date: datetime
    release_date_precision: str
    songs: List[Song.SongId_Type]
    total_tracks: int
