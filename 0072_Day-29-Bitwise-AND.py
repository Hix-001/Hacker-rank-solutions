#30/07/2026
#Medium
#30 DAY OF CODE IN PYTHON [DAY 29]
#Bitwise AND
# HackerRank: Find the maximum bitwise AND value of two integers less than a given limit K.

import math
import os
import random
import re
import sys

def bitwiseAnd(N, K):
    if ((K - 1) | K) <= N:
        return K - 1
    else:
        return K - 2
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(input().strip())

    for t_itr in range(t):
        first_multiple_input = input().rstrip().split()

        count = int(first_multiple_input[0])

        lim = int(first_multiple_input[1])

        res = bitwiseAnd(count, lim)

        fptr.write(str(res) + '\n')

    fptr.close()
