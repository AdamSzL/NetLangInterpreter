import matplotlib.pyplot as plt
from PIL import Image
import networkx as nx
from .constants import SCREEN_SIZE, INFO_PANEL_WIDTH, NODE_RADIUS, icons, ICON_SIZE, LOG_PANEL_WIDTH, suppress_stdout
from .utils import get_device_type, build_uid_map, to_screen, draw_graph

with suppress_stdout():
    import pygame

from shared.model import Host, Router, Switch, Port, Packet
from typing import TYPE_CHECKING

from shared.model.Device import Device

if TYPE_CHECKING:
    from interpreter.interpreter import Interpreter

def draw_graph_and_animate_packet(self: "Interpreter", packet: Packet, start_device: Device, start_port: Port):
    print(start_port.owner)
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

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE + INFO_PANEL_WIDTH + LOG_PANEL_WIDTH, SCREEN_SIZE))
    pygame.display.set_caption("NetLang Graph")
    clock = pygame.time.Clock()

    if start_port.connectedTo:
        end_port = start_port.connectedTo
        end_device = end_port.owner
        start_pos = pos[start_device.uid]
        end_pos = pos[end_device.uid]
        animate_to(screen, start_pos, end_pos, self.connections, pos, uid_to_device, selected_device, clock, log_lines)

    running = True
    while running:
        screen.fill((255, 255, 255))
        draw_graph(screen, self.connections, pos, uid_to_device, selected_device, log_lines)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for uid, (cx, cy) in pos.items():
                    if (mx - cx) ** 2 + (my - cy) ** 2 <= NODE_RADIUS ** 2:
                        selected_device = uid_to_device[uid]
                        break

        clock.tick(60)

    pygame.quit()


def animate_to(screen, start_pos: tuple[int, int], end_pos: tuple[int, int],
                connections, pos, uid_to_device, selected_device, clock, log_lines):
    steps = 60
    for step in range(steps):
        t = step / steps
        px = int(start_pos[0] * (1 - t) + end_pos[0] * t)
        py = int(start_pos[1] * (1 - t) + end_pos[1] * t)

        screen.fill((255, 255, 255))
        draw_graph(screen, connections, pos, uid_to_device, selected_device, log_lines)

        icon = pygame.transform.scale(icons["packet"], (ICON_SIZE // 2, ICON_SIZE // 2))
        screen.blit(icon, (px - NODE_RADIUS // 2, py - NODE_RADIUS // 2))

        pygame.display.flip()
        clock.tick(60)