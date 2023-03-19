from datetime import datetime
from typing import ClassVar, List

from library.artist import Artist
from utils.json_serializable import JSONSerializable


class Song(JSONSerializable):
    IDType: ClassVar = str
    NameType: ClassVar = str

    def __init__(
        self,
        song_id: IDType,
        added_at: str,
        artists: List[Artist.IDType],
        duration_ms: int,
        explicit: bool,
        name: NameType,
        popularity: int,
        track_number: int,
        album_id: str,
        disc_number: int,
        is_local: bool
    ) -> None:
        self.song_id = song_id
        self.added_at = datetime.fromisoformat(added_at)
        self.artists = artists
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.name = name
        self.popularity = popularity
        self.track_number = track_number
        self.album_id = album_id
        self.disc_number = disc_number
        self.is_local = is_local
