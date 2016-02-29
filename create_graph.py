import networkx as nx
import pydsm
import queue
from collections import defaultdict


# TODO: if queue is empty, load next unvisited word from model into queue and restart

def create_graph(model, root, save_file=None, save_every_nth_iteration=1000):
    g = nx.Graph()
    q = queue.Queue()

    visited = set()

    potential_edges = defaultdict(list)

    q.put(root)
    visited.add(root)

    n = 0

    while not q.empty():
        word = q.get()

        rng = model.relative_neighborhood(word, 20, format='networkx')
        
        if save_file:
            if n % save_every_nth_iteration == 0:
                nx.write_gpickle(g, save_file)
                print("Saving graph to file: '" + save_file + "' (iteration: " + str(n) + ", nodes: " + str(g.number_of_nodes()) + ")")

        for neighbor, labels in rng[word].items():
            if word in potential_edges[neighbor]:
                g.add_edge(word, neighbor, labels)
            else:
                potential_edges[word].append(neighbor)
            if neighbor not in visited:
                q.put(neighbor)
                visited.add(neighbor)

        n += 1