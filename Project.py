import networkx as nx
from networkx.algorithms import bipartite
import random
import matplotlib.pyplot as plt
import numpy as np

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
comments_dict = {}
ratings_dict = {}
designs_dict = {}
for key, value in edge_types.items():
    if value == 'comment':
        comments_dict[key] = value
    elif value == 'rate':
        ratings_dict[key] = value
    else:
        designs_dict[key] = value # !!!!!Not the right length

######################################
# Creating Null Models for comparison#
######################################


def myMultiDiGraphGenerator(numUsers, numDesigns, numRatings, numComments):
    # create graph and nodes
    G = nx.MultiDiGraph()
    users = list(range(numUsers))
    designs = list(range(numDesigns))
    G.add_nodes_from(users, bipartite=0)
    G.add_nodes_from(designs, bipartite=1)
    # link every design to a users with uniform prob
    for design in designs:
        G.add_edge(random.choice(users), design, edge_type='design')
    # assign every comment to a random user about a random design
    for comment in range(numComments):
        # not checking if edge already exists because user can comment multiple times
        G.add_edge(random.choice(users), random.choice(designs), edge_type='comment')
    # assign every rating to a random user about a random design
    rates_remaining = numRatings
    while rates_remaining != 0:
        # need to check if edge already exist because you can only rate once
        randUser = random.choice(users)
        randDesign = random.choice(designs)
        if not G.has_edge(randUser, randDesign):
            G.add_edge(randUser, randDesign, edge_type='rating')
            rates_remaining -= 1
    return G


# Null Comparisons for bipartite
null_comps = [myMultiDiGraphGenerator(579, 646, numRatings=5662, numComments=1906) for i in range(100)]

# Null Comparisons for Users projection

###################################################
# Useful Bipartite statistics using all edge types#
###################################################
# Number of Nodes and Edges
numNodes = len(node_types)
numEdges = len(edge_types)

# Degree Measures
numDesigns = len(designs)
numUsers = len(users)
b_density = len(edge_types)/(numDesigns + 2*((numUsers-1)*numDesigns))   # Each design can/has only on edge + Each user (except creator) can comment/rate every design
avg_deg_designs = len(edge_types)/numDesigns
avg_deg_users = 0
# Plot DEGREE DISTRIBUTION OF DESIGNS vs Random Graph Designs
design_degree_dist = [degree for node, degree in list(network.in_degree(designs))]
rand_graph = myMultiDiGraphGenerator(579, 646, numRatings=5662, numComments=1906)
rand_design_degree_dist = [degree for node, degree in list(rand_graph.in_degree)]
kmin1 = min(design_degree_dist)
kmax1 = max(design_degree_dist)
kmin2 = min(rand_design_degree_dist)
kmax2 = max(rand_design_degree_dist)
bin_edges1 = np.logspace(np.log10(kmin1), np.log10(kmax1), num=10)
bin_edges2 = np.logspace(np.log10(kmin2), np.log10(kmax2), num=10)
density1, _ = np.histogram(design_degree_dist, bins=bin_edges1, density=True)
density2, _ = np.histogram(rand_design_degree_dist, bins=bin_edges2, density=True)
fig = plt.figure(figsize=(6,4))
log_be1 = np.log10(bin_edges1)
x1 = 10**((log_be1[1:] + log_be1[:-1])/2)
log_be2 = np.log10(bin_edges2)
x2 = 10**((log_be2[1:] + log_be2[:-1])/2)
plt.scatter(x1, density1, label='ScrapLabs')
plt.scatter(x2, density2, label='Random')
plt.xlabel(r"degree $k$", fontsize=16)
plt.ylabel(r"$P(k)$", fontsize=16)
plt.title('Distribution of Incoming Degree for Designs')
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
#plt.show()


# ADD PLOTS OF DEGREE DISTRIBUTION CONSIDERING EACH EDGE TYPE (3 PLOTS)

# Connectedness
numSCC = nx.number_strongly_connected_components(network)
numWCC = nx.number_weakly_connected_components(network)

# Clustering
# No C3 clustering by definition of bipartite, elaborate and explain C4 during talk
cluster1 = nx.square_clustering(network)  # No clustering because edges only go from users to designs
cluster2 = bipartite.clustering(network)  # No clustering because edges only go from users to designs

# Centrality Measures
# Do these factor in directedness!!!!!!!!!!!!!!!!!!!!!!!!!???????????????????????
closeness_centrality = bipartite.closeness_centrality(network, users)
total_closeness_centrality = 0
for key, value in closeness_centrality.items():
    total_closeness_centrality += value
avg_closeness_centrality = total_closeness_centrality/len(closeness_centrality)

degree_centrality = bipartite.degree_centrality(network, users)
total_degree_centrality = 0
for key, value in degree_centrality.items():
    total_degree_centrality += value
avg_degree_centrality = total_degree_centrality/len(degree_centrality)

betweenness_centrality = bipartite.betweenness_centrality(network, users)
total_betweenness_centrality = 0
for key, value in betweenness_centrality.items():
    total_betweenness_centrality += value
avg_betweenness_centrality = total_betweenness_centrality/len(betweenness_centrality)


###################################################
# Projection onto Users considering all edge types#
###################################################
network = nx.DiGraph(network)
user_network = bipartite.projected_graph(network, users, multigraph=True)
print(type(user_network))
exit()

# Degree Measures

# Connectedness
numSCC = nx.number_strongly_connected_components(user_network)
numWCC = nx.number_weakly_connected_components(user_network)

# Clustering

# Centrality

# Path Lengths

# Communities

# Nodes in Largest Component (Distribution of component size)


########################################
# Application of a few multigraph algos#
########################################











