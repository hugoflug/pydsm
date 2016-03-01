import networkx as nx
import pydsm
import queue
from collections import defaultdict
from itertools import chain


def nearest_indices(model, word, neighbor, n=1):
    nin = model.nearest_index_neighbors(model[word] + model[neighbor])
    return ", ".join(nin[i][1] for i in range(n))


def create_graph(model, root, save_file=None, save_every_nth_iteration=1000, label_function=None):
    g = nx.Graph()
    q = queue.Queue()

    visited = set()

    potential_edges = defaultdict(list)

    first_time = True

    q.put(root)
    visited.add(root)

    n = 0

    for word_vec in chain([None], model):
        if not first_time:
            root = word_vec.row2word[0]
        first_time = False

        if root not in visited:
            while not q.empty():
                word = q.get()

                rng = model.relative_neighborhood(word, 20, format='networkx')
                
                if save_file:
                    if n % save_every_nth_iteration == 0:
                        nx.write_gpickle(g, save_file)
                        print("Saving graph to file: '" + save_file + "' (iteration: " + str(n) + ", nodes: " + str(g.number_of_nodes()) + ")")

                for neighbor, labels in rng[word].items():
                    if word in potential_edges[neighbor]:
                        if label_function is not None:
                            new_label = label_function(word, neighbor)
                        g.add_edge(word, neighbor, l=new_label)
                    else:
                        potential_edges[word].append(neighbor)
                    if neighbor not in visited:
                        q.put(neighbor)
                        visited.add(neighbor)

                n += 1