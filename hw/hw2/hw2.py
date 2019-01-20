# Zachary McNulty (zmcnulty, ID: 1636402)

# FINDING BICONNECTED COMPONENTS 


# Reads input files of the form:

# the input will consist of an odd number of whitespace-separated integers.
# The first must be a positive integer “N”; this is followed by some
# number of pairs of integers in the range 0 to N − 1. “N ” represents the 
# number of vertices in the graph, and each pair u, v represents an edge
# between vertices u and v.


# Can be run from the command line using:
# python3  hw2.py inpute_file_name.txt start_vertex(optional)

import time
import sys

# @ params:
#   v : vertex currently being expanded
#   parent: vertex that v was reached from in the DFS
def DFS_biconnect(v, parent):

    global dfscounter, dfs_nums, edgeList, biconnected_components
    global visited, adjacency_list, articulation_points

    dfs_nums[v] = dfscounter
    dfscounter += 1
    lows[v] = dfs_nums[v]
    
    for x in adjacency_list[v]:
        

        if dfs_nums[x] == -1:
            # node unvisited; move towards it next
            edgeList.append((v,x))
            DFS_biconnect(x, v)
            lows[v] = min(lows[v], lows[x])

            if lows[x] >= dfs_nums[v]:
                articulation_points.add(v) 

                next_edge = (-1,-1) 
                next_bi_comp = []

                while next_edge[0] != v:
                    next_edge = edgeList.pop()
                    next_bi_comp.append(next_edge)

                biconnected_components.append(next_bi_comp)

        # edge going to non-parent ancestor in tree
        elif x != parent and dfs_nums[x] < dfs_nums[v]:
            lows[v] = min(lows[v], dfs_nums[x])
            edgeList.append((v,x))

# Reading Input File =============================================================

start_input = time.time()

input_file = sys.argv[1] 

f = open(input_file).read()

output_filename = input_file.replace(".txt", "") + "_results.txt"
results = open(output_filename, 'w')

input_data = f.split()
N = int(input_data[0])

print("input file read in: ", time.time() - start_input)


# Generating Adjacency List ====================================================

start_adj = time.time()

edges = list(zip(input_data[1::2], input_data[2::2]))

adjacency_list = {v:[] for v in range(N)}

for e in edges:
    u = int(e[0])
    v = int(e[1])
    adjacency_list[u].append(v)
    adjacency_list[v].append(u)

print("adjacency list generated in: ", time.time() - start_adj)


# Finding Biconnected Components ==============================================

start_alg = time.time()

# initialization of our dfs nums and the LOW(v) values

#   dfscounter: current vertex number to be assigned
#   dfs_nums : order vertices were visited/expanded in
#   edge_list : edge list as described in algorithm
#   biconnected_components : list of biconnected components of G to be built up
dfs_nums = [-1]*N
lows = [N+1]*N
dfscounter = 1
edgeList = []
biconnected_components = []
articulation_points = set([])
try:
    start_vertex = int(sys.argv[2])
except:
    start_vertex = 0 


# parent = -1 because the root has no parent 
# NOTE: this algorithm does NOT tell us whether the start_vertex is an articulation point or
#       not.  
#       Since recursion starts with start_vertex, we will  explore all other paths below it before 
#       we fully recurse back to it and add more edges adjacent to it.
#       more edges from it if it connects two separate biconnected components.
#       So I can check if 0 occurs in two separate biconnected components to see if it is an articulation point.

DFS_biconnect(start_vertex, 0)
count = 0
articulation_points.remove(start_vertex)

# check separately whether start vertex is articulation point
for bc in biconnected_components:
    for edge in bc:
        if start_vertex in edge:
            count += 1
            break

if count > 1:
    articulation_points.add(start_vertex)

alg_runtime = time.time() - start_alg

# Outputting Results ==========================================================
results.write("number nodes: " + str(N) + "\n")
print("number nodes: " + str(N) + "\n")
results.write("number edges: " + str(len(list(edges))) + "\n")
print("number edges: " + str(len(list(edges))) + "\n")
results.write("number biconnected components: " + str(len(biconnected_components))+ "\n" )
print("number biconnected components: " + str(len(biconnected_components))+ "\n" )
results.write("number of articulation points: " + str(len(articulation_points))+ "\n")
print("number of articulation points: " + str(len(articulation_points))+ "\n")
results.write("articulation points: " + str(articulation_points)+ "\n")
print("articulation points: " + str(articulation_points)+ "\n")

for i, bc in enumerate(biconnected_components):
    results.write("biconnected component " + str(i+1) + ": " + str( biconnected_components[i]) + "\n")
    print("biconnected component " + str(i+1) + ": " + str( biconnected_components[i]) + "\n")

results.write("biconnected algorithm ran in: " + str(alg_runtime)+ "\n")
print("algorithm ran in ", alg_runtime)
