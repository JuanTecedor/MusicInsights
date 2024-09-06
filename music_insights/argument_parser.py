import argparse


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--create_playlists_by_decades", action="store_true")
    parser.add_argument("--force_download", action="store_true")
    return parser


def get_parser_args(argv) -> argparse.Namespace:
    return get_parser().parse_args(argv)
