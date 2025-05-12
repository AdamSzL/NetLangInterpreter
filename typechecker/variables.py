from __future__ import annotations

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError, NetLangTypeError
from typing import TYPE_CHECKING, Any

from shared.model.Variable import Variable
from shared.utils.types import is_known_type, are_types_compatible

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitVariableDeclaration(self: "TypeCheckingVisitor", ctx: NetLangParser.VariableDeclarationContext):
    name: str = ctx.ID().getText()
    declared_type: str = ctx.type_().getText()

    if not is_known_type(declared_type):
        raise NetLangTypeError(f"Unknown type '{declared_type}'", ctx)

    if declared_type == "void":
        raise NetLangTypeError("Cannot declare variable of type 'void'", ctx)

    self.expected_type = declared_type
    try:
        expr_type: str = self.visit(ctx.expression())
    finally:
        self.expected_type = None

    if not are_types_compatible(declared_type, expr_type):
        raise NetLangTypeError(
            f"Type mismatch: cannot assign {expr_type} to variable '{name}' of type {declared_type}",
            ctx
        )

    self.declare_variable(name, Variable(declared_type, ctx.start.line), ctx)
    return declared_type

def visitVariableAssignment(self: "TypeCheckingVisitor", ctx: NetLangParser.VariableAssignmentContext):
    name = ctx.ID().getText()
    expr_type = self.visit(ctx.expression())

    variable = self.lookup_variable(name, ctx)
    expected_type = variable.type

    if not are_types_compatible(expected_type, expr_type):
        raise NetLangTypeError(
            f"Type mismatch in assignment to variable '{name}': expected '{expected_type}', got '{expr_type}'",
            ctx
        )

    return expected_type