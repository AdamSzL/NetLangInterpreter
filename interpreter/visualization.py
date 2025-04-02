import matplotlib.pyplot as plt
from PIL import Image
import networkx as nx
from model import Host, Router, Switch


def draw_graph(self):
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

    for conn in self.connections:
        dev1 = conn.device1
        dev2 = conn.device2
        G.add_edge(dev1, dev2)

    pos = nx.spring_layout(G, seed=1734289230)
    fig, ax = plt.subplots()
    ax.axis("off")

    nx.draw_networkx_edges(
        G,
        pos=pos,
        ax=ax,
        arrows=True,
        arrowstyle="-",
        min_source_margin=15,
        min_target_margin=15,
    )

    tr_figure = ax.transData.transform
    tr_axes = fig.transFigure.inverted().transform

    icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.025
    icon_center = icon_size / 2.0

    for n in G.nodes:
        xf, yf = tr_figure(pos[n])
        xa, ya = tr_axes((xf, yf))
        a = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
        a.imshow(G.nodes[n]["image"])
        a.axis("off")
        label = self.variables[n].name
        a.text(
            0.5, -0.1,
            label,
            ha='center',
            va='top',
            fontsize=9,
            fontweight='bold',
            transform=a.transAxes
        )

    plt.show()