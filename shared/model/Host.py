from shared.utils.errors import NetLangRuntimeError
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
        host.validate_logic(ctx)

        for port in ports:
            if port.owner is not None:
                raise NetLangRuntimeError(f"Port with id {port.portId} is already owned by device '{host.name}'", ctx)
            port.owner = host

        for port in ports:
            setattr(host, port.portId, port)

        return host

    def validate_logic(self, ctx):
        self.validate_base_logic(ctx)
        seen_ips = set()
        cidr = None
        for port in self.ports:
            if not hasattr(port, "ip") or port.ip is None:
                raise NetLangRuntimeError(
                    f"Host port '{port.portId}' must have an IP address",
                    ctx
                )

            ip_str = str(port.ip.ip.ip)
            if ip_str in seen_ips:
                raise NetLangRuntimeError(
                    f"Duplicate IP '{ip_str}' in Host '{self.name}'",
                    ctx
                )
            seen_ips.add(ip_str)

            if cidr is None:
                cidr = port.ip.current_network()
            elif port.ip.current_network() != cidr:
                raise NetLangRuntimeError(
                    f"All ports in Host '{self.name}' must be in the same subnet",
                    ctx
                )