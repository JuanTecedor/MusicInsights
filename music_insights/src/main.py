from argument_parser import get_parser_args
from library.library_reader import LibraryReaderChain
from spotify.spotifyClient import SpotifyClient

if __name__ == "__main__":
    arguments = get_parser_args()
    if arguments.force_download:
        library = LibraryReaderChain.only_api().get_library()
    else:
        library = LibraryReaderChain.default().get_library()
    library.save_to_file()

    if arguments.create_playlists_by_decades:
        if arguments.create_playlists_by_decades:
            songs_by_decades = sorted(library.get_songs_by_decades().items())
            client = SpotifyClient.read_write_playlist_client()
            for decade, songs in songs_by_decades:
                client.create_playlist(str(decade), songs)
