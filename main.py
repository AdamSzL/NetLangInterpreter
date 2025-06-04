import sys
from antlr4 import *

from generated.NetLangLexer import NetLangLexer
from generated.NetLangParser import NetLangParser
from shared.utils.errors import NetLangErrorListener, NetLangRuntimeError, NetLangSyntaxError, NetLangTypeError
from interpreter import Interpreter
from shared.utils.logging import log

from typechecker.type_checker import TypeCheckingVisitor


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <file.netlang>")
        return

    filename = sys.argv[1]

    try:
        with open(filename, "r") as f:
            source_code = f.read()
            input_stream = InputStream(source_code)

        lexer = NetLangLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(NetLangErrorListener(source_code))

        stream = CommonTokenStream(lexer)
        parser = NetLangParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(NetLangErrorListener(source_code))

        tree = parser.program()

        type_checker = TypeCheckingVisitor()
        type_checker.visit(tree)
        type_checker.check_all_function_bodies()

        interpreter = Interpreter()
        interpreter.visitProgram(tree)
    except NetLangRuntimeError as e:
        log(f"[bold red]Runtime Error:[/bold red]", e)
        sys.exit(1)
    except NetLangSyntaxError as e:
        log(f"[bold red]Syntax Error:[/bold red]", e)
        sys.exit(1)
    except NetLangTypeError as e:
        log(f"[bold red]Type Error:[/bold red]", e)
        sys.exit(1)

if __name__ == '__main__':
    main()