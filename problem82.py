#04/08/2026
#Easy
#itertools.combinations()
# HackerRank: Generate all combinations of a string up to size k in lexicographic order.
from itertools import combinations
s, k = input().split()
k = int(k)
sorted_s = sorted(s)
for i in range(1, k + 1):
    for c in combinations(sorted_s, i):
        print("".join(c))