from interpreter.errors import NetLangRuntimeError
from interpreter.types import type_map, is_known_type, check_type
from model.base import NetLangObject

def visitVariableDeclaration(self, ctx):
    name = ctx.ID().getText()
    declared_type = ctx.type_().getText()
    value = self.visit(ctx.expression())

    if isinstance(value, dict) and declared_type in type_map and issubclass(type_map[declared_type], NetLangObject):
        value = type_map[declared_type].from_dict(value, ctx)

    if not is_known_type(declared_type):
        raise NetLangRuntimeError(
            message=f"Unknown type '{declared_type}'",
            ctx=ctx
        )

    if not check_type(declared_type, value):
        raise NetLangRuntimeError(
            f"Type mismatch: cannot assign value '{value}' ({type(value).__name__}) to variable '{name}' of type {declared_type}",
            ctx
        )

    self.variables[name] = value
    print(f"[set] {name}: {declared_type} = {value}")
    return value

def visitVariableAssignment(self, ctx):
    name = ctx.ID().getText()
    value = self.visit(ctx.expression())
    if name in self.variables:
        self.variables[name] = value
        print(f"[assign] {name} <- {value}")
    else:
        raise NetLangRuntimeError(f"Undefined variable {name}", ctx)
    return value

def visitFieldAssignment(self, ctx):
    access = ctx.fieldAccess()
    value = self.visit(ctx.expression())

    # Zacznij od pierwszego ID
    current = self.variables.get(access.ID(0).getText())
    if current is None:
        raise NetLangRuntimeError(f"Variable '{access.ID(0).getText()}' not defined")

    # Przechodzimy po chainie, ale ZATRZYMUJEMY się na przedostatnim
    for i in range(1, len(access.children) - 2, 2):
        op = access.getChild(i).getText()
        operand = access.getChild(i + 1)

        if op == ".":
            field = operand.getText()
            if not hasattr(current, field):
                raise NetLangRuntimeError(f"'{type(current).__name__}' has no field '{field}'")
            current = getattr(current, field)

        elif op == "<":
            index = int(self.visit(operand))
            if not isinstance(current, list):
                raise NetLangRuntimeError(f"Tried to index non-list object")
            try:
                current = current[index]
            except IndexError:
                raise NetLangRuntimeError(f"Index {index} out of range")

    # Teraz zostały ostatnie dwa elementy: operator + field/index
    last_op = access.getChild(-2).getText()
    last_operand = access.getChild(-1)

    if last_op == ".":
        field_name = last_operand.getText()
        if not hasattr(current, field_name):
            raise NetLangRuntimeError(f"'{type(current).__name__}' has no field '{field_name}'")
        setattr(current, field_name, value)
        print(f"[assign] ...{field_name} ← {value}")
        return value

    elif last_op == "<":
        index = int(self.visit(last_operand))
        if not isinstance(current, list):
            raise NetLangRuntimeError(f"Tried to index non-list object")
        if index >= len(current):
            raise NetLangRuntimeError(f"Index {index} out of range")
        current[index] = value
        print(f"[assign] ...<{index}> ← {value}")
        return value

    raise NetLangRuntimeError(f"Unsupported assignment operator '{last_op}'")