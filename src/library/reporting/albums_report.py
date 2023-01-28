import os
import matplotlib.pyplot as plt

from library.dataframe_library import DataFrameLibrary
from library.reporting.html_report import HTMLReport


class AlbumsReport:
    def __init__(self, library: DataFrameLibrary, report: HTMLReport) -> None:
        self._library = library
        self.report = report
        self._calculate_decade_hist()

    def _calculate_decade_hist(self) -> None:
        decade_data = self._library.albums["release_date"] \
            .apply(lambda x: x.year - (x.year % 10)) \
            .value_counts() \
            .rename_axis("decade") \
            .to_frame("count") \
            .reset_index()
        decade_data.sort_values(by="decade", inplace=True)
        plt.step(
            decade_data["decade"],
            decade_data["count"],
            where="mid"
        )
        plt.xticks(decade_data["decade"])
        plt.xlabel("Decade")
        plt.ylabel("Count")
        plt.xlim(
            left=min(decade_data["decade"]) - 10,
            right=max(decade_data["decade"]) + 10
        )
        plt.title("Album Decade Histogram")
        plt.savefig(os.path.join(".", "out", "decade_count.png"))
        plt.clf()
        self.report.add_image("Album Decade Histogram", "decade_count.png")
