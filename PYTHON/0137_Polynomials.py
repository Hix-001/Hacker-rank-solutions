#09/09/2026
#Easy
#Polynomials
# HackerRank: Evaluate a polynomial at a given point using numpy.polyval.

import numpy
coefficients = list(map(float, input().split()))
x = float(input())
print(numpy.polyval(coefficients, x))