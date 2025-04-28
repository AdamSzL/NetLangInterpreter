from typing import Any

from interpreter.errors import NetLangRuntimeError


def get_interface_label(port_id: str, bandwidth: int) -> str:
    if bandwidth == 10:
        prefix = "Ethernet"
    elif bandwidth == 100:
        prefix = "FastEthernet"
    elif bandwidth == 1000:
        prefix = "GigabitEthernet"
    elif bandwidth == 10000:
        prefix = "TenGigabitEthernet"
    else:
        prefix = "UnknownSpeed"

    return f"{prefix}0/{port_id.lstrip('eth')}"

def get_port_by_id(device, port_id):
    for port in device.ports:
        if port.portId == port_id:
            return port
    return None

def ensure_numeric(value: Any, ctx, operator: str = None):
    if type(value) not in (int, float):
        if operator:
            raise NetLangRuntimeError(
                f"Invalid operand for operator '{operator}': got {type(value).__name__}, expected int/float",
                ctx
            )
        else:
            raise NetLangRuntimeError("Expected numeric value", ctx)


def ensure_boolean(value: Any, ctx, operator: str = None):
    if not isinstance(value, bool):
        if operator:
            raise NetLangRuntimeError(
                f"Invalid operand for operator '{operator}': got {type(value).__name__}, expected bool",
                ctx
            )
        else:
            raise NetLangRuntimeError("Expected boolean value", ctx)
