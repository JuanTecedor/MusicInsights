import pytest

from music_insights.argument_parser import get_parser_args


def test_create_playlists_args():
    arguments = get_parser_args(["--create_playlists_by_decades"])
    assert not arguments.force_download
    assert arguments.create_playlists_by_decades


def test_all_args():
    arguments = get_parser_args([
        "--force_download",
        "--create_playlists_by_decades"
    ])
    assert arguments.force_download
    assert arguments.create_playlists_by_decades


def test_create_playlists_force_download_args():
    arguments = get_parser_args(["--force_download"])
    assert arguments.force_download
    assert not arguments.create_playlists_by_decades


def test_create_playlists_no_args():
    arguments = get_parser_args([])
    assert not arguments.force_download
    assert not arguments.create_playlists_by_decades


def test_unknown_arg():
    with pytest.raises(SystemExit):
        get_parser_args(["--unknown"])
