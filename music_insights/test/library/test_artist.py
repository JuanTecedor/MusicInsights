from pytest import fixture

from music_insights.library.artist import Artist


@fixture
def example_artist() -> Artist:
    return Artist(
        name="artist_name",
        artist_id="artistid",
        followers=11,
        genres=["genre1", "genre2"],
        popularity=21
    )


class TestAlbum:
    def test_serialization(self, example_artist: Artist):
        deserialized = Artist.from_json_dict(example_artist.to_json_dict())
        assert example_artist == deserialized
