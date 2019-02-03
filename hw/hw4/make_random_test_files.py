import random
import sys
import numpy as np
import time




try:
    # number of points
    num_points = int(sys.argv[1])

    # number of tests to make
    tests = int(sys.argv[2])

    x_range = int(sys.argv[3])
    y_range = int(sys.argv[4])
except:
    raise ValueError("give me a number of points, x range, and y range loser")



for i in range(tests):
    # normally distributed points
    filename = "test_files/test" + str(i).zfill(4) + "_" + str(time.time()) + "_" # pad num with zeros
    f = open(filename + "N" + str(num_points) + ".txt", 'w')
    points = zip(x_range * np.random.randn(num_points), y_range * np.random.randn(num_points))
    for p in points:
        f.write(str(p[0]) + " " + str(p[1]) + " ")
    f.close()

    # uniformly distributed points
    f = open(filename + "U" + str(num_points) + ".txt", 'w')
    points = zip(np.random.uniform(low= -x_range, high=x_range, size=num_points), np.random.uniform(low= -y_range, high=y_range, size=num_points))
    for p in points:
        f.write(str(p[0]) + " " + str(p[1]) + " ")
    f.close()
    

    # edge case: straight line of opens
    f = open(filename + "LINE" + str(num_points) + ".txt", 'w')
    for i in range(num_points):
        f.write("0 " + str(i) + " ")
    f.close()






