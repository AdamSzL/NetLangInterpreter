from antlr4.error.ErrorListener import ErrorListener


class NetLangErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line: int, column: int, msg: str, e):
        raise NetLangSyntaxError(f"[Line {line}, Column {column}]: {msg}")


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
