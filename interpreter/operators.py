from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError
from .utils import ensure_numeric, ensure_boolean, ensure_numeric_or_string
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitOrExpr(self: "Interpreter", ctx: NetLangParser.OrExprContext):
    left = self.visit(ctx.andExpr(0))
    for i in range(1, len(ctx.andExpr())):
        operator = ctx.getChild(2 * i - 1).getText()
        right = self.visit(ctx.andExpr(i))
        ensure_boolean(left, ctx, operator)
        ensure_boolean(right, ctx, operator)
        left = left or right
    return left

def visitAndExpr(self: "Interpreter", ctx: NetLangParser.AndExprContext):
    left = self.visit(ctx.notExpr(0))
    for i in range(1, len(ctx.notExpr())):
        operator = ctx.getChild(2 * i - 1).getText()
        right = self.visit(ctx.notExpr(i))
        ensure_boolean(left, ctx, operator)
        ensure_boolean(right, ctx, operator)
        left = left and right
    return left

def visitNotExpr(self: "Interpreter", ctx: NetLangParser.NotExprContext):
    if ctx.NOT():
        value = self.visit(ctx.notExpr())
        ensure_boolean(value, ctx, '!')
        return not value
    else:
        return self.visit(ctx.comparisonExpr())

def visitComparisonExpr(self: "Interpreter", ctx: NetLangParser.ComparisonExprContext):
    left = self.visit(ctx.equalityExpr(0))
    for i in range(1, len(ctx.equalityExpr())):
        operator = ctx.getChild(2 * i - 1).getText()
        right = self.visit(ctx.equalityExpr(i))
        ensure_numeric(left, ctx, operator)
        ensure_numeric(right, ctx, operator)
        if operator == '<':
            left = left < right
        elif operator == '>':
            left = left > right
        elif operator == '<=':
            left = left <= right
        elif operator == '>=':
            left = left >= right
    return left


def visitEqualityExpr(self: "Interpreter", ctx: NetLangParser.EqualityExprContext):
    left = self.visit(ctx.addSubExpr(0))
    for i in range(1, len(ctx.addSubExpr())):
        operator = ctx.getChild(2 * i - 1).getText()
        right = self.visit(ctx.addSubExpr(i))
        if operator == '==':
            left = left == right
        elif operator == '!=':
            left = left != right
    return left

def visitAddSubExpr(self: "Interpreter", ctx: NetLangParser.AddSubExprContext):
    left = self.visit(ctx.mulDivExpr(0))
    for i in range(1, len(ctx.mulDivExpr())):
        operator = ctx.getChild(2 * i - 1).getText()
        right = self.visit(ctx.mulDivExpr(i))
        if operator == '+':
            ensure_numeric_or_string(left, ctx, operator)
            ensure_numeric_or_string(right, ctx, operator)
            if isinstance(left, str) or isinstance(right, str):
                left = str(left) + str(right)
            else:
                left += right

        elif operator == '-':
            ensure_numeric(left, ctx, operator)
            ensure_numeric(right, ctx, operator)
            left -= right
    return left

def visitMulDivExpr(self: "Interpreter", ctx: NetLangParser.MulDivExprContext):
    left = self.visit(ctx.castExpr(0))
    for i in range(1, len(ctx.castExpr())):
        operator = ctx.getChild(2 * i - 1).getText()
        right = self.visit(ctx.castExpr(i))
        ensure_numeric(left, ctx, operator)
        ensure_numeric(right, ctx, operator)
        if operator == '*':
            left *= right
        elif operator == '/':
            if right == 0:
                raise NetLangRuntimeError("Division by zero", ctx)
            left /= right
        elif operator == '\\':
            if right == 0:
                raise NetLangRuntimeError("Division by zero", ctx)
            left //= right
        elif operator == '%':
            if right == 0:
                raise NetLangRuntimeError("Modulo by zero", ctx)
            left %= right

    return left

def visitPowExpr(self: "Interpreter", ctx: NetLangParser.PowExprContext):
    base = self.visit(ctx.atomExpr())
    if ctx.powExpr():
        exponent = self.visit(ctx.powExpr())
        ensure_numeric(base, ctx, operator='^')
        ensure_numeric(exponent, ctx, operator='^')
        return base ** exponent
    else:
        return base

def visitCastExpr(self: "Interpreter", ctx: NetLangParser.CastExprContext):
    value = self.visit(ctx.unaryExpr())

    if ctx.type_():
        target_type = ctx.type_().getText()

        try:
            if target_type == "int":
                return int(value)
            elif target_type == "float":
                return float(value)
            elif target_type == "bool":
                return bool(value)
            elif target_type == "string":
                if isinstance(value, bool):
                    return "true" if value else "false"
                return str(value)
            else:
                raise NetLangRuntimeError(
                    f"Unsupported cast to type '{target_type}'",
                    ctx
                )
        except Exception:
            raise NetLangRuntimeError(
                f"Cannot convert value '{value}' of type '{type(value).__name__}' to target type '{target_type}'",
                ctx
            )

    return value

def visitUnaryExpr(self: "Interpreter", ctx: NetLangParser.UnaryExprContext):
    if ctx.PLUS():
        value = self.visit(ctx.unaryExpr())
        ensure_numeric(value, ctx, operator='+ (unary)')
        return value
    if ctx.MINUS():
        value = self.visit(ctx.unaryExpr())
        ensure_numeric(value, ctx, operator='- (unary)')
        return -value
    else:
        return self.visit(ctx.powExpr())

def visitParensExpr(self: "Interpreter", ctx: NetLangParser.ParensExprContext):
    return self.visit(ctx.expression())