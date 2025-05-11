from typing import Any

from shared.errors import NetLangRuntimeError
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
    allowed_fields = {"portId", "ip", "mac", "bandwidth", "wavelength", "mtu", "connector"}

    portId: str
    ip: CIDR
    mac: MACAddress
    bandwidth: int = 10000
    wavelength: int = 1310
    mtu: int = 1500
    connector: str = ConnectorType.LC
    connectedTo: Any = None

    @classmethod
    def from_dict(cls, data: dict, ctx=None):
        cls.check_fields(data, ctx)

        portId = data.get("portId")
        ip = data.get("ip")
        mac = data.get("mac")
        bandwidth = data.get("bandwidth", 10000)
        wavelength = data.get("wavelength", 1310)
        mtu = data.get("mtu", 1500)
        connector = data.get("connector", ConnectorType.LC)

        if not isinstance(portId, str):
            raise NetLangRuntimeError("OpticalEthernetPort must have string portId", ctx)

        if ip is not None and not isinstance(ip, CIDR):
            raise NetLangRuntimeError("Invalid ip for OpticalEthernetPort", ctx)

        if mac is None:
            mac = MACAddress.generate()
        else:
            if not isinstance(mac, MACAddress):
                raise NetLangRuntimeError("Invalid MAC address", ctx)
            if MACAddress.is_registered(mac.mac):
                raise NetLangRuntimeError(f"MAC address {mac.mac} is already in use", ctx)
            MACAddress.register(mac.mac)

        if not isinstance(bandwidth, int):
            raise NetLangRuntimeError("Bandwidth must be an integer", ctx)

        if not isinstance(wavelength, int):
            raise NetLangRuntimeError("Wavelength must be an integer", ctx)

        if not isinstance(connector, ConnectorType):
            raise NetLangRuntimeError(
                "Invalid connector type",
                ctx
            )

        return cls(portId, ip, mac, bandwidth, wavelength, mtu, connector)


    def __hash__(self):
        return hash(self.mac)

    def __eq__(self, other):
        return isinstance(other, OpticalEthernetPort) and self.mac == other.mac
