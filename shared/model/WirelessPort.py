from typing import Any

from shared.errors import NetLangRuntimeError
from shared.model.CIDR import CIDR
from shared.model.MACAddress import MACAddress
from shared.model.Port import Port
from shared.model.base import NetLangObject
from dataclasses import dataclass

@dataclass
class WirelessPort(NetLangObject, Port):
    portId: str
    ip: CIDR
    mac: MACAddress
    bandwidth: int = 150
    mtu: int = 1500
    frequency: float = 2.4
    connectedTo: Any = None

    @classmethod
    def from_dict(cls, data: dict, ctx=None):
        portId = data.get("portId")
        ip = data.get("ip")
        mac = data.get("mac")
        bandwidth = data.get("bandwidth", 150)
        mtu = data.get("mtu", 1500)
        frequency = data.get("frequency", 2.4)

        if mac is None:
            mac = MACAddress.generate()
        else:
            if MACAddress.is_registered(mac.mac):
                raise NetLangRuntimeError(f"MAC address {mac.mac} is already in use", ctx)
            MACAddress.register(mac.mac)

        return cls(portId, ip, mac, bandwidth, mtu, frequency)

    def __hash__(self):
        return hash(self.mac)

    def __eq__(self, other):
        return isinstance(other, WirelessPort) and self.mac == other.mac