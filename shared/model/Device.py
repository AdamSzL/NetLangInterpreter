from dataclasses import dataclass, field
from typing import Optional

from shared.utils.errors import NetLangRuntimeError


@dataclass
class Device:
    name: str
    ports: list
    uid: Optional[str] = field(default=None, init=False)

    def validate_base_logic(self, ctx):
        seen_port_ids = set()
        for port in self.ports:
            if port.portId in seen_port_ids:
                raise NetLangRuntimeError(
                    f"Duplicate portId '{port.portId}' in {self.__class__.__name__} '{getattr(self, 'name', '?')}'",
                    ctx
                )
            seen_port_ids.add(port.portId)