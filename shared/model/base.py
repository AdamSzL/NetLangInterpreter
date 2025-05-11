from abc import ABC, abstractmethod
from typing import ClassVar

from shared.errors import NetLangRuntimeError


class NetLangObject(ABC):
    allowed_fields: ClassVar[set[str]] = set()

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict, ctx):
        ...

    @classmethod
    def check_fields(cls, data: dict, ctx):
        unknown = set(data.keys()) - cls.allowed_fields
        if unknown:
            raise NetLangRuntimeError(
                f"Unknown field(s) for {cls.__name__}: {', '.join(unknown)}",
                ctx
            )