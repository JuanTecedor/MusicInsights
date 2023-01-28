import argparse

from library.dataframe_library import DataFrameLibrary
from library.json_library import JSONLibrary
from spotify.spotifyAuthenticator import SpotifyAuthenticator
from spotify.spotifyClient import SpotifyClient
from library.reporting.albums_report import AlbumsReport
from library.reporting.library_report import LibraryReport
from library.reporting.html_report import HTMLReport


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download_and_save_library", action="store_true")
    parser.add_argument("--create_playlists_by_decades", action="store_true")
    parser.add_argument("--create_report", action="store_true")
    return parser.parse_args()


def download_and_save_library() -> None:
    token = SpotifyAuthenticator() \
        .authenticate([SpotifyAuthenticator.AvailableScopes.USER_LIBRARY_READ])
    spotify_client = SpotifyClient(token)
    library_data = spotify_client.download_library_as_json()
    library_data.save_to_file()


def create_playlists_by_decades(library: DataFrameLibrary) -> None:
    songs_by_decades = library.songs_by_decades()
    token = SpotifyAuthenticator() \
        .authenticate([
            SpotifyAuthenticator.AvailableScopes.PLAYLIST_MODIFY_PRIVATE,
            SpotifyAuthenticator.AvailableScopes.PLAYLIST_READ_PRIVATE
        ])
    spotify_client = SpotifyClient(token)
    for decade, song_ids in songs_by_decades.items():
        spotify_client.create_playlist(str(decade), song_ids)


def create_report(library: DataFrameLibrary) -> None:
    html_report = HTMLReport()
    LibraryReport(library, html_report)
    AlbumsReport(library, html_report)
    html_report.output_to_file()


if __name__ == "__main__":
    arguments = parse_arguments()

    if arguments.download_and_save_library:
        download_and_save_library()

    if arguments.create_playlists_by_decades or arguments.create_report:
        json_library = JSONLibrary()
        json_library.load_from_files()
        df_library = DataFrameLibrary(json_library)

        if arguments.create_playlists_by_decades:
            create_playlists_by_decades(df_library)

        if arguments.create_report:
            create_report(df_library)
