import random
import sys
import numpy as np
import time

''' Generates random collection of points both uniformly within the given x range and y range
and uniformly along a line at x = 0 within the given y range

usage: python3 make_random_test_files.py number_points number_tests x_min x_max y_min y_max
'''

try:
    # number of points
    num_points = int(sys.argv[1])

    # number of tests to make
    tests = int(sys.argv[2])

    x_min = int(sys.argv[3])
    x_max  = int(sys.argv[4])
    y_min = int(sys.argv[5])
    y_max  = int(sys.argv[6])
    
except:
    raise ValueError("usage: python3 make_random_test_files.py number_points number_tests x_min x_max y_min y_max")


x_range = x_max - x_min
x_mean = (x_max + x_min) / 2
y_range = y_max - y_min
y_mean = (y_max + y_min) / 2

for i in range(tests):
    # normally distributed points
    filename = "test_files/test" + str(i).zfill(4) + "_" + str(time.time()) + "_" # pad num with zeros


#    f = open(filename + "N" + str(num_points) + ".txt", 'w')
#    points = zip(x_range * np.random.randn(num_points) + x_mean, y_range * np.random.randn(num_points) + y_mean)
#    for p in points:
#        f.write(str(p[0]) + " " + str(p[1]) + " ")
#    f.close()

    # uniformly distributed points
    f = open(filename + "U" + str(num_points) + ".txt", 'w')
    points = zip(np.random.uniform(low= x_min, high=x_max, size=num_points), np.random.uniform(low = y_min, high= y_max, size=num_points))
    for p in points:
        f.write(str(p[0]) + " " + str(p[1]) + " ")
    f.close()
   

    # edge case: straight line of opens
    f = open(filename + "LINE" + str(num_points) + ".txt", 'w')
    y_coordinates = np.random.uniform(low=y_min, high=y_max, size = num_points)
    for y in y_coordinates:
        f.write("0 " + str(y) + " ")
    f.close()






