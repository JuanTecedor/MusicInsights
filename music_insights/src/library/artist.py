from typing import List

from attrs import define

from library.attr_serialization import AttrSerialization


@define
class Artist(AttrSerialization):
    ArtistId_Type = str
    ArtistName_Type = str

    name: ArtistName_Type
    artist_id: ArtistId_Type
    followers: int
    genres: List[str]
    popularity: int
