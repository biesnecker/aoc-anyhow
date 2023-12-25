import itertools
import networkx as nx

G = nx.Graph()
with open("202325.txt", "r") as f:
    for line in f:
        a, bs = line.strip().split(": ")
        for b in bs.split():
            G.add_edge(a, b, capacity=1)

part_one = None
for a, b in itertools.combinations(G.nodes, 2):
    cut, partitions = nx.minimum_cut(G, a, b)
    if cut == 3:
        part_one = len(partitions[0]) * len(partitions[1])
        break
print(f"Part one: {part_one}")
