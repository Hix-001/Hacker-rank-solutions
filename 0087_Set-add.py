#09/08/2026
#Easy
#Set .add()
# HackerRank: Count the number of distinct elements using the set .add() method.
n = int(input())
stamps = set()
for _ in range(n):
    stamps.add(input().strip())
print(len(stamps))