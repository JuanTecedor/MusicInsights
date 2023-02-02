import json
import os
from typing import Dict

from attrs import define

from library.song import Song
from library.album import Album
from library.artist import Artist


@define
class Library:
    SongsContainer_Type = Dict[Song.SongId_Type, Song]
    AlbumsContainer_Type = Dict[Album.AlbumId_Type, Album]
    ArtistsContainer_Type = Dict[Artist.ArtistId_Type, Artist]

    songs: Dict[Song.SongId_Type, Song]
    albums: Dict[Album.AlbumId_Type, Album]
    artists: Dict[Artist.ArtistId_Type, Artist]

    def save_to_file(self) -> None:
        with open(os.path.join("out", "songs.json"), "w") as file:
            json.dump({x: y.to_json_dict() for x, y in self.songs.items()}, file, indent=4)
            
        # TODO
        raise NotImplementedError("TODO")
