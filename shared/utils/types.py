from typing import Any, cast

from shared.errors import NetLangTypeError
from shared.model.CIDR import CIDR
from shared.model import CopperEthernetPort
from shared.model.Host import Host
from shared.model import IPAddress
from shared.model import MACAddress
from shared.model import OpticalEthernetPort
from shared.model.Packet import Packet
from shared.model import Router
from shared.model import RoutingEntry
from shared.model.Switch import Switch
from shared.model.WirelessPort import WirelessPort

type_map = {
    "int": int,
    "float": float,
    "string": str,
    "bool": bool,
    "IP": IPAddress,
    "CIDR": CIDR,
    "MAC": MACAddress,
    "CopperEthernetPort": CopperEthernetPort,
    "OpticalEthernetPort": OpticalEthernetPort,
    "WirelessPort": WirelessPort,
    "RoutingEntry": RoutingEntry,
    "Packet": Packet,
    "Host": Host,
    "Switch": Switch,
    "Router": Router,
    "void": type(None)
}

def is_known_type(type_str: str) -> bool:
    if type_str.startswith("[") and type_str.endswith("]"):
        inner = type_str[1:-1].strip()
        return is_known_type(inner)
    return type_str in type_map.keys()

def check_type(declared_type: str, value: Any) -> bool:
    if declared_type.startswith("[") and declared_type.endswith("]"):
        if not isinstance(value, list):
            return False
        element_type_str = declared_type[1:-1]
        return all(check_type(element_type_str, v) for v in cast(list[Any], value))

    expected_type = type_map.get(declared_type)
    if expected_type:
        if expected_type is float:
            return type(value) is float or type(value) is int
        else:
            return type(value) is expected_type

    return False

def are_types_compatible(expected: str, actual: str) -> bool:
    if expected.startswith("[") and expected.endswith("]"):
        if not actual.startswith("[") or not actual.endswith("]"):
            return False
        expected_elem_type = expected[1:-1]
        actual_elem_type = actual[1:-1]
        return are_types_compatible(expected_elem_type, actual_elem_type)

    if expected == "float" and actual == "int":
        return True

    return expected == actual

def get_field_type(type_name: str, field: str) -> str:
    if type_name == "Host":
        if field == "ports":
            return "[CopperEthernetPort]"
        if field.startswith("eth"):
            return "CopperEthernetPort"
    elif type_name == "RoutingEntry":
        if field == "destination":
            return "CIDR"
    elif type_name == "CIDR":
        if field == "broadcast":
            return "IP"
        elif field == "network":
            return "IP"
        elif field == "ip":
            return "IP"
        elif field == "mask":
            return "int"
    elif type_name == "Router":
        if field == "routingTable":
            return "[RoutingEntry]"
        if field == "ports":
            return "[CopperEthernetPort]"
        if field.startswith("eth"):
            return "CopperEthernetPort"
    elif type_name == "Switch":
        if field == "ports":
            return "[CopperEthernetPort]"
        if field.startswith("eth"):
            return "CopperEthernetPort"
    elif type_name == "CopperEthernetPort":
        if field == "ip":
            return "IP"
        if field == "portId":
            return "string"
    raise NetLangTypeError(f"Unknown field '{field}' for type '{type_name}'")
