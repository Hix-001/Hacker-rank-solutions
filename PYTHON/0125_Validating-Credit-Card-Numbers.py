#07/09/2026
#Medium
#Validating Credit Card Numbers
# HackerRank: Use dual regex evaluations to validate structural format and character repetition.

import re

for _ in range(int(input())):
    card = input().strip()
    
    if re.match(r"^[456]([\d]{15}|[\d]{3}(-[\d]{4}){3})$", card):
        if not re.search(r"(\d)\1{3,}", card.replace("-", "")):
            print("Valid")
        else:
            print("Invalid")
    else:
        print("Invalid")