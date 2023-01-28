class Artist:
    ArtistId_Type = str
    ArtistName_Type = str

    def __init__(
        self,
        name: ArtistName_Type,
        artist_id: ArtistId_Type,
        artist_type: str
    ) -> None:
        self.name = name
        self.artist_id = artist_id
        self.artist_type = artist_type
