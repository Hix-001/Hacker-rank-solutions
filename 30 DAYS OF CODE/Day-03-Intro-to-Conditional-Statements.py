#05/07/2026
#Easy
#Q25
#Intro to Conditional Statements
# HackerRank: Evaluate a given integer to determine if it is 'Weird' or 'Not Weird' based on its parity and ranges.

import math
import os
import random
import re
import sys

if __name__ == '__main__':
    n = int(input().strip())
    
    if n % 2 != 0 or (6 <= n <= 20):
        print("Weird")
    else:
        print("Not Weird")
