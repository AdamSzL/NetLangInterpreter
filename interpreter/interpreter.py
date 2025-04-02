from generated.NetLangVisitor import NetLangVisitor
from .variables import visitVariableDeclaration, visitVariableAssignment, visitFieldAssignment
from .lists import visitAddToListStatement, visitRemoveFromListStatement, visitListLiteral, visitListIndexAccess, visitListIndexAssignment
from .expressions import visitExpression, visitFieldAccess, visitObjectInitializer, visitCidrLiteral
from .devices import visitConnectStatement, visitShowInterfacesStatement
from .visualization import draw_graph
from .packets import visitSendPacketStatement, forward_packet

class Interpreter(NetLangVisitor):
    def __init__(self):
        self.variables = {}
        self.connections = []

    def visitProgram(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)
        self.draw_graph()

    def visitPrintStatement(self, ctx):
        print(self.visit(ctx.expression()))

    visitVariableDeclaration = visitVariableDeclaration
    visitVariableAssignment = visitVariableAssignment
    visitExpression = visitExpression
    visitConnectStatement = visitConnectStatement
    visitAddToListStatement = visitAddToListStatement
    visitRemoveFromListStatement = visitRemoveFromListStatement
    visitListLiteral = visitListLiteral
    visitCidrLiteral = visitCidrLiteral
    visitObjectInitializer = visitObjectInitializer
    visitFieldAccess = visitFieldAccess
    visitFieldAssignment = visitFieldAssignment
    visitListIndexAccess = visitListIndexAccess
    visitListIndexAssignment = visitListIndexAssignment
    visitShowInterfacesStatement = visitShowInterfacesStatement
    visitSendPacketStatement = visitSendPacketStatement
    draw_graph = draw_graph
    forward_packet = forward_packet