from typing import TYPE_CHECKING

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangRuntimeError
from shared.model import IPAddress, MACAddress

if TYPE_CHECKING:
    from .interpreter import Interpreter

def visitFieldAccessExpr(self: "Interpreter", ctx: NetLangParser.FieldAccessExprContext):
    return self.visit(ctx.fieldAccess())

def visitFieldAccess(self: "Interpreter", ctx: NetLangParser.FieldAccessContext):
    return self.evaluateFieldAccessUntil(ctx, stop_before_last=False)

def visitFieldAssignment(self: "Interpreter", ctx: NetLangParser.FieldAssignmentContext):
    access = ctx.fieldAccess()
    value = self.visit(ctx.expression())

    parent = self.evaluateParentOfAccess(access)
    last_operator = access.getChild(-2).getText()
    last_operand = access.getChild(-1)
    if last_operator == ".":
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

        setattr(parent, field_name, value)

        if hasattr(parent, "validate_logic") and callable(parent.validate_logic):
            parent.validate_logic(ctx)

        return value
    elif last_operator == "<":
        index = int(self.visit(last_operand))
        try:
            parent[index] = value
        except:
            raise NetLangRuntimeError(f"Index {index} out of range", ctx)
        return value

    raise NetLangRuntimeError(f"Unsupported assignment operator '{last_operator}'", ctx)

def evaluateParentOfAccess(self: "Interpreter", ctx: NetLangParser.FieldAccessContext):
    return self.evaluateFieldAccessUntil(ctx, stop_before_last=True)

def evaluateFieldAccessUntil(self: "Interpreter", ctx, stop_before_last=False):
    scope, var_name = self.visit(ctx.scopedIdentifier())
    current = scope.variables[var_name].value

    end = len(ctx.children)

    if stop_before_last:
        last_dot_index = -1
        for j in range(1, len(ctx.children)):
            if ctx.getChild(j).getText() == ".":
                last_dot_index = j

        if last_dot_index == -1:
            return current

        end = last_dot_index

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
                raise NetLangRuntimeError(f"Index {index} out of range", ctx)
            i += 3

    return current