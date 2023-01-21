import argparse

from library.dataframe_library import DataFrameLibrary
from library.json_library import JSONLibrary
from spotify.spotifyAuthenticator import SpotifyAuthenticator
from spotify.spotifyClient import SpotifyClient
from library.reporting.albums_report import AlbumsReport


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download_and_save_library", action="store_true")
    parser.add_argument("--process_data", action="store_true")
    parser.add_argument("--create_playlists", action="store_true")
    return parser.parse_args()


def download_and_save_library() -> None:
    token = SpotifyAuthenticator() \
        .authenticate([SpotifyAuthenticator.AvailableScopes.USER_LIBRARY_READ])
    spotify_client = SpotifyClient(token)
    library_data = spotify_client.download_library()
    library_data.save_to_file()


def create_playlists(library: DataFrameLibrary) -> None:
    songs_by_decades = library.songs_by_decades()
    token = SpotifyAuthenticator() \
        .authenticate([
            SpotifyAuthenticator.AvailableScopes.PLAYLIST_MODIFY_PRIVATE,
            SpotifyAuthenticator.AvailableScopes.PLAYLIST_READ_PRIVATE
        ])
    spotify_client = SpotifyClient(token)
    for decade, song_ids in songs_by_decades.items():
        spotify_client.create_playlist(str(decade), song_ids)


if __name__ == "__main__":
    arguments = parse_arguments()
    if arguments.download_and_save_library:
        download_and_save_library()

    if arguments.process_data:
        json_library = JSONLibrary()
        json_library.load_from_files()
        df_library = DataFrameLibrary(json_library)
        albums_report = AlbumsReport(df_library.albums)
        if arguments.create_playlists:
            create_playlists(df_library)
