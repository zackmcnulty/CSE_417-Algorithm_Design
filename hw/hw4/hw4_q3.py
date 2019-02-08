# reads given input file that is specified on the command line
# Assumes points are given as pairs of white space characters:

# 1 2 3 4 5 6

# Would specify the points (1,2), (3,4), (5,6)



# The 2nd algorithm is actually faster? This might be because the list of filtered points
# is really short so sorting it is fast. With the third algorithm, we have to perform the
# O(n) operation of merging the two sorted sublists from the recursive case, and 
# this maybe outweighs the sorting of the small filtered list. i.e. the 3rd algorithm
# makes it impossible to sort after filtering because we need to return the full
# sorted list by y values to the parent problem in every recursive call.

# Usage: python3 hw4_p3.py path/to/inputfile.txt

import sys
import itertools
import math
import time



try:
    input_file = sys.argv[1]
except:
    raise ValueError("Expecting an input file e.g. : python3 hw4_q3.py input.txt")

#input_file = "test_files/test0000_1549077011.2610948_U10.txt"

f = open(input_file).read()
output = open(input_file[:-4] + "_OUT.txt", 'w')
#output = open("output_unitsquare.txt", 'a') #append to existing file

file_string = f.split()
points = list(zip([float(x) for x in file_string[::2]] ,[float(y) for y in file_string[1::2]]))
N = len(points)

# returns square of the distance between two points p1 = (x,y), p2 = (x2, y2)
def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# ========================================================
# Naive algorithm: simply brute force all n choose 2 distances.

# used for testing less slow algs on higher n values
run_naive = True

if run_naive:
    start_naive = time.time()

    min_dist = float("inf")
    min_pair = None

    if N == 1:
        min_pair = points + [None]
    else:

        for i,p1 in enumerate(points):
            for p2 in points[i+1:]:
                next_dist = dist(p1,p2)
                if next_dist < min_dist:
                    min_dist = next_dist
                    min_pair = [p1, p2]



    runtime_naive = time.time() - start_naive
#    print("1: ", min_pair, " ", min_dist, " ", runtime_naive)
    print("Version 1 (n = ", N ,"): ", "min pair = ", min_pair, "min dist =",  min_dist, " runtime:", runtime_naive, " seconds")

    output.write("1, " + str(N)  + ", " + str(min_pair)  + ", " + str(min_dist) + " ," + str(runtime_naive) + "\n")


#=============================================================
# O(n log^2(n)) algorithm described in lecture


