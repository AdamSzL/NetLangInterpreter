from interpreter.errors import NetLangRuntimeError

def visitAddToListStatement(self, ctx):
    value = self.visit(ctx.expression())
    target_list = self.visit(ctx.fieldAccess())

    if not isinstance(target_list, list):
        raise NetLangRuntimeError(
            message=f"Target of 'add' is not a list",
            ctx=ctx
        )

    target_list.append(value)
    # print(f"[add] {value} to {ctx.fieldAccess().getText()}")
    return value


def visitRemoveFromListStatement(self, ctx):
    value = self.visit(ctx.expression())
    target_list = self.visit(ctx.fieldAccess())

    if not isinstance(target_list, list):
        raise NetLangRuntimeError(
            message=f"Target of 'remove' is not a list",
            ctx=ctx
        )

    try:
        target_list.remove(value)
        # print(f"[remove] {value} from {ctx.fieldAccess().getText()}")
    except ValueError:
        raise NetLangRuntimeError(
            message=f"Value '{value}' not found in list '{ctx.fieldAccess().getText()}'",
            ctx=ctx
        )

    return value


def visitListLiteral(self, ctx):
    elements = []
    if ctx.expressionList():
        for expr in ctx.expressionList().expression():
            elements.append(self.visit(expr))
    return elements

def visitListIndexAccess(self, ctx):
    list_name = ctx.ID().getText()
    index = self.visit(ctx.expression())

    if list_name not in self.variables:
        raise NetLangRuntimeError(f"Variable {list_name} not defined", ctx)

    lst = self.variables[list_name]
    if not isinstance(lst, list):
        raise NetLangRuntimeError(f"{list_name} is not a list", ctx)

    try:
        return lst[index]
    except IndexError:
        raise NetLangRuntimeError(f"Index {index} out of range for list {list_name}", ctx)

def visitListIndexAssignment(self, ctx):
    list_access = ctx.listIndexAccess()
    list_name = list_access.ID().getText()
    index = self.visit(list_access.expression())

    value = self.visit(ctx.expression())

    lst = self.variables.get(list_name)
    if not isinstance(lst, list):
        raise NetLangRuntimeError(f"{list_name} is not a list")

    if index >= len(lst):
        raise NetLangRuntimeError(f"Index {index} out of range for list {list_name}")

    lst[index] = value
    # print(f"[update] {list_name} at {index} <- {value}")