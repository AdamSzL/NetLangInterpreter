from abc import ABC, abstractmethod
from typing import ClassVar

from shared.errors import NetLangRuntimeError


class NetLangObject(ABC):
    allowed_fields: ClassVar[set[str]] = set()

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict, ctx):
        ...