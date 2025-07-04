from dataclasses import dataclass
from generated.NetLangVisitor import NetLangVisitor
from shared.model import Connection
from shared.model.Scope import Scope
from shared.utils.scopes import ScopedVisitorBase
from .variables import visitVariableDeclaration, visitVariableAssignment, visitScopedIdentifier,assign_device_uids, generate_uid
from .functions import visitFunctionCall, visitFunctionCallExpr, visitReturnStatement, visitFunctionDeclarationStatement
from .lists import visitAddToListStatement, visitDeleteListElementStatement, visitListLiteral, getListAndIndex
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
from .fields import visitFieldAccess, visitFieldAccessExpr, visitFieldAssignment, evaluateParentOfAccess, evaluateFieldAccessUntil
from .devices import visitConnectStatement
from .flowcontrol import visitIfStatement, visitRepeatWhileLoop, visitRepeatTimes, visitRepeatRange, visitEachLoop, visitBreakStatement, visitContinueStatement, visitRepeatTimesLoop, visitBlockStatement
from interpreter.visualization.main import draw_graph_and_animate_packet, assign_uids_from_connections
from .packets import visitSendPacketStatement
from types import MethodType

@dataclass
class Interpreter(NetLangVisitor, ScopedVisitorBase):

    def visitProgram(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)

    def visitPrintStatement(self, ctx):
        values = [self.visit(expr) for expr in ctx.expressionList().expression()]
        stringified = []
        for value in values:
            if isinstance(value, bool):
                stringified.append("true" if value else "false")
            elif value is None:
                stringified.append("void")
            else:
                stringified.append(str(value))
        print(" ".join(stringified))

    def __init__(self):
        self.visitVariableDeclaration = MethodType(visitVariableDeclaration, self)
        self.visitVariableAssignment = MethodType(visitVariableAssignment, self)
        self.assign_device_uids = MethodType(assign_device_uids, self)
        self.generate_uid = MethodType(generate_uid, self)

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
        self.evaluateParentOfAccess = MethodType(evaluateParentOfAccess, self)
        self.evaluateFieldAccessUntil = MethodType(evaluateFieldAccessUntil, self)

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
        self.visitIfStatement = MethodType(visitIfStatement, self)
        self.visitRepeatWhileLoop = MethodType(visitRepeatWhileLoop, self)
        self.visitRepeatTimesLoop = MethodType(visitRepeatTimesLoop, self)
        self.visitRepeatTimes = MethodType(visitRepeatTimes, self)
        self.visitRepeatRange = MethodType(visitRepeatRange, self)
        self.visitEachLoop = MethodType(visitEachLoop, self)
        self.visitBlockStatement = MethodType(visitBlockStatement, self)
        self.visitSendPacketStatement = MethodType(visitSendPacketStatement, self)
        self.visitBreakStatement = MethodType(visitBreakStatement, self)
        self.visitContinueStatement = MethodType(visitContinueStatement, self)

        self.visitFunctionDeclarationStatement = MethodType(visitFunctionDeclarationStatement, self)
        self.visitFunctionCallExpr = MethodType(visitFunctionCallExpr, self)
        self.visitFunctionCall = MethodType(visitFunctionCall, self)
        self.visitReturnStatement = MethodType(visitReturnStatement, self)
        self.visitScopedIdentifier = MethodType(visitScopedIdentifier, self)

        self.draw_graph_and_animate_packet = MethodType(draw_graph_and_animate_packet, self)
        self.assign_uids_from_connections = MethodType(assign_uids_from_connections, self)

        ScopedVisitorBase.__init__(self)
        self.connections: list[Connection] = []
        self.used_ids: set[str] = set()
        self.call_depth = 0
        self.max_call_depth = 100
        self.arp_table: dict[str, str] = {}