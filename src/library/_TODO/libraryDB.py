import os

import pandas as pd

from library.json_library import JSONLibrary


class LibraryDB:

    @staticmethod
    def _add_artists(library: JSONLibrary) -> pd.DataFrame:
        data = []
        for artist in library.artists.values():
            row = [artist.artist_id, artist.name, artist.artist_type]
            data.append(row)
        return pd.DataFrame(data, columns=["id", "name", "type"])

    @staticmethod
    def _add_albums(library: JSONLibrary) -> pd.DataFrame:
        data = []
        for album in library.albums.values():
            row = [album.album_id, album.album_type, album.artists,
                   album.name, album.release_date,
                   album.release_date_precision,
                   album.songs, album.total_tracks]
            data.append(row)
        return pd.DataFrame(data, columns=["id", "type", "artists", "name",
                                           "release_date",
                                           "release_date_precision", "songs",
                                           "total_tracks"])

    @staticmethod
    def _add_songs(library: JSONLibrary) -> pd.DataFrame:
        data = []
        for song in library.songs.values():
            row = [song.song_id, song.added_at, song.artists,
                   song.duration_ms, song.explicit, song.name,
                   song.popularity, song.track_number, song.is_local,
                   song.album_id, song.disc_number, song.song_type]
            data.append(row)
        return pd.DataFrame(data, columns=[
            "id", "added_at", "artists", "duration_ms",
            "explicit", "name", "popularity", "track_number",
            "is_local", "album_id", "disc_number", "song_type"
        ])

    @staticmethod
    def output_to_file(library: JSONLibrary) -> None:
        html_str = f"""
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
            <p>Number of songs: {len(library.songs)}</p>
            <p>Number of albums: {len(library.albums)}</p>
            <p>Number of artists: {len(library.artists)}</p>
            <p>Songs table:</p>
            {{}}
            <p>Albums table:</p>
            {{}}
            <p>Artists table:</p>
            {{}}
        </body>
        </html>
        """
        songs_table_html = LibraryDB._add_songs(library)\
            .sort_values("popularity").to_html(index=False)
        albums_table_html = LibraryDB._add_albums(library).to_html(index=False)
        artists_table_html = LibraryDB._add_artists(library)\
            .to_html(index=False)
        html_str = html_str.format(
            songs_table_html, albums_table_html, artists_table_html
        )
        with open(os.path.join("out", "index.html"), "w") as file:
            file.write(html_str)
