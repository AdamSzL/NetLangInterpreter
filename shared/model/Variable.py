from dataclasses import dataclass
from typing import Any


@dataclass
class Variable:
    type: str
    line_declared: int
    value: Any = None