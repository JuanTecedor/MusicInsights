from datetime import datetime
from json import JSONEncoder
from typing import Any


class ItemEncoder(JSONEncoder):
    def default(self, obj: Any) -> str:
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return JSONEncoder.default(self, obj)
