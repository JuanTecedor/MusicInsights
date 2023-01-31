import os
from typing import Any, List, Tuple


class HTMLReport:
    def __init__(self) -> None:
        self._start_str = """
        <!DOCTYPE html>
        <html>
        <head>
        </head>

        <style>
        html {
            display: flex;
            justify-content: center;
            font-family: Arial;
            margin-left: auto;
            margin-right: auto;
            margin: auto;
            align-items: center;
        }
        table, th, td {
            border: 1px solid;
        }
        table {
            border-collapse: collapse;
            margin-left: auto;
            margin-right: auto;
        }
        </style>

        <body>
        """
        self._body_str = ""
        self._end_str = """
        </body>
        </html>
        """

    def add_image(self, image_name: str, file_name: str) -> None:
        self._body_str += f"""
        <div>
            <h2>{image_name}</h2>
            <img src={file_name} alt={file_name}>
        </div>
        """

    def add_table(self, table_title: str, table: List[Tuple[Any, Any]]) \
            -> None:
        self._body_str += f"""
        <h2>{table_title}</h2>
        <div>
            <table>
        """
        for a, b in table:
            self._body_str += f"""
            <tr>
                <td>{a}</td>
                <td>{b}</td>
            </tr>
            """
        self._body_str += """
                </tr>
            </table>
        </div>
        """

    def output_to_file(self) -> None:
        with open(os.path.join("out", "index.html"), "w") as file:
            file.write(self._start_str)
            file.write(self._body_str)
            file.write(self._end_str)
