#06/09/2026
#Medium
#Validating and Parsing Email Addresses
# HackerRank: Use email.utils and regex to parse and strictly validate email components.

import re
import email.utils

for _ in range(int(input())):
    name, email_addr = email.utils.parseaddr(input())
    if re.match(r"^[a-zA-Z][a-zA-Z0-9\-._]*@[a-zA-Z]+\.[a-zA-Z]{1,3}$", email_addr):
        print(email.utils.formataddr((name, email_addr)))