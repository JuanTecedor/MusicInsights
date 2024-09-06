from argparse import ArgumentError

import pytest

from music_insights.argument_parser import get_parser_args


@pytest.mark.parametrize(
    "input_args, valid",
    [
        ([], True),
        (["unknown_arg"], False),
        (["-s"], False),
        (["--src", "api"], True),
        (["--src", "unknown"], False),
    ]
)
def test_argparse(input_args: list[str], valid: bool) -> None:
    if valid:
        arguments = get_parser_args(input_args)
        assert getattr(arguments, "src") is not None
        assert getattr(arguments, "dir") is not None
        assert getattr(arguments, "create_playlists") is not None
        assert getattr(arguments, "json") is not None
    else:
        with pytest.raises((SystemExit, ArgumentError)):
            get_parser_args(input_args)


def test_defaults() -> None:
    arguments = get_parser_args([])
    assert arguments.src == "file"
    assert arguments.dir == "out"
    assert arguments.json
    assert not arguments.create_playlists
