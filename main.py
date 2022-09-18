import argparse

from library.library import Library
from library.libraryView import LibraryView
from spotifyAuthenticator import SpotifyAuthenticator, AccessTokenNotFoundException
from spotifyClient import SpotifyClient, SpotifyClientWrongResponseStatusCode


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--download_and_save_library", action="store_true")
    return parser.parse_args()


def download_and_save_library():
    try:
        token = SpotifyAuthenticator().authenticate()
    except AccessTokenNotFoundException as ex:
        print(ex)
        exit(-1)
    spotify_client = SpotifyClient(token)
    try:
        library = spotify_client.download_library()
        library.save_to_file()
    except SpotifyClientWrongResponseStatusCode as ex:
        print(ex)
        exit(-2)


if __name__ == "__main__":
    arguments = parse_arguments()
    if arguments.download_and_save_library:
        download_and_save_library()

    library = Library()
    library.load_from_files()

    library_view = LibraryView()
    print(f"{library_view.explicit_percentage(library)=}")
    print(f"{library_view.top_n_artists_by_liked_songs(library, reverse=True)=}")  # TODO fix representation
    print(f"{library_view.albums_ordered_by_year(library, reverse=False)=}")  # TODO fix representation

    print("Done. Do not forget to deauthorize the app in https://www.spotify.com/account/apps/")
