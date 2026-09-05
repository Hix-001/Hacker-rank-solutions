#12/07/2026
#Easy
#Q45
#2D Arrays
# HackerRank: Calculate the maximum hourglass sum in a 6x6 2D array using a sliding window.

import math
import os
import random
import re
import sys

if __name__ == '__main__':
    arr = []
    for _ in range(6):
        arr.append(list(map(int, input().rstrip().split())))
    max_sum = float('-inf')
    for i in range(4):
        for j in range(4):
            current_sum = (
                arr[i][j]   + arr[i][j+1]   + arr[i][j+2] +
                              arr[i+1][j+1] +
                arr[i+2][j] + arr[i+2][j+1] + arr[i+2][j+2]
            )
            if current_sum > max_sum:
                max_sum = current_sum
    print(max_sum)
