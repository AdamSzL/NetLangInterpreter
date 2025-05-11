from dataclasses import dataclass
from typing import Any


@dataclass
class ReturnValue(Exception):
    value: Any