from dataclasses import dataclass, field

from generated.NetLangListener import NetLangListener
from generated.NetLangParser import NetLangParser
from interpreter.errors import NetLangRuntimeError
from interpreter.variables import Variable, Function


@dataclass
class VariableCollectorListener(NetLangListener):
    variables: dict[str, Variable] = field(default_factory=dict)

    def enterVariableDeclaration(self, ctx: NetLangParser.VariableDeclarationContext):
        variable_name: str = ctx.ID().getText()
        variable_type: str = ctx.type_().getText()
        line: int = ctx.start.line

        if variable_name in self.variables:
            existing = self.variables[variable_name]
            if existing.type == "function":
                raise NetLangRuntimeError(
                    f"Cannot declare variable '{variable_name}' – function with this name was already declared on line {existing.line_declared}",
                    ctx
                )
            else:
                raise NetLangRuntimeError(
                    f"Redeclaration of variable '{variable_name}' (first declared on line {existing.line_declared})",
                    ctx
                )

        self.variables[variable_name] = Variable(variable_type, line)

    def enterFunctionDeclarationStatement(self, ctx: NetLangParser.FunctionDeclarationStatementContext):
        function_name: str = ctx.ID().getText()
        return_type: str = ctx.type_().getText() if ctx.type_() else None
        line: int = ctx.start.line

        if function_name in self.variables:
            existing = self.variables[function_name]
            if existing.type != "function":
                raise NetLangRuntimeError(
                    f"Cannot declare function '{function_name}' – variable with this name was already declared on line {existing.line_declared}",
                    ctx
                )
            else:
                raise NetLangRuntimeError(
                    f"Redeclaration of function '{function_name}' (first declared on line {existing.line_declared})",
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
            body_ctx=ctx.block()
        )

        self.variables[function_name] = Variable("function", line, function)