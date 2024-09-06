import sys

from music_insights.argument_parser import get_parser_args
from music_insights.library.library_reader import (LibraryReaderFromAPI,
                                                   LibraryReaderFromFile)
from music_insights.spotify.spotify_client import SpotifyClient


def main(argv=None):
    arguments = get_parser_args(argv)

    if arguments.src == "api":
        library_reader = LibraryReaderFromAPI()
    elif arguments.src == "file":
        library_reader = LibraryReaderFromFile()
    else:
        assert False, "Should be unreachable"

    library = library_reader.get_library()

    if arguments.json:
        library.save_to_file()

    if arguments.create_playlists:
        songs_by_decades = sorted(library.get_songs_by_decades().items())
        client = SpotifyClient.read_write_playlist_client()
        for decade, songs in songs_by_decades:
            client.create_playlist(str(decade), songs)


if __name__ == "__main__":
    sys.exit(main())
