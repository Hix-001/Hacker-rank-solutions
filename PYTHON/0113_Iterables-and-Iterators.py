#30/08/2026
#Medium
#Iterables and Iterators
# HackerRank: Calculate combination probabilities using itertools.

from itertools import combinations

n = int(input())
letters = input().split()
k = int(input())

combos = list(combinations(letters, k))
with_a = sum(1 for c in combos if 'a' in c)

print(round(with_a / len(combos), 4))
