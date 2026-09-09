#09/09/2026
#Easy
#Group(), Groups() & Groupdict()
# HackerRank: Use regex capture groups and backreferences to find repeating characters.

import re
S = input()
m = re.search(r'([a-zA-Z0-9])\1', S)
if m:
    print(m.group(1))
else:
    print("-1")