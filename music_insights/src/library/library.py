
import json
import os
from typing import Dict, TypeAlias


from library.song import Song
from library.album import Album
from library.artist import Artist


class LibraryFilePaths:
    FILE_PATH = os.path.join("out")
    SONGS_PATH = os.path.join(FILE_PATH, "songs.json")
    ARTISTS_PATH = os.path.join(FILE_PATH, "artists.json")
    ALBUMS_PATH = os.path.join(FILE_PATH, "albums.json")


class Library:
    SongsContainer_Type: TypeAlias = Dict[Song.SongId_Type, Song]
    AlbumsContainer_Type: TypeAlias = Dict[Album.AlbumId_Type, Album]
    ArtistsContainer_Type: TypeAlias = Dict[Artist.ArtistId_Type, Artist]

    def __init__(
        self,
        songs: Dict[Song.SongId_Type, Song],
        albums: Dict[Album.AlbumId_Type, Album],
        artists: Dict[Artist.ArtistId_Type, Artist]
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
