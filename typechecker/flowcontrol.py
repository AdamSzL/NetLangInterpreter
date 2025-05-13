from typing import TYPE_CHECKING, Any

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError, NetLangTypeError
from shared.model.Variable import Variable
from typechecker.utils import check_bool

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

def visitIfStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.IfStatementContext):
    condition_type = self.visit(ctx.expression())
    check_bool(condition_type, ctx, statement="if")

    self.push_scope()

    try:
        for stmt in ctx.block().statement():
            self.visit(stmt)
    finally:
        self.pop_scope()

    for elseif in ctx.elseIfClause():
        elseif_type = self.visit(elseif.expression())
        check_bool(elseif_type, ctx, statement="else-if")

        self.push_scope()
        try:
            for stmt in elseif.block().statement():
                self.visit(stmt)
        finally:
            self.pop_scope()

    if ctx.elseClause():
        self.push_scope()
        try:
            for stmt in ctx.elseClause().block().statement():
                self.visit(stmt)
        finally:
            self.pop_scope()

def visitRepeatWhileLoop(self: "TypeCheckingVisitor", ctx: NetLangParser.RepeatWhileLoopContext):
    condition_type = self.visit(ctx.expression())
    check_bool(condition_type, ctx, statement="repeat-while")

    old_flag = self.in_loop
    self.in_loop = True
    self.push_scope()
    for stmt in ctx.block().statement():
        self.visit(stmt)
    self.pop_scope()
    self.in_loop = old_flag


def visitRepeatTimesLoop(self: "TypeCheckingVisitor", ctx: NetLangParser.RepeatTimesLoopContext):
    times_type = self.visit(ctx.expression())
    if times_type != "int":
        raise NetLangTypeError(
            f"Repeat-times count must be an integer (got {times_type} instead)",
            ctx
        )

    index_var_name = ctx.ID().getText()

    old_flag = self.in_loop
    self.in_loop = True
    self.push_scope()
    self.declare_variable(index_var_name, Variable("int", ctx.start.line), ctx)
    for stmt in ctx.block().statement():
        self.visit(stmt)
    self.pop_scope()
    self.in_loop = old_flag

def visitEachLoop(self: "TypeCheckingVisitor", ctx: NetLangParser.EachLoopContext):
    loop_var = ctx.ID(0).getText()
    list_var = ctx.ID(1).getText()

    variable = self.lookup_variable(list_var, ctx)
    list_type = variable.type

    if not list_type.startswith("[") or not list_type.endswith("]"):
        raise NetLangTypeError(f"'{list_var}' is not a list type", ctx)

    element_type = list_type[1:-1]

    old_flag = self.in_loop
    self.in_loop = True
    self.push_scope()
    self.declare_variable(loop_var, Variable(element_type, ctx.start.line), ctx)
    for stmt in ctx.block().statement():
        self.visit(stmt)
    self.pop_scope()
    self.in_loop = old_flag

def visitBreakStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.BreakStatementContext):
    if not self.in_loop:
        raise NetLangTypeError("'break' can only be used inside a loop", ctx)

def visitContinueStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.ContinueStatementContext):
    if not self.in_loop:
        raise NetLangTypeError("'continue' can only be used inside a loop", ctx)
