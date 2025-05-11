from dataclasses import dataclass

from shared.errors import NetLangRuntimeError
from shared.model.CIDR import CIDR
from shared.model.base import NetLangObject


@dataclass
class RoutingEntry(NetLangObject):
    allowed_fields = {"destination", "via"}
    destination: CIDR
    via: str

    @classmethod
    def from_dict(cls, data: dict, ctx=None):
        cls.check_fields(data, ctx)

        destination = data.get("destination")
        via = data.get("via")

        if not isinstance(destination, CIDR):
            raise NetLangRuntimeError(
                "RoutingEntry field 'destination' must be a CIDR object",
                ctx
            )

        if not isinstance(via, str):
            raise NetLangRuntimeError(
                "RoutingEntry field 'via' must be a string (portId)",
                ctx
            )

        return RoutingEntry(destination, via)



