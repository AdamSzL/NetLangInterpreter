import ipaddress
from dataclasses import dataclass
from typing import ClassVar

from shared.errors import NetLangRuntimeError


class IPAddress:
    active_addresses: ClassVar[set[str]] = set()
    ip: ipaddress.IPv4Address

    def __init__(self, address: str):
        self.ip = ipaddress.ip_address(address)

    @classmethod
    def register(cls, ip: str, ctx):
        if ip in cls.active_addresses:
            raise NetLangRuntimeError(f"IP address {ip} is already in use", ctx)
        cls.active_addresses.add(ip)

    @classmethod
    def unregister(cls, ip: str):
        cls.active_addresses.discard(ip)

    def __repr__(self) -> str:
        return str(self.ip)

    def __add__(self, other: int) -> "IPAddress":
        try:
            new_ip = int(self.ip) + other
            result = IPAddress(str(ipaddress.IPv4Address(new_ip)))
        except ipaddress.AddressValueError:
            raise NetLangRuntimeError(
                f"Result of {self} + {other} is out of valid IPv4 range (0.0.0.0 – 255.255.255.255)",
            )
        return result

    def __sub__(self, other: int) -> "IPAddress":
        try:
            new_ip = int(self.ip) - other
            result = IPAddress(str(ipaddress.IPv4Address(new_ip)))
        except ipaddress.AddressValueError:
            raise NetLangRuntimeError(
                f"Result of {self} - {other} is out of valid IPv4 range (0.0.0.0 – 255.255.255.255)",
            )
        return result