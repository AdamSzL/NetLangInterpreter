from typing import TYPE_CHECKING

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangTypeError, NetLangRuntimeError
from shared.model import CIDR
from shared.model.base import NetLangObject
from shared.utils.types import type_map

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitAtomExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.AtomExprContext):
    return self.visitChildren(ctx)

def visitIntLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.IntLiteralContext) -> str:
    return "int"

def visitFloatLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.FloatLiteralContext) -> str:
    return "float"

def visitBoolLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.BoolLiteralContext) -> str:
    return "bool"

def visitStringLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.StringLiteralContext) -> str:
    return "string"

def visitVariableExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.VariableExprContext):
    variable_name: str = ctx.ID().getText()
    if variable_name not in self.variables:
        raise NetLangTypeError(f"Undefined variable '{variable_name}'", ctx)
    line = ctx.start.line
    if line == self.variables[variable_name].line_declared:
        raise NetLangTypeError(
            f"Error: Variable '{variable_name}' cannot be used on the same line it is declared",
            ctx
        )
    if line < self.variables[variable_name].line_declared:
        raise NetLangTypeError(
            f"Variable '{variable_name}' used before its declaration (declared at line {self.variables[variable_name].line_declared}, used at line {line})",
            ctx
        )
    return self.variables[variable_name].type

def visitIPAddressLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.IPAddressLiteralContext) -> str:
    return "IP"

def visitMacAddressLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.MacAddressLiteralContext) -> str:
    return "MAC"

def visitListLiteralExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.ListLiteralExprContext) -> list:
    return self.visit(ctx.listLiteral())

def visitCIDRLiteralExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.CIDRLiteralExprContext) -> CIDR:
    return self.visit(ctx.cidrLiteral())

def visitObjectInitializerExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.ObjectInitializerExprContext) -> NetLangObject:
    return self.visit(ctx.objectInitializer())

def visitListIndexAccessExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.ListIndexAccessExprContext):
    return self.visit(ctx.listIndexAccess())


def visitObjectInitializer(self: "TypeCheckingVisitor", ctx: NetLangParser.ObjectInitializerContext):
    if not ctx.objectType() and not ctx.deviceType():
        if self.expected_type:
            return self.expected_type
        raise NetLangTypeError("Missing object type in initializer", ctx)

    if ctx.objectType():
        type_name = ctx.objectType().getText()
        if type_name not in type_map:
            raise NetLangTypeError(f"Unknown object type '{type_name}'", ctx)

        return type_name
    elif ctx.deviceType():
        type_name = ctx.deviceType().getText()
        if type_name not in type_map:
            raise NetLangTypeError(f"Unknown device type '{type_name}'", ctx)

        return type_name

def visitCidrLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.CidrLiteralContext):
    return "CIDR"