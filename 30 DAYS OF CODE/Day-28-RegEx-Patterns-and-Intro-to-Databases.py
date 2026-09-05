#29/07/2026
#Medium
#Q71
#RegEx, Patterns, and Intro to Databases
# HackerRank: Filter and sort a list of first names based on a regex match for a Gmail domain.

import re

if __name__ == '__main__':
    N = int(input().strip())
    gmail_users = []
    for _ in range(N):
        firstName, emailID = input().rstrip().split()
        if re.search(r'@gmail\.com$', emailID):
            gmail_users.append(firstName)
    gmail_users.sort()
    for name in gmail_users:
        print(name)
