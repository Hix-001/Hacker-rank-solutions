#02/08/2026
#Medium
#Company Logo
# HackerRank: Find the top 3 most common characters in a string and sort them by frequency and alphabetical order.
import math
import os
import random
import re
import sys

from collections import Counter
if __name__ == '__main__':
    s = input()
    counts = Counter(s)
    sorted_chars = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    for i in range(3):
        print(f"{sorted_chars[i][0]} {sorted_chars[i][1]}")