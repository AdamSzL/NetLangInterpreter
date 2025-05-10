from interpreter.errors import NetLangRuntimeError
from model.Device import Device
from model.base import NetLangObject
from dataclasses import dataclass

@dataclass
class Switch(NetLangObject, Device):
    allowed_fields = {"name", "ports"}
    name: str
    ports: list

    @classmethod
    def from_dict(cls, data: dict, ctx):
        cls.check_fields(data, ctx)

        name = data.get("name")
        ports = data.get("ports", [])

        cls.validate_field_types(name, ports, ctx)

        switch = cls(name, ports)

        cls.validate_logic(name, ports, ctx)

        for port in ports:
            setattr(switch, port.portId, port)

        return switch

    @staticmethod
    def validate_field_types(name, ports, ctx):
        if not isinstance(name, str):
            raise NetLangRuntimeError("Switch device must have string 'name' field", ctx)

        if not isinstance(ports, list):
            raise NetLangRuntimeError("Switch device must have list of ports in 'ports' field", ctx)

    @staticmethod
    def validate_logic(name, ports, ctx=None):
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

    def validate(self, ctx=None):
        self.__class__.validate_field_types(self.name, self.ports, ctx)
        self.__class__.validate_logic(self.name, self.ports, ctx)
