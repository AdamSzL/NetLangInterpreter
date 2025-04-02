from interpreter.errors import NetLangRuntimeError
from model.MACAddress import MACAddress
from model.CIDR import CIDR
from enum import Enum

from model.base import NetLangObject

class ConnectorType(Enum):
    LC = "LC"
    SC = "SC"

class OpticalEthernetPort(NetLangObject):
    allowed_fields = {"portId", "ip", "mac", "bandwidth", "wavelength", "mtu", "connector"}

    def __init__(self, port_id: str, ip: CIDR | None, mac: MACAddress | None,
                 bandwidth: int = 10000, wavelength: int = 1310,
                 mtu: int = 1500, connector: str = ConnectorType.LC):
        self.portId = port_id
        self.ip = ip
        self.mac = mac or MACAddress.generate()
        self.bandwidth = bandwidth
        self.wavelength = wavelength
        self.mtu = mtu
        self.connector = connector
        self.connectedTo = None

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
            raise NetLangRuntimeError("OpticalEthernetPort must have string portId", ctx=ctx)

        if ip is not None and not isinstance(ip, CIDR):
            raise NetLangRuntimeError("Invalid ip for OpticalEthernetPort", ctx=ctx)

        if mac is not None:
            if not isinstance(mac, MACAddress):
                raise NetLangRuntimeError("Invalid MAC address", ctx=ctx)
            if MACAddress.is_registered(mac.mac):
                raise NetLangRuntimeError(message=f"MAC address {mac.mac} is already in use", ctx=ctx)
            MACAddress.register(mac.mac)

        if not isinstance(bandwidth, int) or not isinstance(mtu, int) or not isinstance(wavelength, int):
            raise NetLangRuntimeError("Bandwidth, MTU and wavelength must be integers", ctx=ctx)

        if not isinstance(connector, ConnectorType):
            raise NetLangRuntimeError(
                message="Invalid connector type",
                ctx=ctx
            )

        return cls(portId, ip, mac, bandwidth, wavelength, mtu, connector)

    def __repr__(self):
        return f"{self.portId} ({self.mac}, {self.ip}, {self.bandwidth}Mbps, {self.wavelength}nm, {self.mtu}B, {self.connector})"
