#25/08/2026
#Easy
#Hex Color Code
# HackerRank: Extract hex color codes from CSS using regex lookarounds.

import re

for _ in range(int(input())):
    matches = re.findall(r"(?i)(?<!^)(#(?:[0-9a-f]{3}){1,2})(?![0-9a-f])", input())
    for match in matches:
        print(match)