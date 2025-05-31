from typing import Any, cast, Optional

from shared.errors import NetLangTypeError
from shared.model.CIDR import CIDR
from shared.model import CopperEthernetPort, Port
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
    "Port": Port,
    "RoutingEntry": RoutingEntry,
    "Packet": Packet,
    "Host": Host,
    "Switch": Switch,
    "Router": Router,
    "void": type(None)
}

type_field_map = {
    "CopperEthernetPort": {
        "required": {
            "portId": "string"
        },
        "optional": {
            "ip": "CIDR",
            "mac": "MAC",
            "bandwidth": "int",
            "mtu": "int",
            "gateway": "IP"
        },
        "readonly": {}
    },
    "OpticalEthernetPort": {
        "required": {
            "portId": "string"
        },
        "optional": {
            "ip": "CIDR",
            "mac": "MAC",
            "bandwidth": "int",
            "wavelength": "int",
            "mtu": "int",
            "connector": "string",
            "gateway": "IP"
},
        "readonly": {}
    },
    "WirelessPort": {
        "required": {
            "portId": "string"
        },
        "optional": {
            "ip": "CIDR",
            "mac": "MAC",
            "bandwidth": "int",
            "mtu": "int",
            "frequency": "float",
            "gateway": "IP"
        },
        "readonly": {}
    },
    "Port": {
        "required": {
            "portId": "string"
        },
        "optional": {
            "ip": "CIDR",
            "mac": "MAC",
            "bandwidth": "int",
            "mtu": "int",
            "gateway": "IP"
        },
        "readonly": {}
    },
    "CIDR": {
        "required": {
            "ip": "IP",
            "mask": "int"
        },
        "optional": {},
        "readonly": {
            "network": "CIDR",
            "broadcast": "CIDR"
        }
    },
    "Host": {
        "required": {
            "name": "string",
            "ports": "[Port]"
        },
        "optional": {},
        "readonly": {}
    },
    "Switch": {
        "required": {
            "name": "string",
            "ports": "[Port]"
        },
        "optional": {},
        "readonly": {}
    },
    "Router": {
        "required": {
            "name": "string",
            "ports": "[Port]",
            "routingTable": "[RoutingEntry]"
        },
        "optional": {},
        "readonly": {}
    },
    "RoutingEntry": {
        "required": {
            "destination": "CIDR",
            "via": "string"
        },
        "optional": {},
        "readonly": {}
    },
    "Packet": {
        "required": {
            "payload": "string",
            "protocol": "string",
            "size": "int"
        },
        "optional": {},
        "readonly": {}
    }
}

type_hierarchy = {
    "CopperEthernetPort": "Port",
    "OpticalEthernetPort": "Port",
    "WirelessPort": "Port",
    "int": "float",
}

abstract_types = {"Port"}

def is_known_type(type_str: str) -> bool:
    if type_str.startswith("[") and type_str.endswith("]"):
        inner = type_str[1:-1].strip()
        return is_known_type(inner)
    return type_str in type_map.keys()

def are_types_compatible(expected: str, actual: str) -> bool:
    if expected.startswith("[") and expected.endswith("]"):
        if not actual.startswith("[") or not actual.endswith("]"):
            return False
        expected_elem_type = expected[1:-1]
        actual_elem_type = actual[1:-1]
        return are_types_compatible(expected_elem_type, actual_elem_type)

    current = actual
    while current in type_hierarchy:
        if type_hierarchy[current] == expected:
            return True
        current = type_hierarchy[current]

    return expected == actual

def is_subtype(sub: str, super: str) -> bool:
    current = sub
    while current in type_hierarchy:
        if type_hierarchy[current] == super:
            return True
        current = type_hierarchy[current]
    return sub == super

def get_all_supertypes(t: str) -> list[str]:
    supertypes = [t]
    while t in type_hierarchy:
        t = type_hierarchy[t]
        supertypes.append(t)
    return supertypes

def find_common_supertype(types: list[str]) -> Optional[str]:
    if not types:
        return None
    if len(types) == 1:
        return types[0]

    supertypes_sets = [set(get_all_supertypes(t)) for t in types]
    common = set.intersection(*supertypes_sets)

    if not common:
        return None

    for candidate in get_all_supertypes(types[0]):
        if candidate in common:
            return candidate

    return None


def get_field_type(type_name: str, field_name: str, ctx) -> str:
    current = type_name

    while True:
        field_sets = type_field_map.get(current)
        if field_sets:
            for section in ["required", "optional", "readonly"]:
                if field_name in field_sets.get(section, {}):
                    return field_sets[section][field_name]
        if current in type_hierarchy:
            current = type_hierarchy[current]
        else:
            break

    raise NetLangTypeError(
        f"Unknown field '{field_name}' for type '{type_name}'",
        ctx
    )