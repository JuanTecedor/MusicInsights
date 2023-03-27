from music_insights.library.song import Song
from pytest import fixture


@fixture
def example_song() -> Song:
    return Song(
        song_id="song_id",
        added_at="2023-01-26T23:47:21Z",
        artists=["artist_id_1", "artist_id_2"],
        duration_ms=185000,
        explicit=True,
        name="track_name",
        popularity=40,
        track_number=2,
        album_id="album_id",
        disc_number=4,
        is_local=False
    )


class TestSong:
    def test_serialization(self, example_song: Song):
        deserialized = Song.from_json_dict(example_song.to_json_dict())
        assert example_song == deserialized
