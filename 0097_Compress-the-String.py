#16/08/2026
#Medium
#Compress the String!
# HackerRank: Compress a string by grouping consecutive characters using itertools.groupby.

from itertools import groupby

s = input()

result = [(len(list(g)), int(k)) for k, g in groupby(s)]

print(*result)
