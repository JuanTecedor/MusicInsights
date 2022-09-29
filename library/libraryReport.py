from library.library import Library
from library.libraryView import LibraryView


class LibraryReport:
    def __init__(self):
        self.report = "YOUR LIBRARY REPORT\n"

    def create_report(self, library: Library):
        self.report += f"Number of songs: {len(library.songs)}\n" \
                       f"Number of albums: {len(library.albums)}\n" \
                       f"Number of artists: {len(library.artists)}\n"
        self.report += "Explicit percentage: " + "{:.1%}".format(LibraryView.explicit_proportion(library))
        with open("out/report.txt", "w") as file:
            file.write(self.report)
