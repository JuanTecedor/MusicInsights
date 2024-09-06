from typing import Final, Optional


class InvalidClientIdException(Exception):
    pass


client_id: Final[Optional[str]] = None
