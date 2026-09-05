#29/08/2026
#Easy
#Concatenate
# HackerRank: Combine multiple Numpy arrays along a specific axis.

import numpy
n, m, p = map(int, input().split())
array_1 = numpy.array([input().split() for _ in range(n)], int)
array_2 = numpy.array([input().split() for _ in range(m)], int)
print(numpy.concatenate((array_1, array_2), axis=0))