import re
import random
from typing import ClassVar

from shared.errors import NetLangRuntimeError


class MACAddress:
    active_addresses: ClassVar[set[str]] = set()
    mac: str

    def __init__(self, mac: str):
        # Sprawdzenie poprawności MAC-a (np. A0:BA:E6:E3:FD:E1)
        if not re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', mac):
            raise ValueError(f"Invalid MAC address: {mac.upper()}")
        self.mac = mac.upper()
        # MACAddress._generated.add(mac)

    def __repr__(self):
        return self.mac

    @classmethod
    def generate(cls):
        while True:
            # Wygeneruj 6 losowych bajtów (ostatni bajt nie może być multicast ani lokalny)
            mac_bytes = [random.randint(0x00, 0xFF) for _ in range(6)]
            mac_bytes[0] &= 0xFC  # wyczyść bity multicast i lokalny (bit 0 i 1)

            mac_str = ":".join(f"{b:02X}" for b in mac_bytes)

            if mac_str not in cls.active_addresses:
                return MACAddress(mac_str)

    @classmethod
    def register(cls, mac: str, ctx):
        if mac in cls.active_addresses:
            raise NetLangRuntimeError(f"MAC address {mac} is already in use", ctx)
        cls.active_addresses.add(mac)

    @classmethod
    def unregister(cls, mac):
        cls.active_addresses.discard(mac)
