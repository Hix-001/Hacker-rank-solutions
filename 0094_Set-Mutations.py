#14/08/2026
#Medium
#Set Mutations
# HackerRank: Execute dynamic in-place set mutation methods and calculate the final sum.

_ = int(input())
A = set(map(int, input().split()))
n = int(input())

for _ in range(n):
    command, _ = input().split()
    other_set = set(map(int, input().split()))
    getattr(A, command)(other_set)

print(sum(A))