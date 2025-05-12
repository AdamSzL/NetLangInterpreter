from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError, NetLangTypeError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitConnectStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.ConnectStatementContext):
    port1_type = self.visit(ctx.fieldAccess(0))
    port2_type = self.visit(ctx.fieldAccess(1))

    if not port1_type.endswith("Port") or not port2_type.endswith("Port"):
        raise NetLangTypeError("'connect' statement can only be used with ports", ctx)

    if port1_type != port2_type:
        raise NetLangTypeError(f"Cannot connect port of type {port1_type} to port of type {port2_type}", ctx)

    return None

def visitShowInterfacesStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.ShowInterfacesStatementContext):
    device_name = ctx.ID().getText()
    device_var = self.lookup_variable(device_name, ctx)
    device_type = device_var.type

    if device_type not in ["Host", "Router", "Switch"]:
        raise NetLangRuntimeError(f"'{device_name}' is not a device", ctx)

    return None