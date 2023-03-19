from dataclasses import dataclass
from typing import ClassVar, List

from utils.json_serializable import JSONSerializable


@dataclass
class Artist(JSONSerializable):
    IDType: ClassVar = str
    NameType: ClassVar = str

    name: NameType
    artist_id: IDType
    followers: int
    genres: List[str]
    popularity: int
