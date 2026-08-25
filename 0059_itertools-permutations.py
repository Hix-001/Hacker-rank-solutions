#21/07/2026
#Easy
# HackerRank: Generate lexicographically sorted permutations using itertools.

from itertools import permutations

if __name__ == '__main__':
    s, k = input().split()
    k = int(k)
    
    s = sorted(s)
    
    perms = permutations(s, k)
    
    for p in perms:
        print("".join(p))