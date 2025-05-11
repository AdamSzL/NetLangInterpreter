from generated.NetLangParser import NetLangParser
from typing import TYPE_CHECKING

from shared.errors import NetLangRuntimeError
from shared.model.Variable import Variable
from .utils import ensure_boolean

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitIfStatement(self: "Interpreter", ctx: NetLangParser.IfStatementContext):
    if self.visit(ctx.expression()):
        for stmt in ctx.block().statement():
            self.visit(stmt)
    else:
        for elseif in ctx.elseIfClause():
            if self.visit(elseif.expression()):
                for stmt in elseif.block().statement():
                    self.visit(stmt)
                return
        if ctx.elseClause():
            for stmt in ctx.elseClause().block().statement():
                self.visit(stmt)

def visitRepeatWhileLoop(self: "Interpreter", ctx: NetLangParser.RepeatWhileLoopContext):
    while True:
        if not self.visit(ctx.expression()):
            break
        for stmt in ctx.block().statement():
            self.visit(stmt)

def visitRepeatTimesLoop(self: "Interpreter", ctx: NetLangParser.RepeatTimesLoopContext):
    times = self.visit(ctx.expression())
    index_var_name = ctx.ID().getText()

    for i in range(times):
        self.variables[index_var_name] = Variable("int", -1, i)
        for stmt in ctx.block().statement():
            self.visit(stmt)

def visitEachLoop(self: "Interpreter", ctx: NetLangParser.EachLoopContext):
    loop_var_name = ctx.ID(0).getText()
    list_var_name = ctx.ID(1).getText()

    list_var = self.variables[list_var_name]
    element_type = list_var.type[1:-1]

    for element in list_var.value:
        self.variables[loop_var_name] = Variable(element_type, 0, element)
        for stmt in ctx.block().statement():
            self.visit(stmt)