from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from shared.errors import NetLangRuntimeError
from shared.model import IPAddress, CIDR
from shared.model.Port import Port
from shared.model.base import NetLangObject

@dataclass
class Packet(NetLangObject):
    payload: str
    source: Optional[Port] = field(default=None, init=False)
    destination_ip: Optional[IPAddress] = field(default=None, init=False)
    destination_mac: Optional[str] = field(default=None, init=False)

    @classmethod
    def from_dict(cls, data: dict, ctx):
        payload = data.get("payload")

        return cls(payload)