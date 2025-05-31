import matplotlib.pyplot as plt
from PIL import Image
import networkx as nx
from shared.model import Host, Switch
from shared.model.Packet import Packet
from shared.model.Connection import Connection
from shared.model.Port import Port
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, INFO_PANEL_WIDTH, NODE_RADIUS, icons, ICON_SIZE, LOG_PANEL_HEIGHT, suppress_stdout, \
    font, BACKGROUND_COLOR
from .utils import get_device_type, build_uid_map, to_screen, draw_graph, LogEntry, show_constructed_frame, \
    PacketHop, resolve_mac_for_packet, draw_ip_labels

with suppress_stdout():
    import pygame

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from interpreter.interpreter import Interpreter

def draw_graph_and_animate_packet(self: "Interpreter", packet: Packet):
    def init_pygame_window():
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH + INFO_PANEL_WIDTH, SCREEN_HEIGHT + LOG_PANEL_HEIGHT))
        pygame.display.set_caption("NetLang Graph")
        return screen, pygame.time.Clock()

    def process_events():
        nonlocal running, selected_device, paused
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for uid, (cx, cy) in pos.items():
                    if (mx - cx) ** 2 + (my - cy) ** 2 <= NODE_RADIUS ** 2:
                        selected_device = uid_to_device[uid]
                        break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

    def render_paused_state():
        if animating and current_hop_index < len(packet_hops):
            hop = packet_hops[current_hop_index]
            t = animation_step / animation_steps
            render_packet_movement(screen, hop, pos, t)
        label = font.render("PAUSED", True, (200, 0, 0))
        screen.blit(label, (10, 10))

    def handle_frame_waiting():
        nonlocal frame_display_counter, frame_waiting, animating, animation_step, current_hop_index, pending_log_hop
        frame_display_counter += 1
        if frame_display_counter >= frame_display_ticks:
            log_lines.clear()
            frame_waiting = False
            animating = True
            animation_step = 0
            current_hop_index = 0
            pending_log_hop = 0

    def handle_packet_animation():
        nonlocal animation_step, current_hop_index, animating, pending_log_hop
        hop = packet_hops[current_hop_index]
        t = animation_step / animation_steps
        render_packet_movement(screen, hop, pos, t)
        animation_step += 1
        if animation_step > animation_steps:
            animation_step = 0
            if pending_log_hop is not None:
                handle_packet_arrival(packet_hops[pending_log_hop], packet, dst_mac, log_lines)
                pending_log_hop = None
            current_hop_index += 1
            if current_hop_index >= len(packet_hops):
                animating = False
            else:
                pending_log_hop = current_hop_index

    G = nx.Graph()
    for conn in self.connections:
        G.add_node(conn.device1.uid)
        G.add_node(conn.device2.uid)
        G.add_edge(conn.device1.uid, conn.device2.uid)
    raw_pos = nx.spring_layout(G, seed=42, k=0.8)
    pos = {uid: to_screen(x, y) for uid, (x, y) in raw_pos.items()}
    uid_to_device = build_uid_map(self.connections)
    selected_device = None
    log_lines = []
    screen, clock = init_pygame_window()

    packet_hops: list[PacketHop] = []
    current_hop_index = 0
    animation_step = 0
    animation_steps = 60
    animating = False
    frame_display_ticks = 300
    frame_display_counter = 0
    frame_waiting = False
    paused = False
    pending_log_hop = None

    dst_mac = resolve_mac_for_packet(packet, self.arp_table, log_lines)
    if dst_mac is not None:
        show_constructed_frame(packet, log_lines, dst_mac)
        frame_waiting = True
        packet_hops = forward_packet_from_port(packet.source, dst_mac)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_graph(screen, self.connections, pos, uid_to_device, selected_device, log_lines)
        draw_ip_labels(screen, self.connections, pos)
        process_events()

        if paused:
            render_paused_state()
        elif frame_waiting:
            handle_frame_waiting()
        elif animating and current_hop_index < len(packet_hops):
            handle_packet_animation()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def render_packet_movement(screen, hop: PacketHop, pos, t: float) -> None:
    x1, y1 = pos[hop.from_port.owner.uid]
    x2, y2 = pos[hop.to_port.owner.uid]
    px = int(x1 * (1 - t) + x2 * t)
    py = int(y1 * (1 - t) + y2 * t)

    icon = pygame.transform.scale(icons["packet"], (ICON_SIZE // 2, ICON_SIZE // 2))
    screen.blit(icon, (px - NODE_RADIUS // 2, py - NODE_RADIUS // 2))

def handle_packet_arrival(hop: PacketHop, packet: Packet, dst_mac: str, log_lines: list[LogEntry]) -> None:
    dst_device = hop.to_port.owner
    log_lines.append(LogEntry(
        f"→ Packet arrived at port {hop.to_port.portId} on device {dst_device.name}",
        (0, 0, 150)
    ))

    if isinstance(dst_device, Switch):
        log_lines.append(LogEntry(
            f"{dst_device.name} is forwarding packet...",
            (100, 100, 100)
        ))

    elif isinstance(dst_device, Host):
        if hop.to_port.mac.mac == dst_mac:
            log_lines.append(LogEntry(
                f"{dst_device.name} accepted packet",
                (0, 128, 0)
            ))
        else:
            log_lines.append(LogEntry(
                f"{dst_device.name} ignored packet (wrong MAC)",
                (100, 100, 100)
            ))

def forward_packet_from_port(
    start_port: Port,
    dst_mac: str,
) -> list[PacketHop]:
    visited_ports = set()
    port_queue = []
    hops: list[PacketHop] = []

    if start_port.connectedTo:
        port_queue.append((start_port.connectedTo, start_port))

    while port_queue:
        current_port, from_port = port_queue.pop(0)
        if current_port in visited_ports:
            continue
        visited_ports.add(current_port)

        device = current_port.owner

        if from_port:
            hops.append(PacketHop(from_port, current_port))

        if current_port.mac == dst_mac:
            return hops

        if isinstance(device, Host):
            continue

        elif isinstance(device, Switch):
            for port in device.ports:
                if port == current_port:
                    continue
                next_port = port.connectedTo
                if next_port and next_port not in visited_ports:
                    port_queue.append((next_port, port))
    return hops