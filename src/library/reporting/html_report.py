import os


class HTMLReport:
    def __init__(self) -> None:
        self._start_str = """
        <!DOCTYPE html>
        <html>
        <head>
        </head>

        <style>
        body
        {
            width:80%;
            margin-left:auto;
            margin-right:auto;
        }
        </style>

        <body>
        """
        self._body_str = ""
        self._end_str = """
        </body>
        </html>
        """

    def add_image(self, title: str, file_name: str):
        self._body_str += f"""
        <h2>{title}</h2>
        <img src={file_name} alt={file_name}>
        """

    def add_count(self, count_title: str, count: int):
        self._body_str += f"""
        <table>
            <tr>
                <td>{count_title}</td>
                <td>{count}</td>
            </tr>
        </table>
        """

    def output_to_file(self) -> None:
        with open(os.path.join("out", "index.html"), "w") as file:
            file.write(self._start_str)
            file.write(self._body_str)
            file.write(self._end_str)
