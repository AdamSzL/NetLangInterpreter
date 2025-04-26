from typing import Any, cast

from model.CIDR import CIDR
from model.CopperEthernetPort import CopperEthernetPort
from model.Host import Host
from model.IPAddress import IPAddress
from model.MACAddress import MACAddress
from model.OpticalEthernetPort import OpticalEthernetPort
from model.Packet import Packet
from model.Router import Router
from model.RoutingEntry import RoutingEntry
from model.Switch import Switch
from model.WirelessPort import WirelessPort

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
        return isinstance(value, expected_type)

    return False