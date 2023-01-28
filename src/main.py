from argument_parser import get_parser
from library.dataframe_library import DataFrameLibrary
from library.json_library import JSONLibrary
from library.reporting.albums_report import AlbumsReport
from library.reporting.artist_report import ArtistReport
from library.reporting.html_report import HTMLReport
from library.reporting.library_report import LibraryReport
from library.reporting.song_report import SongReport
from spotify.spotifyAuthenticator import SpotifyAuthenticator
from spotify.spotifyClient import SpotifyClient


class FileNotFoundException(Exception):
    pass


def download_and_save_library() -> None:
    token = SpotifyAuthenticator() \
        .authenticate([SpotifyAuthenticator.AvailableScopes.USER_LIBRARY_READ])
    spotify_client = SpotifyClient(token)
    library_data = spotify_client.download_library_as_json()
    library_data.save_to_file()


def get_df_library() -> DataFrameLibrary:
    json_library = JSONLibrary()
    try:
        json_library.load_from_files()
    except FileNotFoundError as file:
        raise FileNotFoundException(
            f"File {file} not found. First download the files."
        )
    return DataFrameLibrary(json_library)


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
    SongReport(library, html_report)
    ArtistReport(library, html_report)
    html_report.output_to_file()


if __name__ == "__main__":
    arguments = get_parser()

    if arguments.download_and_save_library:
        download_and_save_library()

    if arguments.create_playlists_by_decades or arguments.create_report:
        df_library = get_df_library()

        if arguments.create_playlists_by_decades:
            create_playlists_by_decades(df_library)

        if arguments.create_report:
            create_report(df_library)
