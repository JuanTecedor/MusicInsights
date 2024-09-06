import json
import os

from music_insights.library.album import Album
from music_insights.library.artist import Artist
from music_insights.library.song import Song
from music_insights.utils.json_serializable import JSONSerializableSubClass


class LibraryFilePaths:
    FILE_PATH = os.path.join("out")
    SONGS_PATH = os.path.join(FILE_PATH, "songs.json")
    ARTISTS_PATH = os.path.join(FILE_PATH, "artists.json")
    ALBUMS_PATH = os.path.join(FILE_PATH, "albums.json")


class Library:
    SongsContainerType = dict[Song.IDType, Song]
    AlbumsContainerType = dict[Album.IDType, Album]
    ArtistsContainerType = dict[Artist.IDType, Artist]

    def __init__(
        self,
        songs: dict[Song.IDType, Song],
        albums: dict[Album.IDType, Album],
        artists: dict[Artist.IDType, Artist]
    ) -> None:
        self._songs = songs
        self._albums = albums
        self._artists = artists

    @staticmethod
    def _save_dict_to_file(
        data: dict[str, JSONSerializableSubClass],
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

    def get_songs_by_decades(self) -> dict[int, list[Song.IDType]]:
        songs_by_decades = {}
        for song_id, song_data in self._songs.items():
            year = self._albums[song_data.album_id].release_date.year
            decade = year - (year % 10)
            if decade in songs_by_decades:
                songs_by_decades[decade].append(song_id)
            else:
                songs_by_decades[decade] = [song_id]
        return songs_by_decades
