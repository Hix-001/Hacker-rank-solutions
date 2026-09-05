#04/09/2026
#Medium
#Validating Email Addresses With a Filter
# HackerRank: Validate complex string formatting using regular expressions and the filter function.

import re

def fun(s):
    return bool(re.match(r"^[a-zA-Z0-9_\-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}$", s))

def filter_mail(emails):
    return list(filter(fun, emails))

if __name__ == '__main__':
    n = int(input())
    emails = []
    for _ in range(n):
        emails.append(input())

filtered_emails = filter_mail(emails)
filtered_emails.sort()
print(filtered_emails)