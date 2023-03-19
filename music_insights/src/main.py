from argument_parser import get_parser_args
from library.library_reader import LibraryReaderChain


# def create_playlists_by_decades(library: DataFrameLibrary) -> None:
#     songs_by_decades = library.songs_by_decades()
#     token = SpotifyAuthenticator() \
#         .authenticate([
#             SpotifyAuthenticator.AvailableScopes.PLAYLIST_MODIFY_PRIVATE,
#             SpotifyAuthenticator.AvailableScopes.PLAYLIST_READ_PRIVATE
#         ])
#     spotify_client = SpotifyClient(token)
#     for decade, song_ids in songs_by_decades.items():
#         spotify_client.create_playlist(str(decade), song_ids


if __name__ == "__main__":
    arguments = get_parser_args()
    if arguments.force_download:
        library = LibraryReaderChain.force_download().get_library()
    else:
        library = LibraryReaderChain.default().get_library()
    library.save_to_file()

    # if arguments.create_playlists_by_decades:
    #     df_library = get_df_library()

    #     if arguments.create_playlists_by_decades:
    #         create_playlists_by_decades(df_library)

    #     if arguments.create_report:
    #         create_report(df_library)
