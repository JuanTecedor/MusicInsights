class Artist:
    artist_id_type = str

    def __init__(self, name: str, artist_id: artist_id_type, artist_type: str):
        self.name = name
        self.artist_id = artist_id
        self.artist_type = artist_type
