import contextlib
import os
import sys

from pygments.styles.paraiso_light import BACKGROUND


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
font_small = pygame.font.Font("fonts/OpenSans-Regular.ttf", 16)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
PADDING = 100
DRAWING_WIDTH = SCREEN_WIDTH - 2 * PADDING
DRAWING_HEIGHT = SCREEN_HEIGHT - 2 * PADDING
INFO_PANEL_WIDTH = 250
LOG_PANEL_HEIGHT = 300
ICON_SIZE = 100
NODE_RADIUS = ICON_SIZE // 2

COLOR_DARK_GREY = (30, 30, 30)
COLOR_WHITE = (255, 255, 255)
COLOR_SLATE_BLUE = (80, 90, 160)
COLOR_BLACK = (0, 0, 0)
COLOR_LIGHT_GREY = (210, 210, 210)

BACKGROUND_COLOR = COLOR_WHITE
DEVICE_LABEL_COLOR = COLOR_BLACK
EDGE_COLOR = COLOR_DARK_GREY
IP_LABEL_COLOR = COLOR_SLATE_BLUE
INFO_PANEL_COLOR = COLOR_LIGHT_GREY
LOG_PANEL_COLOR = COLOR_LIGHT_GREY