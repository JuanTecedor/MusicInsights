from abc import ABC
import json
from typing import Dict, Self, Type

import attrs
from attrs import asdict

from library.item_encoder import JSON_Types, JSONEncoder


class AttrSerialization(ABC):
    def to_json_dict(self: attrs.AttrsInstance) -> Dict[JSON_Types, JSON_Types]:
        if not attrs.has(self):
            raise TypeError(
                "Only attrs classes can be serialized."
            )
        return {
            k: JSONEncoder.to_json(v)
            for k, v
            in asdict(self).items()
        }

    @classmethod
    def from_json_dict(cls, data: Dict[str, JSON_Types]) -> Self:
        return cls(**data)