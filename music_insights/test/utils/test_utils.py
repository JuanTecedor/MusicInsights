import pytest

from music_insights.utils.utils import split_list_in_chunks


def test_split_list_max_size_greater_than_elem():
    test_list = [1, 2, 3]
    assert list(split_list_in_chunks(test_list, 4)) == [[1, 2, 3]]


def test_split_list_5_elem():
    test_list = [1, 2, 3, 4, 5]
    assert list(split_list_in_chunks(test_list, 2)) == [[1, 2], [3, 4], [5]]


def test_split_list_zero_max_size():
    with pytest.raises(AssertionError):
        list(split_list_in_chunks([1, 2], 0))


def test_split_list_neg_max_size():
    with pytest.raises(AssertionError):
        list(split_list_in_chunks([1, 2], -5))
