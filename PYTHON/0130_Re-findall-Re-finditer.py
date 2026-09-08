#08/09/2026
#Easy
#Re.findall() & Re.finditer()
# HackerRank: Extract specific string patterns using regex lookarounds to avoid consuming boundaries.

import re

vowels = "aeiouAEIOU"
consonants = "qwrtypsdfghjklzxcvbnmQWRTYPSDFGHJKLZXCVBNM"
pattern = r'(?<=[%s])([%s]{2,})(?=[%s])' % (consonants, vowels, consonants)

matches = re.findall(pattern, input())

if matches:
    print(*matches, sep='\n')
else:
    print("-1")