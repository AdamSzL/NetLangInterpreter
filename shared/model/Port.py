from dataclasses import dataclass, field
from typing import Optional, Any

from shared.errors import NetLangRuntimeError
from shared.model.CIDR import CIDR
from shared.model.MACAddress import MACAddress
from shared.model.IPAddress import IPAddress
from shared.model.Device import Device


@dataclass
class Port:
    portId: str
    ip: CIDR
    mac: MACAddress
    mtu: int = 1500
    connectedTo: Any = None
    gateway: Optional[IPAddress] = None
    owner: Optional[Device] = field(default=None, init=False)

    @classmethod
    def base_from_dict(cls, data: dict, ctx):
        port_id = data.get("portId")
        ip = data.get("ip")
        mac = data.get("mac")
        mtu = data.get("mtu", 1500)
        gateway = data.get("gateway")

        if ip is not None:
            ip_str = str(ip.ip)
            IPAddress.register(ip_str, ctx)

        if mac is None:
            mac = MACAddress.generate()
        else:
            MACAddress.register(mac.mac, ctx)

        return port_id, ip, mac, mtu, gateway

    def validate_logic(self, ctx):
        if self.ip and self.gateway:
            if self.gateway.ip == self.ip.ip.ip:
                raise NetLangRuntimeError(
                    f"Gateway IP {self.gateway} cannot be the same as port IP {self.ip.ip}",
                    ctx
                )
            if self.gateway.ip not in self.ip.current_network():
                raise NetLangRuntimeError(
                    f"Gateway {self.gateway} is not in subnet {self.ip}",
                    ctx
                )

        if self.owner and hasattr(self.owner, "validate_logic"):
            self.owner.validate_logic(ctx)