from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError, NetLangTypeError

from typing import TYPE_CHECKING

from shared.utils.types import are_types_compatible, find_common_supertype

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitAddToListStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.AddToListStatementContext):
    value_type = self.visit(ctx.expression())
    list_type: str = self.visit(ctx.fieldAccess())

    if not list_type.startswith("[") or not list_type.endswith("]"):
        raise NetLangTypeError("Target of 'add' must be a list", ctx)

    element_type = list_type[1:-1]
    if not are_types_compatible(element_type, value_type):
        raise NetLangTypeError(f"Cannot add element of type {value_type} to list of {element_type}", ctx)

    return None

def visitDeleteListElementStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.DeleteListElementStatementContext):
    scoped_ctx = ctx.listIndexAccess().scopedIdentifier()
    list_type = self.visit(scoped_ctx)

    if not list_type.startswith("[") or not list_type.endswith("]"):
        raise NetLangTypeError("Target of 'delete' must be a list", ctx)
    return None

def visitListLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.ListLiteralContext):
    element_types = []

    if ctx.expressionList():
        for expr in ctx.expressionList().expression():
            element_types.append(self.visit(expr))

    if not element_types:
        if self.expected_type and self.expected_type.startswith("[") or self.expected_type.endswith("]"):
            return self.expected_type
        raise NetLangTypeError("Cannot infer type of empty list", ctx)

    common_type = find_common_supertype(element_types)
    if not common_type:
        raise NetLangTypeError(
            f"List contains incompatible element types: {', '.join(set(element_types))}",
            ctx
        )

    return f"[{common_type}]"

def visitListIndexAccess(self: "TypeCheckingVisitor", ctx: NetLangParser.ListIndexAccessContext):
    scoped_ctx = ctx.scopedIdentifier()
    list_type = self.visit(scoped_ctx)
    var_name = scoped_ctx.ID().getText()

    index_type = self.visit(ctx.expression())
    if index_type != "int":
        raise NetLangTypeError("List index must be of type int", ctx)

    if not list_type.startswith("[") or not list_type.endswith("]"):
        raise NetLangTypeError(f"Variable '{var_name}' is not a list", ctx)

    return list_type[1:-1]

def visitListIndexAssignment(self: "TypeCheckingVisitor", ctx: NetLangParser.ListIndexAssignmentContext):
    scoped_ctx = ctx.listIndexAccess().scopedIdentifier()
    list_type = self.visit(scoped_ctx)

    index_type = self.visit(ctx.listIndexAccess().expression())
    value_type = self.visit(ctx.expression())
    var_name = scoped_ctx.ID().getText()

    if not list_type.startswith("[") or not list_type.endswith("]"):
        raise NetLangTypeError(f"Variable '{var_name}' is not a list", ctx)

    if index_type != "int":
        raise NetLangTypeError("List index must be of type int", ctx)

    element_type = list_type[1:-1]
    if not are_types_compatible(element_type, value_type):
        raise NetLangTypeError(
            f"Cannot assign {value_type} to element of type {element_type} in list '{var_name}'",
            ctx
        )

    return None
