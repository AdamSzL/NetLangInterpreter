from typing import TYPE_CHECKING

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangTypeError
from shared.model.Variable import Variable

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitSendPacketStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.SendPacketStatementContext):
    packet_name: str = ctx.ID().getText()

    packet_var: Variable = self.lookup_variable(packet_name, ctx)
    if packet_var.type != "Packet":
        raise NetLangTypeError(
            f"Variable '{packet_name}' must be of type Packet, got {packet_var.type}",
            ctx
        )

    device_name: str = ctx.fieldAccess().ID(0).getText()
    device_var: Variable = self.lookup_variable(device_name, ctx)

    if device_var.type != "Host":
        raise NetLangTypeError("Only hosts can send packets", ctx)

    port_type = self.visit(ctx.fieldAccess())
    if not port_type.endswith("Port"):
        raise NetLangTypeError(f"Packet can only be sent from a port, got {port_type} instead")

    return None