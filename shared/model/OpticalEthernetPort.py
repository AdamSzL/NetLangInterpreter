from typing import Any, Optional

from shared.errors import NetLangRuntimeError
from shared.model import IPAddress
from shared.model.MACAddress import MACAddress
from shared.model.CIDR import CIDR
from enum import Enum

from shared.model.Port import Port
from shared.model.base import NetLangObject
from dataclasses import dataclass

class ConnectorType(Enum):
    LC = "LC"
    SC = "SC"

@dataclass
class OpticalEthernetPort(NetLangObject, Port):
    bandwidth: int = 10000
    wavelength: int = 1310
    connector: str = ConnectorType.LC

    @classmethod
    def from_dict(cls, data: dict, ctx):
        port_id, ip, mac, mtu, gateway = Port.base_from_dict(data, ctx)
        bandwidth = data.get("bandwidth", 10000)
        wavelength = data.get("wavelength", 1310)
        connector = data.get("connector", ConnectorType.LC)

        port = cls(port_id, ip, mac, mtu, None, gateway, bandwidth, wavelength, connector)
        port.validate_logic(ctx)
        return port


    def __hash__(self):
        return hash(self.mac)

    def __eq__(self, other):
        return isinstance(other, OpticalEthernetPort) and self.mac == other.mac
