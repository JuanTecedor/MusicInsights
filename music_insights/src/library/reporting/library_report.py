from library.dataframe_library import DataFrameLibrary
from library.reporting.html_report import HTMLReport


class LibraryReport:
    def __init__(self, library: DataFrameLibrary, report: HTMLReport) -> None:
        self._library = library
        self.report = report
        self._counts()

    def _counts(self) -> None:
        self.report.add_table(
            "Library Counts",
            [
                ("Songs", len(self._library.songs)),
                ("Albums", len(self._library.albums)),
                ("Artists", len(self._library.artists))
            ]
        )
