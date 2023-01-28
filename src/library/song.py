from datetime import datetime
from typing import List

from attrs import define

from library.artist import Artist


@define
class Song:
    SongId_Type = str
    SongName_Type = str

    added_at: datetime
    artists: List[Artist.ArtistId_Type]
    duration_ms: int
    explicit: bool
    song_id: SongId_Type
    name: SongName_Type
    popularity: int
    track_number: int
    is_local: bool
    album_id: str
    disc_number: int
    song_type: str
