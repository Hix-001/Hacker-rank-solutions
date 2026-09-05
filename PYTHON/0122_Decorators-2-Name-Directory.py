#05/09/2026
#Medium
#Decorators 2 - Name Directory
# HackerRank: Use a decorator to sort nested lists before applying string formatting.

import operator

def person_lister(f):
    def inner(people):
        return [f(person) for person in sorted(people, key=lambda x: int(x[2]))]
    return inner

@person_lister
def name_format(person):
    return ("Mr. " if person[3] == "M" else "Ms. ") + person[0] + " " + person[1]

if __name__ == '__main__':
    people = [input().split() for i in range(int(input()))]
    print(*name_format(people), sep='\n')

    