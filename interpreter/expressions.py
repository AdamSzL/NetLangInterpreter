from interpreter.errors import NetLangRuntimeError
from interpreter.types import type_map
from model import ConnectorType, Protocol, IPAddress, MACAddress, CIDR
from model.base import NetLangObject

def visitExpression(self, ctx):
    if ctx.INT():
        return int(ctx.INT().getText())
    elif ctx.FLOAT():
        return float(ctx.FLOAT().getText())
    elif ctx.STRING():
        return str(ctx.STRING().getText().strip('"'))
    elif ctx.BOOL():
        return bool(ctx.BOOL().getText())
    elif ctx.ID():
        var_name = ctx.ID().getText()
        if var_name in ConnectorType.__members__:
            return ConnectorType[var_name]
        if var_name in Protocol.__members__:
            return Protocol[var_name]
        if var_name in self.variables:
            return self.variables[var_name]
        raise NetLangRuntimeError(f'Variable {var_name} not defined', ctx)
    elif ctx.listLiteral():
        return self.visit(ctx.listLiteral())
    elif ctx.IPADDR():
        return IPAddress(ctx.IPADDR().getText())
    elif ctx.cidrLiteral():
        return self.visit(ctx.cidrLiteral())
    elif ctx.MACADDR():
        return MACAddress(ctx.MACADDR().getText())
    elif ctx.objectInitializer():
        return self.visit(ctx.objectInitializer())
    elif ctx.fieldAccess():
        return self.visit(ctx.fieldAccess())
    elif ctx.listIndexAccess():
        return self.visit(ctx.listIndexAccess())
    else:
        return None

def visitFieldAccess(self, ctx):
    # Zacznij od pierwszego identyfikatora (np. "h1")
    current = self.variables.get(ctx.ID(0).getText())
    if current is None:
        raise NetLangRuntimeError(f"Variable '{ctx.ID(0).getText()}' not defined")

    i = 1
    while i < len(ctx.children):
        operator = ctx.getChild(i).getText()

        if operator == ".":
            field_name = ctx.getChild(i + 1).getText()

            if isinstance(current, list) and field_name == "size":
                current = len(current)
            elif hasattr(current, field_name):
                current = getattr(current, field_name)
            else:
                raise NetLangRuntimeError(
                    f"Object of type {type(current).__name__} has no field '{field_name}'"
                )

            i += 2  # przeskocz kropkę i ID

        elif operator == "<":
            expression_ctx = ctx.getChild(i + 1)
            index = int(self.visit(expression_ctx))
            if not isinstance(current, list):
                raise NetLangRuntimeError(
                    f"Trying to index non-list object of type {type(current).__name__}"
                )
            try:
                current = current[index]
            except IndexError:
                raise NetLangRuntimeError(f"Index {index} out of range")

            i += 3  # przeskocz < expression >

        else:
            raise NetLangRuntimeError(f"Unknown field access operator '{operator}'")

    return current

def visitObjectInitializer(self, ctx):
    obj = {}
    for field in ctx.objectFieldList().objectField():
        name = field.ID().getText()
        value = self.visit(field.expression())
        obj[name] = value
    if ctx.objectType():
        type_name = ctx.objectType().getText()
        if type_name in type_map and issubclass(type_map[type_name], NetLangObject):
            return type_map[type_name].from_dict(obj, ctx)
        else:
            raise NetLangRuntimeError(
                message=f"Unknown object type '{type_name}'",
                ctx=ctx
            )
    return obj

def visitCidrLiteral(self, ctx):
    if ctx.ID():  # np. [routerIP]/24
        var_name = ctx.ID().getText()
        ip = self.variables.get(var_name)

        if not isinstance(ip, IPAddress):
            raise NetLangRuntimeError(f"Variable '{var_name}' is not an IP address", ctx)

        mask = int(ctx.INT().getText())
        return CIDR(f"{ip}/{mask}")

    else:
        ip = ctx.IPADDR().getText()
        mask = int(ctx.INT().getText())
        return CIDR(f"{ip}/{mask}")