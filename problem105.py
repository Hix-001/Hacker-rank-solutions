#23/08/2026
#Easy
#Detect Floating Point Number
# HackerRank: Validate string structure using regular expression quantifiers and anchors.

import re

t = int(input())

for _ in range(t):
    print(bool(re.match(r"^[-+]?\d*\.\d+$", input())))