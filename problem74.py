#01/08/2026
#Easy
#Symmetric Difference
# HackerRank: Find and print the symmetric difference of two sets in ascending order.

m = int(input())
set_m = set(map(int, input().split()))
n = int(input())
set_n = set(map(int, input().split()))
sym_diff = sorted(set_m.symmetric_difference(set_n))
for num in sym_diff:
    print(num)