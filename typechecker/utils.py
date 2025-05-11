from shared.errors import NetLangTypeError


def check_bool(actual_type: str, ctx, operator: str = None, statement: str = None):
    if actual_type != "bool":
        if operator:
            raise NetLangTypeError(
                f"Invalid operand for operator '{operator}': got {actual_type}, expected bool",
                ctx
            )
        elif statement:
            raise NetLangTypeError(
                f"Condition in '{statement}' statement must be a value of type bool (got {actual_type} instead)",
                ctx
            )

def check_numeric(actual_type: str, ctx, operator: str = None):
    if actual_type != "int" and actual_type != "float":
        if operator:
            raise NetLangTypeError(
                f"Invalid operand for operator '{operator}': got {actual_type}, expected int/float",
                ctx
            )


def check_numeric_or_string(actual_type: str, ctx, operator: str = None):
    if actual_type != "int" and actual_type != "float" and actual_type != "string":
        if operator:
            raise NetLangTypeError(
                f"Invalid operand for operator '{operator}': got {actual_type}, expected int/float/string",
                ctx
            )

def dummy_value_for_type(type_name: str):
    return {
        "int": 0,
        "string": "",
        "bool": False,
        "float": 0.0,
    }.get(type_name, None)