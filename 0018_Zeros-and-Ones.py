# HackerRank: Given the dimensions of an array as space-separated integers, utilize NumPy to generate and print an integer array of zeros followed by an integer array of ones of the specified shape.
import numpy as np

if __name__ == '__main__':
    # Read the space-separated integers and convert them to a tuple
    shape = tuple(map(int, input().split()))
    
    # Print the zeros array, explicitly setting the type to standard int
    print(np.zeros(shape, dtype=int))
    
    # Print the ones array, explicitly setting the type to standard int
    print(np.ones(shape, dtype=int))