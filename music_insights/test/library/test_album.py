from pytest import fixture

from music_insights.library.album import Album


@fixture
def example_album() -> Album:
    return Album(
        artists=["artist1", "artist2"],
        album_id="album_id",
        name="album_name",
        release_date="2023-03-27",
        release_date_precision="day",
        songs=["song1", "song2"],
        total_tracks=2,
        genres=["genre1", "genre2"],
        label="label1",
        popularity=10
    )


class TestAlbum:
    def test_serialization(self, example_album: Album):
        deserialized = Album.from_json_dict(example_album.to_json_dict())
        assert example_album == deserialized
