import json
from datetime import datetime
from typing import List, Self

from attrs import define, field, asdict

from src.library.artist import Artist
from src.library.json_serializable import JSONSerializable
from src.library.item_encoder import ItemEncoder


@define
class Song(JSONSerializable):
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
    preview_url: str = ""

    def to_json_str(self) -> str:
        return json.dumps(asdict(self), cls=ItemEncoder)

    @classmethod
    def from_json_str(cls, data: str) -> Self:
        data = json.loads(data)
        return cls(**data)
