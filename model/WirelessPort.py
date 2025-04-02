from interpreter.errors import NetLangRuntimeError
from model.CIDR import CIDR
from model.MACAddress import MACAddress
from model.base import NetLangObject


class WirelessPort(NetLangObject):
    allowed_fields = {"portId", "ip", "mac", "bandwidth", "mtu", "frequency"}

    def __init__(self, port_id: str, ip: CIDR = None, mac: MACAddress = None, bandwidth: int = 150, mtu: int = 1500, frequency: float = 2.4):
        self.portId = port_id
        self.ip = ip
        self.mac = mac or MACAddress.generate()
        self.bandwidth = bandwidth
        self.mtu = mtu
        self.frequency = frequency
        self.connectedTo = None

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

        if mac is not None:
            if not isinstance(mac, MACAddress):
                raise NetLangRuntimeError("Invalid MAC address", ctx=ctx)
            if MACAddress.is_registered(mac.mac):
                raise NetLangRuntimeError(message=f"MAC address {mac.mac} is already in use", ctx=ctx)
            MACAddress.register(mac.mac)

        if not isinstance(bandwidth, int) or not isinstance(mtu, int) or not isinstance(frequency, float):
            raise NetLangRuntimeError("Bandwidth and MTU must be integers, frequency must be float", ctx=ctx)

        return cls(portId, ip, mac, bandwidth, mtu, frequency)

    def __repr__(self):
        return f"{self.portId} ({self.mac or 'None'}, {self.ip or 'None'}, {self.bandwidth}Mbps, {self.frequency}GHz, {self.mtu}B)"
