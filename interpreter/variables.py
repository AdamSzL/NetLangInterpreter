from __future__ import annotations

from generated.NetLangParser import NetLangParser
from shared.model.Variable import Variable
from shared.model.base import NetLangObject
from shared.errors import NetLangRuntimeError
from shared.utils.types import type_map, check_type
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitVariableDeclaration(self: "Interpreter", ctx: NetLangParser.VariableDeclarationContext):
    name: str = ctx.ID().getText()
    declared_type: str = ctx.type_().getText()
    value = self.visit(ctx.expression())

    if isinstance(value, dict) and declared_type in type_map and issubclass(type_map[declared_type], NetLangObject):
        value = type_map[declared_type].from_dict(value, ctx)

    if not check_type(declared_type, value):
        raise NetLangRuntimeError(
            f"Type mismatch: cannot assign {type(value).__name__} to variable '{name}' of type {declared_type}",
            ctx
        )

    self.declare_variable(name, Variable(declared_type, ctx.start.line, value=value), ctx)
    return value

def visitVariableAssignment(self: "Interpreter", ctx: NetLangParser.VariableAssignmentContext):
    name = ctx.ID().getText()
    value = self.visit(ctx.expression())

    variable = self.lookup_variable(name, ctx)
    expected_type = variable.type
    if not check_type(expected_type, value):
        raise NetLangRuntimeError(
            f"Type mismatch in assignment to variable '{name}': expected '{expected_type}', got '{type(value).__name__}'",
            ctx
        )

    variable.value = value
    return value
