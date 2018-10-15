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

###################################################
# Useful Bipartite statistics using all edge types#
###################################################

# Degree Measures
numDesigns = len(designs)
numUsers = len(users)
b_density = len(edge_types)/(numDesigns + 2*((numUsers-1)*numDesigns))   # Each design can/has only on edge + Each user (except creator) can comment/rate every design
avg_deg_designs = len(edge_types)/numDesigns
avg_deg_users = 0
# ADD PLOT OF DEGREE DISTRIBUTION OF DESIGNS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ADD PLOTS OF DEGREE DISTRIBUTION CONSIDERING EACH EDGE TYPE (3 PLOTS)

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

# Degree Measures

# Clustering

# Centrality

# Path Lengths

# Communities

# Nodes in Largest Component (Distribution of component size)

######################################
# Creating Null Models for comparison#
######################################

def myMultiDiGraphGenerator(numUsers, numDesigns, numRatings, numComments):
    pass

# Null Comparisons for bipartite

# Null Comparisons for Users projection

########################################
# Application of a few multigraph algos#
########################################











