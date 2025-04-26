from typing import Any

from interpreter.errors import NetLangRuntimeError
from model.CIDR import CIDR
from model.MACAddress import MACAddress
from model.Port import Port
from model.base import NetLangObject
from dataclasses import dataclass

@dataclass
class WirelessPort(NetLangObject, Port):
    allowed_fields = {"portId", "ip", "mac", "bandwidth", "mtu", "frequency"}

    portId: str
    ip: CIDR
    mac: MACAddress
    bandwidth: int = 150
    mtu: int = 1500
    frequency: float = 2.4
    connectedTo: Any = None

    @classmethod
    def from_dict(cls, data: dict, ctx=None):
        cls.check_fields(data, ctx)

        portId = data.get("portId")
        ip = data.get("ip")
        mac = data.get("mac")
        bandwidth = data.get("bandwidth", 150)
        mtu = data.get("mtu", 1500)
        frequency = data.get("frequency", 2.4)

        if not isinstance(portId, str):
            raise NetLangRuntimeError("WirelessPort must have string portId", ctx=ctx)

        if ip is not None and not isinstance(ip, CIDR):
            raise NetLangRuntimeError("Invalid IP for WirelessPort", ctx=ctx)

        if mac is None:
            mac = MACAddress.generate()
        else:
            if not isinstance(mac, MACAddress):
                raise NetLangRuntimeError("Invalid MAC address", ctx=ctx)
            if MACAddress.is_registered(mac.mac):
                raise NetLangRuntimeError(message=f"MAC address {mac.mac} is already in use", ctx=ctx)
            MACAddress.register(mac.mac)

        if not isinstance(bandwidth, int):
            raise NetLangRuntimeError("Bandwidth must be an integer", ctx=ctx)

        if not isinstance(mtu, int):
            raise NetLangRuntimeError("MTU must be an integer", ctx=ctx)

        if not isinstance(frequency, float):
            raise NetLangRuntimeError("Frequency must be a float", ctx=ctx)

        return cls(portId, ip, mac, bandwidth, mtu, frequency)