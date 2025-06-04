from generated.NetLangParser import NetLangParser
from shared.model.Device import Device
from shared.model.Port import Port
from shared.utils.errors import NetLangRuntimeError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitAddToListStatement(self: "Interpreter", ctx: NetLangParser.AddToListStatementContext):
    value = self.visit(ctx.expression())
    field_access_ctx = ctx.fieldAccess()

    parent = self.evaluateParentOfAccess(field_access_ctx)
    target_list = self.visit(field_access_ctx)
    target_list.append(value)

    if isinstance(parent, Device) and isinstance(value, Port):
        raise NetLangRuntimeError(f"Cannot modify ports of the device '{parent.name}'", ctx)

    if hasattr(parent, "validate_logic") and callable(parent.validate_logic):
        parent.validate_logic(ctx)
    return value

def visitDeleteListElementStatement(self: "Interpreter", ctx: NetLangParser.DeleteListElementStatementContext):
    list_obj, index = self.getListAndIndex(ctx.fieldAccess())

    try:
        del list_obj[index]
    except IndexError:
        raise NetLangRuntimeError(f"Index {index} is out of range for list of length {len(list_obj)}", ctx)

def visitListLiteral(self: "Interpreter", ctx: NetLangParser.ListLiteralContext):
    return [self.visit(expr) for expr in ctx.expressionList().expression()] if ctx.expressionList() else []

def getListAndIndex(self: "Interpreter", ctx: NetLangParser.FieldAccessContext):
    list_obj = self.evaluateFieldAccessUntil(ctx, stop_before_last_index=True)

    last_index = None
    for i in range(1, len(ctx.children)):
        if ctx.getChild(i).getText() == "<":
            last_index = self.visit(ctx.getChild(i + 1))

    return list_obj, last_index