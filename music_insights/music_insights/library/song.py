from datetime import datetime
from typing import Any

from music_insights.library.artist import Artist
from music_insights.utils.json_serializable import JSONSerializable


class Song(JSONSerializable):
    IDType = str
    NameType = str

    def __init__(
        self,
        song_id: IDType,
        added_at: str,
        artists: list[Artist.IDType],
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

    def __eq__(self, other: Any) -> bool:
        if isinstance(self, Song):
            return vars(self) == vars(other)
        return False
