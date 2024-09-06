from unittest.mock import mock_open, patch

from pytest import fixture

from music_insights.library.album import Album
from music_insights.library.artist import Artist
from music_insights.library.library import Library
from music_insights.library.song import Song


@fixture
def example_song1() -> Song:
    return Song(
        song_id="song_id1",
        added_at="2023-01-26T23:47:21Z",
        artists=["artist_id_1", "artist_id_2"],
        duration_ms=185000,
        explicit=True,
        name="track_name",
        popularity=40,
        track_number=2,
        album_id="album_id1",
        disc_number=4,
        is_local=False
    )


@fixture
def example_song2() -> Song:
    return Song(
        song_id="song_id2",
        added_at="2023-01-26T23:47:21Z",
        artists=["artist_id_1", "artist_id_2"],
        duration_ms=185000,
        explicit=True,
        name="track_name",
        popularity=40,
        track_number=2,
        album_id="album_id2",
        disc_number=4,
        is_local=False
    )


@fixture
def example_album1() -> Album:
    return Album(
        artists=["artist_id"],
        album_id="album_id1",
        name="album_name",
        release_date="2030-01-01",
        release_date_precision="day",
        songs=["song_id1"],
        total_tracks=2,
        genres=["genre1", "genre2"],
        label="label1",
        popularity=10
    )


@fixture
def example_album2() -> Album:
    return Album(
        artists=["artist_id"],
        album_id="album_id2",
        name="album_name",
        release_date="2050-01-01",
        release_date_precision="day",
        songs=["song_id2"],
        total_tracks=2,
        genres=["genre1", "genre2"],
        label="label1",
        popularity=10
    )


@fixture
def example_artist() -> Artist:
    return Artist(
        name="artist_name",
        artist_id="artist_id",
        followers=11,
        genres=["genre1", "genre2"],
        popularity=21
    )


@fixture
def example_library(
    example_song1: Song,
    example_song2: Song,
    example_album1: Album,
    example_album2: Album,
    example_artist: Artist
) -> Library:
    return Library(
        {
            example_song1.song_id: example_song1,
            example_song2.song_id: example_song2
        },
        {
            example_album1.album_id: example_album1,
            example_album2.album_id: example_album2
        },
        {
            example_artist.artist_id: example_artist
        }
    )


class TestLibrary:
    def test_serialization(self, example_library: Library):
        mock = mock_open()
        with patch("music_insights.library.library.open", mock, create=True):
            example_library.save_to_file()
        assert mock.call_count == 3

    def test_songs_by_decades(self, example_library: Library):
        songs_by_decades = example_library.get_songs_by_decades()
        assert songs_by_decades == {2030: ["song_id1"], 2050: ["song_id2"]}
