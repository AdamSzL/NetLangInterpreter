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
        raise NetLangRuntimeError("One of the ports is already connected", ctx)

    port1.connectedTo = port2
    port2.connectedTo = port1

    device1 = self.evaluateParentOfAccess(ctx.fieldAccess(0))
    device2 = self.evaluateParentOfAccess(ctx.fieldAccess(1))

    connection = Connection(device1, port1, device2, port2)
    self.connections.append(connection)

def visitShowInterfacesStatement(self: "Interpreter", ctx: NetLangParser.ShowInterfacesStatementContext):
    scoped_ctx = ctx.scopedIdentifier()
    device_name = scoped_ctx.ID().getText()
    scope, var_name = self.visit(scoped_ctx)
    device = scope.variables[var_name].value

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