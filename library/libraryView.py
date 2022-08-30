from library.library import Library


class LibraryView:
    def __init__(self, library: Library):
        self.library = library

    @staticmethod
    def _take_n_first_from_dict(dictionary: dict, n: int):
        return {k: dictionary[k] for k in list(dictionary)[:n]}

    def explicit_percentage(self):
        explicit_count = 0
        for song_data in self.library.songs.values():
            if song_data.explicit:
                explicit_count += 1
        return explicit_count / len(self.library.songs) * 100

    def top_n_artists_by_liked_songs(self, n=10, reverse=False):
        artist_songs_count = {}
        for song_data in self.library.songs.values():
            for artist_id in song_data.artists:
                artist_name = self.library.artists[artist_id].name
                if artist_name not in artist_songs_count:
                    artist_songs_count[artist_name] = 1
                else:
                    artist_songs_count[artist_name] += 1
        artist_songs_count = {k: v for k, v in sorted(
            artist_songs_count.items(), key=lambda item: item[1], reverse=reverse
        )}
        return self._take_n_first_from_dict(artist_songs_count, n)

    def albums_ordered_by_year(self, n=10, reverse=False):
        albums_ordered_by_year = {v.name: str(v.release_date) for k, v in sorted(
            self.library.albums.items(), key=lambda item: item[1].release_date, reverse=reverse
        )}
        return self._take_n_first_from_dict(albums_ordered_by_year, n)
