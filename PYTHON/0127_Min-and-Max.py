#08/09/2026
#Easy
#Min and Max
# HackerRank: Compute minimum along axis 1 and then find the maximum using numpy.

import numpy
n, m = map(int, input().split())
arr = numpy.array([input().split() for _ in range(n)], int)
print(numpy.max(numpy.min(arr, axis=1)))