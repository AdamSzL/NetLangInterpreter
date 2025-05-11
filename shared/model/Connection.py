from dataclasses import dataclass

@dataclass
class Connection:
    device1_id: str
    port1_id: str
    device2_id: str
    port2_id: str