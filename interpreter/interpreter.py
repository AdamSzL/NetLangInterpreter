from dataclasses import dataclass
from generated.NetLangVisitor import NetLangVisitor
from shared.model import Connection
from shared.model.Function import Function
from shared.model.Scope import Scope
from shared.model.Variable import Variable
from shared.scopes import ScopedVisitorBase
from .variables import visitVariableDeclaration, visitVariableAssignment, visitScopedIdentifier
from .functions import visitFunctionCall, visitFunctionCallExpr, visitReturnStatement, visitFunctionDeclarationStatement
from .lists import visitAddToListStatement, visitDeleteListElementStatement, visitListLiteral, visitListIndexAccess, visitListIndexAssignment, getListAndIndex
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
    visitListIndexAccessExpr,
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
from .fields import visitFieldAccess, visitFieldAccessExpr, visitFieldAssignment
from .devices import visitConnectStatement, visitShowInterfacesStatement
from .flowcontrol import visitIfStatement, visitRepeatWhileLoop, visitRepeatTimesLoop, visitEachLoop, visitBreakStatement, visitContinueStatement
from .visualization import draw_graph
from .packets import visitSendPacketStatement, forward_packet
from types import MethodType

@dataclass
class Interpreter(NetLangVisitor, ScopedVisitorBase):

    def visitProgram(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)
        self.draw_graph()

    def visitPrintStatement(self, ctx):
        value = self.visit(ctx.expression())
        if isinstance(value, bool):
            print("true" if value else "false")
        elif value is None:
            print("void")
        else:
            print(value)

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
        self.visitListIndexAccessExpr = MethodType(visitListIndexAccessExpr, self)

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
        self.getListAndIndex = MethodType(getListAndIndex, self)
        self.visitListLiteral = MethodType(visitListLiteral, self)
        self.visitObjectInitializerExpr = MethodType(visitObjectInitializerExpr, self)
        self.visitFieldAccessExpr = MethodType(visitFieldAccessExpr, self)
        self.visitFieldAssignment = MethodType(visitFieldAssignment, self)
        self.visitListIndexAccess = MethodType(visitListIndexAccess, self)
        self.visitListIndexAssignment = MethodType(visitListIndexAssignment, self)
        self.visitShowInterfacesStatement = MethodType(visitShowInterfacesStatement, self)
        self.visitIfStatement = MethodType(visitIfStatement, self)
        self.visitRepeatWhileLoop = MethodType(visitRepeatWhileLoop, self)
        self.visitRepeatTimesLoop = MethodType(visitRepeatTimesLoop, self)
        self.visitEachLoop = MethodType(visitEachLoop, self)
        self.visitSendPacketStatement = MethodType(visitSendPacketStatement, self)
        self.visitBreakStatement = MethodType(visitBreakStatement, self)
        self.visitContinueStatement = MethodType(visitContinueStatement, self)

        self.visitFunctionDeclarationStatement = MethodType(visitFunctionDeclarationStatement, self)
        self.visitFunctionCallExpr = MethodType(visitFunctionCallExpr, self)
        self.visitFunctionCall = MethodType(visitFunctionCall, self)
        self.visitReturnStatement = MethodType(visitReturnStatement, self)
        self.visitScopedIdentifier = MethodType(visitScopedIdentifier, self)

        self.draw_graph = MethodType(draw_graph, self)
        self.forward_packet = MethodType(forward_packet, self)

        ScopedVisitorBase.__init__(self)
        self.connections: list[Connection] = []
        self.call_depth = 0
        self.max_call_depth = 100