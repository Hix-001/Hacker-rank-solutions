#15/08/2026
#Easy
#Check Strict Superset
# HackerRank: Validate strict superset conditions against multiple sets using the > operator.

a = set(input().split())
n = int(input())

is_strict = True

for _ in range(n):
    other_set = set(input().split())
    if not (a > other_set):
        is_strict = False
        break

print(is_strict)