from attrs import define


@define
class Artist:
    ArtistId_Type = str
    ArtistName_Type = str

    name: ArtistName_Type
    artist_id: ArtistId_Type
    artist_type: str
