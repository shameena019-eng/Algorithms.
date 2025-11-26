import os
import sys
import random
import time
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(base_dir)

clrs_dir = os.path.join(parent_dir, 'clrsPython')

required_folders = [
    "Chapter 21",
    "Utility functions",
    "Chapter 6",
    "Chapter 10",
    "Chapter 2",
    "Chapter 19"
]

for folder in required_folders:
    sys.path.append(os.path.join(clrs_dir, folder))

from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal, prim, get_total_weight

labels = ['A', 'B', 'C', 'D', 'E']
index = {v: i for i, v in enumerate(labels)}

edges = [
    ('A', 'B', 4),
    ('A', 'C', 3),
    ('B', 'C', 1),
    ('B', 'D', 2),
    ('C', 'E', 5),
    ('D', 'E', 3),
]

G = AdjacencyListGraph(len(labels), False, True)

for u, v, w in edges:
    G.insert_edge(index[u], index[v], w)

def undirected_edge_list(graph):
    out = []
    for u in range(graph.get_card_V()):
        for e in graph.get_adj_list(u):
            v = e.get_v()
            if u < v:
                out.append((labels[u], labels[v], e.get_weight()))
    out.sort(key=lambda t: (t[2], t[0], t[1]))
    return out


mst_k = kruskal(G)
total_k = get_total_weight(mst_k)

mst_p = prim(G, index['A'])
total_p = get_total_weight(mst_p)

mst_edges = undirected_edge_list(mst_k)

mst_set = {(min(a, b), max(a, b)) for (a, b, _) in mst_edges}
closable = []

for (u, v, w) in edges:
    a, b = min(u, v), max(u, v)
    if (a, b) not in mst_set:
        closable.append((a, b, w))

closable.sort(key=lambda t: (t[2], t[0], t[1]))

print("=== TASK 4A ===")
print("Vertices:", labels)
print("All edges:", sorted([(min(u, v), max(u, v), w) for (u, v, w) in edges], key=lambda t: (t[2], t[0], t[1])))
print("MST (Kruskal):", mst_edges)
print("MST total weight (Kruskal):", total_k)
print("MST total weight (Prim):", total_p)
print("Closable edges:", closable)


def generate_random_graph(n, edge_prob=0.15, max_w=20):
    G = AdjacencyListGraph(n, False, True)
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < edge_prob:
                w = random.randint(1, max_w)
                G.insert_edge(u, v, w)
    return G


def measure_mst_runtime():
    sizes = list(range(100, 1001, 100))
    runtimes = []

    for n in sizes:
        times = []
        for _ in range(3):
            G = generate_random_graph(n)
            start = time.time()
            mst = kruskal(G)
            end = time.time()
            times.append(end - start)

        avg = sum(times) / len(times)
        print(f"n={n}, avg MST time={avg:.6f}s")
        runtimes.append(avg)

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, runtimes, marker='o')
    plt.title("Task 4b – MST Runtime vs Number of Stations")
    plt.xlabel("Number of Stations (n)")
    plt.ylabel("Avg Running Time (seconds)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return sizes, runtimes



def example_placeholder_loader():
    return ["A", "B", "C"], [("A", "B", 5), ("B", "C", 2)]


def build_real_graph(stations, edges):
    index = {name: i for i, name in enumerate(stations)}
    G = AdjacencyListGraph(len(stations), False, True)

    best = {}
    for u, v, w in edges:
        a, b = min(u, v), max(u, v)
        if (a, b) not in best or w < best[(a, b)]:
            best[(a, b)] = w

    for (u, v), w in best.items():
        G.insert_edge(index[u], index[v], w)

    return G, index


def extract_edge_list(graph, stations):
    out = []
    for u in range(graph.get_card_V()):
        for e in graph.get_adj_list(u):
            v = e.get_v()
            if u < v:
                out.append((stations[u], stations[v], e.get_weight()))
    return out


def task4b_real_network():
    print("\n--- Task 4b: Real London Dataset ---\n")

    stations, edges = example_placeholder_loader()
    G, index_map = build_real_graph(stations, edges)

    mst = kruskal(G)
    mst_total = get_total_weight(mst)

    mst_edges = extract_edge_list(mst, stations)
    mst_set = {(min(a, b), max(a, b)) for (a, b, _) in mst_edges}

    redundant = []
    for (u, v, w) in edges:
        a, b = min(u, v), max(u, v)
        if (a, b) not in mst_set:
            redundant.append((a, b, w))

    redundant.sort(key=lambda t: (t[2], t[0], t[1]))

    print("Total MST Backbone Weight:", mst_total)
    print("\nFirst redundant edges:")
    for r in redundant[:10]:
        print("  ", r)

    return mst, mst_edges, redundant

if __name__ == "__main__":
    measure_mst_runtime()
    task4b_real_network()
