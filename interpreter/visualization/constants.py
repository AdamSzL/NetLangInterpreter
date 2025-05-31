import contextlib
import os
import sys

@contextlib.contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

with suppress_stdout():
    import pygame

icons = {
    "router": pygame.image.load("images/router.png"),
    "switch": pygame.image.load("images/switch.png"),
    "host": pygame.image.load("images/host.png"),
    "packet": pygame.image.load("images/packet.png"),
}

pygame.init()

font = pygame.font.Font("fonts/OpenSans-Regular.ttf", 20)

SCREEN_SIZE = 800
PADDING = 100
drawing_area = SCREEN_SIZE - 2 * PADDING
INFO_PANEL_WIDTH = 400
LOG_PANEL_WIDTH = 300
ICON_SIZE = 100
NODE_RADIUS = ICON_SIZE // 2