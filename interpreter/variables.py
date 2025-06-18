from __future__ import annotations

from generated.NetLangParser import NetLangParser
from shared.model.Scope import Scope
from shared.model.Variable import Variable
from shared.utils.errors import NetLangRuntimeError
from shared.utils.types import get_typename
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitVariableDeclaration(self: "Interpreter", ctx: NetLangParser.VariableDeclarationContext):
    name: str = ctx.ID().getText()
    has_type = ctx.type_() is not None
    has_expr = ctx.expression() is not None

    if has_type and not has_expr:
        declared_type = ctx.type_().getText()
        self.declare_variable(name, Variable(declared_type, ctx.start.line, value=None), ctx)
        return None

    value = self.visit(ctx.expression())
    if has_type:
        declared_type = ctx.type_().getText()
    else:
        declared_type = get_typename(value)

    self.declare_variable(name, Variable(declared_type, ctx.start.line, value=value), ctx)
    return value

def visitVariableAssignment(self: "Interpreter", ctx: NetLangParser.VariableAssignmentContext):
    scope, var_name = self.visit(ctx.scopedIdentifier())
    value = self.visit(ctx.expression())

    scope.variables[var_name].value = value
    return value

def visitScopedIdentifier(self: "Interpreter", ctx: NetLangParser.ScopedIdentifierContext) -> (Scope, str):
    prefix_ctx = ctx.scopePrefix()
    var_name = ctx.ID().getText()
    scope = self.scopes[-1]

    if prefix_ctx:
        prefix = prefix_ctx.getText()
        if prefix.startswith("^"):
            levels_up = len(prefix)
            for _ in range(levels_up):
                scope = scope.parent
        else:
            while scope.parent is not None:
                scope = scope.parent

    s = scope
    while s:
        if var_name in s.variables or var_name in s.functions:
            return s, var_name
        s = s.parent

    raise NetLangRuntimeError(f"Identifier '{var_name}' not found (should be impossible at runtime)")

def assign_device_uids(self: "Interpreter", value):
    if isinstance(value, list):
        for item in value:
            if hasattr(item, "uid"):
                item.uid = self.generate_uid()
    else:
        if hasattr(value, "uid"):
            value.uid = self.generate_uid()

def generate_uid(self: "Interpreter") -> str:
    while True:
        uid = f"device_{uuid.uuid4().hex[:8]}"
        if uid not in self.used_ids:
            self.used_ids.add(uid)
            return uid
