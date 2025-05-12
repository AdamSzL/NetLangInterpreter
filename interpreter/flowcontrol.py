from generated.NetLangParser import NetLangParser
from typing import TYPE_CHECKING

from shared.model.Variable import Variable

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitIfStatement(self: "Interpreter", ctx: NetLangParser.IfStatementContext):
    if self.visit(ctx.expression()):
        self.push_scope()
        for stmt in ctx.block().statement():
            self.visit(stmt)
        self.pop_scope()
    else:
        for elseif in ctx.elseIfClause():
            if self.visit(elseif.expression()):
                self.push_scope()
                for stmt in elseif.block().statement():
                    self.visit(stmt)
                self.pop_scope()
                return
        if ctx.elseClause():
            self.push_scope()
            for stmt in ctx.elseClause().block().statement():
                self.visit(stmt)
            self.pop_scope()

def visitRepeatWhileLoop(self: "Interpreter", ctx: NetLangParser.RepeatWhileLoopContext):
    while True:
        if not self.visit(ctx.expression()):
            break
        self.push_scope()
        for stmt in ctx.block().statement():
            self.visit(stmt)
        self.pop_scope()

def visitRepeatTimesLoop(self: "Interpreter", ctx: NetLangParser.RepeatTimesLoopContext):
    times: int = self.visit(ctx.expression())
    index_var_name: str = ctx.ID().getText()

    for i in range(times):
        self.push_scope()
        self.declare_variable(index_var_name, Variable("int", -1, i), ctx)
        for stmt in ctx.block().statement():
            self.visit(stmt)
        self.pop_scope()

def visitEachLoop(self: "Interpreter", ctx: NetLangParser.EachLoopContext):
    loop_var_name: str = ctx.ID(0).getText()
    list_var_name: str = ctx.ID(1).getText()

    list_var: Variable = self.lookup_variable(list_var_name, ctx)
    element_type: str = list_var.type[1:-1]

    for element in list_var.value:
        self.push_scope()
        self.declare_variable(loop_var_name, Variable(element_type, -1, element), ctx)
        for stmt in ctx.block().statement():
            self.visit(stmt)
        self.pop_scope()