import argparse


def get_parser_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--create_playlists", action="store_true")
    parser.add_argument("--force_download", action="store_true")
    return parser.parse_args()
