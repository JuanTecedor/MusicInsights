from abc import ABC, abstractmethod
import json
import logging
from typing import List, Self

from spotify.spotifyClient import SpotifyClient, UnableToGetTracksException
from library.library import Library, LibraryFilePaths
from library.song import Song
from library.album import Album
from library.album import Artist


class UnableToGetLibrary(Exception):
    pass


class LibraryReader(ABC):
    @abstractmethod
    def get_library(self) -> Library:
        raise NotImplementedError()


class LibraryReaderFromFile(LibraryReader):
    def get_library(self) -> Library:
        try:
            with open(LibraryFilePaths.SONGS_PATH, "r") as file:
                logging.info(
                    "File found, loading library from file "
                    " if you want to force a refresh, delete "
                    f"or rename {LibraryFilePaths.SONGS_PATH}"
                )
                library_songs = {
                    song_id: Song.from_json_dict(song_data)
                    for song_id, song_data
                    in json.load(file).items()
                }
                library_albums = {
                    album_id: Album.from_json_dict(album_data)
                    for album_id, album_data
                    in json.load(file).items()
                }
                library_artists = {
                    artist_id: Artist.from_json_dict(artist_data)
                    for artist_id, artist_data
                    in json.load(file).items()
                }
                return Library(library_songs, library_albums, library_artists)
        except FileNotFoundError as ex:
            raise UnableToGetLibrary(ex)


class LibraryReaderFromAPI(LibraryReader):
    def __init__(self, client: SpotifyClient) -> None:
        self._client = client

    def get_library(self) -> Library:
        try:
            logging.info("Loading library from API")
            songs = self._client.get_liked_songs()
            artists = self._client.get_artists(list(
                {
                    album_id
                    for song
                    in songs.values()
                    for album_id
                    in song.artists
                }
            ))
            albums = self._client.get_albums(list(
                {
                    song.album_id
                    for song
                    in songs.values()
                }
            ))
            return Library(
                songs=songs,
                albums=albums,
                artists=artists
            )
        except UnableToGetTracksException as ex:
            raise UnableToGetLibrary(ex)


class LibraryReaderChain(LibraryReader):
    def __init__(self, library_readers: List[LibraryReader]) -> None:
        self._readers = library_readers

    @classmethod
    def default(cls) -> Self:
        return cls([
            LibraryReaderFromFile(),
            LibraryReaderFromAPI(SpotifyClient.read_only_client())
        ])

    @classmethod
    def force_download(cls) -> Self:
        return cls([LibraryReaderFromAPI(SpotifyClient.read_only_client())])

    def get_library(self) -> Library:
        for reader in self._readers:
            try:
                return reader.get_library()
            except UnableToGetLibrary:
                continue
        raise UnableToGetLibrary()
