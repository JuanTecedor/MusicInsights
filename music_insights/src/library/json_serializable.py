from abc import ABC, abstractmethod
from typing import Type


class JSONSerializable(ABC):
    @abstractmethod
    def to_json_str(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def from_json_str(data: str) -> Type:
        pass
