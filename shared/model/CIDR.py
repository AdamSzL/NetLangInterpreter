import ipaddress
from dataclasses import dataclass
from typing import cast

from shared.model.IPAddress import IPAddress
from shared.model.base import NetLangObject

@dataclass
class CIDR(NetLangObject):
    ip: IPAddress
    mask: int

    # def __init__(self, ip: IPAddress, mask: int):
        # net = ipaddress.IPv4Network(cidr, strict=True)
        # self.ip = IPAddress(str(net.network_address))
        # self.mask = net.prefixlen
        # self.ip = ip
        # self.mask = mask

    def current_network(self):
        return ipaddress.IPv4Network(f"{self.ip}/{self.mask}", strict=False)

    @property
    def network(self):
        return str(self.current_network().network_address)

    @property
    def broadcast(self):
        return str(self.current_network().broadcast_address)

    @classmethod
    def from_dict(cls, data: dict, ctx):
        ip = data.get("ip")
        mask = data.get("mask")

        return cls(cast(IPAddress, ip), cast(int, mask))

    def __repr__(self):
        return f"{self.ip.ip}/{self.mask}"

    def __add__(self, other: int) -> "CIDR":
        new_ip = int(self.ip.ip) + other
        return CIDR(IPAddress(str(ipaddress.IPv4Address(new_ip))), self.mask)

    def __sub__(self, other: int) -> "CIDR":
        new_ip = int(self.ip.ip) - other
        return CIDR(IPAddress(str(ipaddress.IPv4Address(new_ip))), self.mask)
