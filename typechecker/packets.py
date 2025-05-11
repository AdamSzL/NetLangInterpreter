from typing import TYPE_CHECKING

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangTypeError

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitSendPacketStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.SendPacketStatementContext):
    packet_name = ctx.ID().getText()

    if packet_name not in self.variables:
        raise NetLangTypeError(
            f"Packet '{packet_name}' is not defined",
            ctx
        )

    packet_type = self.variables[packet_name].type

    if packet_type != "Packet":
        raise NetLangTypeError(
            f"Variable '{packet_name}' must be of type Packet, got {packet_type}",
            ctx
        )

    device_name = ctx.fieldAccess().ID(0).getText()

    if device_name not in self.variables:
        raise NetLangTypeError(
            f"Undefined device '{device_name}' is not defined",
            ctx
        )

    device_type = self.variables[device_name].type
    if device_type != "Host":
        raise NetLangTypeError(
            "Only hosts can send packets",
            ctx
        )

    port_type = self.visit(ctx.fieldAccess())
    if not port_type.endswith("Port"):
        raise NetLangTypeError(f"Packet can only be sent from a port, got {port_type} instead")

    return None