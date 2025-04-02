import ipaddress

class IPAddress:
    def __init__(self, address: str):
        self.address = str(ipaddress.IPv4Address(address))

    def __repr__(self):
        return self.address
