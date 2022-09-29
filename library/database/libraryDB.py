import pandas as pd

from library.library import Library


class LibraryDB:
    def __init__(self):
        self.artists = pd.DataFrame()
        self.albums = pd.DataFrame()
        self.songs = pd.DataFrame()

    def add_artists(self, library: Library):
        data = []
        for artist in library.artists.values():
            row = [artist.artist_id, artist.name, artist.artist_type]
            data.append(row)
        self.artists = pd.DataFrame(data, columns=["id", "name", "type"])

    def add_albums(self, library: Library):
        data = []
        for album in library.albums.values():
            row = [album.album_id, album.album_type, album.artists,
                   album.name, album.release_date, album.release_date_precision,
                   album.songs, album.total_tracks]
            data.append(row)
        self.albums = pd.DataFrame(data, columns=["id", "type", "artists",
                                                  "name", "release_date", "release_date_precission",
                                                  "songs", "total_tracks"])

    def add_songs(self, library: Library):
        data = []
        for song in library.songs.values():
            row = [song.song_id, song.added_at, song.artists, song.duration_ms,
                   song.explicit, song.name, song.popularity, song.track_number,
                   song.is_local, song.album_id, song.disc_number, song.song_type]
            data.append(row)
        self.songs = pd.DataFrame(data, columns=[
            "id", "added_at", "artists", "duration_ms",
            "explicit", "name", "popularity", "track_number",
            "is_local", "album_id", "disc_number", "song_type"
        ])

    def output_to_file(self):
        html_str = """
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
            {}
        </body>
        </html>
        """
        tables = self.songs.sort_values("popularity").to_html(index=False)
        html_str = html_str.format(tables)
        with open("out/index.html", "w") as file:
            file.write(html_str)
