#09/08/2026
#Easy
#itertools.combinations_with_replacement()
# HackerRank: Generate all combinations of a string of size k allowing character replacement.

from itertools import combinations_with_replacement
s, k = input().split()
k = int(k)
sorted_s = sorted(s)
for c in combinations_with_replacement(sorted_s, k):
    print("".join(c))
