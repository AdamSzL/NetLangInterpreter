import matplotlib.pyplot as plt
from PIL import Image
import networkx as nx

from shared.model import Host, Router, Switch
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interpreter import Interpreter

def draw_graph(self: "Interpreter"):
    icons = {
        "router": "images/router.png",
        "switch": "images/switch.png",
        "host": "images/host.png",
    }

    images = {k: Image.open(fname) for k, fname in icons.items()}

    G = nx.Graph()
    for name, value in self.variables.items():
        if isinstance(value, Host):
            G.add_node(name, image=images["host"])
        elif isinstance(value, Router):
            G.add_node(name, image=images["router"])
        elif isinstance(value, Switch):
            G.add_node(name, image=images["switch"])

    if G.number_of_nodes() == 0:
        return

    for conn in self.connections:
        dev1 = conn.device1_id
        dev2 = conn.device2_id
        G.add_edge(dev1, dev2, port1=conn.port1_id, port2=conn.port2_id)

    pos = nx.spring_layout(G, seed=1734289230)
    fig, ax = plt.subplots(figsize=(14, 11))
    fig.canvas.manager.set_window_title("NetLang Network Topology")
    ax.axis("off")

    nx.draw_networkx_edges(
        G,
        pos=pos,
        ax=ax,
        arrows=True,
        arrowstyle="-",
        min_source_margin=25,
        min_target_margin=25,
    )

    # Rysujemy etykiety na środku krawędzi
    # nx.draw_networkx_edge_labels(
    #     G,
    #     pos=pos,
    #     edge_labels=edge_labels,
    #     font_size=12,
    #     ax=ax,
    #     label_pos=0.5,  # środek krawędzi
    #     verticalalignment='center'
    # )

    tr_figure = ax.transData.transform
    tr_axes = fig.transFigure.inverted().transform

    multiplier = 0.25 / G.number_of_nodes()
    # multiplier = 0.05
    icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * multiplier
    icon_center = icon_size / 2.0

    for n in G.nodes:
        xf, yf = tr_figure(pos[n])
        xa, ya = tr_axes((xf, yf))
        a = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
        a.imshow(G.nodes[n]["image"])
        a.axis("off")
        label = self.variables[n].name
        a.text(
            0.5, -0.01,
            label,
            ha='center',
            va='top',
            fontsize=14,
            fontweight='bold',
            transform=a.transAxes
        )

    plt.show()