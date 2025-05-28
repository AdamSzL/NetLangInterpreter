from shared.errors import NetLangRuntimeError
from shared.model.Device import Device
from shared.model.base import NetLangObject
from dataclasses import dataclass

@dataclass
class Host(NetLangObject, Device):
    name: str
    ports: list

    @classmethod
    def from_dict(cls, data: dict, ctx):
        name = data.get("name")
        ports = data.get("ports", [])

        host = cls(name, ports)

        cls.validate_logic(name, ports, ctx)

        for port in ports:
            setattr(host, port.portId, port)

        return host

    @staticmethod
    def validate_logic(name, ports, ctx):
        seen_ids = set()
        for port in ports:
            if port.portId in seen_ids:
                raise NetLangRuntimeError(
                    f"Duplicate portId '{port.portId}' in Host '{name}'",
                    ctx
                )
            if not hasattr(port, "ip") or port.ip is None:
                raise NetLangRuntimeError(
                    f"Host port '{port.portId}' must have an IP address",
                    ctx
                )
            seen_ids.add(port.portId)
