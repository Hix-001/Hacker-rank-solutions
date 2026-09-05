#01/09/2026
#Easy
#Re.start() & Re.end()
# HackerRank: Isolate starting and ending indices of overlapping regex matches.

import re

s = input()
k = input()

pattern = re.compile(k)
match = pattern.search(s)

if not match:
    print((-1, -1))
else:
    while match:
        print((match.start(), match.end() - 1))
        match = pattern.search(s, match.start() + 1)