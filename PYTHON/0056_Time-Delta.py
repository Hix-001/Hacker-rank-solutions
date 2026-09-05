#19/07/2026
#Medium
#Time Delta
# HackerRank: Calculate the absolute difference between two timestamps using the datetime module.

import math
import os
import random
import re
import sys
import datetime

def time_delta(t1, t2):
    format_string = "%a %d %b %Y %H:%M:%S %z"
    time1 = datetime.datetime.strptime(t1, format_string)
    time2 = datetime.datetime.strptime(t2, format_string)
    difference = time1 - time2
    seconds = abs(difference.total_seconds())
    return str(int(seconds))
    
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    t = int(input())
    for t_itr in range(t):
        t1 = input()
        t2 = input()
        delta = time_delta(t1, t2)
        fptr.write(delta + '\n')
    fptr.close()
