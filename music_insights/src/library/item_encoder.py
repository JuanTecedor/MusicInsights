from datetime import datetime, date
from typing import Any, Dict, List, Union


class JSONEncoder():
    JSON_Types = Union[str, int, List, Dict, bool, None]

    @staticmethod
    def to_json(value: Any) -> JSON_Types:
        if isinstance(value, JSONEncoder.JSON_Types):
            return value
        elif isinstance(value, datetime) or isinstance(value, date):
            return value.isoformat()
        else:
            TypeError()
