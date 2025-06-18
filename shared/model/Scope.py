from __future__ import annotations

from dataclasses import dataclass, field
from shared.model.Function import Function
from shared.model.Variable import Variable
from typing import Optional


@dataclass
class Scope:
    variables: dict[str, Variable] = field(default_factory=dict)
    functions: dict[str, Function] = field(default_factory=dict)
    parent: Optional[Scope] = None