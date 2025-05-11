import sys
from antlr4 import *

from collector.collector import VariableCollectorListener
from generated.NetLangLexer import NetLangLexer
from generated.NetLangParser import NetLangParser
from shared.errors import NetLangErrorListener, NetLangRuntimeError, NetLangSyntaxError, NetLangTypeError
from interpreter import Interpreter
from shared.logging import log

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

        collector = VariableCollectorListener()
        walker = ParseTreeWalker()
        walker.walk(collector, tree)

        type_checker = TypeCheckingVisitor(collector.variables, collector.functions)
        type_checker.visit(tree)
        type_checker.check_all_function_bodies()

        interpreter = Interpreter(collector.variables, collector.functions)
        for statement in tree.statement():
            if statement.functionDeclarationStatement():
                continue
            interpreter.visit(statement)
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