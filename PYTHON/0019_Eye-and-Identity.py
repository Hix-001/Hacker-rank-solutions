#05/07/2026
#Easy
#Eye and Identity
# HackerRank: Utilize NumPy to generate and print an N x M 2D array with ones on the main diagonal and zeros elsewhere.

import numpy as np
np.set_printoptions(legacy='1.13')
if __name__ == '__main__':
    n, m = map(int, input().split())
    print(np.eye(n, m))
