import argparse


def get_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download_and_save_library", action="store_true")
    parser.add_argument("--load_from_file", action="store_true")
    return parser.parse_args()
