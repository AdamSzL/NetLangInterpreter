from shared.errors import NetLangRuntimeError
from shared.model.Device import Device
from shared.model.base import NetLangObject
from dataclasses import dataclass

@dataclass
class Router(NetLangObject, Device):
    allowed_fields = {"name", "ports", "routingTable"}
    name: str
    ports: list
    routingTable: list

    @classmethod
    def from_dict(cls, data: dict, ctx):
        cls.check_fields(data, ctx)

        name = data.get("name")
        ports = data.get("ports", [])
        routingTable = data.get("routingTable", [])

        cls.validate_field_types(name, ports, routingTable, ctx)

        router = cls(name, ports, routingTable)

        cls.validate_logic(name, ports, routingTable, ctx)

        for port in ports:
            setattr(router, port.portId, port)

        return router

    @staticmethod
    def validate_field_types(name, ports, routingTable, ctx):
        if not isinstance(name, str):
            raise NetLangRuntimeError("Router device must have string 'name' field", ctx)

        if not isinstance(ports, list):
            raise NetLangRuntimeError("Router device must have list of ports in 'ports' field", ctx)

        if not isinstance(routingTable, list):
            raise NetLangRuntimeError("Router device must have list of routing table in 'routingTable' field", ctx)

    @staticmethod
    def validate_logic(name, ports, routingTable, ctx=None):
        seen_ids = set()
        for port in ports:
            if port.portId in seen_ids:
                raise NetLangRuntimeError(
                    f"Duplicate portId '{port.portId}' in Router '{name}'",
                    ctx
                )
            if not hasattr(port, "ip") or port.ip is None:
                raise NetLangRuntimeError(
                    f"Host port '{port.portId}' must have an IP address",
                    ctx
                )
            seen_ids.add(port.portId)

        port_ids = {port.portId for port in ports}
        for entry in routingTable:
            if entry.via not in port_ids:
                raise NetLangRuntimeError(
                    f"RoutingEntry refers to unknown portId '{entry.via}' in Router '{name}'",
                    ctx
                )

    def validate(self, ctx=None):
        self.__class__.validate_field_types(self.name, self.ports, self.routingTable, ctx)
        self.__class__.validate_logic(self.name, self.ports, self.routingTable, ctx)