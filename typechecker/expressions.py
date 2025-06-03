from typing import TYPE_CHECKING

from generated.NetLangParser import NetLangParser
from shared.errors import NetLangTypeError, NetLangRuntimeError
from shared.model import CIDR, ConnectorType
from shared.model.base import NetLangObject
from shared.utils.types import type_map, type_field_map, are_types_compatible, abstract_types

import difflib

if TYPE_CHECKING:
    from type_checker import TypeCheckingVisitor

def visitAtomExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.AtomExprContext):
    return self.visitChildren(ctx)

def visitIntLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.IntLiteralContext) -> str:
    return "int"

def visitFloatLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.FloatLiteralContext) -> str:
    return "float"

def visitBoolLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.BoolLiteralContext) -> str:
    return "bool"

def visitStringLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.StringLiteralContext) -> str:
    return "string"

def visitVariableExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.VariableExprContext):
    name = ctx.scopedIdentifier().ID().getText()

    if name in ConnectorType.__members__:
        return "string"

    self.scoped_identifier_expectation = "variable"
    try:
        return self.visit(ctx.scopedIdentifier())
    finally:
        self.scoped_identifier_expectation = None

def visitIPAddressLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.IPAddressLiteralContext) -> str:
    return "IP"

def visitMacAddressLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.MacAddressLiteralContext) -> str:
    return "MAC"

def visitListLiteralExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.ListLiteralExprContext) -> list:
    return self.visit(ctx.listLiteral())

def visitCIDRLiteralExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.CIDRLiteralExprContext) -> CIDR:
    return self.visit(ctx.cidrLiteral())

def visitObjectInitializerExpr(self: "TypeCheckingVisitor", ctx: NetLangParser.ObjectInitializerExprContext) -> NetLangObject:
    return self.visit(ctx.objectInitializer())

def visitObjectInitializer(self: "TypeCheckingVisitor", ctx: NetLangParser.ObjectInitializerContext):
    type_name = ctx.objectType().getText()
    if type_name in abstract_types:
        raise NetLangTypeError(
            f"Cannot instantiate abstract type '{type_name}'",
            ctx
        )

    field_def = type_field_map[type_name]
    required_fields = field_def.get("required", {})
    optional_fields = field_def.get("optional", {})
    expected_fields = {**required_fields, **optional_fields}

    seen_fields = set()
    given_fields = set()

    if ctx.objectFieldList():
        for fieldCtx in ctx.objectFieldList().objectField():
            field_name = fieldCtx.ID().getText()

            if field_name in seen_fields:
                raise NetLangTypeError(
                    f"Field '{field_name}' is specified more than once in initializer of type '{type_name}'",
                    fieldCtx
                )
            seen_fields.add(field_name)
            given_fields.add(field_name)

            if field_name not in expected_fields:
                available_fields = list(expected_fields.keys())
                suggestions = difflib.get_close_matches(field_name, available_fields, n=1, cutoff=0.7)

                if suggestions:
                    message = (
                        f"Field '{field_name}' not allowed in type '{type_name}'. "
                        f"Did you mean '{suggestions[0]}'?"
                    )
                else:
                    fields_list = ", ".join(available_fields)
                    message = (
                        f"Field '{field_name}' not allowed in type '{type_name}'. "
                        f"Available fields: {fields_list}."
                    )

                raise NetLangTypeError(message, fieldCtx)

            expected_field_type = expected_fields[field_name]
            actual_field_type = self.visit(fieldCtx.expression())

            if not are_types_compatible(expected_field_type, actual_field_type):
                raise NetLangTypeError(
                    f"Type mismatch in field '{field_name}': expected '{expected_field_type}', got '{actual_field_type}'",
                    fieldCtx
                )

    if are_types_compatible("Port", type_name):
        if "gateway" in given_fields and "ip" not in given_fields:
            raise NetLangTypeError(
                f"Cannot specify 'gateway' without 'ip' in port of type '{type_name}'",
                ctx
            )

    missing_required = set(required_fields.keys()) - given_fields
    if missing_required:
        raise NetLangTypeError(
            f"Missing required fields for type '{type_name}': {', '.join(sorted(missing_required))}",
            ctx
        )

    return type_name

def visitCidrLiteral(self: "TypeCheckingVisitor", ctx: NetLangParser.CidrLiteralContext):
    if ctx.fieldAccess():
        ip_type = self.visit(ctx.fieldAccess())
        if ip_type != "IP":
            raise NetLangTypeError(
                f"Expected IP inside CIDR, but got {ip_type}",
                ctx.fieldAccess()
            )

    return "CIDR"