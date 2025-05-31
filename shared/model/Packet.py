from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from shared.errors import NetLangRuntimeError
from shared.model import IPAddress, CIDR
from shared.model.Port import Port
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
    source: Optional[Port] = field(default=None, init=False)
    destination: Optional[IPAddress] = field(default=None, init=False)

    @classmethod
    def from_dict(cls, data: dict, ctx):
        payload = data.get("payload")
        protocol = data.get("protocol")
        size = data.get("size")

        return cls(payload, protocol, size)