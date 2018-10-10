import networkx as nx

network = nx.read_graphml('ScrapLab-Graph-FULL.graphml')
print(network.nodes())