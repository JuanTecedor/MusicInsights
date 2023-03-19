import json
import sys

sys.path.append("src")

from pytest import fixture

from src.library.song import Song

@fixture
def example_song() -> Song:
    return Song(
        added_at="2023-01-26T23:47:21Z",
        song_id="song_id",
        album_id="album_id",
        popularity=40,
        track_number=2,
        duration_ms=185000,
        explicit=True,
        name="track_name",
        is_local=False,
        disc_number=4,
        artists=["artist_id_1", "artist_id_2"]
    )


def test_encode_songs(example_song):
    songs = [example_song] * 3
    s = json.dumps(songs, indent=4)
    pass


def test_serialize_song(example_song):
    assert example_song.to_json_str() \
        == '{"song_id": "song_id", "added_at": "2023-01-26T23:47:21+00:00",' \
        ' "artists": ["artist_id_1", "artist_id_2"], "duration_ms": 185000,' \
        ' "explicit": true, "name": "track_name", "popularity": 40, ' \
        '"track_number": 2, "album_id": "album_id", "disc_number": 4, ' \
        '"is_local": false, "preview_url": ""}'


def test_deserialize_song(example_song):
    assert Song.from_json_str(example_song.to_json_str()) == example_song
