from generated.NetLangParser import NetLangParser
from shared.model import Packet, IPAddress

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitSendPacketStatement(self: "Interpreter", ctx: NetLangParser.SendPacketStatementContext):
    payload = ctx.STRING().getText()[1:-1]
    port = self.visit(ctx.fieldAccess())
    target_ip = IPAddress(ctx.IPADDR().getText())

    packet = Packet(payload)
    packet.source = port
    packet.destination_ip = target_ip

    self.draw_graph_and_animate_packet(packet, ctx)