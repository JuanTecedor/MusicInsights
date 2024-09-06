from typing import Any, TypeAlias

from music_insights.utils.json_serializable import JSONSerializable


class Artist(JSONSerializable):
    IDType: TypeAlias = str
    NameType: TypeAlias = str

    def __init__(
        self,
        name: NameType,
        artist_id: IDType,
        followers: int,
        genres: list[str],
        popularity: int
    ) -> None:
        self.name = name
        self.artist_id = artist_id
        self.followers = followers
        self.genres = genres
        self.popularity = popularity

    def __eq__(self, other: Any) -> bool:
        if isinstance(self, Artist):
            return vars(self) == vars(other)
        return False
