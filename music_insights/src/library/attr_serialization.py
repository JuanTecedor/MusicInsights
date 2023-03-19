from abc import ABC
from typing import Dict, Self

import attrs
from attrs import asdict

from library.item_encoder import JSONEncoder


class AttrSerialization(ABC):
    def to_json_dict(self: attrs.AttrsInstance) \
            -> Dict[JSONEncoder.JSON_Types, JSONEncoder.JSON_Types]:
        if not attrs.has(self):  # type: ignore
            raise TypeError(
                "Only attrs classes can be serialized."
            )
        return {
            k: JSONEncoder.to_json(v)
            for k, v
            in asdict(self).items()
        }

    @classmethod
    def from_json_dict(cls, data: Dict[str, JSONEncoder.JSON_Types]) -> Self:
        return cls(**data)
