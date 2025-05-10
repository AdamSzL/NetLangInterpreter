from generated.NetLangParser import NetLangParser
from typing import TYPE_CHECKING

from .errors import NetLangRuntimeError
from .utils import ensure_boolean
from .variables import Variable

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitIfStatement(self: "Interpreter", ctx: NetLangParser.IfStatementContext):
    condition_value = self.visit(ctx.expression())
    ensure_boolean(condition_value, ctx, statement="if")

    if condition_value:
        for stmt in ctx.block().statement():
            self.visit(stmt)
    else:
        for elseif in ctx.elseIfClause():
            elseif_condition = self.visit(elseif.expression())
            ensure_boolean(elseif_condition, ctx, statement="if")

            if elseif_condition:
                for stmt in elseif.block().statement():
                    self.visit(stmt)
                return
        if ctx.elseClause():
            for stmt in ctx.elseClause().block().statement():
                self.visit(stmt)

def visitRepeatWhileLoop(self: "Interpreter", ctx: NetLangParser.RepeatWhileLoopContext):
    while True:
        condition = self.visit(ctx.expression())
        ensure_boolean(condition, ctx, statement="repeat while")

        if not condition:
            break

        for stmt in ctx.block().statement():
            self.visit(stmt)

def visitRepeatTimesLoop(self: "Interpreter", ctx: NetLangParser.RepeatTimesLoopContext):
    times = self.visit(ctx.expression())

    if not isinstance(times, int):
        raise NetLangRuntimeError(
            f"Repeat count must be an integer, got {type(times).__name__}",
            ctx
        )

    index_var_name = ctx.ID().getText()

    for i in range(times):
        self.variables[index_var_name] = Variable(
            type="int",
            line_declared=-1,
            value=i
        )

        for stmt in ctx.block().statement():
            self.visit(stmt)