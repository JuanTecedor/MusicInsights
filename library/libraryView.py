from library.library import Library


class LibraryView:
    @staticmethod
    def _take_n_first_from_dict(dictionary: dict, n: int):
        return {k: dictionary[k] for k in list(dictionary)[:n]}

    @staticmethod
    def explicit_proportion(library: Library) -> float:
        explicit_count = 0
        for song_data in library.songs.values():
            if song_data.explicit:
                explicit_count += 1
        return explicit_count / len(library.songs)

    @staticmethod
    def top_n_artists_by_liked_songs(library: Library, n=10, reverse=False):
        artist_songs_count = {}
        for song_data in library.songs.values():
            for artist_id in song_data.artists:
                artist_name = library.artists[artist_id].name
                if artist_name not in artist_songs_count:
                    artist_songs_count[artist_name] = 1
                else:
                    artist_songs_count[artist_name] += 1
        artist_songs_count = {k: v for k, v in sorted(
            artist_songs_count.items(), key=lambda item: item[1], reverse=reverse
        )}
        return LibraryView._take_n_first_from_dict(artist_songs_count, n)

    @staticmethod
    def albums_ordered_by_year(library: Library, reverse=False):
        return {v.name: v.release_date for k, v in sorted(
            library.albums.items(), key=lambda item: item[1].release_date, reverse=reverse
        )}
