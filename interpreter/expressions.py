from typing import Any, cast

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError
from shared.model.Port import Port
from shared.model.Variable import Variable
from shared.utils.types import type_map
from shared.model import ConnectorType, IPAddress, MACAddress, CIDR
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
    name = ctx.scopedIdentifier().ID().getText()

    if name in ConnectorType.__members__:
        return ConnectorType[name]

    scope, var_name = self.visit(ctx.scopedIdentifier())
    if scope.variables[var_name].value is None:
        raise NetLangRuntimeError(f"Variable '{var_name}' is used before being initialized", ctx)
    return scope.variables[var_name].value

def visitIPAddressLiteral(self: "Interpreter", ctx: NetLangParser.IPAddressLiteralContext) -> IPAddress:
    return IPAddress(ctx.IPADDR().getText())

def visitMacAddressLiteral(self: "Interpreter", ctx: NetLangParser.MacAddressLiteralContext) -> MACAddress:
    return MACAddress(ctx.MACADDR().getText().upper())

def visitListLiteralExpr(self: "Interpreter", ctx: NetLangParser.ListLiteralExprContext) -> list:
    return self.visit(ctx.listLiteral())

def visitCIDRLiteralExpr(self: "Interpreter", ctx: NetLangParser.CIDRLiteralExprContext) -> CIDR:
    return self.visit(ctx.cidrLiteral())

def visitObjectInitializerExpr(self: "Interpreter", ctx: NetLangParser.ObjectInitializerExprContext) -> NetLangObject:
    return self.visit(ctx.objectInitializer())

def visitObjectInitializer(self: "Interpreter", ctx: NetLangParser.ObjectInitializerContext):
    obj = {}
    for field in ctx.objectFieldList().objectField():
        name = field.ID().getText()
        value = self.visit(field.expression())
        obj[name] = value

    type_name = ctx.objectType().getText()
    result = type_map[type_name].from_dict(obj, ctx)

    if hasattr(result, "uid") and result.uid is None:
        result.uid = self.generate_uid()

    if isinstance(result, Port) and result.ip is not None and result.mac is not None:
        self.arp_table[str(result.ip.ip)] = result.mac.mac

    return result

def visitCidrLiteral(self: "Interpreter", ctx: NetLangParser.CidrLiteralContext):
    if ctx.fieldAccess():
        ip_value = self.visit(ctx.fieldAccess())
    else:
        ip_value = IPAddress(ctx.IPADDR().getText())

    mask: int = int(ctx.INT().getText())

    if not (0 <= mask <= 32):
        raise NetLangRuntimeError(f"CIDR mask must be between 0 and 32, got {mask}", ctx)
    return CIDR(ip_value, mask)