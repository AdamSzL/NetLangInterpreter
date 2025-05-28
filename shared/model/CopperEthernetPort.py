from typing import Any

from shared.errors import NetLangRuntimeError
from shared.model.CIDR import CIDR
from shared.model.MACAddress import MACAddress
from shared.model.Port import Port
from shared.model.base import NetLangObject
from dataclasses import dataclass


@dataclass
class CopperEthernetPort(NetLangObject, Port):
    portId: str
    ip: CIDR
    mac: MACAddress
    bandwidth: int = 100
    mtu: int = 1500
    connectedTo: Any = None

    @classmethod
    def from_dict(cls, data: dict, ctx):
        port_id = data.get("portId")
        ip = data.get("ip")
        mac = data.get("mac")
        bandwidth = data.get("bandwidth", 100)
        mtu = data.get("mtu", 1500)

        if mac is None:
            mac = MACAddress.generate()
        else:
            if MACAddress.is_registered(mac.mac):
                raise NetLangRuntimeError(f"MAC address {mac.mac} is already in use", ctx)
            MACAddress.register(mac.mac)

        return cls(port_id, ip, mac, bandwidth, mtu)

    def __hash__(self):
        return hash(self.mac)

    def __eq__(self, other):
        return isinstance(other, CopperEthernetPort) and self.mac == other.mac
