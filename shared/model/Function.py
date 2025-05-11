from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Function:
    parameters: list[tuple[str, str]]
    return_type: Optional[str]
    line_declared: int
    body_ctx: Any