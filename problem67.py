#26/07/2026
#Easy
#DefaultDict Tutorial
# HackerRank: Use defaultdict to track 1-based indices of words from one group and search for them with another.
from collections import defaultdict
n, m = map(int, input().split())
d = defaultdict(list)
for i in range(1, n + 1):
    word = input()
    d[word].append(str(i))
for _ in range(m):
    word = input()
    if d[word]:
        print(" ".join(d[word]))
    else:
        print("-1")