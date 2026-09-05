#21/07/2026
#Easy
#Q58
#Sorting
# HackerRank: Given an array of integers, sort it in ascending order using Bubble Sort and print swap count.

import math
import os
import random
import re
import sys

if __name__ == '__main__':
    n = int(input().strip())
    a = list(map(int, input().rstrip().split()))

    total_swaps = 0

    for i in range(n):
        current_swaps = 0
        
        for j in range(n - 1):
            if a[j] > a[j + 1]:
                temp = a[j]
                a[j] = a[j + 1]
                a[j + 1] = temp
                
                current_swaps += 1
                total_swaps += 1
                
        if current_swaps == 0:
            break

    print("Array is sorted in " + str(total_swaps) + " swaps.")
    print("First Element: " + str(a[0]))
    print("Last Element: " + str(a[-1]))
