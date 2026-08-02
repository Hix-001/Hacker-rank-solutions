#02/08/2026
#Medium
#Piling Up!
# HackerRank: Determine if cubes can be stacked by greedily picking from the ends of a deque.
from collections import deque
T = int(input())
for _ in range(T):
    n = int(input())
    d = deque(map(int, input().split()))
    possible = True
    top_of_pile = float('inf')
    while d:
        if d[0] >= d[-1]:
            picked = d.popleft()
        else:
            picked = d.pop()
        if picked <= top_of_pile:
            top_of_pile = picked
        else:
            possible = False
            break
    if possible:
        print("Yes")
    else:
        print("No")