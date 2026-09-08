#08/09/2026
#Easy
#Re.split()
# HackerRank: Use a regex character class to split a string by multiple delimiters.

regex_pattern = r"[.,]"

import re
print("\n".join(re.split(regex_pattern, input())))