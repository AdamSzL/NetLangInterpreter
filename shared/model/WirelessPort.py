from typing import Any, Optional

from shared.errors import NetLangRuntimeError
from shared.model import IPAddress
from shared.model.CIDR import CIDR
from shared.model.MACAddress import MACAddress
from shared.model.Port import Port
from shared.model.base import NetLangObject
from dataclasses import dataclass

@dataclass
class WirelessPort(NetLangObject, Port):
    bandwidth: int = 150
    frequency: float = 2.4

    @classmethod
    def from_dict(cls, data: dict, ctx=None):
        port_id, ip, mac, mtu, gateway = Port.base_from_dict(data, ctx)
        bandwidth = data.get("bandwidth", 150)
        frequency = data.get("frequency", 2.4)

        port = cls(port_id, ip, mac, mtu, None, gateway, bandwidth, frequency)
        port.validate_logic(ctx)
        return port

    def __hash__(self):
        return hash(self.mac)

    def __eq__(self, other):
        return isinstance(other, WirelessPort) and self.mac == other.mac