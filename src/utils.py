import re
from typing import Any, Iterator, List

class AccessTokenNotFoundException(Exception):
    pass


def extract_token_from_response(url_string_response: str) -> str:
    search = re.search("access_token=([^&]+)", url_string_response)
    if search is None:
        raise AccessTokenNotFoundException(
            "Unable to extract token from the URL"
        )
    return search.group(1)

def split_list_in_chunks(data: List[Any], max_size: int) -> Iterator[List[List[Any]]]:
    for i in range(0, len(data), max_size):
        yield data[i:i + max_size]
