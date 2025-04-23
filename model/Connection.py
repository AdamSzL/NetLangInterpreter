from dataclasses import dataclass

@dataclass
class Connection:
    def __init__(self, device1, port1, device2, port2):
        self.device1 = device1
        self.port1 = port1
        self.device2 = device2
        self.port2 = port2