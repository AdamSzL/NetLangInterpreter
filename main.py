import sys
from antlr4 import *
from generated.NetLangLexer import NetLangLexer
from generated.NetLangParser import NetLangParser
from interpreter.errors import NetLangErrorListener, NetLangRuntimeError
from interpreter import Interpreter
from interpreter.logging import log

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
        interpreter = Interpreter()
        interpreter.visit(tree)
    except NetLangRuntimeError as e:
        log(f"[bold red]Runtime Error:[/bold red] {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()