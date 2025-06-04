from typing import TYPE_CHECKING

from generated.NetLangParser import NetLangParser
from shared.model.Device import Device
from shared.model.Port import Port
from shared.utils.errors import NetLangRuntimeError
from shared.model import IPAddress, MACAddress

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitFieldAccessExpr(self: "Interpreter", ctx: NetLangParser.FieldAccessExprContext):
    return self.visit(ctx.fieldAccess())

def visitFieldAccess(self: "Interpreter", ctx: NetLangParser.FieldAccessContext):
    return self.evaluateFieldAccessUntil(ctx, stop_before_last_dot=False)

def visitFieldAssignment(self: "Interpreter", ctx: NetLangParser.FieldAssignmentContext):
    access = ctx.fieldAccess()
    value = self.visit(ctx.expression())

    last_operator, last_operand = get_last_field_access_step(access)

    if last_operator == ".":
        parent = self.evaluateFieldAccessUntil(access, stop_before_last_dot=True)
        field_name = last_operand.getText()

        old_value = getattr(parent, field_name)

        if field_name == "ip":
            if old_value is not None:
                IPAddress.unregister(str(old_value.ip))
                self.arp_table.pop(str(old_value.ip), None)
            IPAddress.register(str(value.ip), ctx)
            self.arp_table[str(value.ip)] = value.ip

        elif field_name == "mac":
            if old_value is not None:
                MACAddress.unregister(old_value.mac)
                self.arp_table.pop(str(parent.ip.ip), None)
            MACAddress.register(value.mac, ctx)
            self.arp_table[str(parent.ip.ip)] = value.mac

        elif field_name == "ports":
            raise NetLangRuntimeError(f"Cannot modify ports of the device '{parent.name}'", ctx)

        setattr(parent, field_name, value)

        if hasattr(parent, "validate_logic") and callable(parent.validate_logic):
            parent.validate_logic(ctx)

        return value
    elif last_operator == "<":
        object_parent = self.evaluateFieldAccessUntil(access, stop_before_last_dot=True)
        parent = self.evaluateFieldAccessUntil(access, stop_before_last_index=True)
        index = int(self.visit(last_operand))

        if object_parent is not None and isinstance(object_parent, Device) and isinstance(value, Port):
            raise NetLangRuntimeError(f"Cannot modify ports of the device '{object_parent.name}'", ctx)

        try:
            parent[index] = value
        except:
            raise NetLangRuntimeError(f"Index {index} is out of range for list of length {len(parent)}", ctx)
        return value

    raise NetLangRuntimeError(f"Unsupported assignment operator '{last_operator}'", ctx)

def evaluateParentOfAccess(self: "Interpreter", ctx: NetLangParser.FieldAccessContext):
    return self.evaluateFieldAccessUntil(ctx, stop_before_last_dot=True)

def evaluateFieldAccessUntil(
        self: "Interpreter",
        ctx: NetLangParser.FieldAccessContext,
        stop_before_last_dot: bool = False,
        stop_before_last_index: bool = False
):
    scope, var_name = self.visit(ctx.scopedIdentifier())
    current = scope.variables[var_name].value
    if current is None:
        raise NetLangRuntimeError(f"Variable '{var_name}' is used before being initialized", ctx)

    end = len(ctx.children)

    if stop_before_last_dot:
        last_dot_index = -1
        for j in range(1, len(ctx.children)):
            if ctx.getChild(j).getText() == ".":
                last_dot_index = j
        if last_dot_index == -1:
            return current
        end = last_dot_index
    elif stop_before_last_index:
        last_index = -1
        for j in range(1, len(ctx.children)):
            if ctx.getChild(j).getText() == "<":
                last_index = j
        if last_index == -1:
            return current
        end = last_index

    i = 1
    while i < end:
        operator = ctx.getChild(i).getText()

        if operator == ".":
            field_name = ctx.getChild(i + 1).getText()
            if isinstance(current, list) and field_name == "size":
                current = len(current)
            else:
                current = getattr(current, field_name)
            i += 2
        elif operator == "<":
            index = int(self.visit(ctx.getChild(i + 1)))
            try:
                current = current[index]
            except IndexError:
                raise NetLangRuntimeError(f"Index {index} is out of range for list of length {len(current)}", ctx)
            i += 3

    return current

def get_last_field_access_step(ctx: NetLangParser.FieldAccessContext) -> tuple[str, any]:
    i = 1
    last_op = None
    last_arg = None

    while i < len(ctx.children):
        op = ctx.getChild(i).getText()
        if op == ".":
            last_op = "."
            last_arg = ctx.getChild(i + 1)
            i += 2
        elif op == "<":
            last_op = "<"
            last_arg = ctx.getChild(i + 1)
            i += 3
        else:
            break

    return last_op, last_arg