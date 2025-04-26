from typing import Any
from generated.NetLangParser import NetLangParser
from .errors import NetLangRuntimeError


def _ensure_numeric(value: Any, ctx):
    if not isinstance(value, (int, float)):
        raise NetLangRuntimeError("Expected numeric value", ctx)


def _ensure_boolean(value: Any, ctx):
    if not isinstance(value, bool):
        raise NetLangRuntimeError("Expected boolean value", ctx)


def visitAddExpr(self, ctx: NetLangParser.AddExprContext):
    left = self.visit(ctx.expression(0))
    right = self.visit(ctx.expression(1))
    _ensure_numeric(left, ctx)
    _ensure_numeric(right, ctx)
    return left + right


def visitSubExpr(self, ctx: NetLangParser.SubExprContext):
    left = self.visit(ctx.expression(0))
    right = self.visit(ctx.expression(1))
    _ensure_numeric(left, ctx)
    _ensure_numeric(right, ctx)
    return left - right


def visitMulExpr(self, ctx: NetLangParser.MulExprContext):
    left = self.visit(ctx.expression(0))
    right = self.visit(ctx.expression(1))
    _ensure_numeric(left, ctx)
    _ensure_numeric(right, ctx)
    return left * right


def visitDivExpr(self, ctx: NetLangParser.DivExprContext):
    left = self.visit(ctx.expression(0))
    right = self.visit(ctx.expression(1))
    _ensure_numeric(left, ctx)
    _ensure_numeric(right, ctx)
    if right == 0:
        raise NetLangRuntimeError("Division by zero", ctx)
    return left / right


def visitEqualsExpr(self, ctx: NetLangParser.EqualsExprContext):
    return self.visit(ctx.expression(0)) == self.visit(ctx.expression(1))


def visitNotEqualsExpr(self, ctx: NetLangParser.NotEqualsExprContext):
    return self.visit(ctx.expression(0)) != self.visit(ctx.expression(1))


def visitLessThanExpr(self, ctx: NetLangParser.LessThanExprContext):
    left = self.visit(ctx.expression(0))
    right = self.visit(ctx.expression(1))
    _ensure_numeric(left, ctx)
    _ensure_numeric(right, ctx)
    return left < right


def visitGreaterThanExpr(self, ctx: NetLangParser.GreaterThanExprContext):
    left = self.visit(ctx.expression(0))
    right = self.visit(ctx.expression(1))
    _ensure_numeric(left, ctx)
    _ensure_numeric(right, ctx)
    return left > right


def visitLessEqualExpr(self, ctx: NetLangParser.LessEqualExprContext):
    left = self.visit(ctx.expression(0))
    right = self.visit(ctx.expression(1))
    _ensure_numeric(left, ctx)
    _ensure_numeric(right, ctx)
    return left <= right


def visitGreaterEqualExpr(self, ctx: NetLangParser.GreaterEqualExprContext):
    left = self.visit(ctx.expression(0))
    right = self.visit(ctx.expression(1))
    _ensure_numeric(left, ctx)
    _ensure_numeric(right, ctx)
    return left >= right


def visitAndExpr(self, ctx: NetLangParser.AndExprContext):
    left = self.visit(ctx.expression(0))
    right = self.visit(ctx.expression(1))
    _ensure_boolean(left, ctx)
    _ensure_boolean(right, ctx)
    return left and right


def visitOrExpr(self, ctx: NetLangParser.OrExprContext):
    left = self.visit(ctx.expression(0))
    right = self.visit(ctx.expression(1))
    _ensure_boolean(left, ctx)
    _ensure_boolean(right, ctx)
    return left or right


def visitNotExpr(self, ctx: NetLangParser.NotExprContext):
    value = self.visit(ctx.expression())
    _ensure_boolean(value, ctx)
    return not value


def visitParensExpr(self, ctx: NetLangParser.ParensExprContext):
    return self.visit(ctx.expression())