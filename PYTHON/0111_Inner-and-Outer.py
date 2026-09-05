#28/08/2026
#Easy
#Inner and Outer
# HackerRank: Compute mathematical inner and outer products of 1-D vectors using Numpy.

import numpy

a = numpy.array(input().split(), int)
b = numpy.array(input().split(), int)

print(numpy.inner(a, b))
print(numpy.outer(a, b))k