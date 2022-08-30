from library.library import Library
from spotifyAuthenticator import SpotifyAuthenticator, AccessTokenNotFoundException
from spotifyClient import SpotifyClient


if __name__ == "__main__":
    # try:
    #     token = SpotifyAuthenticator().authenticate()
    # except AccessTokenNotFoundException as ex:
    #     print(ex)
    #     exit(-1)
    # spotify_client = SpotifyClient(token)
    # spotify_client.download_library()
    library = Library()
    library.load_from_files()

    explicit_count = 0
    for song_data in library.songs.values():
        if song_data.explicit:
            explicit_count += 1
    print(f"{explicit_count=} {len(library.songs)=} {explicit_count / len(library.songs) * 100=}")

    artist_songs_count = {}
    for song_data in library.songs.values():
        artist_ids = song_data.artists
        if isinstance(artist_ids, str):
            artist_ids = [artist_ids]

        for artist_id in artist_ids:
            artist_name = library.artists[artist_id].name

        if artist_name not in artist_songs_count:
            artist_songs_count[artist_name] = 1
        else:
            artist_songs_count[artist_name] += 1
    artist_songs_count = {k: v for k, v in sorted(artist_songs_count.items(),
                                                  key=lambda item: item[1], reverse=True)}

    albums_ordered_by_year = {k: v for k, v in sorted(library.albums.items(),
                                                      key=lambda item: item[1].release_date, reverse=True)}

    print("Done. Do not forget to deauthorize the app in https://www.spotify.com/account/apps/")
