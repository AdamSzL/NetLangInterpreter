from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitAddToListStatement(self: "Interpreter", ctx: NetLangParser.AddToListStatementContext):
    value = self.visit(ctx.expression())
    target_list = self.visit(ctx.fieldAccess())
    target_list.append(value)
    return value

def visitDeleteListElementStatement(self: "Interpreter", ctx: NetLangParser.DeleteListElementStatementContext):
    list_name, index = self.getListAndIndex(ctx.listIndexAccess())
    try:
        self.variables[list_name].value.pop(index)
    except IndexError:
        raise NetLangRuntimeError(f"Index {index} out of range for list {list_name}", ctx)

def visitListLiteral(self: "Interpreter", ctx: NetLangParser.ListLiteralContext):
    return [self.visit(expr) for expr in ctx.expressionList().expression()] if ctx.expressionList() else []

def visitListIndexAccess(self: "Interpreter", ctx: NetLangParser.ListIndexAccessContext):
    list_name, index = self.getListAndIndex(ctx)
    try:
        return self.variables[list_name].value[index]
    except IndexError:
        raise NetLangRuntimeError(f"Index {index} out of range for list {list_name}", ctx)

def visitListIndexAssignment(self: "Interpreter", ctx: NetLangParser.ListIndexAssignmentContext):
    list_access = ctx.listIndexAccess()
    list_name = list_access.ID().getText()
    index = self.visit(list_access.expression())
    value = self.visit(ctx.expression())

    lst = self.variables.get(list_name)

    if index >= len(lst.value):
        raise NetLangRuntimeError(f"Index {index} out of range for list '{list_name}'", ctx)

    lst.value[index] = value

def getListAndIndex(self: "Interpreter", ctx: NetLangParser.ListIndexAccessContext) -> tuple[str, int]:
    list_name = ctx.ID().getText()
    index = self.visit(ctx.expression())

    if list_name not in self.variables:
        raise NetLangRuntimeError(f"Undefined list {list_name}", ctx)

    list_var = self.variables[list_name]

    if not isinstance(list_var.value, list):
        raise NetLangRuntimeError(f"{list_name} is not a list", ctx)

    if type(index) is not int:
        raise NetLangRuntimeError(
            f"List index must be an integer, got {type(index).__name__} instead",
            ctx
        )

    return list_name, index