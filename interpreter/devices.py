from rich.table import Table
from rich.text import Text

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError
from .utils import get_interface_label
from shared.logging import log
from shared.model import Host, Router, Switch, Connection
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitConnectStatement(self: "Interpreter", ctx: NetLangParser.ConnectStatementContext):
    port1 = self.visit(ctx.fieldAccess(0))
    port2 = self.visit(ctx.fieldAccess(1))

    if port1.connectedTo is not None or port2.connectedTo is not None:
        raise NetLangRuntimeError("One of the ports is already connected")

    port1.connectedTo = port2
    port2.connectedTo = port1

    dev1_id = ctx.fieldAccess(0).ID(0).getText()
    port1_id = ctx.fieldAccess(0).ID(1).getText()
    dev2_id = ctx.fieldAccess(1).ID(0).getText()
    port2_id = ctx.fieldAccess(1).ID(1).getText()

    self.connections.append(Connection(dev1_id, port1_id, dev2_id, port2_id))

    print(f"Connected {dev1_id}.{port1_id} <-> {dev2_id}.{port2_id}")

def visitShowInterfacesStatement(self: "Interpreter", ctx: NetLangParser.ShowInterfacesStatementContext):
    device_name = ctx.ID().getText()
    device = self.variables[device_name].value

    if not hasattr(device, "ports"):
        raise NetLangRuntimeError(f"Device '{device_name}' has no ports", ctx)

    log(f"\n[bold]Interfaces of {device.name}[/bold]\n")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Interface", style="white", no_wrap=True)
    table.add_column("Label", style="white")
    table.add_column("IP Address", style="white")
    table.add_column("Status", style="bold")
    table.add_column("MAC Address", style="dim")
    table.add_column("Type", style="white")

    for port in device.ports:
        port_id = port.portId
        bandwidth = getattr(port, "bandwidth", None)
        label = get_interface_label(port_id, bandwidth) if bandwidth else "-"
        ip = str(getattr(port, "ip", "None"))
        mac = str(getattr(port, "mac", "-"))
        port_type = type(port).__name__.replace("Port", "")

        status = "down"
        for conn in self.connections:
            if (conn.device1_id == device_name and conn.port2_id == port_id) or \
                    (conn.device2_id == device_name and conn.port2_id== port_id):
                status = "up"
                break

        status_text = Text(status, style="green" if status == "up" else "red")

        table.add_row(
            port_id,
            label,
            ip,
            status_text,
            mac,
            port_type
        )

    log(table)