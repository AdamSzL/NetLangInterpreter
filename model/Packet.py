from enum import Enum

from interpreter.errors import NetLangRuntimeError
from model.base import NetLangObject


class Protocol(Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"


class Packet(NetLangObject):
    allowed_fields = {"payload", "protocol", "size"}

    def __init__(
        self,
        payload: str,
        protocol: str = Protocol.ICMP,
        size: int = 500
    ):
        self.payload = payload
        self.protocol = protocol
        self.size = size

    @classmethod
    def from_dict(cls, data: dict, ctx=None):
        cls.check_fields(data, ctx)

        payload = data.get("payload")
        protocol = data.get("protocol")
        size = data.get("size")

        if not isinstance(payload, str):
            raise NetLangRuntimeError(
                message="Packet payload must be a string",
                ctx=ctx
            )

        if not isinstance(protocol, Protocol):
            raise NetLangRuntimeError(
                message="Packet protocol must be a Protocol enum",
                ctx=ctx
            )

        if not isinstance(size, int):
            raise NetLangRuntimeError(
                message="Packet size must be an integer",
                ctx=ctx
            )

        return cls(payload, protocol, size)

    def __repr__(self):
        return f'Packet("{self.payload}", {self.protocol.name}, {self.size}B)'