from dataclasses import dataclass

from shared.utils.errors import NetLangTypeError
from typing import Optional

from shared.model.Function import Function
from shared.model.Scope import Scope
from shared.model.Variable import Variable

@dataclass
class ScopedVisitorBase:

    def __init__(self):
        self.scopes: list[Scope] = [Scope()]
        self.current_call_line: Optional[int] = None
        self.call_stack: list[tuple[str, Scope]] = []

    def push_scope(self):
        new_scope = Scope(parent=self.scopes[-1])
        self.scopes.append(new_scope)

    def pop_scope(self):
        self.scopes.pop()

    def declare_variable(self, name: str, variable: Variable, ctx):
        if name in self.scopes[-1].variables:
            raise NetLangTypeError(
                f"Redeclaration of variable '{name}' (first declared on line {self.scopes[-1].variables[name].line_declared})",
                ctx
            )
        if name in self.scopes[-1].functions:
            raise NetLangTypeError(
                f"Cannot declare variable '{name}' – function with this name was already declared on line {self.scopes[-1].functions[name].line_declared}",
                ctx
            )
        self.scopes[-1].variables[name] = variable

    def declare_function(self, name: str, function: Function, ctx):
        if name in self.scopes[-1].functions:
            raise NetLangTypeError(
                f"Redeclaration of function '{name}' (first declared on line {self.scopes[-1].functions[name].line_declared})",
                ctx
            )
        if name in self.scopes[-1].variables:
            raise NetLangTypeError(
                f"Cannot declare function '{name}' – variable with this name was already declared on line {self.scopes[-1].variables[name].line_declared}",
                ctx
            )
        self.scopes[-1].functions[name] = function