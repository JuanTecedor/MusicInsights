import argparse


def get_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download_and_save_library", action="store_true")
    parser.add_argument("--create_playlists_by_decades", action="store_true")
    parser.add_argument("--create_report", action="store_true")
    return parser.parse_args()
