from networkx import *
from companies import *
import random
from matplotlib.pyplot import show


def hassolitarynodes(g):
    lonelies = [x for x in g if not g[x]]

    return bool(lonelies)


network = MultiGraph()

randComp = [onerollcompany(randomname(), random.randint(5, 15)) for x in range(30)]

print("Companies:", len(randComp))

network.add_nodes_from(randComp)

while hassolitarynodes(network):
    network.add_edge(random.choice(network.nodes()), random.choice(network.nodes()))

draw(network, labels={node: node.name for node in network})
show()


