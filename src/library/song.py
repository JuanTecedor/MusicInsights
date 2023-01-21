from datetime import datetime
from typing import List

from library.artist import Artist


class Song:
    SongId = str

    def __init__(self,
                 added_at: datetime,
                 artists: List[Artist.ArtistId],
                 duration_ms: int,
                 explicit: bool,
                 song_id: SongId,
                 name: str,
                 popularity: int,
                 track_number: int,
                 is_local: bool,
                 album_id: str,
                 disc_number: int,
                 song_type: str) -> None:
        self.added_at = added_at
        self.artists = artists
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.song_id = song_id
        self.name = name
        self.popularity = popularity
        self.track_number = track_number
        self.is_local = is_local
        self.album_id = album_id
        self.disc_number = disc_number
        self.song_type = song_type
