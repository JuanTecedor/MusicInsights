from typing import Any, Iterator


def split_list_in_chunks(data: list[Any], max_size: int) \
        -> Iterator[list[Any]]:
    for i in range(0, len(data), max_size):
        yield data[i:i + max_size]
