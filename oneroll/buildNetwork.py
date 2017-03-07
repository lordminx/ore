from networkx import *
from .companies import *
import random


def hassolitarynodes(g):
    lonelies = [x for x in g if not g[x]]

    return bool(lonelies)


if __name__ == "__main__":

    network = Graph()
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

    # build directed relationship graph from network
    relationships = DiGraph()


    for x, y in network.edges():
        # compare _actions
        print("'{}' vs '{}'".format(x.name, y.name))
        for k, v in _actions.items():

            if v[1]:
                print(x.stats)
                print(y.stats)
                print(k, "{} vs {}".format(v[0], v[1]))
                pool1 = sum([getattr(x, stat) for stat in v[0]])
                pool2 = sum([getattr(y, stat) for stat in v[1]])

                print("{} vs {}".format(pool1, pool2))


    #draw(network, labels={node: node.name for node in network})
    #show()


