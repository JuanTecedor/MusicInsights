from datetime import date
from typing import Dict, List, Self

from attrs import define

from library.artist import Artist
from library.attr_serialization import AttrSerialization
from library.item_encoder import JSONEncoder
from library.song import Song


class UnknownDatePrecisionException(Exception):
    pass


@define
class Album(AttrSerialization):
    AlbumId_Type = str
    AlbumName_Type = str

    artists: List[Artist.ArtistId_Type]
    album_id: AlbumId_Type
    name: AlbumName_Type
    release_date: date
    release_date_precision: str
    songs: List[Song.SongId_Type]
    total_tracks: int
    genres: List[str]
    label: str
    popularity: int

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

    @classmethod
    def from_json_dict(cls, data: Dict[str, JSONEncoder.JSON_Types]) -> Self:
        album = super().from_json_dict(data)
        album.release_date = \
            date.fromisoformat(album.release_date)  # type: ignore
        return album
