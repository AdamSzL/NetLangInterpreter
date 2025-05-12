from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Any

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError
from shared.model.Function import Function
from shared.model.ReturnValue import ReturnValue
from shared.model.Variable import Variable
from shared.utils.types import check_type

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitFunctionCallExpr(self, ctx: NetLangParser.FunctionCallExprContext):
    return self.visit(ctx.functionCall())

def visitFunctionCall(self: "Interpreter", ctx: NetLangParser.FunctionCallContext):
    function_name = ctx.ID().getText()
    expr_list = ctx.expressionList()
    args = [self.visit(expr) for expr in expr_list.expression()] if expr_list else []

    function = self.lookup_function(function_name, ctx)

    self.push_scope()
    for (param_name, param_type), arg_value in zip(function.parameters, args):
        self.declare_variable(param_name, Variable(param_type, 1, arg_value), ctx)
    result = self.visit(function.body_ctx)
    self.pop_scope()

    return result

def visitFunctionDeclarationStatement(self: "Interpreter", ctx: NetLangParser.FunctionDeclarationStatementContext):
    function_name: str = ctx.ID().getText()
    return_type: str = ctx.type_().getText() if ctx.type_() else "void"
    line: int = ctx.start.line

    parameters = []
    parameter_list = ctx.parameterList()
    if parameter_list:
        for param_ctx in parameter_list.parameter():
            param_name = param_ctx.ID().getText()
            param_type = param_ctx.type_().getText()
            parameters.append((param_name, param_type))

    function = Function(
        parameters=parameters,
        return_type=return_type,
        line_declared=line,
        body_ctx=ctx.block()
    )

    self.declare_function(function_name, function, ctx)

def visitReturnStatement(self: "Interpreter", ctx: NetLangParser.ReturnStatementContext):
    if ctx.expression():
        value = self.visit(ctx.expression())
        raise ReturnValue(value)
    else:
        raise ReturnValue(None)