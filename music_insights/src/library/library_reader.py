from abc import ABC, abstractmethod
import json
import logging
from typing import List, Self

from spotify.spotifyClient import SpotifyClient, UnableToGetTracksException
from library.library import Library, LibraryFilePaths
from library.song import Song


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
                return Library(library_songs, {}, {})  # TODO
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
            return Library(
                songs=songs,
                albums={},
                artists=artists
            )  # TODO
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
