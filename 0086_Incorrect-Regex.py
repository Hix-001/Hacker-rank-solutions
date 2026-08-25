#08/08/2026
#Easy
#Incorrect Regex
# HackerRank: Validate regex strings using try-except blocks and re.compile.
import re
t = int(input())
for _ in range(t):
    s = input()
    if '*+' in s or '++' in s or '?+' in s:
        print("False")
        continue
    try:
        re.compile(s)
        print("True")
    except re.error:
        print("False")