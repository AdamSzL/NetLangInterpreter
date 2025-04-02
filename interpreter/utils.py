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