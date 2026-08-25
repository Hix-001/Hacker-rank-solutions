#02/08/2026
#Easy
#Collections.deque()
# HackerRank: Perform double-ended queue operations based on dynamic string commands.

from collections import deque
n = int(input())
d = deque()
for _ in range(n):
    command = input().split()
    if len(command) > 1:
        getattr(d, command[0])(int(command[1]))
    else:
        getattr(d, command[0])()
print(*d)
