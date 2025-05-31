from __future__ import annotations

from generated.NetLangParser import NetLangParser
from shared.model.Port import Port
from shared.model.Scope import Scope
from shared.model.Variable import Variable
from shared.model.base import NetLangObject
from shared.errors import NetLangRuntimeError
from shared.utils.types import type_map
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitVariableDeclaration(self: "Interpreter", ctx: NetLangParser.VariableDeclarationContext):
    name: str = ctx.ID().getText()
    declared_type: str = ctx.type_().getText()
    value = self.visit(ctx.expression())

    if isinstance(value, dict) and declared_type in type_map and issubclass(type_map[declared_type], NetLangObject):
        value = type_map[declared_type].from_dict(value, ctx)

        if isinstance(value, Port) and value.ip is not None and value.mac is not None:
            self.arp_table[str(value.ip.ip)] = value.mac.mac

    self.declare_variable(name, Variable(declared_type, ctx.start.line, value=value), ctx)
    self.assign_device_uids(value)
    return value

def visitVariableAssignment(self: "Interpreter", ctx: NetLangParser.VariableAssignmentContext):
    scope, var_name = self.visit(ctx.scopedIdentifier())
    value = self.visit(ctx.expression())

    scope.variables[var_name].value = value
    return value

def visitScopedIdentifier(self: "Interpreter", ctx: NetLangParser.ScopedIdentifierContext) -> (Scope, str):
    prefix_ctx = ctx.scopePrefix()
    var_name = ctx.ID().getText()
    scopes = self.scopes
    current_index = len(scopes) - 1

    if prefix_ctx:
        prefix = prefix_ctx.getText()
        if prefix.startswith("^"):
            levels_up = len(prefix)
            target_index = current_index - levels_up
        else:  # ~
            target_index = 0

        scope = scopes[target_index]
        return scope, var_name

    for scope in reversed(scopes):
        if var_name in scope.variables or var_name in scope.functions:
            return scope, var_name

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
