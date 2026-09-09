#09/09/2026
#Easy
#Array Mathematics
# HackerRank: Perform element-wise mathematical operations on 2D arrays using NumPy.

import numpy
n, m = map(int, input().split())
a = numpy.array([input().split() for _ in range(n)], int)
b = numpy.array([input().split() for _ in range(n)], int)
print(a + b)
print(a - b)
print(a * b)
print(a // b)
print(a % b)
print(a ** b)