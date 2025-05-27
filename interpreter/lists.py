from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError
from typing import TYPE_CHECKING

from shared.model.Variable import Variable

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitAddToListStatement(self: "Interpreter", ctx: NetLangParser.AddToListStatementContext):
    value = self.visit(ctx.expression())
    target_list = self.visit(ctx.fieldAccess())
    target_list.append(value)
    return value

def visitDeleteListElementStatement(self: "Interpreter", ctx: NetLangParser.DeleteListElementStatementContext):
    list_var, index, list_name = self.getListAndIndex(ctx.listIndexAccess())
    try:
        del list_var.value[index]
    except IndexError:
        raise NetLangRuntimeError(f"Index {index} out of range for list {list_name}", ctx)

def visitListLiteral(self: "Interpreter", ctx: NetLangParser.ListLiteralContext):
    return [self.visit(expr) for expr in ctx.expressionList().expression()] if ctx.expressionList() else []

def visitListIndexAccess(self: "Interpreter", ctx: NetLangParser.ListIndexAccessContext):
    list_var, index, list_name = self.getListAndIndex(ctx)
    try:
        return list_var.value[index]
    except IndexError:
        raise NetLangRuntimeError(f"Index {index} out of range for list {list_name}", ctx)

def visitListIndexAssignment(self: "Interpreter", ctx: NetLangParser.ListIndexAssignmentContext):
    list_var, index, list_name = self.getListAndIndex(ctx.listIndexAccess())
    value = self.visit(ctx.expression())

    try:
        list_var.value[index] = value
    except IndexError:
        raise NetLangRuntimeError(f"Index {index} out of range for list {list_name}", ctx)

def getListAndIndex(self: "Interpreter", ctx: NetLangParser.ListIndexAccessContext) -> tuple[Variable, int, str]:
    scope, list_name = self.visit(ctx.scopedIdentifier())
    list_var = scope.variables[list_name]
    index = self.visit(ctx.expression())

    if not isinstance(list_var.value, list):
        raise NetLangRuntimeError(f"{list_name} is not a list", ctx)

    if type(index) is not int:
        raise NetLangRuntimeError(
            f"List index must be an integer, got {type(index).__name__} instead",
            ctx
        )

    return list_var, index, list_name