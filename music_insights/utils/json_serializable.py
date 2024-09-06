from abc import ABC
from datetime import date, datetime
from typing import Any, TypeAlias, TypeVar, get_args

from typing_extensions import Self


class JSONSerializable(ABC):
    JSON_Types: TypeAlias = str | int | list | dict | bool | None

    @staticmethod
    def _to_json(value: Any) -> JSON_Types:
        if isinstance(value, get_args(JSONSerializable.JSON_Types)):
            return value
        elif isinstance(value, datetime) or isinstance(value, date):
            return value.isoformat()
        else:
            raise TypeError(f"The type {type(value)} is not serializable.")

    def to_json_dict(self: Any) -> dict[JSON_Types, JSON_Types]:
        return {
            variable_name: JSONSerializable._to_json(variable_value)
            for variable_name, variable_value
            in vars(self).items()
        }

    @classmethod
    def from_json_dict(cls, data: dict[str, JSON_Types]) -> Self:
        return cls(**data)


JSONSerializableSubClass = TypeVar(
    "JSONSerializableSubClass",
    bound=JSONSerializable
)
