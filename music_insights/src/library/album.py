from datetime import datetime
from typing import List

from attrs import define

from library.artist import Artist
from library.song import Song
from library.attr_serialization import AttrSerialization


@define
class Album(AttrSerialization):
    AlbumId_Type = str
    AlbumName_Type = str

    artists: List[Artist.ArtistId_Type]
    album_id: AlbumId_Type
    name: AlbumName_Type
    release_date: datetime
    release_date_precision: str
    songs: List[Song.SongId_Type]
    total_tracks: int
    genres: List[str]
    label: str
    popularity: int
