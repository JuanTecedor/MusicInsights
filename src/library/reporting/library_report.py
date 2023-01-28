import os
import matplotlib.pyplot as plt

from library.dataframe_library import DataFrameLibrary
from library.reporting.html_report import HTMLReport


class LibraryReport:
    def __init__(self, library: DataFrameLibrary, report: HTMLReport) -> None:
        self._library = library
        self.report = report
        self._counts()
        self._explicit_pie_chart()

    def _counts(self) -> None:
        self.report.add_count("Song count", len(self._library.songs))
        self.report.add_count("Album count", len(self._library.albums))
        self.report.add_count("Artist count", len(self._library.artists))

    def _explicit_pie_chart(self) -> None:
        labels = ["Explicit", "Non-Explicit"]
        explicit_count \
            = len(self._library.songs[self._library.songs["explicit"]])
        sizes = [explicit_count, len(self._library.songs) - explicit_count]
        plt.pie(sizes, labels=labels, autopct="%1.1f%%")
        plt.axis("equal")
        plt.savefig(os.path.join(".", "out", "explicit_pie.png"))
        plt.clf()
        self.report.add_image("Explicit Pie", "explicit_pie.png")
