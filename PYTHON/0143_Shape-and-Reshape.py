#10/09/2026
#Easy
#Shape and Reshape
# HackerRank: Convert a 1-D array into a 2-D grid using numpy.reshape.

import numpy
arr = numpy.array(input().split(), int)
print(numpy.reshape(arr, (3, 3)))