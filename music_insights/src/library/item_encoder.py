from datetime import datetime
from typing import Any, Dict, List, Union
from attr import define


JSON_Types = Union[str, int, List, Dict, bool, None]


class JSONEncoder():
    @staticmethod
    def to_json(value: Any) -> JSON_Types:
        if isinstance(value, JSON_Types):
            return value
        elif isinstance(value, datetime):
            return value.isoformat()
        else:
            TypeError()
