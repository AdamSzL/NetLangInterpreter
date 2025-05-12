from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError, NetLangTypeError
from typing import TYPE_CHECKING

from shared.utils.types import get_field_type, are_types_compatible

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitFieldAccessExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.FieldAccessExprContext):
    return self.visit(ctx.fieldAccess())

def visitFieldAccess(self: "TypeCheckingVisitor", ctx: NetLangParser.FieldAccessContext):
    var_name = ctx.ID(0).getText()
    variable = self.lookup_variable(var_name, ctx)
    current_type = variable.type
    i = 1

    while i < len(ctx.children):
        operator = ctx.getChild(i).getText()

        if operator == ".":
            field_name = ctx.getChild(i + 1).getText()

            if current_type.startswith("[") and current_type.endswith("]") and field_name == "size":
                current_type = "int"
            else:
                current_type = get_field_type(current_type, field_name)

            i += 2

        elif operator == "<":
            index_type = self.visit(ctx.getChild(i + 1))  # expr
            if index_type != "int":
                raise NetLangTypeError("List index must be Int", ctx)

            if not current_type.startswith("[") or not current_type.endswith("]"):
                raise NetLangTypeError(f"Tried to index non-list type '{current_type}'", ctx)

            current_type = current_type[1:-1]  # np. "[Port]" → "Port"

            i += 3

        else:
            raise NetLangTypeError(f"Unknown field access operator '{operator}'", ctx)

    return current_type

def visitFieldAssignment(self: "TypeCheckingVisitor", ctx: NetLangParser.FieldAssignmentContext):
    target_type = self.visit(ctx.fieldAccess())
    value_type = self.visit(ctx.expression())

    if not are_types_compatible(target_type, value_type):
        raise NetLangTypeError(
            f"Cannot assign {value_type} to field of type {target_type}",
            ctx
        )

    return None
