# Reads input files of the form:
# the input will consist of an odd number of whitespace-separated integers.
# The first must be a positive integer “N”; this is followed by some
# number of pairs of integers in the range 0 to N − 1. “N ” represents the 
# number of vertices in the graph, and each pair u, v represents an edge
# between vertices u and v.

import time
import sys

# @ params:
#   v : vertex currently being expanded
#   parent: vertex that v was reached from in the DFS
#   dfscounter: current vertex number to be assigned
#   dfs_nums : order vertices were visited/expanded in
#   edge_list : edge list as described in algorithm
#   biconnected_components : list of biconnected components of G to be built up
def DFS_biconnect(v, parent):
    global dfscounter, dfs_nums, edgeList, biconnected_components, adjacency_list, articulation_points
    dfs_nums[v] = dfscounter
    dfscounter += 1
    lows[v] = dfs_nums[v]

    for x in adjacency_list[v]:
        
        edgeList.append((v,x))

        if dfs_nums[x] == -1:
            DFS_biconnect(x, v)
            lows[v] = min(lows[v], lows[x])

            if lows[x] >= dfs_nums[v]:
                print(v, " is articulating point separating ", x)
                articulation_points.append(v) 
                next_edge = edgeList.pop()
                next_bi_comp = set()
                next_bi_comp.add(next_edge)

                while next_edge[0] != v:
                    next_edge = edgeList.pop()
                    next_bi_comp.add(next_edge)

                biconnected_components.append(next_bi_comp)

        elif x != parent and x != -1:
            lows[v] = min(lows[v], dfs_nums[x])

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

edges = zip(input_data[1::2], input_data[2::2])

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
dfs_nums = [-1]*N
lows = [N+1]*N
dfscounter = 1
edgeList = []
biconnected_components = []
articulation_points = []
start_vertex = 0
# parent = -1 because the root has no parent 
DFS_biconnect(start_vertex, -1)

alg_runtime = time.time() - start_alg

# Outputting Results ==========================================================
results.write("number nodes: " + str(N))
results.write("number edges: " + str(len(edges)))
results.write("number biconnected components: " + str(len(biconnected_components)))
results.write("number of articulation points: " + str(len(articulation_points)))
results.write("articulation points: " + str(articulation_points))

for i, bc in enumerate(biconnected_components):
    results.write("biconnected component " + str(i+1) + ": " + str( biconnected_components[i]))

results.write("biconnected algorithm ran in: " + str(alg_runtime))
