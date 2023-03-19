import json
import os
from typing import Dict, List

from library.album import Album
from library.artist import Artist
from library.song import Song


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

    def save_to_file(self) -> None:
        with open(LibraryFilePaths.SONGS_PATH, "w") as file:
            json.dump(
                {
                    song_id: song_data.to_json_dict()
                    for song_id, song_data
                    in self._songs.items()
                },
                file,
                indent=4
            )
        with open(LibraryFilePaths.ARTISTS_PATH, "w") as file:
            json.dump(
                {
                    artist_id: artist_data.to_json_dict()
                    for artist_id, artist_data
                    in self._artists.items()
                },
                file,
                indent=4
            )
        with open(LibraryFilePaths.ALBUMS_PATH, "w") as file:
            json.dump(
                {
                    album_id: album_data.to_json_dict()
                    for album_id, album_data
                    in self._albums.items()
                },
                file,
                indent=4
            )

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
