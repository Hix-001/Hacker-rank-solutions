#15/08/2026
#Easy
#Check Subset
# HackerRank: Verify if one set is entirely contained within another.
t = int(input())

for _ in range(t):
    _ = input()
    a = set(input().split())
    
    _ = input()
    b = set(input().split())
    
    print(a.issubset(b))