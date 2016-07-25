from networkx import *
from companies import *
import random
from matplotlib.pyplot import show


def hassolitarynodes(g):
    lonelies = [x for x in g if not g[x]]

    return bool(lonelies)


network = MultiGraph()
corpus = Corpus()


# generate 30 random companies
randComp = [onerollcompany(corpus.randomname(), random.randint(5, 15)) for x in range(30)]


# add Companies as nodes to graph
for comp in randComp:
    if len(network) == 0:
        network.add_node(comp)
    else:
        network.add_edge(choice(network.nodes()), comp)


# throw some random connections into the mix
for x in range(5):
    network.add_edge(choice(network.nodes()), choice(network.nodes()))


# Betweenness centrality for trade centers?
for x, y in sorted(list(betweenness_centrality(network).items()), key=lambda x: x[1], reverse=True)[:5]:
    print(x)
    print(y)


#draw(network, labels={node: node.name for node in network})
#show()


