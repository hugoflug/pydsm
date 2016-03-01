import networkx as nx
import graph_methods
import matplotlib.pyplot as plt
import sys

def draw_graph(graph_file='data/labelled_graph.pickle', root='sweden', depth=4):
    lg = nx.read_gpickle(graph_file)
    g = graph_methods.subgraph(lg, root, depth)

    pos = nx.spring_layout(g)
    nx.draw(g, pos=pos, with_labels=True)
    nx.draw_networkx_edge_labels(g, pos=pos)

    plt.show()


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        depth = int(sys.argv[3])
    else:
        depth = 4

    if len(sys.argv) >= 3:
        root = sys.argv[2]
    else:
        root = 'sweden'

    if len(sys.argv) >= 2:
        graph_file = sys.argv[1]
    else:
        graph_file = 'data/labelled_graph.pickle'

    draw_graph(graph_file, root, depth)