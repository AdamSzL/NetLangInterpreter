from __future__ import annotations

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError, NetLangTypeError, UndefinedFunctionError, UndefinedVariableError
from typing import TYPE_CHECKING, Any

from shared.model.Scope import Scope
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
    expr_type = self.visit(ctx.expression())
    scoped_ctx = ctx.scopedIdentifier()

    var_name = scoped_ctx.ID().getText()

    self.scoped_identifier_expectation = "variable"
    try:
        expected_type = self.visit(scoped_ctx)
    except UndefinedVariableError:
        self.scoped_identifier_expectation = "function"
        try:
            _ = self.visit(scoped_ctx)
            raise NetLangTypeError(f"Cannot assign to function '{var_name}'", ctx)
        except UndefinedFunctionError:
            raise NetLangTypeError(f"Undefined variable '{var_name}'", ctx)
    finally:
        self.scoped_identifier_expectation = None

    if not are_types_compatible(expected_type, expr_type):
        raise NetLangTypeError(
            f"Type mismatch in assignment to variable '{var_name}': expected '{expected_type}', got '{expr_type}'",
            ctx
        )

    return expected_type

def visitScopedIdentifier(self: "TypeCheckingVisitor", ctx: NetLangParser.ScopedIdentifierContext):
    prefix_ctx = ctx.scopePrefix()
    var_name = ctx.ID().getText()
    scopes = self.scopes
    current_index = len(scopes) - 1

    if prefix_ctx:
        prefix = prefix_ctx.getText()
        if prefix.startswith('^'):
            levels_up = len(prefix)
            target_index = current_index - levels_up
            if target_index < 0:
                raise NetLangTypeError(f"Too many '^' levels when accessing identifier '{var_name}'", ctx)
        elif prefix == '~':
            target_index = 0
        else:
            raise NetLangTypeError(f"Unknown scope prefix: '{prefix}'")

        scope = scopes[target_index]
        return self._resolve_identifier_in_scope(scope, var_name, ctx)

    last_error = None
    for scope in reversed(scopes):
        try:
            return self._resolve_identifier_in_scope(scope, var_name, ctx)
        except (UndefinedVariableError, UndefinedFunctionError) as e:
            last_error = e
            continue

    if last_error:
        raise last_error

    raise NetLangTypeError(f"Unknown identifier '{var_name}'", ctx)

def _resolve_identifier_in_scope(self: "TypeCheckingVisitor", scope: Scope, name: str, ctx):
    if self.scoped_identifier_expectation == "variable":
        if name not in scope.variables:
            raise UndefinedVariableError(f"Undefined variable '{name}'", ctx)
        return scope.variables[name].type
    elif self.scoped_identifier_expectation == "function":
        if name not in scope.functions:
            raise UndefinedFunctionError(f"Undefined function '{name}'", ctx)
        return scope.functions[name]
    if name in scope.variables:
        return scope.variables[name].type
    if name in scope.functions:
        return scope.functions[name]
    raise UndefinedVariableError(f"Undefined variable '{name}'", ctx)