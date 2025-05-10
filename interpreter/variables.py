from __future__ import annotations

from generated.NetLangListener import NetLangListener
from generated.NetLangParser import NetLangParser
from .errors import NetLangRuntimeError
from .types import type_map, is_known_type, check_type
from model.base import NetLangObject
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from .interpreter import Interpreter

@dataclass
class Variable:
    type: str
    line_declared: int
    value: Any = None

@dataclass
class Function:
    parameters: list[tuple[str, str]]
    return_type: Optional[str]
    body_ctx: Any

@dataclass
class ReturnValue(Exception):
    value: Any

def visitVariableDeclaration(self: "Interpreter", ctx: NetLangParser.VariableDeclarationContext):
    name: str = ctx.ID().getText()
    declared_type: str = ctx.type_().getText()
    value = self.visit(ctx.expression())

    if isinstance(value, dict) and declared_type in type_map and issubclass(type_map[declared_type], NetLangObject):
        value = type_map[declared_type].from_dict(value, ctx)

    if not is_known_type(declared_type):
        raise NetLangRuntimeError(f"Unknown type '{declared_type}'", ctx)

    if not check_type(declared_type, value):
        raise NetLangRuntimeError(
            f"Type mismatch: cannot assign value {value} ({type(value).__name__}) to variable '{name}' of type {declared_type}",
            ctx
        )

    self.variables[name].value = value
    return value

def visitVariableAssignment(self: "Interpreter", ctx: NetLangParser.VariableAssignmentContext):
    name = ctx.ID().getText()
    value = self.visit(ctx.expression())

    if name not in self.variables:
        raise NetLangRuntimeError(f"Undefined variable '{name}'", ctx)

    expected_type = self.variables[name].type
    if not check_type(expected_type, value):
        raise NetLangRuntimeError(
            f"Type mismatch in assignment to variable '{name}': expected '{expected_type}', got '{type(value).__name__}'",
            ctx
        )

    self.variables[name].value = value

    return value

def visitFunctionCallExpr(self, ctx: NetLangParser.FunctionCallExprContext):
    return self.visit(ctx.functionCall())

def visitFunctionCall(self: "Interpreter", ctx: NetLangParser.FunctionCallContext):
    function_name = ctx.ID().getText()
    expr_list = ctx.expressionList()
    args = [self.visit(expr) for expr in expr_list.expression()] if expr_list else []

    if function_name not in self.variables:
        raise NetLangRuntimeError(f"Undefined function '{function_name}'", ctx)

    func_var = self.variables[function_name]
    if not isinstance(func_var.value, Function):
        raise NetLangRuntimeError(f"'{function_name}' is not callable", ctx)

    function: Function = func_var.value
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

    previous_in_function = self.in_function
    self.in_function = True
    try:
        self.visit(function.body_ctx)
        if function.return_type is not None:
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
        self.in_function = previous_in_function

def visitReturnStatement(self: "Interpreter", ctx: NetLangParser.ReturnStatementContext):
    if not self.in_function:
        raise NetLangRuntimeError("Cannot use 'return' statement outside of a function", ctx)

    value = self.visit(ctx.expression())
    raise ReturnValue(value)