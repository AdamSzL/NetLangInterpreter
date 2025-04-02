import ipaddress

from interpreter.errors import NetLangRuntimeError
from model.IPAddress import IPAddress
from model.base import NetLangObject

class CIDR(NetLangObject):
    allowed_fields = {"ip", "mask"}

    def __init__(self, cidr: str):
        # net = ipaddress.IPv4Network(cidr, strict=True)
        # self.ip = IPAddress(str(net.network_address))
        # self.mask = net.prefixlen
        self.ip = cidr.split('/')[0]
        self.mask = cidr.split('/')[1]

    def _current_network(self):
        return ipaddress.IPv4Network(f"{self.ip}/{self.mask}", strict=False)

    @property
    def network(self):
        return str(self._current_network().network_address)

    @property
    def broadcast(self):
        return str(self._current_network().broadcast_address)

    @classmethod
    def from_dict(cls, data: dict, ctx=None):
        cls.check_fields(data, ctx)

        ip = data.get("ip")
        mask = data.get("mask")
        if not isinstance(ip, IPAddress) or not isinstance(mask, int):
            raise NetLangRuntimeError(f"Invalid CIDR object: expected fields 'ip: IP' and 'mask: int'", ctx)
        return cls(f"{ip}/{mask}")

    def __repr__(self):
        return f"{self.ip}/{self.mask}"
