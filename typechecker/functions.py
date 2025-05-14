from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Any

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError, NetLangTypeError, UndefinedFunctionError, UndefinedVariableError
from shared.model.Function import Function
from shared.model.Variable import Variable
from shared.utils.types import check_type, are_types_compatible, is_known_type

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitFunctionCallExpr(self, ctx: NetLangParser.FunctionCallExprContext):
    return self.visit(ctx.functionCall())

def visitFunctionCall(self: "TypeCheckingVisitor", ctx: NetLangParser.FunctionCallContext):
    function_name = ctx.ID().getText()
    call_line = ctx.start.line
    expr_list = ctx.expressionList()
    arg_types = [self.visit(expr) for expr in expr_list.expression()] if expr_list else []

    try:
        function = self.lookup_function(function_name, ctx)
    except UndefinedFunctionError:
        try:
            _ = self.lookup_variable(function_name, ctx)
            raise NetLangTypeError(f"Variable '{function_name}' is not callable", ctx)
        except UndefinedVariableError:
            raise NetLangTypeError(f"Undefined function '{function_name}'", ctx)

    if len(arg_types) != len(function.parameters):
        raise NetLangTypeError(
            f"Function '{function_name}' expects {len(function.parameters)} arguments, got {len(arg_types)}",
            ctx
        )

    for (param_name, param_type), actual_type in zip(function.parameters, arg_types):
        if not are_types_compatible(param_type, actual_type):
            raise NetLangTypeError(
                f"Type mismatch for parameter '{param_name}': expected {param_type}, got {actual_type}",
                ctx
            )

    self.current_call_line = call_line
    if function_name not in self.currently_checking_functions:
        self.currently_checking_functions.add(function_name)
        self.execute_function_body(function_name, function)
        self.currently_checking_functions.remove(function_name)
    self.current_call_line = None

    return function.return_type or "void"

def visitReturnStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.ReturnStatementContext):
    if not self.in_function_body:
        raise NetLangTypeError("Cannot use 'return' statement outside of a function", ctx)

    if self.expected_return_type is None:
        raise NetLangTypeError("Return value not allowed in function with no declared return type (assumed 'void')", ctx)

    if ctx.expression():
        value_type = self.visit(ctx.expression())

        if self.expected_return_type == "void":
            raise NetLangTypeError(
                message=f"Return value not allowed in function returning 'void'",
                ctx=ctx
            )

        if not are_types_compatible(self.expected_return_type, value_type):
            raise NetLangTypeError(
                message=f"Return type mismatch: expected {self.expected_return_type}, got {value_type}",
                ctx=ctx
            )

        return value_type

    else:
        if self.expected_return_type != "void":
            raise NetLangTypeError(
                message=f"Return value required in function returning {self.expected_return_type}",
                ctx=ctx
            )

        return "void"

    self.return_found = True

def visitFunctionDeclarationStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.FunctionDeclarationStatementContext):
    function_name: str = ctx.ID().getText()
    return_type: str = ctx.type_().getText() if ctx.type_() else "void"
    line: int = ctx.start.line

    if not is_known_type(return_type):
        raise NetLangTypeError(f"Unknown return type '{return_type}' for function '{function_name}", ctx)

    parameters = []

    parameter_list = ctx.parameterList()
    if parameter_list:
        for param_ctx in parameter_list.parameter():
            param_name = param_ctx.ID().getText()
            param_type = param_ctx.type_().getText()

            if not is_known_type(param_type):
                raise NetLangTypeError(f"Unknown type '{param_type}' for parameter '{param_name}'", ctx)

            parameters.append((param_name, param_type))

    function = Function(
        parameters=parameters,
        return_type=return_type,
        line_declared=line,
        body_ctx=ctx.block()
    )

    self.declare_function(function_name, function, ctx)

def check_all_function_bodies(self: "TypeCheckingVisitor"):
    for scope in self.scopes:
        for name, function in scope.functions.items():
            if name in self.currently_checking_functions:
                continue
            self.currently_checking_functions.add(name)
            self.disable_line_checks = True
            self.execute_function_body(name, function)
            self.disable_line_checks = False
            self.currently_checking_functions.remove(name)

def execute_function_body(self: "TypeCheckingVisitor", name: str, function: Function):
    self.push_scope()
    for param_name, param_type in function.parameters:
        self.declare_variable(param_name, Variable(param_type, function.line_declared), None)

    self.in_function_body = True
    self.expected_return_type = function.return_type
    return_type = self.block_returns_type(function.body_ctx)
    self.in_function_body = False
    self.expected_return_type = None
    self.pop_scope()

    if function.return_type != "void" and return_type is None:
        raise NetLangTypeError(
            f"Function '{name}' declares return type '{function.return_type}' but not all control paths return a value"
        )

def block_returns_type(self, block_ctx) -> Optional[str]:
    for stmt in block_ctx.statement():
        return_type = self.visit(stmt)
        if return_type is not None:
            return return_type
    return None
