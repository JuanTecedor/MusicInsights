from dataclasses import dataclass
from typing import ClassVar

from music_insights.utils.json_serializable import JSONSerializable


@dataclass
class Artist(JSONSerializable):
    IDType: ClassVar = str
    NameType: ClassVar = str

    name: NameType
    artist_id: IDType
    followers: int
    genres: list[str]
    popularity: int
