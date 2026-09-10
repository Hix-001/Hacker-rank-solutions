#10/09/2026
#Easy
#Mean, Var, and Std
# HackerRank: Compute basic statistical measures along specific array axes using NumPy.

import numpy
n, m = map(int, input().split())
arr = numpy.array([input().split() for _ in range(n)], int)
print(numpy.mean(arr, axis=1))
print(numpy.var(arr, axis=0))
print(round(numpy.std(arr, axis=None), 11))