from typing import cast

from rich.panel import Panel
from rich.text import Text

from generated.NetLangParser import NetLangParser
from model import Switch, Router, Host, Packet
from time import sleep

from .errors import NetLangRuntimeError
from .utils import get_port_by_id
from .logging import log
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitSendPacketStatement(self: "Interpreter", ctx: NetLangParser.SendPacketStatementContext):
    packet_name = ctx.ID().getText()

    if packet_name not in self.variables:
        raise NetLangRuntimeError(
            message=f"Packet '{packet_name}' is not defined",
            ctx=ctx
        )

    packet_var = self.variables[packet_name]

    if not isinstance(packet_var, Packet):
        raise NetLangRuntimeError(
            message=f"Variable '{packet_name}' is not a Packet",
            ctx=ctx
        )

    packet = cast(Packet, packet_var)

    device_name = ctx.fieldAccess().ID(0).getText()
    # trzeba poprawić - nie działa np. dla listy urządzeń

    if device_name not in self.variables:
        raise NetLangRuntimeError(
            message=f"Device '{device_name}' is not defined",
            ctx=ctx
        )

    device = self.variables[device_name]
    if not isinstance(device, Host):
        raise NetLangRuntimeError(
            message="Only hosts can send packets",
            ctx=ctx
        )

    port = self.visit(ctx.fieldAccess())
    target_ip = ctx.IPADDR().getText()

    body = Text()
    body.append("📤 Sending packet\n", style="bold white")
    body.append(Text.from_markup(f"[bold cyan]Source:[/bold cyan] [green]{device.name}.{port.portId}[/green]\n"))
    body.append(Text.from_markup(f"[bold cyan]Destination:[/bold cyan] [yellow]{target_ip}[/yellow]\n"))
    body.append(Text.from_markup(f"[bold cyan]Payload:[/bold cyan] [magenta]{packet.payload}[/magenta]\n"))
    body.append(Text.from_markup(f"[bold cyan]Protocol:[/bold cyan] [blue]{packet.protocol}[/blue]\n"))
    body.append(Text.from_markup(f"[bold cyan]Size:[/bold cyan] [white]{packet.size}[/white] B\n"))

    log(Panel(body, title=f"[b]Host {device.name}[/b]", style="cyan"))

    packet.src = port.ip
    packet.dst = target_ip

    self.forward_packet(packet, device_name, port)

def forward_packet(self: "Interpreter", packet: Packet, start_device: str, start_port):
    visited_ports = set()
    queue = [(start_port, start_device)]  # (port, from_device_name)

    while queue:
        port, from_device_name = queue.pop(0)
        visited_ports.add(port)

        for conn in self.connections:
            if conn.port1 == port.portId and conn.device1 == from_device_name:
                next_device_name = conn.device2
                next_port_id = conn.port2
            elif conn.port2 == port.portId and conn.device2 == from_device_name:
                next_device_name = conn.device1
                next_port_id = conn.port1
            else:
                continue

            next_device = self.variables.get(next_device_name)
            next_port = get_port_by_id(next_device, next_port_id)

            if next_port in visited_ports:
                continue

            sleep(0.3)

            if isinstance(next_device, Switch):
                body = Text()
                body.append(f"Received packet on {next_device.name}.{next_port.portId}\n", style="white")
                for p in next_device.ports:
                    if p != next_port and p not in visited_ports:
                        body.append(f"Forwarded packet to {next_device.name}.{p.portId}\n", style="green")
                        queue.append((p, next_device_name))

                log(Panel(body, title=f"Switch {next_device.name}", style="cyan"))

            elif isinstance(next_device, Router):
                body = Text()
                body.append(f"Received packet on {next_device.name}.{next_port.portId}\n", style="white")
                if str(next_port.ip).split("/")[0] == packet.dst:
                    body.append(f"[✓] Delivered to {packet.dst}\n", style="bold green")
                else:
                    body.append(f"Packet could not be delivered to {packet.dst}\n", style="bold red")

                log(Panel(body, title=f"Router {next_device.name}", style="blue"))

            elif isinstance(next_device, Host):
                body = Text()
                body.append(f"Received packet on {next_device.name}.{next_port.portId}\n", style="white")
                if str(next_port.ip).split("/")[0] == packet.dst:
                    body.append(f"[✓] Delivered to {packet.dst}\n", style="bold green")
                else:
                    body.append(f"Packet could not be delivered to {packet.dst}\n", style="bold red")

                log(Panel(body, title=f"Host {next_device.name}", style="magenta"))
