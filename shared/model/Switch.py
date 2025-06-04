from shared.utils.errors import NetLangRuntimeError
from shared.model.Device import Device
from shared.model.base import NetLangObject
from dataclasses import dataclass

@dataclass
class Switch(NetLangObject, Device):
    name: str
    ports: list

    @classmethod
    def from_dict(cls, data: dict, ctx):
        name = data.get("name")
        ports = data.get("ports", [])

        switch = cls(name, ports)
        switch.validate_logic(ctx)

        for port in ports:
            if port.owner is not None:
                raise NetLangRuntimeError(f"Port with id {port.portId} is already owned by device {switch.name}", ctx)
            port.owner = switch

        for port in ports:
            setattr(switch, port.portId, port)

        return switch

    def validate_logic(self, ctx):
        self.validate_base_logic(ctx)
        for port in self.ports:
            if hasattr(port, "ip") and port.ip is not None:
                raise NetLangRuntimeError(
                    f"Switch port '{port.portId}' must not have an IP address",
                    ctx
                )