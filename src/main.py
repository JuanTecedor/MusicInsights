import argparse

from library.database.libraryDB import LibraryDB
from library.library import Library
from spotifyAuthenticator import SpotifyAuthenticator
from spotifyClient import SpotifyClient


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download_and_save_library", action="store_true")
    return parser.parse_args()


def download_and_save_library() -> None:
    token = SpotifyAuthenticator().authenticate()
    spotify_client = SpotifyClient(token)

    library_data = spotify_client.download_library()
    library_data.save_to_file()


if __name__ == "__main__":
    arguments = parse_arguments()
    if arguments.download_and_save_library:
        download_and_save_library()

    library = Library()
    library.load_from_files()

    libraryDB = LibraryDB()
    libraryDB.add_artists(library)
    libraryDB.add_albums(library)
    libraryDB.add_songs(library)
    libraryDB.output_to_file()

    print("Done. Do not forget to deauthorize the app in "
          "https://www.spotify.com/account/apps/")
