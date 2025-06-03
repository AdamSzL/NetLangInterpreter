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

    if type(port1) != type(port2):
        raise NetLangRuntimeError(
        f"Cannot connect '{type(port1).__name__}' to '{type(port2).__name__}' — port types must match",
            ctx
        )

    if port1.owner.uid == port2.owner.uid:
        raise NetLangRuntimeError(
            "Cannot connect two ports belonging to the same device",
            ctx
        )

    port1.connectedTo = port2
    port2.connectedTo = port1

    device1 = self.evaluateParentOfAccess(ctx.fieldAccess(0))
    device2 = self.evaluateParentOfAccess(ctx.fieldAccess(1))

    connection = Connection(device1, port1, device2, port2)
    self.connections.append(connection)