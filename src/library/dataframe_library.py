from typing import Dict, List
import pandas as pd

from library.json_library import JSONLibrary
from library.album import Album
from library.song import Song


class DataFrameLibrary:
    def __init__(self, json_library: JSONLibrary) -> None:
        self.songs = pd.DataFrame(
            [vars(x) for x in json_library.songs.values()]
        )
        self.albums = pd.DataFrame(
            [vars(x) for x in json_library.albums.values()]
        )
        self.artists = pd.DataFrame(
            [vars(x) for x in json_library.artists.values()]
        )

    def get_album_songs(self, album_id: Album.AlbumId_Type) \
            -> List[Song.SongId_Type]:
        return list(self.songs[self.songs["album_id"] == album_id]["song_id"])

    def songs_by_decades(self) -> Dict[int, List[Song.SongId_Type]]:
        songs_by_decades_dict = {}
        albums = self.albums
        albums["decade"] = \
            albums["release_date"].apply(lambda x: x.year - (x.year % 10))
        for decade in sorted(albums["decade"].unique()):
            songs_by_decades_dict[decade] = []
            for song_list in albums[albums["decade"] == decade]["songs"]:
                songs_by_decades_dict[decade].extend(song_list)

        return songs_by_decades_dict