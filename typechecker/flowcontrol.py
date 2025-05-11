from typing import TYPE_CHECKING, Any

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError, NetLangTypeError
from shared.model.Variable import Variable
from typechecker.utils import check_bool

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor


def visitIfStatement(self: "TypeCheckingVisitor", ctx: NetLangParser.IfStatementContext):
    condition_type = self.visit(ctx.expression())
    check_bool(condition_type, ctx, statement="if")

    for stmt in ctx.block().statement():
        self.visit(stmt)

    for elseif in ctx.elseIfClause():
        elseif_type = self.visit(elseif.expression())
        check_bool(elseif_type, ctx, statement="else-if")
        for stmt in elseif.block().statement():
            self.visit(stmt)

    if ctx.elseClause():
        for stmt in ctx.elseClause().block().statement():
            self.visit(stmt)

def visitRepeatWhileLoop(self: "TypeCheckingVisitor", ctx: NetLangParser.RepeatWhileLoopContext):
    condition_type = self.visit(ctx.expression())
    check_bool(condition_type, ctx, statement="repeat-while")

    for stmt in ctx.block().statement():
        self.visit(stmt)


def visitRepeatTimesLoop(self: "TypeCheckingVisitor", ctx: NetLangParser.RepeatTimesLoopContext):
    times_type = self.visit(ctx.expression())
    if times_type != "int":
        raise NetLangTypeError(
            f"Repeat-times count must be an integer (got {times_type} instead)",
            ctx
        )

    index_var_name = ctx.ID().getText()
    self.variables[index_var_name] = Variable("int", -1, 0)

    for stmt in ctx.block().statement():
        self.visit(stmt)

    del self.variables[index_var_name]

def visitEachLoop(self: "TypeCheckingVisitor", ctx: NetLangParser.EachLoopContext):
    loop_var = ctx.ID(0).getText()
    list_var = ctx.ID(1).getText()

    if list_var not in self.variables:
        raise NetLangTypeError(f"Variable '{list_var}' not defined", ctx)

    list_type = self.variables[list_var].type
    if not list_type.startswith("[") or not list_type.endswith("]"):
        raise NetLangTypeError(f"'{list_var}' is not a list type", ctx)

    element_type = list_type[1:-1]
    self.variables[loop_var] = Variable(element_type, -1, 0)

    for stmt in ctx.block().statement():
        self.visit(stmt)