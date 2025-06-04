from dataclasses import dataclass
from typing import Optional

from generated.NetLangParser import NetLangParser
from generated.NetLangVisitor import NetLangVisitor
from shared.utils.scopes import ScopedVisitorBase
from .variables import visitVariableDeclaration, visitVariableAssignment, visitScopedIdentifier, _resolve_identifier_in_scope
from .functions import visitFunctionCall, visitFunctionCallExpr, visitReturnStatement, check_all_function_bodies, visitFunctionDeclarationStatement, execute_function_body, block_returns_type
from .lists import visitAddToListStatement, visitDeleteListElementStatement, visitListLiteral
from .expressions import (
    visitAtomExpr,
    visitIntLiteral,
    visitFloatLiteral,
    visitBoolLiteral,
    visitStringLiteral,
    visitVariableExpr,
    visitListLiteralExpr,
    visitIPAddressLiteral,
    visitCIDRLiteralExpr,
    visitMacAddressLiteral,
    visitObjectInitializerExpr,
    visitObjectInitializer,
    visitCidrLiteral
)
from .operators import (
    visitPowExpr,
    visitAddSubExpr,
    visitMulDivExpr,
    visitEqualityExpr,
    visitComparisonExpr,
    visitAndExpr,
    visitOrExpr,
    visitNotExpr,
    visitParensExpr,
    visitCastExpr,
    visitUnaryExpr
)
from .fields import visitFieldAccess, visitFieldAccessExpr, visitFieldAssignment, evaluate_type_until, evaluate_type_of_parent, was_last_operator_indexing
from .devices import visitConnectStatement
from .flowcontrol import visitIfStatement, visitRepeatWhileLoop, visitRepeatTimes, visitRepeatRange, visitEachLoop, visitBreakStatement, visitContinueStatement
from .packets import visitSendPacketStatement
from types import MethodType

@dataclass
class TypeCheckingVisitor(NetLangVisitor, ScopedVisitorBase):

    def visitProgram(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)

    def visitPrintStatement(self, ctx:NetLangParser.PrintStatementContext):
        for expr in ctx.expressionList().expression():
            self.visit(expr)

    def __init__(self):
        self.visitVariableDeclaration = MethodType(visitVariableDeclaration, self)
        self.visitVariableAssignment = MethodType(visitVariableAssignment, self)

        self.visitAtomExpr = MethodType(visitAtomExpr, self)
        self.visitIntLiteral = MethodType(visitIntLiteral, self)
        self.visitFloatLiteral = MethodType(visitFloatLiteral, self)
        self.visitBoolLiteral = MethodType(visitBoolLiteral, self)
        self.visitStringLiteral = MethodType(visitStringLiteral, self)
        self.visitVariableExpr = MethodType(visitVariableExpr, self)
        self.visitListLiteralExpr = MethodType(visitListLiteralExpr, self)
        self.visitIPAddressLiteral = MethodType(visitIPAddressLiteral, self)
        self.visitCIDRLiteralExpr = MethodType(visitCIDRLiteralExpr, self)
        self.visitMacAddressLiteral = MethodType(visitMacAddressLiteral, self)
        self.visitObjectInitializerExpr = MethodType(visitObjectInitializerExpr, self)
        self.visitFieldAccessExpr = MethodType(visitFieldAccessExpr, self)

        self.visitMulDivExpr = MethodType(visitMulDivExpr, self)
        self.visitAddSubExpr = MethodType(visitAddSubExpr, self)
        self.visitEqualityExpr = MethodType(visitEqualityExpr, self)
        self.visitComparisonExpr = MethodType(visitComparisonExpr, self)
        self.visitPowExpr = MethodType(visitPowExpr, self)
        self.visitAndExpr = MethodType(visitAndExpr, self)
        self.visitOrExpr = MethodType(visitOrExpr, self)
        self.visitNotExpr = MethodType(visitNotExpr, self)
        self.visitParensExpr = MethodType(visitParensExpr, self)
        self.visitCastExpr = MethodType(visitCastExpr, self)
        self.visitUnaryExpr = MethodType(visitUnaryExpr, self)

        self.visitFieldAccessExpr = MethodType(visitFieldAccessExpr, self)
        self.visitObjectInitializerExpr = MethodType(visitObjectInitializerExpr, self)
        self.visitCidrLiteral = MethodType(visitCidrLiteral, self)
        self.visitFieldAccess = MethodType(visitFieldAccess, self)
        self.visitObjectInitializer = MethodType(visitObjectInitializer, self)

        self.visitConnectStatement = MethodType(visitConnectStatement, self)
        self.visitAddToListStatement = MethodType(visitAddToListStatement, self)
        self.visitDeleteListElementStatement = MethodType(visitDeleteListElementStatement, self)
        self.visitListLiteral = MethodType(visitListLiteral, self)
        self.visitObjectInitializerExpr = MethodType(visitObjectInitializerExpr, self)
        self.visitFieldAccessExpr = MethodType(visitFieldAccessExpr, self)
        self.visitFieldAssignment = MethodType(visitFieldAssignment, self)
        self.visitIfStatement = MethodType(visitIfStatement, self)
        self.visitRepeatWhileLoop = MethodType(visitRepeatWhileLoop, self)
        self.visitRepeatTimes = MethodType(visitRepeatTimes, self)
        self.visitRepeatRange = MethodType(visitRepeatRange, self)
        self.visitEachLoop = MethodType(visitEachLoop, self)
        self.visitSendPacketStatement = MethodType(visitSendPacketStatement, self)
        self.visitBreakStatement = MethodType(visitBreakStatement, self)
        self.visitContinueStatement = MethodType(visitContinueStatement, self)
        self.evaluate_type_of_parent = MethodType(evaluate_type_of_parent, self)
        self.evaluate_type_until = MethodType(evaluate_type_until, self)
        self.was_last_operator_indexing = MethodType(was_last_operator_indexing, self)

        self.visitFunctionCallExpr = MethodType(visitFunctionCallExpr, self)
        self.visitFunctionCall = MethodType(visitFunctionCall, self)
        self.visitFunctionDeclarationStatement = MethodType(visitFunctionDeclarationStatement, self)
        self.visitReturnStatement = MethodType(visitReturnStatement, self)
        self.check_all_function_bodies = MethodType(check_all_function_bodies, self)
        self.execute_function_body = MethodType(execute_function_body, self)
        self.block_returns_type = MethodType(block_returns_type, self)

        self._resolve_identifier_in_scope = MethodType(_resolve_identifier_in_scope, self)
        self.visitScopedIdentifier = MethodType(visitScopedIdentifier, self)

        ScopedVisitorBase.__init__(self)
        self.expected_return_type: Optional[str] = None
        self.scoped_identifier_expectation: Optional[str] = None
        self.return_found: bool = False
        self.in_function_body = False
        self.currently_checking_functions: set[str] = set()
        self.in_loop = False
