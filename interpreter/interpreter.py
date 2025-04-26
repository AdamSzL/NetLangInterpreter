from dataclasses import dataclass, field

from generated.NetLangVisitor import NetLangVisitor
from model import Connection
from .variables import visitVariableDeclaration, visitVariableAssignment, visitFieldAssignment, Variable
from .lists import visitAddToListStatement, visitRemoveFromListStatement, visitListLiteral, visitListIndexAccess, visitListIndexAssignment
from .expressions import (
    visitIntLiteral,
    visitFloatLiteral,
    visitBoolLiteral,
    visitStringLiteral,
    visitVariableExpr,
    visitListLiteralExpr,
    visitIPAddressLiteralExpr,
    visitCIDRLiteralExpr,
    visitMacAddressLiteralExpr,
    visitObjectInitializerExpr,
    visitFieldAccessExpr,
    visitListIndexAccessExpr,
    visitFieldAccess,
    visitObjectInitializer,
    visitCidrLiteral,
)
from .operators import (
    visitAddExpr,
    visitSubExpr,
    visitMulExpr,
    visitDivExpr,
    visitEqualsExpr,
    visitNotEqualsExpr,
    visitLessThanExpr,
    visitGreaterThanExpr,
    visitLessEqualExpr,
    visitGreaterEqualExpr,
    visitAndExpr,
    visitOrExpr,
    visitNotExpr,
    visitParensExpr,
)
from .devices import visitConnectStatement, visitShowInterfacesStatement
from .visualization import draw_graph
from .packets import visitSendPacketStatement, forward_packet
from types import MethodType

@dataclass
class Interpreter(NetLangVisitor):

    def visitProgram(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)
        self.draw_graph()

    def visitPrintStatement(self, ctx):
        print(self.visit(ctx.expression()))

    def __init__(self, variables: dict[str, Variable]):
        self.visitVariableDeclaration = MethodType(visitVariableDeclaration, self)
        self.visitVariableAssignment = MethodType(visitVariableAssignment, self)

        self.visitIntLiteral = MethodType(visitIntLiteral, self)
        self.visitFloatLiteral = MethodType(visitFloatLiteral, self)
        self.visitBoolLiteral = MethodType(visitBoolLiteral, self)
        self.visitStringLiteral = MethodType(visitStringLiteral, self)
        self.visitVariableExpr = MethodType(visitVariableExpr, self)
        self.visitListLiteralExpr = MethodType(visitListLiteralExpr, self)
        self.visitIPAddressLiteralExpr = MethodType(visitIPAddressLiteralExpr, self)
        self.visitCIDRLiteralExpr = MethodType(visitCIDRLiteralExpr, self)
        self.visitMacAddressLiteralExpr = MethodType(visitMacAddressLiteralExpr, self)
        self.visitObjectInitializerExpr = MethodType(visitObjectInitializerExpr, self)
        self.visitFieldAccessExpr = MethodType(visitFieldAccessExpr, self)
        self.visitListIndexAccessExpr = MethodType(visitListIndexAccessExpr, self)

        self.visitAddExpr = MethodType(visitAddExpr, self)
        self.visitSubExpr = MethodType(visitSubExpr, self)
        self.visitMulExpr = MethodType(visitMulExpr, self)
        self.visitDivExpr = MethodType(visitDivExpr, self)
        self.visitEqualsExpr = MethodType(visitEqualsExpr, self)
        self.visitNotEqualsExpr = MethodType(visitNotEqualsExpr, self)
        self.visitLessThanExpr = MethodType(visitLessThanExpr, self)
        self.visitGreaterThanExpr = MethodType(visitGreaterThanExpr, self)
        self.visitLessEqualExpr = MethodType(visitLessEqualExpr, self)
        self.visitGreaterEqualExpr = MethodType(visitGreaterEqualExpr, self)
        self.visitAndExpr = MethodType(visitAndExpr, self)
        self.visitOrExpr = MethodType(visitOrExpr, self)
        self.visitNotExpr = MethodType(visitNotExpr, self)
        self.visitParensExpr = MethodType(visitParensExpr, self)

        self.visitFieldAccess = MethodType(visitFieldAccess, self)
        self.visitObjectInitializer = MethodType(visitObjectInitializer, self)
        self.visitCidrLiteral = MethodType(visitCidrLiteral, self)

        self.visitConnectStatement = MethodType(visitConnectStatement, self)
        self.visitAddToListStatement = MethodType(visitAddToListStatement, self)
        self.visitRemoveFromListStatement = MethodType(visitRemoveFromListStatement, self)
        self.visitListLiteral = MethodType(visitListLiteral, self)
        self.visitCidrLiteral = MethodType(visitCidrLiteral, self)
        self.visitObjectInitializer = MethodType(visitObjectInitializer, self)
        self.visitFieldAccess = MethodType(visitFieldAccess, self)
        self.visitFieldAssignment = MethodType(visitFieldAssignment, self)
        self.visitListIndexAccess = MethodType(visitListIndexAccess, self)
        self.visitListIndexAssignment = MethodType(visitListIndexAssignment, self)
        self.visitShowInterfacesStatement = MethodType(visitShowInterfacesStatement, self)
        self.visitSendPacketStatement = MethodType(visitSendPacketStatement, self)

        self.draw_graph = MethodType(draw_graph, self)
        self.forward_packet = MethodType(forward_packet, self)

        self.variables: dict[str, Variable] = variables
        self.connections: list[Connection] = []