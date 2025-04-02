# Generated from ./NetLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .NetLangParser import NetLangParser
else:
    from NetLangParser import NetLangParser

# This class defines a complete generic visitor for a parse tree produced by NetLangParser.

class NetLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by NetLangParser#program.
    def visitProgram(self, ctx:NetLangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#statement.
    def visitStatement(self, ctx:NetLangParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:NetLangParser.VariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#variableAssignment.
    def visitVariableAssignment(self, ctx:NetLangParser.VariableAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#addToListStatement.
    def visitAddToListStatement(self, ctx:NetLangParser.AddToListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#removeFromListStatement.
    def visitRemoveFromListStatement(self, ctx:NetLangParser.RemoveFromListStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#fieldAssignment.
    def visitFieldAssignment(self, ctx:NetLangParser.FieldAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#connectStatement.
    def visitConnectStatement(self, ctx:NetLangParser.ConnectStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#disconnectStatement.
    def visitDisconnectStatement(self, ctx:NetLangParser.DisconnectStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#showInterfacesStatement.
    def visitShowInterfacesStatement(self, ctx:NetLangParser.ShowInterfacesStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#sendPacketStatement.
    def visitSendPacketStatement(self, ctx:NetLangParser.SendPacketStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#ifStatement.
    def visitIfStatement(self, ctx:NetLangParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#elseIfClause.
    def visitElseIfClause(self, ctx:NetLangParser.ElseIfClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#elseClause.
    def visitElseClause(self, ctx:NetLangParser.ElseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#block.
    def visitBlock(self, ctx:NetLangParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#printStatement.
    def visitPrintStatement(self, ctx:NetLangParser.PrintStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#loopStatement.
    def visitLoopStatement(self, ctx:NetLangParser.LoopStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#repeatTimesLoop.
    def visitRepeatTimesLoop(self, ctx:NetLangParser.RepeatTimesLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#repeatWhileLoop.
    def visitRepeatWhileLoop(self, ctx:NetLangParser.RepeatWhileLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#eachLoop.
    def visitEachLoop(self, ctx:NetLangParser.EachLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#functionDeclarationStatement.
    def visitFunctionDeclarationStatement(self, ctx:NetLangParser.FunctionDeclarationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#parameterList.
    def visitParameterList(self, ctx:NetLangParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#parameter.
    def visitParameter(self, ctx:NetLangParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#returnStatement.
    def visitReturnStatement(self, ctx:NetLangParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#listIndexAssignment.
    def visitListIndexAssignment(self, ctx:NetLangParser.ListIndexAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#type.
    def visitType(self, ctx:NetLangParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#objectType.
    def visitObjectType(self, ctx:NetLangParser.ObjectTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#deviceType.
    def visitDeviceType(self, ctx:NetLangParser.DeviceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#geExpr.
    def visitGeExpr(self, ctx:NetLangParser.GeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#gtExpr.
    def visitGtExpr(self, ctx:NetLangParser.GtExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#orExpr.
    def visitOrExpr(self, ctx:NetLangParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#subExpr.
    def visitSubExpr(self, ctx:NetLangParser.SubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#parenExpr.
    def visitParenExpr(self, ctx:NetLangParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#neqExpr.
    def visitNeqExpr(self, ctx:NetLangParser.NeqExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#ltExpr.
    def visitLtExpr(self, ctx:NetLangParser.LtExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#eqExpr.
    def visitEqExpr(self, ctx:NetLangParser.EqExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#addExpr.
    def visitAddExpr(self, ctx:NetLangParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#leExpr.
    def visitLeExpr(self, ctx:NetLangParser.LeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#mulExpr.
    def visitMulExpr(self, ctx:NetLangParser.MulExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#divExpr.
    def visitDivExpr(self, ctx:NetLangParser.DivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#unaryNotExpr.
    def visitUnaryNotExpr(self, ctx:NetLangParser.UnaryNotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#andExpr.
    def visitAndExpr(self, ctx:NetLangParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#expression.
    def visitExpression(self, ctx:NetLangParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#listLiteral.
    def visitListLiteral(self, ctx:NetLangParser.ListLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#expressionList.
    def visitExpressionList(self, ctx:NetLangParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#cidrLiteral.
    def visitCidrLiteral(self, ctx:NetLangParser.CidrLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#objectInitializer.
    def visitObjectInitializer(self, ctx:NetLangParser.ObjectInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#objectFieldList.
    def visitObjectFieldList(self, ctx:NetLangParser.ObjectFieldListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#objectField.
    def visitObjectField(self, ctx:NetLangParser.ObjectFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#fieldAccess.
    def visitFieldAccess(self, ctx:NetLangParser.FieldAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#functionCall.
    def visitFunctionCall(self, ctx:NetLangParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NetLangParser#listIndexAccess.
    def visitListIndexAccess(self, ctx:NetLangParser.ListIndexAccessContext):
        return self.visitChildren(ctx)



del NetLangParser