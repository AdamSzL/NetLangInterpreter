from dataclasses import dataclass
from typing import Optional

from shared.model import IPAddress
from shared.model.CIDR import CIDR
from shared.model.base import NetLangObject


@dataclass
class RoutingEntry(NetLangObject):
    destination: CIDR
    via: str
    nextHop: Optional[IPAddress] = None

    @classmethod
    def from_dict(cls, data: dict, ctx):
        destination = data.get("destination")
        via = data.get("via")
        nextHop = data.get("nextHop")

        return RoutingEntry(destination, via, nextHop)