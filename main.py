import sys
from antlr4 import *
from generated.NetLangLexer import NetLangLexer
from generated.NetLangParser import NetLangParser
from interpreter.errors import NetLangErrorListener, NetLangRuntimeError, NetLangSyntaxError
from interpreter import Interpreter
from interpreter.logging import log
from rich.text import Text

from interpreter.variables import VariableCollectorListener


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <file.netlang>")
        return

    filename = sys.argv[1]

    try:
        with open(filename, "r") as f:
            input_stream = InputStream(f.read())

        lexer = NetLangLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(NetLangErrorListener())

        stream = CommonTokenStream(lexer)
        parser = NetLangParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(NetLangErrorListener())

        tree = parser.program()

        collector = VariableCollectorListener()
        walker = ParseTreeWalker()
        walker.walk(collector, tree)

        interpreter = Interpreter(collector.variables)
        interpreter.visit(tree)
    except NetLangRuntimeError as e:
        log(f"[bold red]Runtime Error:[/bold red]", e)
        sys.exit(1)
    except NetLangSyntaxError as e:
        log(f"[bold red]Syntax Error:[/bold red]", e)
        sys.exit(1)

if __name__ == '__main__':
    main()