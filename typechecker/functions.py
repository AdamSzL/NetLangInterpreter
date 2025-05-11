from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Any

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError, NetLangTypeError
from shared.utils.types import check_type, are_types_compatible
from .variables import Variable

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

@dataclass
class Function:
    parameters: list[tuple[str, str]]
    return_type: Optional[str]
    line_declared: int
    body_ctx: Any

@dataclass
class ReturnValue(Exception):
    value: Any

def visitFunctionCallExpr(self, ctx: NetLangParser.FunctionCallExprContext):
    return self.visit(ctx.functionCall())

def visitFunctionCall(self: "TypeCheckingVisitor", ctx: NetLangParser.FunctionCallContext):
    function_name = ctx.ID().getText()
    expr_list = ctx.expressionList()
    arg_types = [self.visit(expr) for expr in expr_list.expression()] if expr_list else []

    if function_name not in self.functions:
        if function_name in self.variables:
            raise NetLangTypeError(f"Variable '{function_name}' is not callable", ctx)
        raise NetLangTypeError(f"Undefined function '{function_name}'", ctx)

    function = self.functions[function_name]

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

    return function.return_type or "Void"

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

    else:
        if self.expected_return_type != "void":
            raise NetLangTypeError(
                message=f"Return value required in function returning {self.expected_return_type}",
                ctx=ctx
            )

    self.return_found = True

def visitFunctionDeclarationStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.FunctionDeclarationStatementContext):
    pass

def check_all_function_bodies(self):
    for name, function in self.functions.items():
        # self.enter_new_scope()
        previous_variables = self.variables.copy()
        for param_name, param_type in function.parameters:
            self.variables[param_name] = Variable(param_type, -1, 0)

        self.in_function_body = True
        self.expected_return_type = function.return_type
        self.return_found = False

        self.visit(function.body_ctx)

        self.in_function_body = False

        if self.expected_return_type and not self.return_found and self.expected_return_type != "void":
            raise NetLangTypeError(
                f"Function '{name}' declares return type '{self.expected_return_type}' but no return was found"
            )

        self.expected_return_type = None
        self.variables = previous_variables

        # self.exit_scope()