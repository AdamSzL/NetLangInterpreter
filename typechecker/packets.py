from typing import TYPE_CHECKING

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangTypeError
from shared.model.Variable import Variable
from shared.utils.types import are_types_compatible

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitSendPacketStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.SendPacketStatementContext):
    packet_ctx = ctx.fieldAccess(0)
    port_ctx = ctx.fieldAccess(1)

    packet_type = self.visit(packet_ctx)
    if packet_type != "Packet":
        raise NetLangTypeError(
            f"First argument of send must be of type Packet, got {packet_type}",
            ctx
        )

    device_var_type = self.evaluate_type_of_parent(port_ctx)
    if device_var_type != "Host":
        raise NetLangTypeError(
            "Only hosts can send packets",
            ctx
        )

    port_type = self.visit(port_ctx)
    if not are_types_compatible("Port", port_type):
        raise NetLangTypeError(
            f"Packet can only be sent from a port, got {port_type} instead",
            ctx
        )

    return None