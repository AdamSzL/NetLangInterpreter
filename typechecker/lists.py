from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError, NetLangTypeError

from typing import TYPE_CHECKING

from shared.utils.types import are_types_compatible

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
    var_name = ctx.listIndexAccess().ID().getText()
    variable = self.lookup_variable(var_name, ctx)

    list_type = variable.type
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

    first_type = element_types[0]
    for t in element_types:
        if t != first_type:
            raise NetLangTypeError(f"List contains mixed element types: {first_type} and {t}", ctx)

    return f"[{first_type}]"

def visitListIndexAccess(self: "TypeCheckingVisitor", ctx: NetLangParser.ListIndexAccessContext):
    list_name = ctx.ID().getText()
    index_type = self.visit(ctx.expression())

    if index_type != "int":
        raise NetLangTypeError("List index must be of type int", ctx)

    variable = self.lookup_variable(list_name, ctx)
    list_type = variable.type

    if not list_type.startswith("[") or not list_type.endswith("]"):
        raise NetLangTypeError(f"Variable '{list_name}' is not a list", ctx)

    return list_type[1:-1]

def visitListIndexAssignment(self: "TypeCheckingVisitor", ctx: NetLangParser.ListIndexAssignmentContext):
    list_name = ctx.listIndexAccess().ID().getText()
    index_type = self.visit(ctx.listIndexAccess().expression())
    value_type = self.visit(ctx.expression())

    variable = self.lookup_variable(list_name, ctx)
    list_type = variable.type

    if not list_type.startswith("[") or not list_type.endswith("]"):
        raise NetLangTypeError(f"Variable '{list_name}' is not a list", ctx)

    if index_type != "int":
        raise NetLangTypeError("List index must be of type int", ctx)

    element_type = list_type[1:-1]
    if not are_types_compatible(element_type, value_type):
        raise NetLangTypeError(
            f"Cannot assign {value_type} to element of type {element_type} in list '{list_name}'",
            ctx
        )

    return None
