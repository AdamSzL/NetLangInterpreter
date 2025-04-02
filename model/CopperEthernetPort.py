from interpreter.errors import NetLangRuntimeError
from model.CIDR import CIDR
from model.MACAddress import MACAddress
from model.base import NetLangObject

class CopperEthernetPort(NetLangObject):
    allowed_fields = {"portId", "ip", "mac", "bandwidth", "mtu"}

    def __init__(self, port_id: str, ip: CIDR = None, mac: MACAddress = None, bandwidth: int = 100, mtu: int = 1500):
        self.portId = port_id
        self.ip = ip
        self.mac = mac or MACAddress.generate()  # generuj MAC jeśli nie podano
        self.bandwidth = bandwidth
        self.mtu = mtu
        self.connectedTo = None

    @classmethod
    def from_dict(cls, data: dict, ctx=None):
        cls.check_fields(data, ctx)

        port_id = data.get("portId")
        ip = data.get("ip")
        mac = data.get("mac")
        bandwidth = data.get("bandwidth", 100)
        mtu = data.get("mtu", 1500)

        if not isinstance(port_id, str):
            raise NetLangRuntimeError("CopperEthernetPort must have string portId", ctx=ctx)

        if ip is not None and not isinstance(ip, CIDR):
            raise NetLangRuntimeError("Invalid ip for CopperEthernetPort", ctx=ctx)

        if mac is not None:
            if not isinstance(mac, MACAddress):
                raise NetLangRuntimeError("Invalid MAC address", ctx=ctx)
            if MACAddress.is_registered(mac.mac):
                raise NetLangRuntimeError(message=f"MAC address {mac.mac} is already in use", ctx=ctx)
            MACAddress.register(mac.mac)

        if not isinstance(bandwidth, int) or not isinstance(mtu, int):
            raise NetLangRuntimeError("Bandwidth and MTU must be integers", ctx=ctx)

        return cls(port_id, ip, mac, bandwidth, mtu)

    def __repr__(self):
        return f"{self.portId} ({self.mac}, {self.ip}, {self.bandwidth}Mbps, {self.mtu}B)"
