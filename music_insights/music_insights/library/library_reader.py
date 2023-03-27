import json
import logging
from abc import ABC, abstractmethod
from typing import Self

from music_insights.library.album import Album
from music_insights.library.artist import Artist
from music_insights.library.library import Library, LibraryFilePaths
from music_insights.library.song import Song
from music_insights.spotify.spotifyClient import (SpotifyClient,
                                                  UnableToGetTracksException)


class UnableToGetLibrary(Exception):
    pass


class LibraryReader(ABC):
    @abstractmethod
    def get_library(self) -> Library:
        raise NotImplementedError()


class LibraryReaderFromFile(LibraryReader):
    def get_library(self) -> Library:
        try:
            logging.info("Loading library from file ")
            with open(LibraryFilePaths.SONGS_PATH, "r") as file:
                library_songs = {
                    song_id: Song.from_json_dict(song_data)
                    for song_id, song_data
                    in json.load(file).items()
                }
            with open(LibraryFilePaths.ALBUMS_PATH, "r") as file:
                library_albums = {
                    album_id: Album.from_json_dict(album_data)
                    for album_id, album_data
                    in json.load(file).items()
                }
            with open(LibraryFilePaths.ARTISTS_PATH, "r") as file:
                library_artists = {
                    artist_id: Artist.from_json_dict(artist_data)
                    for artist_id, artist_data
                    in json.load(file).items()
                }
            return Library(library_songs, library_albums, library_artists)
        except FileNotFoundError as ex:
            raise UnableToGetLibrary(ex)


class LibraryReaderFromAPI(LibraryReader):
    def get_library(self) -> Library:
        client = SpotifyClient.read_only_client()
        try:
            logging.info("Loading library from API")
            songs = client.get_liked_songs()
            artists = client.get_artists(list(
                {
                    album_id
                    for song
                    in songs.values()
                    for album_id
                    in song.artists
                }
            ))
            albums = client.get_albums(list(
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
    def __init__(self, library_readers: list[LibraryReader]) -> None:
        self._readers = library_readers

    @classmethod
    def default(cls) -> Self:
        return cls([
            LibraryReaderFromFile(),
            LibraryReaderFromAPI()
        ])

    @classmethod
    def only_api(cls) -> Self:
        return cls([LibraryReaderFromAPI()])

    def get_library(self) -> Library:
        for reader in self._readers:
            try:
                return reader.get_library()
            except UnableToGetLibrary:
                continue
        raise UnableToGetLibrary("Could not load library")
