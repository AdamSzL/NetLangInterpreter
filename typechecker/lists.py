from generated.NetLangParser import NetLangParser
from shared.utils.errors import NetLangTypeError

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
    field_access_ctx = ctx.fieldAccess()

    if not self.was_last_operator_indexing(field_access_ctx):
        raise NetLangTypeError("Delete can only be used on a list element (index access required)", ctx)

    self.visit(field_access_ctx)
    return None

def visitListLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.ListLiteralContext):
    element_types = []

    if ctx.expressionList():
        for expr in ctx.expressionList().expression():
            element_types.append(self.visit(expr))

    if not element_types:
        return "[]"

    common_type = find_common_supertype(element_types)
    if not common_type:
        raise NetLangTypeError(
            f"List contains incompatible element types: {', '.join(set(element_types))}",
            ctx
        )

    return f"[{common_type}]"