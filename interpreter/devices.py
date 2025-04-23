from rich.table import Table
from rich.text import Text

from .errors import NetLangRuntimeError
from .utils import get_interface_label
from .logging import log
from model import Host, Router, Switch, Connection

def visitConnectStatement(self, ctx):
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

    self.connections.append(Connection(
        device1=dev1_id, port1=port1_id,
        device2=dev2_id, port2=port2_id
    ))

    print(f"Connected {dev1_id}.{port1_id} <-> {dev2_id}.{port2_id}")

def visitShowInterfacesStatement(self, ctx):
    device_name = ctx.ID().getText()

    if device_name not in self.variables:
        raise NetLangRuntimeError(f"Device '{device_name}' not found")

    device = self.variables[device_name]

    if not isinstance(device, (Host, Router, Switch)):
        raise NetLangRuntimeError(f"'{device_name}' is not a device")

    if not hasattr(device, "ports"):
        raise NetLangRuntimeError(f"Device '{device_name}' has no ports")

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

        # Sprawdzenie czy port jest połączony
        status = "down"
        for conn in self.connections:
            if (conn.device1 == device_name and conn.port1 == port_id) or \
                    (conn.device2 == device_name and conn.port2 == port_id):
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