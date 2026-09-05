#05/09/2026
#Hard
#Matrix Script
# HackerRank: Decode a matrix string and use regex lookarounds to filter symbols.

import re

n, m = map(int, input().split())
matrix = []

for _ in range(n):
    matrix.append(input())

decoded = ""
for i in range(m):
    for j in range(n):
        decoded += matrix[j][i]

print(re.sub(r'(?<=[a-zA-Z0-9])[^a-zA-Z0-9]+(?=[a-zA-Z0-9])', ' ', decoded))