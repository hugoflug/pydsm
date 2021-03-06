import queue
import networkx as nx

def subgraph(g, root, max_depth):
    sg = nx.Graph()
    q = queue.Queue()
    
    visited = set()
    
    q.put((root, 0))
    visited.add(root)
    
    while not q.empty():
        (node, depth) = q.get()
        
        if depth < max_depth:
            for nbor, labels in g[node].items():
                if nbor not in visited:
                    sg.add_node(nbor)

                    sg.add_edge(node, nbor, attr_dict=labels)

                    q.put((nbor, depth + 1))
                    visited.add(nbor)
                
    return sg