from dataclasses import dataclass
from enum import Enum

from shared.errors import NetLangRuntimeError
from shared.model.base import NetLangObject


class Protocol(Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"

@dataclass
class Packet(NetLangObject):
    payload: str
    protocol: str = Protocol.ICMP
    size: int = 500

    @classmethod
    def from_dict(cls, data: dict, ctx):
        payload = data.get("payload")
        protocol = data.get("protocol")
        size = data.get("size")

        return cls(payload, protocol, size)