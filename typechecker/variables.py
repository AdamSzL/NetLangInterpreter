from __future__ import annotations
from generated.NetLangParser import NetLangParser
from shared.utils.errors import NetLangTypeError, UndefinedFunctionError, UndefinedVariableError
from typing import TYPE_CHECKING
from shared.model.Scope import Scope
from shared.model.Variable import Variable
from shared.utils.types import are_types_compatible
import difflib

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitVariableDeclaration(self: "TypeCheckingVisitor", ctx: NetLangParser.VariableDeclarationContext):
    name: str = ctx.ID().getText()
    has_type = ctx.type_() is not None
    has_expr = ctx.expression() is not None

    if not has_type and not has_expr:
        raise NetLangTypeError(
            f"Variable '{name}' must have either a type or a value (or both)",
            ctx
        )

    if has_type and not has_expr:
        declared_type = ctx.type_().getText()
        if declared_type == "void":
            raise NetLangTypeError("Cannot declare variable of type 'void'", ctx)
        self.declare_variable(name, Variable(declared_type, ctx.start.line), ctx)
        return None

    if has_type and has_expr:
        declared_type = ctx.type_().getText()
        if declared_type == "void":
            raise NetLangTypeError("Cannot declare variable of type 'void'", ctx)
        expr_type = self.visit(ctx.expression())
        if not are_types_compatible(declared_type, expr_type):
            raise NetLangTypeError(
                f"Type mismatch: cannot assign {expr_type} to variable '{name}' of type {declared_type}",
                ctx
            )
        self.declare_variable(name, Variable(declared_type, ctx.start.line), ctx)
        return None

    expr_type = self.visit(ctx.expression())
    if expr_type == "[]":
        raise NetLangTypeError(
            "Cannot infer type of empty list — please provide explicit type",
            ctx
        )
    self.declare_variable(name, Variable(expr_type, ctx.start.line), ctx)
    return None

def visitVariableAssignment(self: "TypeCheckingVisitor", ctx: NetLangParser.VariableAssignmentContext):
    scoped_ctx = ctx.scopedIdentifier()
    var_name = scoped_ctx.ID().getText()

    self.scoped_identifier_expectation = "variable"
    try:
        expected_type = self.visit(scoped_ctx)
    except UndefinedVariableError as undefined_variable_error:
        self.scoped_identifier_expectation = "function"
        try:
            _ = self.visit(scoped_ctx)
            raise NetLangTypeError(f"Cannot assign to function '{var_name}'", ctx)
        except UndefinedFunctionError:
            raise undefined_variable_error
    finally:
        self.scoped_identifier_expectation = None

    expr_type = self.visit(ctx.expression())
    if not are_types_compatible(expected_type, expr_type):
        raise NetLangTypeError(
            f"Type mismatch in assignment to variable '{var_name}': expected '{expected_type}', got '{expr_type}'",
            ctx
        )

    return expected_type

def visitScopedIdentifier(self: "TypeCheckingVisitor", ctx: NetLangParser.ScopedIdentifierContext):
    prefix_ctx = ctx.scopePrefix()
    var_name = ctx.ID().getText()
    scope = self.scopes[-1]

    if prefix_ctx:
        prefix = prefix_ctx.getText()
        if prefix.startswith('^'):
            self.refers_to_outer_scope = True
            levels_up = len(prefix)
            for _ in range(levels_up):
                if scope.parent is None:
                    raise NetLangTypeError(f"Too many '^' levels when accessing identifier '{var_name}'", ctx)
                scope = scope.parent

            return self._resolve_identifier_recursive(scope, var_name, ctx)
        elif prefix == '~':
            while scope.parent is not None:
                scope = scope.parent
            return self._resolve_identifier_recursive(scope, var_name, ctx)
        raise NetLangTypeError(f"Unknown scope prefix: '{prefix}'")

    return self._resolve_identifier_recursive(scope, var_name, ctx)

def _resolve_identifier_recursive(self: "TypeCheckingVisitor", scope: Scope, name: str, ctx):
    error = None
    if self.scoped_identifier_expectation == "variable":
        if name in scope.variables:
            return scope.variables[name].type
        error = UndefinedVariableError(f"Undefined variable '{name}'", ctx)
    elif self.scoped_identifier_expectation == "function":
        if name in scope.functions:
            return scope.functions[name]
        error = UndefinedFunctionError(f"Undefined function '{name}'", ctx)
    elif name in scope.variables:
        return scope.variables[name].type
    elif name in scope.functions:
        return scope.functions[name]

    if scope.parent:
        return self._resolve_identifier_recursive(scope.parent, name, ctx)
    else:
        if error:
            all_names = set()
            current = scope
            while current:
                all_names.update(current.variables.keys())
                all_names.update(current.functions.keys())
                current = current.parent

            suggestions = difflib.get_close_matches(name, all_names, n=1, cutoff=0.6)
            if suggestions:
                suggestion = suggestions[0]
                if isinstance(error, UndefinedVariableError):
                    raise UndefinedVariableError(f"{error.message}. Did you mean '{suggestion}'?")
                elif isinstance(error, UndefinedFunctionError):
                    raise UndefinedFunctionError(f"{error.message}. Did you mean '{suggestion}'?")

            raise error
        raise UndefinedVariableError(f"Undefined identifier'{name}'", ctx)