import networkx as nx
import pydsm
import queue


# TODO: if queue is empty, load next unvisited word from model into queue and restart

def create_graph(model, root, gpickle=None):
    g = nx.Graph()
    q = queue.Queue()

    visited = set()

    q.put(root)
    visited.add(root)

    n = 0

    while not q.empty():
        word = q.get()

        rng = model.relative_neighborhood(word, 20, format='networkx')
        
        if gpickle:
            if n % 1000 == 0:
                nx.write_gpickle(g, gpickle)

        for neighbor, labels in rng[word].items():
            g.add_edge(word, neighbor, labels)
            if neighbor not in visited:
                q.put(neighbor)
                visited.add(neighbor)

        n += 1