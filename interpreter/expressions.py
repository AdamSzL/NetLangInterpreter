from typing import Any, cast

from generated.NetLangParser import NetLangParser
from .errors import NetLangRuntimeError
from .utils import ensure_numeric
from .types import type_map
from model import ConnectorType, Protocol, IPAddress, MACAddress, CIDR
from model.base import NetLangObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitAtomExpr(self: "Interpreter", ctx: NetLangParser.AtomExprContext):
    return self.visitChildren(ctx)

def visitNegateExpr(self, ctx):
    if ctx.negateExpr():  # jeśli jest negacja (MINUS negateExpr)
        value = self.visit(ctx.negateExpr())
        ensure_numeric(value, ctx, operator='-')
        return -value
    else:
        return self.visit(ctx.atomExpr())

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
    if variable_name not in self.variables:
        raise NetLangRuntimeError(f"Undefined variable '{variable_name}'", ctx)
    line = ctx.start.line
    if line == self.variables[variable_name].line_declared:
        raise NetLangRuntimeError(
            message=f"Error: Variable '{variable_name}' cannot be used on the same line it is declared",
            ctx=ctx
        )
    if line < self.variables[variable_name].line_declared:
        raise NetLangRuntimeError(
            message=f"Variable '{variable_name}' used before its declaration (declared at line {self.variables[variable_name].line_declared}, used at line {line})",
            ctx=ctx
        )
    return self.variables[variable_name].value

def visitListLiteralExpr(self: "Interpreter", ctx: NetLangParser.ListLiteralExprContext) -> list:
    return self.visit(ctx.listLiteral())

def visitIPAddressLiteralExpr(self: "Interpreter", ctx: NetLangParser.IPAddressLiteralContext) -> IPAddress:
    return IPAddress(ctx.IPADDR().getText())

def visitCIDRLiteralExpr(self: "Interpreter", ctx: NetLangParser.CIDRLiteralExprContext) -> CIDR:
    return self.visit(ctx.cidrLiteral())

def visitMacAddressLiteralExpr(self: "Interpreter", ctx: NetLangParser.MacAddressLiteralContext) -> MACAddress:
    return MACAddress(ctx.MAC().getText())

def visitObjectInitializerExpr(self: "Interpreter", ctx: NetLangParser.ObjectInitializerExprContext) -> NetLangObject:
    return self.visit(ctx.objectInitializer())

def visitFieldAccessExpr(self: "Interpreter", ctx: NetLangParser.FieldAccessExprContext):
    return self.visit(ctx.fieldAccess())

def visitListIndexAccessExpr(self: "Interpreter", ctx: NetLangParser.ListIndexAccessExprContext):
    return self.visit(ctx.listIndexAccess())

def visitFieldAccess(self: "Interpreter", ctx: NetLangParser.FieldAccessContext):
    # Zacznij od pierwszego identyfikatora (np. "h1")
    current = self.variables.get(ctx.ID(0).getText())
    if current is None:
        raise NetLangRuntimeError(f"Variable '{ctx.ID(0).getText()}' not defined")

    i = 1
    while i < len(ctx.children):
        operator = ctx.getChild(i).getText()

        if operator == ".":
            field_name = ctx.getChild(i + 1).getText()

            if isinstance(current, list) and field_name == "size":
                current = len(current)
            elif hasattr(current, field_name):
                current = getattr(current, field_name)
            else:
                raise NetLangRuntimeError(
                    f"Object of type {type(current).__name__} has no field '{field_name}'"
                )

            i += 2  # przeskocz kropkę i ID

        elif operator == "<":
            expression_ctx = ctx.getChild(i + 1)
            index = int(self.visit(expression_ctx))
            if not isinstance(current, list):
                raise NetLangRuntimeError(
                    f"Trying to index non-list object of type {type(current).__name__}"
                )
            try:
                current = current[index]
            except IndexError:
                raise NetLangRuntimeError(f"Index {index} out of range")

            i += 3  # przeskocz < expression >

        else:
            raise NetLangRuntimeError(f"Unknown field access operator '{operator}'")

    return current

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
                message=f"Unknown object type '{type_name}'",
                ctx=ctx
            )
    return obj

def visitCidrLiteral(self: "Interpreter", ctx: NetLangParser.CidrLiteralContext):
    if ctx.ID():  # np. [routerIP]/24
        var_name: str = ctx.ID().getText()
        ip: Any = self.variables.get(var_name)

        if not isinstance(ip, IPAddress):
            raise NetLangRuntimeError(f"Variable '{var_name}' is not an IP address", ctx)

        mask = int(ctx.INT().getText())
        return CIDR(cast(IPAddress, ip), mask)

    else:
        ip: IPAddress = IPAddress(ctx.IPADDR().getText())
        mask: int = int(ctx.INT().getText())
        return CIDR(ip, mask)