import ipaddress

from shared.utils.errors import NetLangRuntimeError
from shared.model.Device import Device
from shared.model.base import NetLangObject
from dataclasses import dataclass

@dataclass
class Router(NetLangObject, Device):
    name: str
    ports: list
    routingTable: list

    @classmethod
    def from_dict(cls, data: dict, ctx):
        name = data.get("name")
        ports = data.get("ports", [])
        routingTable = data.get("routingTable", [])

        router = cls(name, ports, routingTable)
        router.validate_logic(ctx)

        for port in ports:
            if port.owner is not None:
                raise NetLangRuntimeError(f"Port with id {port.portId} is already owned by device '{router.name}'", ctx)
            port.owner = router

        for port in ports:
            setattr(router, port.portId, port)

        return router

    def validate_logic(self, ctx):
        self.validate_base_logic(ctx)
        seen_ips = set()
        seen_networks = []
        for port in self.ports:
            if port.gateway is not None:
                raise NetLangRuntimeError(
                    f"Router port '{port.portId}' must not have a gateway assigned",
                    ctx
                )
            if not hasattr(port, "ip") or port.ip is None:
                raise NetLangRuntimeError(
                    f"Host port '{port.portId}' must have an IP address",
                    ctx
                )

            ip_str = str(port.ip.ip.ip)
            if ip_str in seen_ips:
                raise NetLangRuntimeError(
                    f"Duplicate IP '{ip_str}' in Router '{self.name}'",
                    ctx
                )
            seen_ips.add(ip_str)

            new_interface = ipaddress.IPv4Interface(str(port.ip))
            new_network = new_interface.network

            for existing_port_id, existing_network in seen_networks:
                if new_network.overlaps(existing_network):
                    if not (new_network.subnet_of(existing_network) or existing_network.subnet_of(new_network)):
                        raise NetLangRuntimeError(
                            (
                                f"Router '{self.name}' has multiple ports in overlapping subnets:\n"
                                f"- Port '{port.portId}' with IP {new_interface}\n"
                                f"- Port '{existing_port_id}' with IP {existing_network}"
                            ),
                            ctx
                        )

            seen_networks.append((port.portId, new_network))

        port_ids = {port.portId for port in self.ports}
        for entry in self.routingTable:
            if entry.via not in port_ids:
                raise NetLangRuntimeError(
                    f"RoutingEntry refers to unknown portId '{entry.via}' in Router '{self.name}'",
                    ctx
                )