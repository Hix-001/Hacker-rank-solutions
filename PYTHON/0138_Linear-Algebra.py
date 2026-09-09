#09/09/2026
#Easy
#Linear Algebra
# HackerRank: Compute the determinant of an NxN matrix using numpy.linalg.

import numpy

n = int(input())
matrix = [list(map(float, input().split())) for _ in range(n)]
a = numpy.array(matrix)

print(round(numpy.linalg.det(a), 2))