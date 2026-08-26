#26/08/2026
#Medium
#Triangle Quest 2
# HackerRank: Generate palindromic numerical triangles using repunit mathematics.

for i in range(1, int(input())+1):
    print(((10**i - 1) // 9) ** 2)
    