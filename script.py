from numpy import random
from graph_tool.all import *
import scipy

# setting the number of nodes 
nodes = 1000
# setting the probability that a pair if have an edge
p = 1/10

network_matrix = []

for i in range(nodes):
    row = []
    for j in range(nodes):
        row.append(0)
    network_matrix.append(row)

# iterating through every pair of nodes one time
# pairs i,j are being considered equal to pair j,i
for i in range(len(network_matrix)):
    for j in range(i+1, len(network_matrix[0])):
        # if the i node is different from j node, therefore creating a pair of nodes
        if i != j:
            random_prob = random.rand()
            if random_prob <= p:    
                # add an edge
                # is a non directed graph, so the two nodes have the connection
                network_matrix[i][j] = 1
                network_matrix[j][i] = 1
 

ug_random_network = Graph(scipy.sparse.lil_matrix(network_matrix),directed=False)


# saving as an edge list
filepath = "edge-list.tsv"

# itereating to every pair combination once
with open(filepath, 'w') as f:
    for i in range(len(network_matrix)):
        for j in range(i+1, len(network_matrix[1])):
            # if there is a connection
            if network_matrix[i][j] == 1:
                # writting index i tab index j 
                f.write(f"{i}\t{j}\n")



# saving as a metis file
filepath = "network-ug.metis"


with open(filepath, 'w') as f:
    # writing the number of vertices and the edges in the network
    f.write(f"{ug_random_network.num_vertices()} {ug_random_network.num_edges()}\n")
    # iterating through the vertices
    for v in ug_random_network.vertices():
        # list that represents a row in the file contanning the neighboors
        neighboors = []
        # iterating through every neighboor
        for n in v.out_neighbors():
            # appending the neighboor, as a string to neighboors list
            # incrementing the vertex value, because it should be indexed in 1
            neighboors.append(str(int(n)+1))

        # appending the break line, as here we have finished all the neighboors of the vertex
        neighboors.append("\n")
        # joing the list values separated by a space and writting on the file
        f.write(" ".join(neighboors))


# saving as a grampml file
path_file = "network.grapml"

ug_random_network.save(path_file, fmt="graphml")