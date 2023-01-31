from typing import Dict

from attrs import define

from library.song import Song
from library.album import Album
from library.artist import Artist


@define
class Library:
    songs: Dict[Song.SongId_Type, Song]
    albums: Dict[Album.AlbumId_Type, Album]
    artists: Dict[Artist.ArtistId_Type, Artist]
