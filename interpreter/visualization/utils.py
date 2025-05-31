from dataclasses import dataclass
from typing import Optional

from interpreter.visualization.constants import NODE_RADIUS, SCREEN_SIZE, INFO_PANEL_WIDTH, ICON_SIZE, icons, \
    drawing_area, PADDING, LOG_PANEL_HEIGHT, font, suppress_stdout
from shared.model import Host, Router, Switch, OpticalEthernetPort, WirelessPort, Port, Packet, Connection

with suppress_stdout():
    import pygame

@dataclass
class LogEntry:
    text: str
    color: tuple[int, int, int] = (0, 0, 0)

@dataclass
class PacketHop:
    from_port: Port
    to_port: Port

def draw_graph(screen, connections, pos, uid_to_device, selected_device, log_lines):
    draw_edges(screen, connections, pos)
    draw_devices(screen, pos, uid_to_device)
    draw_log_panel(screen, log_lines)

    if selected_device:
        draw_info_panel(screen, selected_device)

def draw_edges(screen, connections, pos):
    for conn in connections:
        x1, y1 = pos[conn.device1.uid]
        x2, y2 = pos[conn.device2.uid]
        pygame.draw.line(screen, (100, 100, 255), (x1, y1), (x2, y2), 2)

def draw_devices(screen, pos, uid_to_device):
    for uid, (cx, cy) in pos.items():
        draw_device_icon(uid, cx, cy, screen, uid_to_device)

        label = font.render(uid_to_device[uid].name, True, (0, 0, 0))
        screen.blit(label, (cx - label.get_width() // 2, cy + NODE_RADIUS + 5))

def draw_info_panel(screen, device):
    pygame.draw.rect(screen, color=(245, 245, 245),
                     rect=(SCREEN_SIZE, 0, INFO_PANEL_WIDTH, SCREEN_SIZE))

    lines: list[LogEntry] = [
        LogEntry(f"UID: {device.uid}", (0, 0, 0)),
        LogEntry(f"Type: {type(device).__name__}", (80, 80, 80)),
        LogEntry(f"Name: {device.name}", (0, 0, 0)),
        LogEntry(f"Ports: {len(device.ports)}", (0, 0, 0))
    ]

    for i, entry in enumerate(lines):
        label = font.render(entry.text, True, entry.color)
        screen.blit(label, (SCREEN_SIZE + 20, 20 + i * 30))

    y = 20 + len(lines) * 30 + 10
    if hasattr(device, "ports"):
        for port in device.ports:
            y = render_port_info(port, screen, SCREEN_SIZE + 20, y)

def draw_log_panel(screen, log_lines: list[LogEntry]):
    pygame.draw.rect(screen, color=(240, 240, 240),
                     rect=(0, SCREEN_SIZE, SCREEN_SIZE + INFO_PANEL_WIDTH, LOG_PANEL_HEIGHT))

    max_lines = SCREEN_SIZE // 24
    visible_lines = log_lines[-max_lines:]

    for i, entry in enumerate(visible_lines):
        label = font.render(entry.text, True, entry.color)
        screen.blit(label, (10, 10 + SCREEN_SIZE + i * 24))

def draw_device_icon(uid, cx, cy, screen, uid_to_device):
    device = uid_to_device[uid]
    device_type = get_device_type(device)
    icon = pygame.transform.scale(icons[device_type], (ICON_SIZE, ICON_SIZE))
    screen.blit(icon, (cx - NODE_RADIUS, cy - NODE_RADIUS))

def get_device_type(device) -> str:
    if isinstance(device, Host):
        return "host"
    elif isinstance(device, Router):
        return "router"
    elif isinstance(device, Switch):
        return "switch"
    return "unknown"

def build_uid_map(connections):
    uid_map = {}
    for conn in connections:
        uid_map[conn.device1.uid] = conn.device1
        uid_map[conn.device2.uid] = conn.device2
    return uid_map

def to_screen(x: float, y: float) -> tuple[int, int]:
    return (
        int((x + 1) / 2 * drawing_area + PADDING),
        int((y + 1) / 2 * drawing_area + PADDING)
    )

def render_port_info(port: Port, screen, x, y) -> int:
    lines: list[LogEntry] = [
        LogEntry(f"Port ID: {port.portId}"),
        LogEntry(f"IP: {port.ip}"),
        LogEntry(f"MAC: {port.mac}"),
        LogEntry(f"MTU: {port.mtu}"),
        LogEntry(f"Bandwidth: {port.bandwidth} Mbps")
    ]

    if isinstance(port, WirelessPort):
        lines.append(LogEntry(f"Frequency: {port.frequency} GHz", (0, 70, 140)))
    elif isinstance(port, OpticalEthernetPort):
        lines.append(LogEntry(f"Wavelength: {port.wavelength} nm", (140, 70, 0)))
        lines.append(LogEntry(f"Connector: {port.connector}", (140, 70, 0)))

    for entry in lines:
        label = font.render(entry.text, True, entry.color)
        screen.blit(label, (x, y))
        y += 25

    return y

def show_constructed_frame(packet: Packet, log_lines: list[LogEntry], dst_mac: str) -> None:
    log_lines.append(LogEntry("------------------------------------------------"))
    log_lines.append(LogEntry("Constructed Ethernet Frame:", (0, 0, 150)))
    log_lines.append(LogEntry(f"| -> Destination MAC: {dst_mac}", (0, 0, 0)))
    log_lines.append(LogEntry(f"| -> Source MAC: {packet.source.mac}", (0, 0, 0)))
    log_lines.append(LogEntry(f"| -> Payload: \"{packet.payload}\"", (0, 0, 0)))
    log_lines.append(LogEntry("------------------------------------------------"))

def resolve_mac_for_packet(packet, arp_table, log_lines) -> Optional[str]:
    if packet.destination.ip in packet.source.ip.current_network():
        log_lines.append(LogEntry(
            f"Destination IP {packet.destination.ip} is in the same subnet as source {packet.source.ip}", (0, 128, 0)
        ))

        dst_ip = packet.destination.ip
    else:
        log_lines.append(LogEntry(
            f"Destination IP {packet.destination.ip} is outside the source subnet {packet.source.ip.current_network()}",
            (150, 100, 0)
        ))

        gateway = packet.source.gateway
        if gateway is None:
            log_lines.append(LogEntry("Error: No gateway configured on the source port.", (200, 0, 0)))
            return None

        dst_ip = gateway.ip
        log_lines.append(LogEntry(f"Using gateway IP: {dst_ip}", (100, 100, 100)))

    dst_mac = arp_table.get(str(dst_ip))
    if dst_mac is None:
        log_lines.append(LogEntry(f"ARP lookup failed: MAC address for {dst_ip} not found.", (200, 0, 0)))
        return None

    log_lines.append(LogEntry(f"ARP lookup successful: MAC = {dst_mac}", (0, 128, 0)))
    return dst_mac