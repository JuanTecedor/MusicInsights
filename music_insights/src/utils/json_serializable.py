from abc import ABC
from datetime import datetime, date
from typing import Any, Dict, List, Self, TypeVar


class JSONSerializable(ABC):
    JSON_Types = str | int | List | Dict | bool | None

    @staticmethod
    def _to_json(value: Any) -> JSON_Types:
        if isinstance(value, JSONSerializable.JSON_Types):
            return value
        elif isinstance(value, datetime) or isinstance(value, date):
            return value.isoformat()
        else:
            TypeError(f"The type {type(value)} is not serializable.")

    def to_json_dict(self: Any) -> Dict[JSON_Types, JSON_Types]:
        return {
            variable_name: JSONSerializable._to_json(variable_value)
            for variable_name, variable_value
            in vars(self).items()
        }

    @classmethod
    def from_json_dict(cls, data: Dict[JSON_Types, JSON_Types]) -> Self:
        return cls(**data)


JSONSerializableSubClass = TypeVar(
    "JSONSerializableSubClass",
    bound=JSONSerializable
)
