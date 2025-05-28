from dataclasses import dataclass

from shared.errors import NetLangRuntimeError
from shared.model.CIDR import CIDR
from shared.model.base import NetLangObject


@dataclass
class RoutingEntry(NetLangObject):
    destination: CIDR
    via: str

    @classmethod
    def from_dict(cls, data: dict, ctx):
        destination = data.get("destination")
        via = data.get("via")

        return RoutingEntry(destination, via)