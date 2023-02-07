import json
import os
from typing import Dict, Self, Union

from attrs import define

from library.song import Song
from library.album import Album
from library.artist import Artist
from library.attr_serialization import AttrSerialization


@define
class Library:
    SongsContainer_Type = Dict[Song.SongId_Type, Song]
    AlbumsContainer_Type = Dict[Album.AlbumId_Type, Album]
    ArtistsContainer_Type = Dict[Artist.ArtistId_Type, Artist]

    FILE_PATH = os.path.join("out")
    SONGS_PATH = os.path.join(FILE_PATH, "songs.json")
    # TODO

    songs: Dict[Song.SongId_Type, Song]
    albums: Dict[Album.AlbumId_Type, Album]
    artists: Dict[Artist.ArtistId_Type, Artist]

    @classmethod
    def empty(cls) -> Self:
        return cls({}, {}, {})
    
    @classmethod
    def from_file(cls) -> Self:
        library = cls.empty()
        library.songs = {
            k: Song.from_json_dict(v)
            for k, v
            in library.load_from_file(cls.SONGS_PATH).items()
        }
        return library

    def save_to_file(self) -> None:
        with open(self.SONGS_PATH, "w") as file:
            json.dump({x: y.to_json_dict() for x, y in self.songs.items()}, file, indent=4)

    @staticmethod
    def _save_to_file(data: Dict[str, AttrSerialization]):
        pass
        # TODO
    
    def load_from_file(self, path: str) \
            -> Dict[str, str]:
        with open(path, "r") as file:
            songs_data = json.load(file)
        return songs_data
