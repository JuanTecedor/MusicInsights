from pytest import fixture

from music_insights.library.artist import Artist


@fixture
def example_album() -> Artist:
    return Artist(
        name="artist_name",
        artist_id="artistid",
        followers=11,
        genres=["genre1", "genre2"],
        popularity=21
    )


class TestAlbum:
    def test_serialization(self, example_album: Artist):
        deserialized = Artist.from_json_dict(example_album.to_json_dict())
        assert example_album == deserialized
