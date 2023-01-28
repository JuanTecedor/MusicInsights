from collections import Counter

from library.dataframe_library import DataFrameLibrary
from library.reporting.html_report import HTMLReport


class ArtistReport:
    def __init__(self, library: DataFrameLibrary, report: HTMLReport) -> None:
        self._library = library
        self.report = report
        self._top_artists()

    def _top_artists(self) -> None:
        artists_names = [
            self._library.get_artist_by_id(artist)
            for song in self._library.songs["artists"]
            for artist in song
        ]
        self.report.add_table(
            "Top Artists by Song Count",
            Counter(artists_names).most_common(50)
        )
