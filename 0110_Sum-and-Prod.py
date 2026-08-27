#27/08/2026
#Easy
#Sum and Prod
# HackerRank: Evaluate sums and products across specific Numpy array axes.

import numpy
n, m = map(int, input().split())
arr = numpy.array([input().split() for _ in range(n)], int)
print(numpy.prod(numpy.sum(arr, axis=0)))
