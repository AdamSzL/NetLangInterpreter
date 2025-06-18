from typing import TYPE_CHECKING

from generated.NetLangParser import NetLangParser
from shared.utils.errors import NetLangRuntimeError
from shared.model.Function import Function
from shared.model.ReturnValue import ReturnValue
from shared.model.Variable import Variable

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitFunctionCallExpr(self, ctx: NetLangParser.FunctionCallExprContext):
    return self.visit(ctx.functionCall())

def visitFunctionCall(self: "Interpreter", ctx: NetLangParser.FunctionCallContext):
    scoped_ctx = ctx.scopedIdentifier()
    expr_list_ctx = ctx.expressionList()

    args = [self.visit(expr) for expr in expr_list_ctx.expression()] if expr_list_ctx else []

    function_scope, function_name = self.visit(scoped_ctx)
    function = function_scope.functions[function_name]

    if self.call_depth >= self.max_call_depth:
        raise NetLangRuntimeError(
            "Stack overflow — possible infinite recursion",
            ctx
        )

    self.call_depth += 1

    is_recursive = self.call_stack and self.call_stack[-1][0] == function_name
    parent_scope = self.call_stack[-1][1].parent if is_recursive else self.scopes[-1]

    self.push_scope()
    self.scopes[-1].parent = parent_scope

    for (param_name, param_type), arg_value in zip(function.parameters, args):
        self.declare_variable(param_name, Variable(param_type, 1, arg_value), ctx)

    try:
        self.call_stack.append((function_name, self.scopes[-1]))
        self.visit(function.body_ctx)
        return None
    except ReturnValue as r:
        return r.value
    finally:
        self.pop_scope()
        self.call_stack.pop()
        self.call_depth -= 1

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
        body_ctx=ctx.block(),
    )

    self.declare_function(function_name, function, ctx)

def visitReturnStatement(self: "Interpreter", ctx: NetLangParser.ReturnStatementContext):
    if ctx.expression():
        value = self.visit(ctx.expression())
        raise ReturnValue(value)
    else:
        raise ReturnValue(None)