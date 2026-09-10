#10/09/2026
#Easy
#Arrays
# HackerRank: Reverse a list and convert it to a float NumPy array.

import numpy
def arrays(arr):
    return numpy.array(arr[::-1], float)
arr = input().strip().split(' ')
result = arrays(arr)
print(result)