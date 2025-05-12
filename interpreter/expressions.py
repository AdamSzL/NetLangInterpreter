from typing import Any, cast

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError
from shared.model.Variable import Variable
from shared.utils.types import type_map
from shared.model import ConnectorType, Protocol, IPAddress, MACAddress, CIDR
from shared.model.base import NetLangObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitAtomExpr(self: "Interpreter", ctx: NetLangParser.AtomExprContext):
    return self.visitChildren(ctx)

def visitIntLiteral(self: "Interpreter", ctx: NetLangParser.IntLiteralContext) -> int:
    return int(ctx.INT().getText())

def visitFloatLiteral(self: "Interpreter", ctx: NetLangParser.FloatLiteralContext) -> float:
    return float(ctx.FLOAT().getText())

def visitBoolLiteral(self: "Interpreter", ctx: NetLangParser.BoolLiteralContext) -> bool:
    return ctx.BOOL().getText() == "true"

def visitStringLiteral(self: "Interpreter", ctx: NetLangParser.StringLiteralContext) -> str:
    return str(ctx.STRING().getText().strip('"'))

def visitVariableExpr(self: "Interpreter", ctx: NetLangParser.VariableExprContext):
    variable_name: str = ctx.ID().getText()
    if variable_name in ConnectorType.__members__:
        return ConnectorType[variable_name]
    if variable_name in Protocol.__members__:
        return Protocol[variable_name]

    variable = self.lookup_variable(variable_name, ctx)
    return variable.value

def visitIPAddressLiteral(self: "Interpreter", ctx: NetLangParser.IPAddressLiteralContext) -> IPAddress:
    return IPAddress(ctx.IPADDR().getText())

def visitMacAddressLiteral(self: "Interpreter", ctx: NetLangParser.MacAddressLiteralContext) -> MACAddress:
    return MACAddress(ctx.MACADDR().getText())

def visitListLiteralExpr(self: "Interpreter", ctx: NetLangParser.ListLiteralExprContext) -> list:
    return self.visit(ctx.listLiteral())

def visitCIDRLiteralExpr(self: "Interpreter", ctx: NetLangParser.CIDRLiteralExprContext) -> CIDR:
    return self.visit(ctx.cidrLiteral())

def visitObjectInitializerExpr(self: "Interpreter", ctx: NetLangParser.ObjectInitializerExprContext) -> NetLangObject:
    return self.visit(ctx.objectInitializer())

def visitListIndexAccessExpr(self: "Interpreter", ctx: NetLangParser.ListIndexAccessExprContext):
    return self.visit(ctx.listIndexAccess())


def visitObjectInitializer(self: "Interpreter", ctx: NetLangParser.ObjectInitializerContext):
    obj = {}
    for field in ctx.objectFieldList().objectField():
        name = field.ID().getText()
        value = self.visit(field.expression())
        obj[name] = value
    if ctx.objectType():
        type_name = ctx.objectType().getText()
        if type_name in type_map and issubclass(type_map[type_name], NetLangObject):
            obj_from_dict = type_map[type_name].from_dict(obj, ctx)
            return obj_from_dict
        else:
            raise NetLangRuntimeError(
                f"Unknown object type '{type_name}'",
                ctx
            )
    return obj

def visitCidrLiteral(self: "Interpreter", ctx: NetLangParser.CidrLiteralContext):
    if ctx.ID():  # np. [routerIP]/24
        var_name: str = ctx.ID().getText()
        ip_var: Variable = self.lookup_variable(var_name, ctx)

        if not isinstance(ip_var.value, IPAddress):
            raise NetLangRuntimeError(f"Variable '{var_name}' is not an IP address", ctx)

        mask = int(ctx.INT().getText())
        return CIDR(cast(IPAddress, ip_var.value), mask)

    else:
        ip: IPAddress = IPAddress(ctx.IPADDR().getText())
        mask: int = int(ctx.INT().getText())
        return CIDR(ip, mask)