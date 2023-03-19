from datetime import datetime
from typing import List

from attrs import define, field

from library.artist import Artist
from library.attr_serialization import AttrSerialization


@define
class Song(AttrSerialization):
    SongId_Type = str
    SongName_Type = str

    song_id: SongId_Type
    added_at: datetime = field(
        converter=datetime.fromisoformat
    )
    artists: List[Artist.ArtistId_Type]
    duration_ms: int
    explicit: bool
    name: SongName_Type
    popularity: int
    track_number: int
    album_id: str
    disc_number: int
    is_local: bool
