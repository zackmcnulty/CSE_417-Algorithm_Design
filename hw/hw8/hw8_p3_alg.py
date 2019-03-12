

# G is the given graph as an adjacency list
# i is the index of the current vertex of interest
# V_1 is the set of vertices in V_1
def max_cut(G, i, V_1):
    if i >= len(G):
        return 0

    # Two case: 

    # v_i is in V_1 in the optimal arrangement
    # dont change anything just recurse

    val_1 = max_cut(G, i + 1, V_1)

    # v_i is in V_2 in the optimal arrangement
    # move v_i to V_2 and find how many bridge edges are
    # created/destroyed
    bridges_made = 0
    bridges_destroyed = 0
    V_1.remove(i) # move v_i from V_1 to V_2

    for other_vertex in G[i]:
        if other_vertex in V_1:
            # by moving v_i to V_2, we create a bridge vertex
            # as the edge (v_i, other_vertex) goes from V_2 to V_1
            bridges_made += 1
        else:
            # by moving v_i to V_2, we destroy a bridge vertex as
            # now the edge (v_i,  other_vertex) goes between two
            # vertices in V_2
            bridges_destroyed += 1
    
    val_2 = (bridges_made - bridges_destroyed) + max_cut(G, i+1, V_1)

    
    return max(val_1, val_2)
