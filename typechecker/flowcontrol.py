from typing import TYPE_CHECKING

from generated.NetLangParser import NetLangParser
from shared.utils.errors import NetLangTypeError
from shared.model.Variable import Variable
from shared.utils.types import are_types_compatible
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

    return_types = []

    self.push_scope()

    try:
        ret = self.block_returns_type(ctx.block())
        return_types.append(ret)
    finally:
        self.pop_scope()

    for elseif in ctx.elseIfClause():
        elseif_type = self.visit(elseif.expression())
        check_bool(elseif_type, ctx, statement="else-if")

        self.push_scope()
        try:
            ret = self.block_returns_type(elseif.block())
            return_types.append(ret)
        finally:
            self.pop_scope()

    if ctx.elseClause():
        self.push_scope()
        try:
            ret = self.block_returns_type(ctx.elseClause().block())
            return_types.append(ret)
        finally:
            self.pop_scope()
    else:
        return_types.append(None)

    if all(rt is not None for rt in return_types):
        first = return_types[0]
        if all(are_types_compatible(first, rt) for rt in return_types):
            return first
    return None

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


def visitRepeatTimes(self: "TypeCheckingVisitor", ctx: NetLangParser.RepeatTimesContext):
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

def visitRepeatRange(self: "TypeCheckingVisitor", ctx: NetLangParser.RepeatRangeContext):
    from_type = self.visit(ctx.expression(0))
    to_type = self.visit(ctx.expression(1))

    if from_type != "int" or to_type != "int":
        raise NetLangTypeError(
            (
                f"Repeat-range 'from' and 'to' must be of type int "
                f"(got: from={from_type}, to={to_type})"
            ),
            ctx
        )

    if ctx.expression(2) is not None:
        step_type = self.visit(ctx.expression(2))
        if step_type != "int":
            raise NetLangTypeError(
                f"'step' must be of type int (got {step_type})",
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
    loop_var = ctx.ID().getText()
    list_type = self.visit(ctx.expression())

    if not list_type.startswith("[") or not list_type.endswith("]"):
        raise NetLangTypeError(f"Expression in 'each' must be a list, got {list_type}", ctx)

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

def visitBlock(self: "TypeCheckingVisitor", ctx: NetLangParser.BlockContext):
    self.push_scope()
    try:
        for stmt in ctx.statement():
            self.visit(stmt)
    finally:
        self.pop_scope()