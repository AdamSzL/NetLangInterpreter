from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError, NetLangTypeError
from typing import TYPE_CHECKING

from shared.model.Function import Function
from shared.utils.types import get_field_type, are_types_compatible, type_field_map

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitFieldAccessExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.FieldAccessExprContext):
    return self.visit(ctx.fieldAccess())

def visitFieldAccess(self: "TypeCheckingVisitor", ctx: NetLangParser.FieldAccessContext):
    return self.evaluate_type_until(ctx, stop_before_last=False)

def visitFieldAssignment(self: "TypeCheckingVisitor", ctx: NetLangParser.FieldAssignmentContext):
    target_type = self.visit(ctx.fieldAccess())
    value_type = self.visit(ctx.expression())

    if not are_types_compatible(target_type, value_type):
        raise NetLangTypeError(
            f"Type mismatch in assignment: expected '{target_type}', got '{value_type}'",
            ctx
        )

    return None

def evaluate_type_of_parent(self: "TypeCheckingVisitor", ctx: NetLangParser.FieldAccessContext) -> str:
    return self.evaluate_type_until(ctx, stop_before_last=True)

def evaluate_type_until(self: "TypeCheckingVisitor", ctx: NetLangParser.FieldAccessContext, stop_before_last: bool = False) -> str:
    current_type = self.visit(ctx.scopedIdentifier())
    if isinstance(current_type, Function):
        raise NetLangTypeError(
            "Functions cannot be used in field access expressions.",
            ctx
        )
    limit = len(ctx.children)

    if stop_before_last:
        last_dot_index = -1
        for j in range(1, len(ctx.children)):
            if ctx.getChild(j).getText() == ".":
                last_dot_index = j
        if last_dot_index == -1:
            return current_type
        limit = last_dot_index

    i = 1
    while i < limit:
        operator = ctx.getChild(i).getText()

        if operator == ".":
            field_name = ctx.getChild(i + 1).getText()
            if current_type.startswith("[") and current_type.endswith("]") and field_name == "size":
                current_type = "int"
            else:
                current_type = get_field_type(current_type, field_name, ctx)
            i += 2

        elif operator == "<":
            index_type = self.visit(ctx.getChild(i + 1))
            if index_type != "int":
                raise NetLangTypeError(f"List index must be of type int (got {index_type} instead)", ctx)

            if not current_type.startswith("[") or not current_type.endswith("]"):
                raise NetLangTypeError(f"Tried to index non-list type '{current_type}'", ctx)

            current_type = current_type[1:-1]
            i += 3

        else:
            raise NetLangTypeError(f"Unknown field access operator '{operator}'", ctx)

    return current_type

def was_last_operator_indexing(self: "TypeCheckingVisitor", ctx: NetLangParser.FieldAccessContext) -> bool:
    i = 1
    last_operator = None
    while i < len(ctx.children):
        operator = ctx.getChild(i).getText()
        if operator in [".", "<"]:
            last_operator = operator
        if operator == ".":
            i += 2
        elif operator == "<":
            i += 3
        else:
            i += 1
    return last_operator == "<"
