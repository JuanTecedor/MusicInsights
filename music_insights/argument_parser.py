from argparse import ArgumentParser, Namespace


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "-s", "--src",
        choices=["api", "file"],
        help="Set the source from which to load the library.",
        default="file"
    )
    parser.add_argument(
        "-d", "--dir",
        required=False,
        help="Change the origin (when using the file as a source)"
             "and destination directory of the library.",
        default="out"
    )
    parser.add_argument(
        "-j", "--json",
        required=False,
        help="Specifies if the program should save "
             "a json file in the output directory.",
        default=True,
        action="store_true"
    )
    parser.add_argument(
        "-c", "--create_playlists",
        required=False,
        help="Specifies if the program should create playlists by decades.",
        default=False
    )
    return parser


def get_parser_args(argv) -> Namespace:
    return get_parser().parse_args(argv)
