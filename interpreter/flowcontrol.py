from generated.NetLangParser import NetLangParser
from typing import TYPE_CHECKING

from shared.errors import NetLangRuntimeError, NetLangTypeError
from shared.model.Variable import Variable
from typechecker.flowcontrol import BreakException, ContinueException

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitIfStatement(self: "Interpreter", ctx: NetLangParser.IfStatementContext):
    if self.visit(ctx.expression()):
        self.push_scope()
        try:
            for stmt in ctx.block().statement():
                self.visit(stmt)
        finally:
            self.pop_scope()
    else:
        for elseif in ctx.elseIfClause():
            if self.visit(elseif.expression()):
                self.push_scope()
                try:
                    for stmt in elseif.block().statement():
                        self.visit(stmt)
                finally:
                    self.pop_scope()
                return
        if ctx.elseClause():
            self.push_scope()
            try:
                for stmt in ctx.elseClause().block().statement():
                    self.visit(stmt)
            finally:
                self.pop_scope()

def visitRepeatWhileLoop(self: "Interpreter", ctx: NetLangParser.RepeatWhileLoopContext):
    while self.visit(ctx.expression()):
        self.push_scope()
        try:
            for stmt in ctx.block().statement():
                try:
                    self.visit(stmt)
                except ContinueException:
                    break
        except BreakException:
            break
        finally:
            self.pop_scope()

def visitRepeatTimesLoop(self: "Interpreter", ctx: NetLangParser.RepeatTimesLoopContext):
    times: int = self.visit(ctx.expression())
    index_var_name: str = ctx.ID().getText()

    if times <= 0:
        raise NetLangRuntimeError(f"Loop count must be a positive integer (got {times})", ctx)

    for i in range(times):
        self.push_scope()
        self.declare_variable(index_var_name, Variable("int", ctx.start.line, i), ctx)
        try:
            for stmt in ctx.block().statement():
                try:
                    self.visit(stmt)
                except ContinueException:
                    break
        except BreakException:
            break
        finally:
            self.pop_scope()

def visitEachLoop(self: "Interpreter", ctx: NetLangParser.EachLoopContext):
    loop_var_name: str = ctx.ID().getText()
    iterable = self.visit(ctx.expression())

    if not isinstance(iterable, list):
        raise NetLangRuntimeError(
            f"Value in 'each' must be a list, got {type(iterable).__name__}",
            ctx
        )

    for element in iterable:
        self.push_scope()
        self.declare_variable(loop_var_name, Variable(type(element).__name__, ctx.start.line, element), ctx)
        try:
            for stmt in ctx.block().statement():
                try:
                    self.visit(stmt)
                except ContinueException:
                    break
        except BreakException:
            break
        finally:
            self.pop_scope()

def visitBreakStatement(self: "Interpreter", ctx: NetLangParser.BreakStatementContext):
    raise BreakException()

def visitContinueStatement(self: "Interpreter", ctx: NetLangParser.ContinueStatementContext):
    raise ContinueException()