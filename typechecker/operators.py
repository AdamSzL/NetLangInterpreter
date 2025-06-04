from generated.NetLangParser import NetLangParser
from shared.utils.errors import NetLangTypeError
from typing import TYPE_CHECKING

from shared.utils.types import is_subtype
from typechecker.utils import check_bool, check_numeric

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitOrExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.OrExprContext) -> str:
    if len(ctx.andExpr()) == 1:
        return self.visit(ctx.andExpr(0))

    for expr in ctx.andExpr():
        expr_type = self.visit(expr)
        check_bool(expr_type, ctx, operator="||")

    return "bool"

def visitAndExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.AndExprContext) -> str:
    if len(ctx.notExpr()) == 1:
        return self.visit(ctx.notExpr(0))

    for expr in ctx.notExpr():
        expr_type = self.visit(expr)
        check_bool(expr_type, ctx, operator="&&")

    return "bool"

def visitNotExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.NotExprContext) -> str:
    if ctx.NOT():
        expr_type = self.visit(ctx.notExpr())
        check_bool(expr_type, ctx, '!')
        return "bool"

    return self.visit(ctx.comparisonExpr())

def visitComparisonExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.ComparisonExprContext) -> str:
    left_type = self.visit(ctx.equalityExpr(0))

    if len(ctx.equalityExpr()) == 1:
        return left_type

    for i in range(1, len(ctx.equalityExpr())):
        operator = ctx.getChild(2 * i - 1).getText()
        right_type = self.visit(ctx.equalityExpr(i))
        check_numeric(left_type, ctx, operator)
        check_numeric(right_type, ctx, operator)

    return "bool"


def visitEqualityExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.EqualityExprContext) -> str:
    left_type = self.visit(ctx.addSubExpr(0))

    if len(ctx.addSubExpr()) == 1:
        return left_type

    for i in range(1, len(ctx.addSubExpr())):
        operator = ctx.getChild(2 * i - 1).getText()
        right_type = self.visit(ctx.addSubExpr(i))

        numeric_types = {"int", "float"}
        if left_type != right_type:
            if {left_type, right_type}.issubset(numeric_types):
                pass
            else:
                raise NetLangTypeError(f"Cannot compare {left_type} and {right_type}", ctx)

    return "bool"

def visitAddSubExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.AddSubExprContext):
    result_type = self.visit(ctx.mulDivExpr(0))
    for i in range(1, len(ctx.mulDivExpr())):
        operator = ctx.getChild(2 * i - 1).getText()
        right_type = self.visit(ctx.mulDivExpr(i))

        if operator == "+":
            if result_type == "string" or right_type == "string":
                result_type = "string"
            elif result_type in ["int", "float"] and right_type in ["int", "float"]:
                result_type = "float" if "float" in (result_type, right_type) else "int"
            elif result_type == "IP" and right_type == "int":
                result_type = "IP"
            elif result_type == "CIDR" and right_type == "int":
                result_type = "CIDR"
            else:
                raise NetLangTypeError(f"Cannot add {result_type} and {right_type}", ctx)
        elif operator == "-":
            if result_type in ["int", "float"] and right_type in ["int", "float"]:
                result_type = "float" if "float" in (result_type, right_type) else "int"
            elif result_type == "IP" and right_type == "int":
                result_type = "IP"
            elif result_type == "CIDR" and right_type == "int":
                result_type = "CIDR"
            else:
                raise NetLangTypeError(f"Cannot subtract {right_type} from {result_type}", ctx)

    return result_type

def visitMulDivExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.MulDivExprContext):
    result_type = self.visit(ctx.castExpr(0))
    for i in range(1, len(ctx.castExpr())):
        operator = ctx.getChild(2 * i - 1).getText()
        right_type = self.visit(ctx.castExpr(i))

        if operator == "%":
            if result_type == "int" and right_type == "int":
                result_type = "int"
            else:
                raise NetLangTypeError(
                    f"Modulo operator '%' requires both operands to be int, got {result_type} and {right_type}",
                    ctx
                )

        elif result_type in ["int", "float"] and right_type in ["int", "float"]:
            result_type = (
                "float"
                if operator == "/" or "float" in (result_type, right_type)
                else "int"
            )
        else:
            raise NetLangTypeError(
                f"Cannot apply '{operator}' to {result_type} and {right_type}",
                ctx
            )

    return result_type

def visitPowExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.PowExprContext):
    base_type = self.visit(ctx.atomExpr())

    if ctx.powExpr():
        exponent_type = self.visit(ctx.powExpr())

        if base_type not in ["int", "float"]:
            raise NetLangTypeError(f"Base of power expression must be numeric, got {base_type}", ctx)
        if exponent_type not in ["int", "float"]:
            raise NetLangTypeError(f"Base of power expression must be numeric, got {base_type}", ctx)

        return "int" if base_type == "int" and exponent_type == "int" else "float"
    else:
        return base_type

def visitCastExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.CastExprContext):
    expr_type = self.visit(ctx.unaryExpr())

    if ctx.type_():
        target_type = ctx.type_().getText()

        if expr_type == target_type:
            return target_type

        if expr_type == "[]" and target_type.startswith("[") and target_type.endswith("]"):
            return target_type

        allowed_casts = {
            "int": ["float", "string", "bool"],
            "float": ["int", "string", "bool"],
            "bool": ["int", "float", "string"],
            "string": ["int", "float", "bool"]
        }

        if expr_type.startswith("[") and target_type.startswith("["):
            from_elem_type = expr_type[1:-1]
            to_elem_type = target_type[1:-1]

            if (
                    from_elem_type == to_elem_type
                    or (from_elem_type in allowed_casts and to_elem_type in allowed_casts[from_elem_type])
                    or is_subtype(to_elem_type, from_elem_type)
            ):
                return target_type

            raise NetLangTypeError(
                f"Cannot cast from {expr_type} to {target_type}",
                ctx
            )

        if expr_type in allowed_casts and target_type in allowed_casts[expr_type] or is_subtype(expr_type, target_type):
            return target_type

        raise NetLangTypeError(f"Cannot cast from type '{expr_type}' to target type '{target_type}'", ctx)

    return expr_type

def visitUnaryExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.UnaryExprContext):
    if ctx.PLUS():
        operand_type = self.visit(ctx.unaryExpr())
        check_numeric(operand_type, ctx, operator='+ (unary)')
        return operand_type
    if ctx.MINUS():
        operand_type = self.visit(ctx.unaryExpr())
        check_numeric(operand_type, ctx, operator='- (unary)')
        return operand_type
    return self.visit(ctx.powExpr())

def visitParensExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.ParensExprContext):
    return self.visit(ctx.expression())
