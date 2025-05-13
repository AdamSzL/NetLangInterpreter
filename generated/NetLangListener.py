# Generated from ./NetLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .NetLangParser import NetLangParser
else:
    from NetLangParser import NetLangParser

# This class defines a complete listener for a parse tree produced by NetLangParser.
class NetLangListener(ParseTreeListener):

    # Enter a parse tree produced by NetLangParser#program.
    def enterProgram(self, ctx:NetLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by NetLangParser#program.
    def exitProgram(self, ctx:NetLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by NetLangParser#statement.
    def enterStatement(self, ctx:NetLangParser.StatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#statement.
    def exitStatement(self, ctx:NetLangParser.StatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#variableDeclaration.
    def enterVariableDeclaration(self, ctx:NetLangParser.VariableDeclarationContext):
        pass

    # Exit a parse tree produced by NetLangParser#variableDeclaration.
    def exitVariableDeclaration(self, ctx:NetLangParser.VariableDeclarationContext):
        pass


    # Enter a parse tree produced by NetLangParser#variableAssignment.
    def enterVariableAssignment(self, ctx:NetLangParser.VariableAssignmentContext):
        pass

    # Exit a parse tree produced by NetLangParser#variableAssignment.
    def exitVariableAssignment(self, ctx:NetLangParser.VariableAssignmentContext):
        pass


    # Enter a parse tree produced by NetLangParser#addToListStatement.
    def enterAddToListStatement(self, ctx:NetLangParser.AddToListStatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#addToListStatement.
    def exitAddToListStatement(self, ctx:NetLangParser.AddToListStatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#deleteListElementStatement.
    def enterDeleteListElementStatement(self, ctx:NetLangParser.DeleteListElementStatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#deleteListElementStatement.
    def exitDeleteListElementStatement(self, ctx:NetLangParser.DeleteListElementStatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#fieldAssignment.
    def enterFieldAssignment(self, ctx:NetLangParser.FieldAssignmentContext):
        pass

    # Exit a parse tree produced by NetLangParser#fieldAssignment.
    def exitFieldAssignment(self, ctx:NetLangParser.FieldAssignmentContext):
        pass


    # Enter a parse tree produced by NetLangParser#connectStatement.
    def enterConnectStatement(self, ctx:NetLangParser.ConnectStatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#connectStatement.
    def exitConnectStatement(self, ctx:NetLangParser.ConnectStatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#disconnectStatement.
    def enterDisconnectStatement(self, ctx:NetLangParser.DisconnectStatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#disconnectStatement.
    def exitDisconnectStatement(self, ctx:NetLangParser.DisconnectStatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#showInterfacesStatement.
    def enterShowInterfacesStatement(self, ctx:NetLangParser.ShowInterfacesStatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#showInterfacesStatement.
    def exitShowInterfacesStatement(self, ctx:NetLangParser.ShowInterfacesStatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#sendPacketStatement.
    def enterSendPacketStatement(self, ctx:NetLangParser.SendPacketStatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#sendPacketStatement.
    def exitSendPacketStatement(self, ctx:NetLangParser.SendPacketStatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#ifStatement.
    def enterIfStatement(self, ctx:NetLangParser.IfStatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#ifStatement.
    def exitIfStatement(self, ctx:NetLangParser.IfStatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#elseIfClause.
    def enterElseIfClause(self, ctx:NetLangParser.ElseIfClauseContext):
        pass

    # Exit a parse tree produced by NetLangParser#elseIfClause.
    def exitElseIfClause(self, ctx:NetLangParser.ElseIfClauseContext):
        pass


    # Enter a parse tree produced by NetLangParser#elseClause.
    def enterElseClause(self, ctx:NetLangParser.ElseClauseContext):
        pass

    # Exit a parse tree produced by NetLangParser#elseClause.
    def exitElseClause(self, ctx:NetLangParser.ElseClauseContext):
        pass


    # Enter a parse tree produced by NetLangParser#block.
    def enterBlock(self, ctx:NetLangParser.BlockContext):
        pass

    # Exit a parse tree produced by NetLangParser#block.
    def exitBlock(self, ctx:NetLangParser.BlockContext):
        pass


    # Enter a parse tree produced by NetLangParser#printStatement.
    def enterPrintStatement(self, ctx:NetLangParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#printStatement.
    def exitPrintStatement(self, ctx:NetLangParser.PrintStatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#loopStatement.
    def enterLoopStatement(self, ctx:NetLangParser.LoopStatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#loopStatement.
    def exitLoopStatement(self, ctx:NetLangParser.LoopStatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#repeatTimesLoop.
    def enterRepeatTimesLoop(self, ctx:NetLangParser.RepeatTimesLoopContext):
        pass

    # Exit a parse tree produced by NetLangParser#repeatTimesLoop.
    def exitRepeatTimesLoop(self, ctx:NetLangParser.RepeatTimesLoopContext):
        pass


    # Enter a parse tree produced by NetLangParser#repeatWhileLoop.
    def enterRepeatWhileLoop(self, ctx:NetLangParser.RepeatWhileLoopContext):
        pass

    # Exit a parse tree produced by NetLangParser#repeatWhileLoop.
    def exitRepeatWhileLoop(self, ctx:NetLangParser.RepeatWhileLoopContext):
        pass


    # Enter a parse tree produced by NetLangParser#eachLoop.
    def enterEachLoop(self, ctx:NetLangParser.EachLoopContext):
        pass

    # Exit a parse tree produced by NetLangParser#eachLoop.
    def exitEachLoop(self, ctx:NetLangParser.EachLoopContext):
        pass


    # Enter a parse tree produced by NetLangParser#functionDeclarationStatement.
    def enterFunctionDeclarationStatement(self, ctx:NetLangParser.FunctionDeclarationStatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#functionDeclarationStatement.
    def exitFunctionDeclarationStatement(self, ctx:NetLangParser.FunctionDeclarationStatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#parameterList.
    def enterParameterList(self, ctx:NetLangParser.ParameterListContext):
        pass

    # Exit a parse tree produced by NetLangParser#parameterList.
    def exitParameterList(self, ctx:NetLangParser.ParameterListContext):
        pass


    # Enter a parse tree produced by NetLangParser#parameter.
    def enterParameter(self, ctx:NetLangParser.ParameterContext):
        pass

    # Exit a parse tree produced by NetLangParser#parameter.
    def exitParameter(self, ctx:NetLangParser.ParameterContext):
        pass


    # Enter a parse tree produced by NetLangParser#returnStatement.
    def enterReturnStatement(self, ctx:NetLangParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#returnStatement.
    def exitReturnStatement(self, ctx:NetLangParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#listIndexAssignment.
    def enterListIndexAssignment(self, ctx:NetLangParser.ListIndexAssignmentContext):
        pass

    # Exit a parse tree produced by NetLangParser#listIndexAssignment.
    def exitListIndexAssignment(self, ctx:NetLangParser.ListIndexAssignmentContext):
        pass


    # Enter a parse tree produced by NetLangParser#breakStatement.
    def enterBreakStatement(self, ctx:NetLangParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#breakStatement.
    def exitBreakStatement(self, ctx:NetLangParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#continueStatement.
    def enterContinueStatement(self, ctx:NetLangParser.ContinueStatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#continueStatement.
    def exitContinueStatement(self, ctx:NetLangParser.ContinueStatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#type.
    def enterType(self, ctx:NetLangParser.TypeContext):
        pass

    # Exit a parse tree produced by NetLangParser#type.
    def exitType(self, ctx:NetLangParser.TypeContext):
        pass


    # Enter a parse tree produced by NetLangParser#objectType.
    def enterObjectType(self, ctx:NetLangParser.ObjectTypeContext):
        pass

    # Exit a parse tree produced by NetLangParser#objectType.
    def exitObjectType(self, ctx:NetLangParser.ObjectTypeContext):
        pass


    # Enter a parse tree produced by NetLangParser#deviceType.
    def enterDeviceType(self, ctx:NetLangParser.DeviceTypeContext):
        pass

    # Exit a parse tree produced by NetLangParser#deviceType.
    def exitDeviceType(self, ctx:NetLangParser.DeviceTypeContext):
        pass


    # Enter a parse tree produced by NetLangParser#expression.
    def enterExpression(self, ctx:NetLangParser.ExpressionContext):
        pass

    # Exit a parse tree produced by NetLangParser#expression.
    def exitExpression(self, ctx:NetLangParser.ExpressionContext):
        pass


    # Enter a parse tree produced by NetLangParser#orExpr.
    def enterOrExpr(self, ctx:NetLangParser.OrExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#orExpr.
    def exitOrExpr(self, ctx:NetLangParser.OrExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#andExpr.
    def enterAndExpr(self, ctx:NetLangParser.AndExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#andExpr.
    def exitAndExpr(self, ctx:NetLangParser.AndExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#notExpr.
    def enterNotExpr(self, ctx:NetLangParser.NotExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#notExpr.
    def exitNotExpr(self, ctx:NetLangParser.NotExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#comparisonExpr.
    def enterComparisonExpr(self, ctx:NetLangParser.ComparisonExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#comparisonExpr.
    def exitComparisonExpr(self, ctx:NetLangParser.ComparisonExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#equalityExpr.
    def enterEqualityExpr(self, ctx:NetLangParser.EqualityExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#equalityExpr.
    def exitEqualityExpr(self, ctx:NetLangParser.EqualityExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#addSubExpr.
    def enterAddSubExpr(self, ctx:NetLangParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#addSubExpr.
    def exitAddSubExpr(self, ctx:NetLangParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#mulDivExpr.
    def enterMulDivExpr(self, ctx:NetLangParser.MulDivExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#mulDivExpr.
    def exitMulDivExpr(self, ctx:NetLangParser.MulDivExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#unaryExpr.
    def enterUnaryExpr(self, ctx:NetLangParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#unaryExpr.
    def exitUnaryExpr(self, ctx:NetLangParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#powExpr.
    def enterPowExpr(self, ctx:NetLangParser.PowExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#powExpr.
    def exitPowExpr(self, ctx:NetLangParser.PowExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#ParensExpr.
    def enterParensExpr(self, ctx:NetLangParser.ParensExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#ParensExpr.
    def exitParensExpr(self, ctx:NetLangParser.ParensExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#VariableExpr.
    def enterVariableExpr(self, ctx:NetLangParser.VariableExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#VariableExpr.
    def exitVariableExpr(self, ctx:NetLangParser.VariableExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#IntLiteral.
    def enterIntLiteral(self, ctx:NetLangParser.IntLiteralContext):
        pass

    # Exit a parse tree produced by NetLangParser#IntLiteral.
    def exitIntLiteral(self, ctx:NetLangParser.IntLiteralContext):
        pass


    # Enter a parse tree produced by NetLangParser#FloatLiteral.
    def enterFloatLiteral(self, ctx:NetLangParser.FloatLiteralContext):
        pass

    # Exit a parse tree produced by NetLangParser#FloatLiteral.
    def exitFloatLiteral(self, ctx:NetLangParser.FloatLiteralContext):
        pass


    # Enter a parse tree produced by NetLangParser#BoolLiteral.
    def enterBoolLiteral(self, ctx:NetLangParser.BoolLiteralContext):
        pass

    # Exit a parse tree produced by NetLangParser#BoolLiteral.
    def exitBoolLiteral(self, ctx:NetLangParser.BoolLiteralContext):
        pass


    # Enter a parse tree produced by NetLangParser#StringLiteral.
    def enterStringLiteral(self, ctx:NetLangParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by NetLangParser#StringLiteral.
    def exitStringLiteral(self, ctx:NetLangParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by NetLangParser#CIDRLiteralExpr.
    def enterCIDRLiteralExpr(self, ctx:NetLangParser.CIDRLiteralExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#CIDRLiteralExpr.
    def exitCIDRLiteralExpr(self, ctx:NetLangParser.CIDRLiteralExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#IPAddressLiteral.
    def enterIPAddressLiteral(self, ctx:NetLangParser.IPAddressLiteralContext):
        pass

    # Exit a parse tree produced by NetLangParser#IPAddressLiteral.
    def exitIPAddressLiteral(self, ctx:NetLangParser.IPAddressLiteralContext):
        pass


    # Enter a parse tree produced by NetLangParser#MacAddressLiteral.
    def enterMacAddressLiteral(self, ctx:NetLangParser.MacAddressLiteralContext):
        pass

    # Exit a parse tree produced by NetLangParser#MacAddressLiteral.
    def exitMacAddressLiteral(self, ctx:NetLangParser.MacAddressLiteralContext):
        pass


    # Enter a parse tree produced by NetLangParser#ListLiteralExpr.
    def enterListLiteralExpr(self, ctx:NetLangParser.ListLiteralExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#ListLiteralExpr.
    def exitListLiteralExpr(self, ctx:NetLangParser.ListLiteralExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#ObjectInitializerExpr.
    def enterObjectInitializerExpr(self, ctx:NetLangParser.ObjectInitializerExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#ObjectInitializerExpr.
    def exitObjectInitializerExpr(self, ctx:NetLangParser.ObjectInitializerExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#FieldAccessExpr.
    def enterFieldAccessExpr(self, ctx:NetLangParser.FieldAccessExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#FieldAccessExpr.
    def exitFieldAccessExpr(self, ctx:NetLangParser.FieldAccessExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#FunctionCallExpr.
    def enterFunctionCallExpr(self, ctx:NetLangParser.FunctionCallExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#FunctionCallExpr.
    def exitFunctionCallExpr(self, ctx:NetLangParser.FunctionCallExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#ListIndexAccessExpr.
    def enterListIndexAccessExpr(self, ctx:NetLangParser.ListIndexAccessExprContext):
        pass

    # Exit a parse tree produced by NetLangParser#ListIndexAccessExpr.
    def exitListIndexAccessExpr(self, ctx:NetLangParser.ListIndexAccessExprContext):
        pass


    # Enter a parse tree produced by NetLangParser#listLiteral.
    def enterListLiteral(self, ctx:NetLangParser.ListLiteralContext):
        pass

    # Exit a parse tree produced by NetLangParser#listLiteral.
    def exitListLiteral(self, ctx:NetLangParser.ListLiteralContext):
        pass


    # Enter a parse tree produced by NetLangParser#expressionList.
    def enterExpressionList(self, ctx:NetLangParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by NetLangParser#expressionList.
    def exitExpressionList(self, ctx:NetLangParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by NetLangParser#cidrLiteral.
    def enterCidrLiteral(self, ctx:NetLangParser.CidrLiteralContext):
        pass

    # Exit a parse tree produced by NetLangParser#cidrLiteral.
    def exitCidrLiteral(self, ctx:NetLangParser.CidrLiteralContext):
        pass


    # Enter a parse tree produced by NetLangParser#objectInitializer.
    def enterObjectInitializer(self, ctx:NetLangParser.ObjectInitializerContext):
        pass

    # Exit a parse tree produced by NetLangParser#objectInitializer.
    def exitObjectInitializer(self, ctx:NetLangParser.ObjectInitializerContext):
        pass


    # Enter a parse tree produced by NetLangParser#objectFieldList.
    def enterObjectFieldList(self, ctx:NetLangParser.ObjectFieldListContext):
        pass

    # Exit a parse tree produced by NetLangParser#objectFieldList.
    def exitObjectFieldList(self, ctx:NetLangParser.ObjectFieldListContext):
        pass


    # Enter a parse tree produced by NetLangParser#objectField.
    def enterObjectField(self, ctx:NetLangParser.ObjectFieldContext):
        pass

    # Exit a parse tree produced by NetLangParser#objectField.
    def exitObjectField(self, ctx:NetLangParser.ObjectFieldContext):
        pass


    # Enter a parse tree produced by NetLangParser#fieldAccess.
    def enterFieldAccess(self, ctx:NetLangParser.FieldAccessContext):
        pass

    # Exit a parse tree produced by NetLangParser#fieldAccess.
    def exitFieldAccess(self, ctx:NetLangParser.FieldAccessContext):
        pass


    # Enter a parse tree produced by NetLangParser#functionCall.
    def enterFunctionCall(self, ctx:NetLangParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by NetLangParser#functionCall.
    def exitFunctionCall(self, ctx:NetLangParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by NetLangParser#listIndexAccess.
    def enterListIndexAccess(self, ctx:NetLangParser.ListIndexAccessContext):
        pass

    # Exit a parse tree produced by NetLangParser#listIndexAccess.
    def exitListIndexAccess(self, ctx:NetLangParser.ListIndexAccessContext):
        pass



del NetLangParser