from typing import TYPE_CHECKING

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitFieldAccessExpr(self: "Interpreter", ctx: NetLangParser.FieldAccessExprContext):
    return self.visit(ctx.fieldAccess())

def visitFieldAccess(self: "Interpreter", ctx: NetLangParser.FieldAccessContext):
    # Zacznij od pierwszego identyfikatora (np. "h1")
    var_name = ctx.ID(0).getText()

    if var_name not in self.variables:
        raise NetLangRuntimeError(f"Undefined variable '{var_name}'", ctx)

    current = self.variables.get(var_name).value

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

def visitFieldAssignment(self: "Interpreter", ctx: NetLangParser.FieldAssignmentContext):
    access = ctx.fieldAccess()
    value = self.visit(ctx.expression())

    # Zacznij od pierwszego ID
    current = self.variables.get(access.ID(0).getText())
    if current is None:
        raise NetLangRuntimeError(f"Variable '{access.ID(0).getText()}' not defined")

    # Przechodzimy po chainie, ale ZATRZYMUJEMY się na przedostatnim
    for i in range(1, len(access.children) - 2, 2):
        op = access.getChild(i).getText()
        operand = access.getChild(i + 1)

        if op == ".":
            field = operand.getText()
            if not hasattr(current.value, field):
                raise NetLangRuntimeError(f"'{type(current.value).__name__}' has no field '{field}'")
            current = getattr(current.value, field)

        elif op == "<":
            index = int(self.visit(operand))
            if not isinstance(current.value, list):
                raise NetLangRuntimeError(f"Tried to index non-list object")
            try:
                current = current[index]
            except IndexError:
                raise NetLangRuntimeError(f"Index {index} out of range")

    # Teraz zostały ostatnie dwa elementy: operator + field/index
    last_op = access.getChild(-2).getText()
    last_operand = access.getChild(-1)

    if last_op == ".":
        field_name = last_operand.getText()
        if not hasattr(current.value, field_name):
            raise NetLangRuntimeError(f"'{type(current.value).__name__}' has no field '{field_name}'")
        setattr(current.value, field_name, value)
        return value

    elif last_op == "<":
        index = int(self.visit(last_operand))
        if not isinstance(current.value, list):
            raise NetLangRuntimeError(f"Tried to index non-list object")
        if index >= len(current.value):
            raise NetLangRuntimeError(f"Index {index} out of range")
        current[index] = value
        return value

    raise NetLangRuntimeError(f"Unsupported assignment operator '{last_op}'")