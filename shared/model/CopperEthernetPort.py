from shared.model.Port import Port
from shared.model.base import NetLangObject
from dataclasses import dataclass


@dataclass
class CopperEthernetPort(NetLangObject, Port):
    bandwidth: int = 100

    @classmethod
    def from_dict(cls, data: dict, ctx):
        port_id, ip, mac, mtu, gateway = Port.base_from_dict(data, ctx)
        bandwidth = data.get("bandwidth", 100)

        port = cls(port_id, ip, mac, mtu, None, gateway, bandwidth)
        port.validate_logic(ctx)
        return port

    def __hash__(self):
        return hash(self.mac)

    def __eq__(self, other):
        return isinstance(other, CopperEthernetPort) and self.mac == other.mac
