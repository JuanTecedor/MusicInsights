import pandas as pd
import matplotlib.pyplot as plt


class AlbumsReport:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
        self.decade_hist = self._calculate_decade_hist()

    def _calculate_decade_hist(self):
        decade_data = self.data["release_date"] \
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
        plt.show()
        pass  # TODO
