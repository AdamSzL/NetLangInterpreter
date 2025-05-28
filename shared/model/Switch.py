from shared.errors import NetLangRuntimeError
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

        cls.validate_logic(name, ports, ctx)

        for port in ports:
            setattr(switch, port.portId, port)

        return switch

    @staticmethod
    def validate_logic(name, ports, ctx):
        seen_ids = set()
        for port in ports:
            if port.portId in seen_ids:
                raise NetLangRuntimeError(
                    f"Duplicate portId '{port.portId}' in Switch '{name}'",
                    ctx
                )
            if hasattr(port, "ip") and port.ip is not None:
                raise NetLangRuntimeError(
                    f"Switch port '{port.portId}' must not have an IP address",
                    ctx
                )
            seen_ids.add(port.portId)