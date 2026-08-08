#07/08/2026
#Medium
#No Idea!
# HackerRank: Calculate a score by checking array elements against positive and negative hash sets.
n, m = map(int, input().split())
arr = input().split()
A = set(input().split())
B = set(input().split())
happiness = sum((i in A) - (i in B) for i in arr)
print(happiness)