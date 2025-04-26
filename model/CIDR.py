import ipaddress
from typing import ClassVar, Any, cast

from interpreter.errors import NetLangRuntimeError
from model.IPAddress import IPAddress
from model.base import NetLangObject

class CIDR(NetLangObject):
    allowed_fields = {"ip", "mask"}
    ip: IPAddress
    mask: int

    def __init__(self, ip: IPAddress, mask: int):
        # net = ipaddress.IPv4Network(cidr, strict=True)
        # self.ip = IPAddress(str(net.network_address))
        # self.mask = net.prefixlen
        self.ip = ip
        self.mask = mask

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

        if not isinstance(ip, IPAddress):
            raise NetLangRuntimeError(f"Invalid CIDR object: field 'ip' must be of type IP", ctx)

        if not isinstance(mask, int):
            raise NetLangRuntimeError(f"Invalid CIDR object: field 'mask' must be of type int", ctx)

        return cls(cast(IPAddress, ip), cast(int, mask))

    def __repr__(self):
        return f"{self.ip.ip}/{self.mask}"
