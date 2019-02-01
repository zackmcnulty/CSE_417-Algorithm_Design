# reads given input file that is specified on the command line
# Assumes points are given as pairs of white space characters:

# 1 2 3 4 5 6

# Would specify the points (1,2), (3,4), (5,6)

import sys
import itertools
import math
import time

try:
    input_file = sys.argv[1]
except:
    raise ValueError("Expecting an input file e.g. : python3 hw4_q3.py input.txt")


f = open(input_file).read()

file_string = f.split()
points = list(zip([float(x) for x in file_string[::2]] ,[float(y) for y in file_string[1::2]]))

# returns the distance between two points p1 = (x,y), p2 = (x2, y2)
def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

#========================================================
# Naive algorithm: simply brute force all n choose 2 distances.

# used for testing less slow algs on higher n values
run_naive = False

if run_naive:
    start_naive = time.time()

    min_dist = float("inf")
    min_pair = None

    for i,p1 in enumerate(points):
        for p2 in points[i+1:]:
            next_dist = dist(p1,p2)
            if next_dist < min_dist:
                min_dist = next_dist
                min_pair = [p1, p2]


    runtime_naive = time.time() - start_naive
#    print("1: ", min_pair, " ", min_dist, " ", runtime_naive)
    print("1: ", min_dist, " ", runtime_naive)



#=============================================================
# O(n log^2(n)) algorithm described in lecture

start_alg = time.time()

# assumes that points is sorted by x coordinate
# or should I save that for the O(n log n) algorithm?)
def closest_pair(points):

    n = len(points)
    if n <= 1: return float("inf")
    
    # sort by x coordinate
    points = sorted(points, key=(lambda point: point[0]))

    # calculate the line which divides around half the points.
    # just choose the x coordinate of L to be in-between the
    # middle two points (when sorted by x coordinate)
    L = (points[n//2 - 1][0] + points[n//2][0] ) / 2
    delta1 = closest_pair(points[:n//2])
    delta2 = closest_pair(points[n//2:])
    delta = min(delta1, delta2)

    # find points within delta of L
    mid_points = list(filter(lambda point: abs(L - point[0]) <= delta, points))
    
    # sort remaining points by y coordinate
    y_sorted = sorted(mid_points, key= (lambda point: point[1]))
    m = len(y_sorted)

    for i in range(len(y_sorted)):
        k = 1
        while i+k < m and y_sorted[i+k][1] < y_sorted[i][1] + delta:
            delta = min(delta, dist(y_sorted[i+k], y_sorted[i] ))
            k += 1

    return delta

min_dist = closest_pair(points)
runtime_alg = time.time() - start_alg

print("2: ", min_dist, " ", runtime_alg) 


#====================================================================
# O(n log n) algorithm 


start_improved_alg = time.time()

# sort x FIRST before calling algorithm
def closest_pair_helper(points):

    n = len(points)
    if n <= 1: return [float("inf"), points]

    L = (points[n//2 - 1][0] + points[n//2][0] ) / 2
    [delta1, y_sorted1] = closest_pair(points[:n//2])
    [delta2, y_sorted2] = closest_pair(points[n//2:])
    delta = min(delta1, delta2)

    y_sorted = []

    # merge the sorted sublists that are sorted by y
    while len(y_sorted1) > 0 and len(y_sorted2) > 0:
        if y_sorted1[0] <= y_sorted2[0]:
            y_sorted.append(y_sorted1.pop(0))
        else:
            y_sorted.append(y_sorted2.pop(0))

    if len(y_sorted1) == 0:
        y_sorted.extend(y_sorted2)
    else:
        y_sorted.extend(y_sorted1)
    
    
    # filter out points whose x values place them too far from L
    filtered = list(filter(lambda point: abs(L - points[0]) <= delta, y_sorted))
    
    m = len(filtered)

    for i in range(len(filtered)):
        k = 1
        while i+k < m and filtered[i+k][1] < filtered[i][1] + delta:
            delta = min(delta, dist(filtered[i+k], filtered[i] ))
            k += 1

    return [delta, y_sorted]

def closest_pair2(points):
    # sort by x coordinate globally
    points = sorted(points, key= (lambda point: point[0]))
    result = closest_pair_helper(points)
    return result[0]


# sort by x coordinate before making function call
min_dist = closest_pair(points)
runtime_improved_alg = time.time() - start_improved_alg

print("3: ", min_dist, " ", runtime_improved_alg) 
