import ipaddress
from dataclasses import dataclass

class IPAddress:
    ip: ipaddress.IPv4Address

    def __init__(self, address: str):
        self.ip = ipaddress.ip_address(address)

    def __repr__(self) -> str:
        return str(self.ip)