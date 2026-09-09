#09/09/2026
#Hard
#Validating UID
# HackerRank: Validate complex overlapping string constraints using regex lookaheads.

import re

for _ in range(int(input())):
    uid = input().strip()
    if re.match(r"^(?!.*(.).*\1)(?=(?:.*[A-Z]){2})(?=(?:.*\d){3})[a-zA-Z0-9]{10}$", uid):
        print("Valid")
    else:
        print("Invalid")