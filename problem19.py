#Read space-separated dimensions N and M, and utilize NumPy to generate and print an N times M 2D array with ones on the main diagonal and zeros elsewhere.
import numpy as np
np.set_printoptions(legacy='1.13')
if __name__ == '__main__':
    n, m = map(int, input().split())
    print(np.eye(n, m))