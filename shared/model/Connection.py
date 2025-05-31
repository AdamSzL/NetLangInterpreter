from dataclasses import dataclass

from shared.model.Device import Device
from shared.model.Port import Port

@dataclass
class Connection:
    device1: Device
    port1: Port
    device2: Device
    port2: Port