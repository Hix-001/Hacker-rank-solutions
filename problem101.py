#20/08/2026
#Easy
#Validating phone numbers
# HackerRank: Use regular expressions to validate exact phone number patterns.

import re
n = int(input())
for _ in range(n):
    if re.match(r"^[789]\d{9}$", input()):
        print("YES")
    else:
        print("NO")