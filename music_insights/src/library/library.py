import json
import os
from typing import Dict, List

from library.album import Album
from library.artist import Artist
from library.song import Song
from utils.json_serializable import JSONSerializableSubClass


class LibraryFilePaths:
    FILE_PATH = os.path.join("out")
    SONGS_PATH = os.path.join(FILE_PATH, "songs.json")
    ARTISTS_PATH = os.path.join(FILE_PATH, "artists.json")
    ALBUMS_PATH = os.path.join(FILE_PATH, "albums.json")


class Library:
    SongsContainerType = Dict[Song.IDType, Song]
    AlbumsContainerType = Dict[Album.IDType, Album]
    ArtistsContainerType = Dict[Artist.IDType, Artist]

    def __init__(
        self,
        songs: Dict[Song.IDType, Song],
        albums: Dict[Album.IDType, Album],
        artists: Dict[Artist.IDType, Artist]
    ) -> None:
        self._songs = songs
        self._albums = albums
        self._artists = artists

    @staticmethod
    def _save_dict_to_file(
        data: Dict[str, JSONSerializableSubClass],
        path: str,
        indent: int = 4
    ) -> None:
        with open(path, "w") as file:
            json.dump(
                {
                    item_id: item.to_json_dict()
                    for item_id, item
                    in data.items()
                },
                file,
                indent=indent
            )

    def save_to_file(self) -> None:
        self._save_dict_to_file(self._songs, LibraryFilePaths.SONGS_PATH)
        self._save_dict_to_file(self._artists, LibraryFilePaths.ARTISTS_PATH)
        self._save_dict_to_file(self._albums, LibraryFilePaths.ALBUMS_PATH)

    def get_songs_by_decades(self) -> Dict[int, List[Song.IDType]]:
        songs_by_decades = {}
        for song_id, song_data in self._songs.items():
            year = self._albums[song_data.album_id].release_date.year
            decade = year - (year % 10)
            if decade in songs_by_decades:
                songs_by_decades[decade].append(song_id)
            else:
                songs_by_decades[decade] = [song_id]
        return songs_by_decades
