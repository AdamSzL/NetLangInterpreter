from dataclasses import dataclass, field
from generated.NetLangListener import NetLangListener
from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError, NetLangTypeError
from interpreter.functions import Function
from interpreter.variables import Variable

@dataclass
class VariableCollectorListener(NetLangListener):
    variables: dict[str, Variable] = field(default_factory=dict)
    functions: dict[str, Function] = field(default_factory=dict)

    def enterVariableDeclaration(self, ctx: NetLangParser.VariableDeclarationContext):
        variable_name: str = ctx.ID().getText()
        variable_type: str = ctx.type_().getText()
        line: int = ctx.start.line

        if variable_name in self.variables:
            raise NetLangTypeError(
                f"Redeclaration of variable '{variable_name}' (first declared on line {self.variables[variable_name].line_declared})",
                ctx
            )

        if variable_name in self.functions:
            raise NetLangTypeError(
                f"Cannot declare variable '{variable_name}' – function with this name was already declared on line {self.functions[variable_name].line_declared}",
                ctx
            )

        self.variables[variable_name] = Variable(variable_type, line)

    def enterFunctionDeclarationStatement(self, ctx: NetLangParser.FunctionDeclarationStatementContext):
        function_name: str = ctx.ID().getText()
        return_type: str = ctx.type_().getText() if ctx.type_() else None
        line: int = ctx.start.line

        if function_name in self.functions:
            raise NetLangTypeError(
                f"Redeclaration of function '{function_name}' (first declared on line {self.functions[function_name].line_declared})",
                ctx
            )

        if function_name in self.variables:
            raise NetLangTypeError(
                f"Cannot declare function '{function_name}' – variable with this name was already declared on line {self.variables[function_name].line_declared}",
                ctx
            )

        parameters = []

        parameter_list = ctx.parameterList()
        if parameter_list:
            for param_ctx in parameter_list.parameter():
                param_name = param_ctx.ID().getText()
                param_type = param_ctx.type_().getText()
                parameters.append((param_name, param_type))

        function = Function(
            parameters=parameters,
            return_type=return_type,
            line_declared=line,
            body_ctx=ctx.block()
        )

        self.functions[function_name] = function
