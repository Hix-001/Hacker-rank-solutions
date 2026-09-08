#08/09/2026
#Medium
#Regex Substitution
# HackerRank: Utilize positive lookahead and lookbehind assertions to substitute string patterns safely.

import re

for _ in range(int(input())):
    line = input()
    line = re.sub(r'(?<= )&&(?= )', 'and', line)
    line = re.sub(r'(?<= )\|\|(?= )', 'or', line)
    print(line)