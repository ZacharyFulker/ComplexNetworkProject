import networkx as nx
from networkx.algorithms import bipartite

network = nx.read_graphml('ScrapLab-Graph-FULL.graphml')
node_types = nx.get_node_attributes(network, "type")
edge_types = nx.get_edge_attributes(network, "Type")

# Create separate lists for each type of node
designs = []
users = []
for key, value in node_types.items():  # True means design
    if value:
        designs.append(key)
    else:
        users.append(key)

# Create separate dictionaries for each edge type
# Each directed edge goes from user to design
comments = {}
ratings = {}
designs = {}
for key, value in edge_types.items():
    if value == 'comment':
        comments[key] = value
    elif value == 'rate':
        ratings[key] = value
    else:
        designs[key] = value

# Bipartite pre-calculations using all edge types
# degDesigns, degUsers = bipartite.degrees(network, users)
# total_deg_designs = 0
# for key, value in degDesigns.items():
#     total_deg_designs += value
# total_deg_users = 0
# for key, value in degUsers.items():
#     total_deg_users += value

# Useful Bipartite statistics using all edge types
b_density = bipartite.density(network, users)
numDesigns = len(designs)
numUsers = len(users)
avg_deg_designs = len(edge_types)/numDesigns
avg_deg_users = len(edge_types)/numUsers

# Useful Bipartite statistics comments only



