from typing import Any, Iterator, List


def split_list_in_chunks(data: List[Any], max_size: int) \
        -> Iterator[List[List[Any]]]:
    for i in range(0, len(data), max_size):
        yield data[i:i + max_size]
