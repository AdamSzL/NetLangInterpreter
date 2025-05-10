from dataclasses import dataclass, field

from generated.NetLangVisitor import NetLangVisitor
from interpreter.variables import Variable


@dataclass
class TypeCheckingVisitor(NetLangVisitor):
    variables: dict[str, Variable] = field(default_factory=dict)


