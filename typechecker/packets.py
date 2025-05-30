from typing import TYPE_CHECKING

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangTypeError
from shared.model.Variable import Variable

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitSendPacketStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.SendPacketStatementContext):
    packet_ctx = ctx.scopedIdentifier()
    port_ctx = ctx.fieldAccess()

    packet_name = packet_ctx.ID().getText()

    self.scoped_identifier_expectation = "variable"
    try:
        packet_type = self.visit(packet_ctx)
    finally:
        self.scoped_identifier_expectation = None

    if packet_type != "Packet":
        raise NetLangTypeError(
            f"Variable '{packet_name}' must be of type Packet, got {packet_type}",
            ctx
        )

    self.scoped_identifier_expectation = "variable"
    try:
        device_var_type = self.visit(port_ctx.scopedIdentifier())
    finally:
        self.scoped_identifier_expectation = None

    if device_var_type != "Host":
        raise NetLangTypeError(
            "Only hosts can send packets",
            ctx
        )

    port_type = self.visit(port_ctx)
    if not port_type.endswith("Port"):
        raise NetLangTypeError(
            f"Packet can only be sent from a port, got {port_type} instead",
            ctx
        )

    return None