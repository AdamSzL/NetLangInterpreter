from abc import ABC, abstractmethod
from typing import ClassVar

from interpreter.errors import NetLangRuntimeError


class NetLangObject(ABC):
    allowed_fields: ClassVar[set[str]] = set()

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict, ctx=None):
        ...

    @classmethod
    def check_fields(cls, data: dict, ctx=None):
        unknown = set(data.keys()) - cls.allowed_fields
        if unknown:
            raise NetLangRuntimeError(
                message=f"Unknown field(s) for {cls.__name__}: {', '.join(unknown)}",
                ctx=ctx
            )