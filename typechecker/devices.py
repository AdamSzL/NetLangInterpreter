from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError, NetLangTypeError, UndefinedVariableError, UndefinedFunctionError
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
    scoped_ctx = ctx.scopedIdentifier()
    device_name = scoped_ctx.ID().getText()

    self.scoped_identifier_expectation = "variable"
    try:
        device_type = self.visit(scoped_ctx)
    except UndefinedVariableError:
        self.scoped_identifier_expectation = "function"
        try:
            self.visit(scoped_ctx)
            raise NetLangTypeError(
                message=f"Cannot show interfaces of function '{device_name}'",
                ctx=ctx
            )
        except UndefinedFunctionError:
            raise NetLangTypeError(
                message=f"Undefined variable '{device_name}'",
                ctx=ctx
            )
    finally:
        self.scoped_identifier_expectation = None

    if device_type not in ["Host", "Router", "Switch"]:
        raise NetLangTypeError(
            message=f"'{device_name}' is not a device",
            ctx=ctx
        )

    return None