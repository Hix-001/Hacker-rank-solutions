#10/09/2026
#Easy
#Transpose and Flatten
# HackerRank: Use numpy.transpose() and .flatten() to restructure 2-D arrays.

import numpy
n, m = map(int, input().split())
arr = numpy.array([input().split() for _ in range(n)], int)
print(numpy.transpose(arr))
print(arr.flatten())