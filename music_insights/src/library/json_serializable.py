import json
from typing import Dict, Self, Type

import attrs
from attrs import asdict

from library.item_encoder import JSON_Types, JSONEncoder


class JSONSerializable:
    @staticmethod
    def to_json_dict(obj: attrs.AttrsInstance) -> Dict[JSON_Types, JSON_Types]:
        if not attrs.has(obj):
            raise TypeError(
                "Only attrs classes can be serialized."
            )
        return {
            k: JSONEncoder.to_json(v)
            for k, v
            in asdict(obj).items()
        }
    
    def to_json_str(self) -> str:
        return json.dumps(self.to_json_dict())
    
    @classmethod
    def from_json_str(cls, data_str: str) -> Self:
        return cls(**json.loads(data_str))
