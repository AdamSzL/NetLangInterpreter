from interpreter.errors import NetLangRuntimeError
from model.base import NetLangObject
from dataclasses import dataclass

@dataclass
class Router(NetLangObject):
    allowed_fields = {"name", "ports", "routingTable"}
    name: str
    ports: list
    routingTable: list

    @classmethod
    def from_dict(cls, data: dict, ctx=None):
        cls.check_fields(data, ctx)

        name = data.get("name")
        ports = data.get("ports", [])
        routingTable = data.get("routingTable", [])

        cls.validate_field_types(name, ports, routingTable)

        router = cls(name, ports, routingTable)

        cls.validate_logic(name, ports, routingTable)

        for port in ports:
            setattr(router, port.portId, port)

        return router

    @staticmethod
    def validate_field_types(name, ports, routingTable, ctx=None):
        if not isinstance(name, str):
            raise NetLangRuntimeError(message="Router device must have string 'name' field", ctx=ctx)

        if not isinstance(ports, list):
            raise NetLangRuntimeError(message="Router device must have list of ports in 'ports' field", ctx=ctx)

        if not isinstance(routingTable, list):
            raise NetLangRuntimeError(message="Router device must have list of routing table in 'routingTable' field", ctx=ctx)

    @staticmethod
    def validate_logic(name, ports, routingTable, ctx=None):
        seen_ids = set()
        for port in ports:
            if port.portId in seen_ids:
                raise NetLangRuntimeError(message=f"Duplicate portId '{port.portId}' in Router '{name}'",
                                          ctx=ctx)
            if not hasattr(port, "ip") or port.ip is None:
                raise NetLangRuntimeError(
                    message=f"Host port '{port.portId}' must have an IP address",
                    ctx=ctx
                )
            seen_ids.add(port.portId)

        port_ids = {port.portId for port in ports}
        for entry in routingTable:
            if entry.via not in port_ids:
                raise NetLangRuntimeError(
                    message=f"RoutingEntry refers to unknown portId '{entry.via}' in Router '{name}'",
                    ctx=ctx
                )

    def validate(self, ctx=None):
        self.__class__.validate_field_types(self.name, self.ports, self.routingTable, ctx=ctx)
        self.__class__.validate_logic(self.name, self.ports, self.routingTable, ctx=ctx)