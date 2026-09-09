#09/09/2026
#Easy
#Dot and Cross
# HackerRank: Compute the matrix product of two 2D arrays using numpy.dot.

import numpy
n = int(input())
a = numpy.array([input().split() for _ in range(n)], int)
b = numpy.array([input().split() for _ in range(n)], int)
print(numpy.dot(a, b))