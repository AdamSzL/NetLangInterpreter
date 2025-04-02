from interpreter.errors import NetLangRuntimeError
from model.base import NetLangObject
from dataclasses import dataclass

@dataclass
class Host(NetLangObject):
    allowed_fields = {"name", "ports"}
    name: str
    ports: list

    @classmethod
    def from_dict(cls, data: dict, ctx=None):
        cls.check_fields(data, ctx)

        name = data.get("name")
        ports = data.get("ports", [])

        cls.validate_field_types(name, ports, ctx)

        host = cls(name, ports)

        cls.validate_logic(name, ports)

        for port in ports:
            setattr(host, port.portId, port)

        return host

    @staticmethod
    def validate_field_types(name, ports, ctx=None):
        if not isinstance(name, str):
            raise NetLangRuntimeError(message="Host device must have string 'name' field", ctx=ctx)

        if not isinstance(ports, list):
            raise NetLangRuntimeError(message="Host device must have list of ports in 'ports' field", ctx=ctx)

    @staticmethod
    def validate_logic(name, ports, ctx=None):
        seen_ids = set()
        for port in ports:
            if port.portId in seen_ids:
                raise NetLangRuntimeError(message=f"Duplicate portId '{port.portId}' in Host '{name}'",
                                          ctx=ctx)
            if not hasattr(port, "ip") or port.ip is None:
                raise NetLangRuntimeError(
                    message=f"Host port '{port.portId}' must have an IP address",
                    ctx=ctx
                )
            seen_ids.add(port.portId)

    def validate(self, ctx=None):
        self.__class__.validate_field_types(self.name, self.ports, ctx=ctx)
        self.__class__.validate_logic(self.name, self.ports, ctx=ctx)
