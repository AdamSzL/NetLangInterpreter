from __future__ import annotations

from generated.NetLangListener import NetLangListener
from generated.NetLangParser import NetLangParser
from .errors import NetLangRuntimeError
from .types import type_map, is_known_type, check_type
from model.base import NetLangObject
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .interpreter import Interpreter

@dataclass
class Variable:
    type: str
    line_declared: int
    value: Any = None

@dataclass
class VariableCollectorListener(NetLangListener):
    variables: dict[str, Variable] = field(default_factory=dict)

    def enterVariableDeclaration(self, ctx: NetLangParser.VariableDeclarationContext):
        variable_name: str = ctx.ID().getText()
        variable_type: str = ctx.type_().getText()
        line: int = ctx.start.line

        if variable_name in self.variables:
            raise NetLangRuntimeError(f"Redeclaration of variable '{variable_name}' (first declared on line {self.variables[variable_name].line_declared})", ctx)

        self.variables[variable_name] = Variable(variable_type, line)

def visitVariableDeclaration(self: "Interpreter", ctx: NetLangParser.VariableDeclarationContext):
    name: str = ctx.ID().getText()
    declared_type: str = ctx.type_().getText()
    value = self.visit(ctx.expression())

    if isinstance(value, dict) and declared_type in type_map and issubclass(type_map[declared_type], NetLangObject):
        value = type_map[declared_type].from_dict(value, ctx)

    if not is_known_type(declared_type):
        raise NetLangRuntimeError(
            message=f"Unknown type '{declared_type}'",
            ctx=ctx
        )

    if not check_type(declared_type, value):
        raise NetLangRuntimeError(
            f"Type mismatch: cannot assign value {value} ({type(value).__name__}) to variable {name} of type {declared_type}",
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
            message=f"Type mismatch in assignment to variable '{name}': expected '{expected_type}', got '{type(value).__name__}'",
            ctx=ctx
        )

    self.variables[name].value = value

    return value

def visitFieldAssignment(self: "Interpreter", ctx: NetLangParser.FieldAssignmentContext):
    access = ctx.fieldAccess()
    value = self.visit(ctx.expression())

    # Zacznij od pierwszego ID
    current = self.variables.get(access.ID(0).getText())
    if current is None:
        raise NetLangRuntimeError(f"Variable '{access.ID(0).getText()}' not defined")

    # Przechodzimy po chainie, ale ZATRZYMUJEMY się na przedostatnim
    for i in range(1, len(access.children) - 2, 2):
        op = access.getChild(i).getText()
        operand = access.getChild(i + 1)

        if op == ".":
            field = operand.getText()
            if not hasattr(current, field):
                raise NetLangRuntimeError(f"'{type(current).__name__}' has no field '{field}'")
            current = getattr(current, field)

        elif op == "<":
            index = int(self.visit(operand))
            if not isinstance(current, list):
                raise NetLangRuntimeError(f"Tried to index non-list object")
            try:
                current = current[index]
            except IndexError:
                raise NetLangRuntimeError(f"Index {index} out of range")

    # Teraz zostały ostatnie dwa elementy: operator + field/index
    last_op = access.getChild(-2).getText()
    last_operand = access.getChild(-1)

    if last_op == ".":
        field_name = last_operand.getText()
        if not hasattr(current, field_name):
            raise NetLangRuntimeError(f"'{type(current).__name__}' has no field '{field_name}'")
        setattr(current, field_name, value)
        # print(f"[assign] ...{field_name} ← {value}")
        return value

    elif last_op == "<":
        index = int(self.visit(last_operand))
        if not isinstance(current, list):
            raise NetLangRuntimeError(f"Tried to index non-list object")
        if index >= len(current):
            raise NetLangRuntimeError(f"Index {index} out of range")
        current[index] = value
        # print(f"[assign] ...<{index}> ← {value}")
        return value

    raise NetLangRuntimeError(f"Unsupported assignment operator '{last_op}'")