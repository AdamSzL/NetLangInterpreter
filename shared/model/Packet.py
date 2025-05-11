from enum import Enum

from shared.errors import NetLangRuntimeError
from shared.model.base import NetLangObject


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
                "Packet payload must be a string",
                ctx
            )

        if not isinstance(protocol, Protocol):
            raise NetLangRuntimeError(
                "Packet protocol must be a Protocol enum",
                ctx
            )

        if not isinstance(size, int):
            raise NetLangRuntimeError(
                "Packet size must be an integer",
                ctx
            )

        return cls(payload, protocol, size)

    def __repr__(self):
        return f'Packet("{self.payload}", {self.protocol.name}, {self.size}B)'