#18/08/2026
#Easy
#Any or All
# HackerRank: Verify conditions using all(), any(), and string palindromes.

_ = input()
nums = input().split()
print(all(int(x) > 0 for x in nums) and any(x == x[::-1] for x in nums))