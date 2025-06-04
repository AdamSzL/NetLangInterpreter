from antlr4.error.ErrorListener import ErrorListener

class NetLangErrorListener(ErrorListener):
    def __init__(self, source_code: str):
        self.source_lines = source_code.splitlines()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg: str, e):
        error_line = self.source_lines[line - 1] if 0 <= line - 1 < len(self.source_lines) else ""
        pointer_line = " " * column + "^"

        pretty_msg = self._prettify_message(msg)

        raise NetLangSyntaxError(
            f"Syntax Error at line {line}, column {column}:\n"
            f"{error_line}\n"
            f"{pointer_line}\n"
            f"{pretty_msg}"
        )

    def _prettify_message(self, raw_msg: str) -> str:
        if "no viable alternative" in raw_msg:
            return "Invalid or incomplete statement"
        if "mismatched input" in raw_msg:
            return "Unexpected token"
        return "Invalid syntax"


class NetLangRuntimeError(Exception):
    def __init__(self, message: str, ctx=None):
        if ctx:
            token = ctx.start
            line = token.line
            column = token.column
            message = f"[Line {line}, Column {column}] {message}"
        super().__init__(message)


class NetLangSyntaxError(Exception):
    def __init__(self, message: str, ctx=None):
        if ctx:
            token = ctx.start
            line = token.line
            column = token.column
            message = f"[Line {line}, Column {column}] {message}"
        super().__init__(message)


class NetLangTypeError(Exception):
    def __init__(self, message: str, ctx=None):
        if ctx:
            token = ctx.start
            line = token.line
            column = token.column
            message = f"[Line {line}, Column {column}] {message}"
        self.message = message
        super().__init__(message)

class UndefinedVariableError(NetLangTypeError): pass

class UndefinedFunctionError(NetLangTypeError): pass