from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Any

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError
from shared.utils.types import check_type
from .variables import Variable

if TYPE_CHECKING:
    from .interpreter import Interpreter

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

def visitFunctionCall(self: "Interpreter", ctx: NetLangParser.FunctionCallContext):
    function_name = ctx.ID().getText()
    expr_list = ctx.expressionList()
    args = [self.visit(expr) for expr in expr_list.expression()] if expr_list else []

    if function_name not in self.functions:
        if function_name in self.variables:
            raise NetLangRuntimeError(f"Variable '{function_name}' is not callable", ctx)
        raise NetLangRuntimeError(f"Undefined function '{function_name}'", ctx)

    function = self.functions[function_name]
    if len(args) != len(function.parameters):
        raise NetLangRuntimeError(f"Function '{function_name}' expects {len(function.parameters)} arguments, got {len(args)}", ctx)

    for (param_name, param_type), arg_value in zip(function.parameters, args):
        if not check_type(param_type, arg_value):
            raise NetLangRuntimeError(
                f"Type mismatch for parameter '{param_name}' in call to function '{function_name}': "
                f"expected '{param_type}', got '{type(arg_value).__name__}'",
                ctx
            )

    previous_variables = self.variables.copy()

    for (param_name, param_type), value in zip(function.parameters, args):
        self.variables[param_name] = Variable(type=param_type, line_declared=1, value=value)

    try:
        self.visit(function.body_ctx)
        if function.return_type is not None and function.return_type != "void":
            raise NetLangRuntimeError(
                f"Missing return in function '{function_name}' which declares return type '{function.return_type}'",
                ctx
            )
    except ReturnValue as ret:
        if function.return_type is None:
            raise NetLangRuntimeError(
                f"Function '{function_name}' does not declare a return type, but 'return' was used.",
                ctx
            )
        if not check_type(function.return_type, ret.value):
            raise NetLangRuntimeError(
                f"Return type mismatch: function '{function_name}' declared to return '{function.return_type}', "
                f"but got '{type(ret.value).__name__}'",
                ctx
            )
        return ret.value
    finally:
        self.variables = previous_variables

def visitReturnStatement(self: "Interpreter", ctx: NetLangParser.ReturnStatementContext):
    if ctx.expression():
        value = self.visit(ctx.expression())
        raise ReturnValue(value)
    else:
        raise ReturnValue(None)