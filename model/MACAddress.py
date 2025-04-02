import re
import random


class MACAddress:
    _active = set()
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

            if mac_str not in cls._active:
                return MACAddress(mac_str)

    @classmethod
    def register(cls, mac):
        cls._active.add(mac.upper())

    @classmethod
    def unregister(cls, mac):
        cls._active.discard(mac.upper())

    @classmethod
    def is_registered(cls, mac):
        return mac in cls._active
