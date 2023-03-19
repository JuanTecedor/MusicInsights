from datetime import date, datetime
from typing import ClassVar, List

from library.artist import Artist
from library.song import Song
from utils.json_serializable import JSONSerializable


class UnknownDatePrecisionException(Exception):
    pass


class Album(JSONSerializable):
    IDType: ClassVar = str
    NameType: ClassVar = str

    def __init__(
        self,
        artists: List[Artist.IDType],
        album_id: IDType,
        name: NameType,
        release_date: str,
        release_date_precision: str,
        songs: List[Song.IDType],
        total_tracks: int,
        genres: List[str],
        label: str,
        popularity: int
    ) -> None:
        self.artists = artists
        self.album_id = album_id
        self.name = name
        date_format = Album.date_precision_to_date_format(
            release_date_precision
        )
        try:
            self.release_date = datetime.strptime(
                release_date,
                date_format
            ).date()
        except ValueError:
            # When loading back from file we always find the full string
            self.release_date = date.fromisoformat(release_date)
        self.release_date_precision = release_date_precision
        self.songs = songs
        self.total_tracks = total_tracks
        self.genres = genres
        self.label = label
        self.popularity = popularity

    @staticmethod
    def date_precision_to_date_format(precision: str) -> str:
        if precision == "year":
            return "%Y"
        elif precision == "month":
            return "%Y-%m"
        elif precision == "day":
            return "%Y-%m-%d"
        else:
            raise UnknownDatePrecisionException(
                f"The precision of the date is unknown {precision}."
            )
