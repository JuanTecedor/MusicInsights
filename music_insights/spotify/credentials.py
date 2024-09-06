from typing import Optional, Final


class InvalidClientIdException(Exception):
    pass


client_id: Final[Optional[str]] = None
