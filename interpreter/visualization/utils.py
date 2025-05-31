from interpreter.visualization.constants import NODE_RADIUS, SCREEN_SIZE, INFO_PANEL_WIDTH, ICON_SIZE, icons, \
    drawing_area, PADDING, LOG_PANEL_WIDTH, font, suppress_stdout
from shared.model import Host, Router, Switch, OpticalEthernetPort, WirelessPort, Port

with suppress_stdout():
    import pygame

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
    pygame.draw.rect(screen, (245, 245, 245), (SCREEN_SIZE + LOG_PANEL_WIDTH, 0, INFO_PANEL_WIDTH, SCREEN_SIZE))
    lines = [
        f"UID: {device.uid}",
        f"Type: {type(device).__name__}",
    ]
    lines.append(f"Name: {device.name}")
    lines.append(f"Ports: {len(device.ports)}")

    for i, line in enumerate(lines):
        label = font.render(line, True, (0, 0, 0))
        screen.blit(label, (SCREEN_SIZE + LOG_PANEL_WIDTH + 20, 20 + i * 30))

    y = 20 + len(lines) * 30 + 10
    if hasattr(device, "ports"):
        for port in device.ports:
            y = render_port_info(port, screen, SCREEN_SIZE + LOG_PANEL_WIDTH + 20, y)

def draw_log_panel(screen, log_lines: list[str]):
    pygame.draw.rect(screen, (240, 240, 240), (0, 0, LOG_PANEL_WIDTH, SCREEN_SIZE))

    max_lines = SCREEN_SIZE // 24
    visible_lines = log_lines[-max_lines:]

    for i, line in enumerate(visible_lines):
        label = font.render(line, True, (50, 50, 50))
        screen.blit(label, (10, 10 + i * 24))

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
        int((x + 1) / 2 * drawing_area + PADDING + LOG_PANEL_WIDTH),
        int((y + 1) / 2 * drawing_area + PADDING)
    )


def render_port_info(port: Port, screen, x, y) -> int:
    lines = [
        f"Port ID: {port.portId}",
        f"IP: {port.ip}",
        f"MAC: {port.mac}",
        f"MTU: {port.mtu}",
        f"Bandwidth: {port.bandwidth} Mbps",
    ]

    if isinstance(port, WirelessPort):
        lines.append(f"Frequency: {port.frequency} GHz")
    elif isinstance(port, OpticalEthernetPort):
        lines.append(f"Wavelength: {port.wavelength} nm")
        lines.append(f"Connector: {port.connector}")

    for line in lines:
        label = font.render(line, True, (0, 0, 0))
        screen.blit(label, (x, y))
        y += 25

    return y