# Does not assume that the points are sorted in any way
def closest_pair(points):

    n = len(points)
    if n <= 1: return [float("inf"), [points[0], None]]
    
    # sort by x coordinate
    x_sorted = sorted(points, key=(lambda point: point[0]))

    # calculate the line which divides around half the points.
    # just choose the x coordinate of L to be in-between the
    # middle two points (when sorted by x coordinate)
    L = (x_sorted[n//2 - 1][0] + x_sorted[n//2][0] ) / 2
    [delta1, pair1] = closest_pair(x_sorted[:n//2])
    [delta2, pair2] = closest_pair(x_sorted[n//2:])

    if delta1 < delta2:
        delta = delta1
        min_pair = pair1
    else:
        delta = delta2
        min_pair = pair2

    # find points within delta of L
    # too slow? use the fact that its sorted by x to elim some comparisions?

    mid_points = []
    index = 0
    while index < n and abs(L - x_sorted[index][0]) > delta:
        index += 1
    while index < n and abs(L - x_sorted[index][0]) <= delta:
            mid_points.append(x_sorted[index])
            index += 1

#    mid_points = list(filter(lambda point: abs(L - point[0]) <= delta, x_sorted))

    # sort remaining points by y coordinate
    y_sorted = sorted(mid_points, key= (lambda point: point[1]))
    m = len(y_sorted)

    for i in range(m):
        k = 1
        while i+k < m and y_sorted[i+k][1] < y_sorted[i][1] + delta:
            distance = dist(y_sorted[i+k], y_sorted[i]) 
            if distance < delta:
                delta = distance
                min_pair = [y_sorted[i], y_sorted[i+k]]

            k += 1

    return [delta, min_pair]

start_alg = time.time()

[min_dist, min_pair] = closest_pair(points)
runtime_alg = time.time() - start_alg

print("Version 2 (n = ", N, "): ", " min pair = ", min_pair, " min dist =",  min_dist, " runtime:", runtime_alg, " seconds")
output.write("2, " + str(N)  + ", " + str(min_pair)  + ", " + str(min_dist) + " ," + str(runtime_alg) + "\n")
#====================================================================
# O(n log n) algorithm described in lecture


# sort x FIRST before calling algorithm
def closest_pair_helper2(x_sorted):

    n = len(x_sorted)
    if n <= 1: return [float("inf"), x_sorted, [x_sorted[0], None]]

    L = (x_sorted[n//2 - 1][0] + x_sorted[n//2][0] ) / 2
    [delta1, y_sorted1, pair1] = closest_pair_helper2(x_sorted[:n//2])
    [delta2, y_sorted2, pair2] = closest_pair_helper2(x_sorted[n//2:])

    if delta1 < delta2:
        delta = delta1
        min_pair = pair1
    else:
        delta = delta2
        min_pair = pair2

    # Have to sort entire list rather than just filtered part?
    y_sorted = []

    # merge the sorted sublists that are sorted by y = O(n)
    ind1 = 0
    ind2 = 0
    while ind1 < len(y_sorted1) and ind2 < len(y_sorted2):
        if y_sorted1[ind1] <= y_sorted2[ind2]:
            y_sorted.append(y_sorted1[ind1])
            ind1 += 1
        else:
            y_sorted.append(y_sorted2[ind2])
            ind2 += 1

    if len(y_sorted2) > ind2:
        y_sorted.extend(y_sorted2[ind2:])
    elif len(y_sorted1) > ind1:
        y_sorted.extend(y_sorted1[ind1:])
    
    
    
    # filter out points whose x values place them too far from L
    filtered = list(filter(lambda point: abs(L - point[0]) <= delta, y_sorted))
    m = len(filtered)

    for i in range(m):
        k = 1
        while i+k < m and filtered[i+k][1] < filtered[i][1] + delta:
            distance = dist(filtered[i+k], filtered[i])
            if distance < delta:
                delta = distance
                min_pair = [filtered[i+k], filtered[i]]

            k += 1

    return [delta, y_sorted, min_pair]

def closest_pair2(points):
    # sort by x coordinate globally
    x_sorted = sorted(points, key= (lambda point: point[0]))
    result = closest_pair_helper2(x_sorted)
    return [result[0], result[2]]



start_improved_alg = time.time()

# sort by x coordinate before making function call
[min_dist, min_pair] = closest_pair2(points)
runtime_improved_alg = time.time() - start_improved_alg

print("Version 3 (n = ", N, "): ", " min pair = ", min_pair, " min dist =",  min_dist, " runtime:", runtime_improved_alg, " seconds")
output.write("3, " + str(N)  + ", " + str(min_pair)  + ", " + str(min_dist) + " ," + str(runtime_improved_alg) + "\n")

# =====================================================================

# O(n log n) algorithm described ins section 5.4 of the textbook
'''


def closest_pair3(points):
    P_x = sorted(points, key=lambda p: p[0]) # sort by x; O(n log n)
    P_y = sorted(points, key=lambda p: p[1]) # sort by y: O(n log n)

    # BOTH are O(n) time ; list traversals + dictionary puts
    D_x = {p:i for i, p in enumerate(P_x)} # index location of point in x list
    D_y = {p:i for i, p in enumerate(P_y)} # index location of point in y list

    # BOTH are O(n); list traversals + O(1) dictionary get
    P_x = [(p, D_y[p]) for p in P_x] # points sorted by x, where each point stored with index in y list
    P_y = [(p, D_x[p]) for p in P_y] # points sorted by y, where each point is stored with index in x list
    return closest_pair_helper3(P_x, P_y) 


# NOTE: P_x has elements of the form ((x, y), index of point in P_y )
# similarly, P_y has elements of form ((x,y), index of point in P_x)

def closest_pair_helper3(P_x, P_y):
    n = len(P_x)

    if n <= 1:
        return [(None, None), float('inf')]

    # dividing line: mean of the middle 2 x coordinates
    L = (P_x[n//2 - 1][0][0] + P_x[n//2][0][0] ) / 2

    # left half
    Q_x = P_x[:n//2]
    Q_y = []

    # right half
    R_x = P_x[n//2:]
    R_y = []

    # O(n) operation time; list traversal with O(1) comparisons & appends
    for (p, x_index) in P_y:

        # if this point is in the x list for left half, put it in left half
        if x_index < n//2:
            Q_y.append((p,x_index))
        else:
            # subtract out the indices for points we put in left half
            R_y.append((p, x_index - n//2)) 
    
    [(q0, q1), delta1] = closest_pair_helper3(Q_x, Q_y)
    [(r0, r1), delta2] = closest_pair_helper3(R_x, R_y)
    delta = min(delta1, delta2)
    
    filtered = list(filter(lambda p: abs(L - p[0][0]) <= delta, P_x ))

    m = len(filtered)
    s = None

    for i in range(m):
        k = 1

        # check if there are points left to compare to, and these points are < delta above current point 
        # i.e. y values are less than delta apart
        while i+k < m and filtered[i+k][0][1] < filtered[i][0][1] + delta:
            distance = dist(filtered[i+k][0], filtered[i][0] )
            
            if distance < delta:
                s = (filtered[i+k][0], filtered[i][0])
                delta = distance

            k += 1

    if s != None:
        return (s, delta)
    elif delta1 < delta2:
        return ((q0, q1), delta)
    else:
        return ((r0, r1), delta)





start_improved_alg3 = time.time()

# sort by x coordinate before making function call
min_dist3 = closest_pair3(points)[1]
runtime_improved_alg3 = time.time() - start_improved_alg3

print("3: ", min_dist3, " ", runtime_improved_alg3) 
'''
