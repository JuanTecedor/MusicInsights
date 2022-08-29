import json
from datetime import datetime
from typing import List

from library.artist import Artist


class Song:
    song_id_type = str

    def __init__(self, added_at: datetime, artists: List[Artist.artist_id_type], duration_ms: int, explicit: bool,
                 song_id: song_id_type, name: str, popularity: int, track_number: int, is_local: bool, album_id: str,
                 disc_number: int, song_type: str):
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

    def to_json(self, indent=4):
        return json.dumps(self.__dict__, indent=indent)
